from random import uniform
import keras
import numpy as np
from keras import optimizers
from keras.callbacks import EarlyStopping
from keras.layers import Input, Dense, Flatten, Embedding, Dropout
from keras.models import Model
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from numpy import zeros
from collections import Counter

import facebookEmb
import reports
import sampling
from corpus import getRelevantModelAndNormalizer
from corpus import getTokens
from extraction import Extractor
from modelLinear import getFeatures
from reports import *
from transitions import TransitionType
from wordEmbLoader import empty
from wordEmbLoader import unk, number

enableCategorization = False

importantFrequentWordDic = dict()


class Network:
    def __init__(self, corpus, linearInMLP=False):
        self.vocabulary = Vocabulary(corpus)
        self.nnExtractor = Extractor(corpus) if configuration['mlp2']['features'] else None
        input, output = self.build(corpus.langName, linearInMLP=linearInMLP)
        self.model = Model(inputs=input, outputs=output)
        if configuration['others']['verbose']:
            sys.stdout.write('# Parameters = {0}\n'.format(self.model.count_params()))
            sys.stdout.write(str(self.model.summary()))

    def build(self, lang, linearInMLP=False):
        inputLayers, concLayers = [], []
        inputToken = Input((3 + configuration['embedding']['useB1'] + configuration['embedding']['useB-1'],))
        inputLayers.append(inputToken)
        tokenEmb = Embedding(len(self.vocabulary.tokenIndices), configuration['mlp']['tokenEmb'],
                             trainable=configuration['mlp']['trainable'],
                             weights=self.getWeightMatrix(self.vocabulary.tokenIndices, lang))(inputToken)
        tokenFlatten = Flatten()(tokenEmb)
        concLayers.append(tokenFlatten)
        inputPos = Input((3 + configuration['embedding']['useB1'] + configuration['embedding']['useB-1'],))
        inputLayers.append(inputPos)
        posEmb = Embedding(len(self.vocabulary.posIndices), configuration['mlp']['posEmb'],
                           trainable=configuration['mlp']['trainable'])(inputPos)
        posFlatten = Flatten()(posEmb)
        concLayers.append(posFlatten)
        if linearInMLP:
            linearPredInput = Input(shape=(8,))
            inputLayers.append(linearPredInput)
            concLayers.append(linearPredInput)

        conc = keras.layers.concatenate(concLayers) if len(concLayers) > 1 else concLayers[0]
        dense1Layer = Dense(configuration['mlp']['dense1UnitNumber'],
                            activation=configuration['nn']['dense1Activation'])(conc)
        lastLayer = Dropout(configuration['mlp']['dense1Dropout'])(dense1Layer)
        if configuration['mlp2']['dense2']:
            dense2Layer = Dense(configuration['mlp2']['dense2UnitNumber'],
                                activation=configuration['mlp2']['dense2Activation'])(lastLayer)
            lastLayer = Dropout(configuration['mlp2']['dense2Dropout'])(dense2Layer)
        softmaxLayer = Dense(8 if enableCategorization else 4, activation='softmax')(lastLayer)
        return inputLayers, softmaxLayer

    def getWeightMatrix(self, tokenVocab, lang):
        if configuration['embedding']['pretrained']:
            self.vocabulary.tokenIndices, embeddingMatrix = facebookEmb.getEmbMatrix(lang, tokenVocab.keys())
            return [embeddingMatrix]
        elif configuration['embedding']['manual']:
            return [initEmbMatrix(tokenVocab)]
        else:
            return None

    def predict(self, trans, linearModels=None, linearVecs=None):
        inputs = []
        tokenIdxs, posIdxs = self.getAttachedIndices(trans, dynamicVocab=configuration['embedding']['dynamicVocab'],
                                                     parse=True)
        inputs.append(np.asarray([tokenIdxs]))
        inputs.append(np.asarray([posIdxs]))
        if linearModels and linearVecs:
            linearModel, linearVec = getRelevantModelAndNormalizer(trans.sent, None, linearModels, linearVecs, True)
            featDic = getFeatures(trans, trans.sent)
            predTrans = linearModel.predict(linearVec.transform(featDic))[0]
            predVec = [1 if t.value == predTrans else 0 for t in TransitionType]
            inputs.append(np.asarray([predVec]))
        if configuration['mlp2']['features']:
            features = np.asarray(self.nnExtractor.vectorize(trans))
            inputs.append(np.asarray([features]))
        oneHotRep = self.model.predict(inputs, batch_size=1,
                                       verbose=configuration['nn']['predictVerbose'])
        return oneHotRep[0]

    def trainWithDynamization(self, s, corpus):
        if configuration['embedding']['dynamicVocab']:
            for w in s.vMWEs:
                for t in w.tokens:
                    if t.getLemma() in corpus.importantFrequentWords and uniform(0, 1) > .5:
                        return True
        return False

    def addTransData(self, trans, sent, corpus, labels, data, linearModels=None, linearNormalizers=None,
                     dynamicVocab=False):
        if not configuration['sampling']['importantTransitions'] or trans.isImportant():
            tokenIdxs, posIdxs = self.getAttachedIndices(trans, dynamicVocab=dynamicVocab)
            if linearModels:
                linearModel, linearNormalizer = getRelevantModelAndNormalizer(sent, corpus.trainingSents,
                                                                              linearModels, linearNormalizers)
                featDic = getFeatures(trans, sent)
                predTransValue = linearModel.predict(linearNormalizer.transform(featDic))[0]
                linearPredictionVector = [1 if t.value == predTransValue else 0 for t in TransitionType]
                data.append(np.asarray(np.concatenate((tokenIdxs, posIdxs, linearPredictionVector))))
            else:
                data.append(np.asarray(np.concatenate((tokenIdxs, posIdxs))))
            labels.append(trans.next.type.value if trans.next.type.value <= 2 else (
                trans.next.type.value if enableCategorization else 3))

    def getLearningData(self, corpus, linearModels=None, linearNormalizers=None):
        labels, data = [], []
        global importantFrequentWordDic
        importantFrequentWordDic = corpus.importantFrequentWords
        for sent in corpus.trainingSents:
            trans = sent.initialTransition
            shouldTrainWithDynamization = self.trainWithDynamization(sent, corpus)
            while trans and trans.next:
                self.addTransData(trans, sent, corpus, labels, data, linearModels=linearModels,
                                  linearNormalizers=linearNormalizers)
                if shouldTrainWithDynamization:
                    self.addTransData(trans, sent, corpus, labels, data, linearModels=linearModels,
                                      linearNormalizers=linearNormalizers, dynamicVocab=True)
                trans = trans.next
        return labels, data

    def getIndices(self, trans, getPos=False, getToken=False):
        s0elems, s1elems, belems = [], [], []
        emptyIdx = self.vocabulary.getEmptyIdx(getPos=getPos, getToken=getToken)
        if trans.configuration.stack:
            s0Tokens = getTokens(trans.configuration.stack[-1])
            s0elems = self.vocabulary.getIndices(s0Tokens)
            if len(trans.configuration.stack) > 1:
                s1Tokens = getTokens(trans.configuration.stack[-2])
                s1elems = self.vocabulary.getIndices(s1Tokens)
        s0elems = padSequence(s0elems, 's0Padding', emptyIdx)
        s1elems = padSequence(s1elems, 's1Padding', emptyIdx)
        if trans.configuration.buffer:
            bTokens = trans.configuration.buffer[:2]
            belems = self.vocabulary.getIndices(bTokens)
        belems = padSequence(belems, 'bPadding', emptyIdx)
        words = np.concatenate((s0elems, s1elems, belems), axis=0)
        return words

    def getAttachedIndices(self, trans, dynamicVocab=False, parse=False):
        emptyTokenIdx = self.vocabulary.tokenIndices[empty]
        emptyPosIdx = self.vocabulary.posIndices[empty]
        tokenIdxs, posIdxs = [], []
        if trans.configuration.stack:
            s0Tokens = getTokens(trans.configuration.stack[-1])
            tokenIdx, posIdx = self.vocabulary.getIndices(s0Tokens, dynamicVocab=dynamicVocab, parse=parse)
            tokenIdxs.append(tokenIdx)
            posIdxs.append(posIdx)
            if len(trans.configuration.stack) > 1:
                s1Tokens = getTokens(trans.configuration.stack[-2])
                tokenIdx, posIdx = self.vocabulary.getIndices(s1Tokens, dynamicVocab=dynamicVocab, parse=parse)
                tokenIdxs.append(tokenIdx)
                posIdxs.append(posIdx)
            else:
                tokenIdxs.append(emptyTokenIdx)
                posIdxs.append(emptyPosIdx)
        else:
            tokenIdxs.append(emptyTokenIdx)
            tokenIdxs.append(emptyTokenIdx)
            posIdxs.append(emptyPosIdx)
            posIdxs.append(emptyPosIdx)

        if trans.configuration.buffer:
            tokenIdx, posIdx = self.vocabulary.getIndices([trans.configuration.buffer[0]], dynamicVocab=dynamicVocab,
                                                          parse=parse)
            tokenIdxs.append(tokenIdx)
            posIdxs.append(posIdx)
            if configuration['embedding']['useB1']:
                if len(trans.configuration.buffer) > 1:
                    tokenIdx, posIdx = self.vocabulary.getIndices([trans.configuration.buffer[1]],
                                                                  dynamicVocab=dynamicVocab, parse=parse)
                    tokenIdxs.append(tokenIdx)
                    posIdxs.append(posIdx)
                else:
                    tokenIdxs.append(emptyTokenIdx)
                    posIdxs.append(emptyPosIdx)
        else:
            tokenIdxs.append(emptyTokenIdx)
            posIdxs.append(emptyPosIdx)
            if configuration['embedding']['useB1']:
                tokenIdxs.append(emptyTokenIdx)
                posIdxs.append(emptyPosIdx)
        if configuration['embedding']['useB-1']:
            if trans.configuration.reduced:
                tokenIdx, posIdx = self.vocabulary.getIndices([trans.configuration.reduced], dynamicVocab=dynamicVocab,
                                                              parse=parse)
                tokenIdxs.append(tokenIdx)
                posIdxs.append(posIdx)
            else:
                tokenIdxs.append(emptyTokenIdx)
                posIdxs.append(emptyPosIdx)

        return np.asarray(tokenIdxs), np.asarray(posIdxs)

    def train(self, corpus, linearModels=None, linearNormalizers=None):
        labels, data = self.getLearningData(corpus, linearModels=linearModels,
                                            linearNormalizers=linearNormalizers)
        if configuration['others']['verbose']:
            sys.stdout.write(reports.seperator + reports.tabs + 'Sampling' + reports.doubleSep)
        if configuration['sampling']['focused']:
            data, labels = sampling.overSampleImporTrans(data, labels, corpus, self.vocabulary)
        labels, data = sampling.overSample(labels, data, linearInMlp=True)
        if configuration['nn']['earlyStop']:
            # To make sure that we will get a random validation dataset
            labelsAndData = sampling.shuffleArrayInParallel(
                [labels, data[0], data[1], data[2]] if linearModels else [labels, data[0], data[1]])
            labels = labelsAndData[0]
            data = labelsAndData[1:]
        if configuration['others']['verbose']:
            lblDistribution = Counter(labels)
            sys.stdout.write(tabs + '{0} Labels in train : {1}\n'.format(len(lblDistribution), lblDistribution))
        if configuration['others']['verbose']:
            valDistribution = Counter(labels[int(len(labels) * (1 - configuration['nn']['validationSplit'])):])
            sys.stdout.write(tabs + '{0} Labels in valid : {1}\n'.format(len(valDistribution), valDistribution))
        self.classWeightDic = sampling.getClassWeights(labels)
        sampleWeights = sampling.getSampleWeightArray(labels, self.classWeightDic)
        labels = to_categorical(labels, num_classes=8 if enableCategorization else 4)
        self.model.compile(loss=configuration['nn']['loss'], optimizer=getOptimizer(), metrics=['accuracy'])
        history = self.model.fit(data, labels,
                                 validation_split=configuration['nn']['validationSplit'],
                                 epochs=configuration['nn']['epochs'],
                                 batch_size=configuration['mlp']['batchSize'],
                                 verbose=2 if configuration['others']['verbose'] else 0,
                                 callbacks=getCallBacks(),
                                 sample_weight=sampleWeights)
        if configuration['nn']['checkPoint']:
            self.model = load_model(
                os.path.join(configuration['path']['projectPath'], 'Reports', configuration['path']['checkPointPath']))
        # if configuration['others']['verbose']:
        #    sys.stdout.write('Epoch Losses = ' + str(history.history['loss']))
        self.trainValidationData(data, labels, history)

    def trainValidationData(self, data, labels, history):
        data, labels = getValidationData(data, labels)
        validationLabelsAsInt = [np.where(r == 1)[0][0] for r in labels]
        sampleWeights = sampling.getSampleWeightArray(validationLabelsAsInt, self.classWeightDic)
        history = self.model.fit(data, labels,
                                 epochs=len(history.epoch),
                                 batch_size=configuration['mlp']['batchSize'],
                                 verbose=0,
                                 sample_weight=sampleWeights)
        return history


def initEmbMatrix(vocab):
    if not configuration['embedding']['manual']:
        return None
    vocabWithoutConc, vocabWithConc = dict(), dict()
    for v in vocab:
        if '_' not in v:
            vocabWithoutConc[v] = vocab[v]
        else:
            vocabWithConc[v] = vocab[v]
    embeddingMatrix = zeros((len(vocab), configuration['mlp']['tokenEmb']))
    for i in vocabWithoutConc.values():
        embeddingMatrix[i] = np.random.uniform(low=-.5, high=.5, size=(1, configuration['mlp']['tokenEmb']))
    for k in vocabWithConc:
        tokens = k.split('_')
        allInVocab = True
        for t in tokens:
            if t not in vocabWithoutConc:
                allInVocab = False
        if not allInVocab:
            embeddingMatrix[vocabWithConc[k]] = np.random.uniform(low=-.5, high=.5,
                                                                  size=(1, configuration['mlp']['tokenEmb']))
        else:
            summ = zeros((configuration['mlp']['tokenEmb'],))
            for t in tokens:
                summ += embeddingMatrix[vocabWithoutConc[t]]
            if configuration['embedding']['average']:
                summ /= len(tokens)
            embeddingMatrix[vocabWithConc[k]] = summ
    return embeddingMatrix


def getValidationData(data, labels):
    validationData = []
    for dataTensor in data:
        validationData.append(dataTensor[int(len(dataTensor) * (1 - configuration['nn']['validationSplit'])):])
    validationLabel = labels[int(len(labels) * (1 - configuration['nn']['validationSplit'])):]
    return validationData, validationLabel


def getOptimizer():
    if configuration['others']['verbose']:
        sys.stdout.write(reports.seperator + reports.tabs +
                         'Optimizer : Adagrad,  learning rate = {0}'.format(configuration['mlp']['lr'])
                         + reports.seperator)
    return optimizers.Adagrad(lr=configuration['mlp']['lr'], epsilon=None, decay=0.0)


def getCallBacks():
    callbacks = []
    if configuration['nn']['earlyStop']:
        es = EarlyStopping(monitor='val_loss',
                           min_delta=configuration['nn']['minDelta'],
                           patience=configuration['nn']['patience'],
                           verbose=configuration['others']['verbose'])
        callbacks.append(es)
    return callbacks


class Vocabulary:
    def __init__(self, corpus):
        self.tokenFreqs, self.posFreqs = getFrequencyDics(corpus)
        self.tokenIndices = indexateDic(self.tokenFreqs)
        self.posIndices = indexateDic(self.posFreqs)
        if configuration['others']['verbose'] == 1:
            sys.stdout.write(str(self))
            self.verify(corpus)

    def __str__(self):
        res = seperator + tabs + 'Vocabulary' + doubleSep
        res += tabs + 'Tokens := {0} * POS : {1}'.format(len(self.tokenIndices), len(self.posIndices)) \
            if not configuration['xp']['compo'] else ''
        res += seperator
        return res

    def getIndices(self, tokens, dynamicVocab=False, parse=False):
        if parse:
            tokenTxt, posTxt = attachTokens(tokens, dynamicVocab=False)
        else:
            tokenTxt, posTxt = attachTokens(tokens, dynamicVocab=dynamicVocab)
        if tokenTxt in self.tokenIndices:
            tokenIdx = self.tokenIndices[tokenTxt]
        else:
            if dynamicVocab and parse:
                tokenTxt, posTxt = attachTokens(tokens, dynamicVocab=dynamicVocab, parse=parse)
                if tokenTxt in self.tokenIndices:
                    tokenIdx = self.tokenIndices[tokenTxt]
                else:
                    tokenIdx = self.tokenIndices[unk]
            else:
                tokenIdx = self.tokenIndices[unk]
        if posTxt in self.posIndices:
            posIdx = self.posIndices[posTxt]
        else:
            posIdx = self.posIndices[unk]
        return tokenIdx, posIdx

    def getEmptyIdx(self, getPos=False, getToken=False):
        pass

    def verify(self, corpus):
        importTokens = 0
        for t in corpus.mweTokenDictionary:
            if t not in self.tokenIndices:
                importTokens += 1
        if importTokens:
            sys.stdout.write(tabs + 'Important words not in vocabulary {0}\n'.format(importTokens))
        importMWEs = 0
        for mwe in corpus.mweDictionary:
            mwe = mwe.replace(' ', '_')
            if mwe not in self.tokenIndices:
                importMWEs += 1
        if importMWEs:
            sys.stdout.write(tabs + 'MWE not in vocabulary {0}\n'.format(importMWEs))
        if unk not in self.tokenIndices or empty not in self.tokenIndices:
            sys.stdout.write(tabs + 'unk or empty is not in vocabulary\n')
        dashedKeys = 0
        for k in self.tokenIndices:
            if '_' in k:
                dashedKeys += 1
        # supposedDashedKeys = 0
        # for mwe in corpus.mweDictionary:
        #     supposedDashedKeys += len(mwe.split(' ')) - 1
        # sys.stdout.write(tabs + 'Suupposed dashed keys in vocabulary {0}\n'.format(supposedDashedKeys))
        sys.stdout.write(tabs + 'Dashed keys in vocabulary {0}\n'.format(dashedKeys))
        oneFreq = 0
        for k in self.tokenFreqs:
            if self.tokenFreqs[k] == 1:
                oneFreq += 1
        sys.stdout.write(tabs + 'One occurrence keys in vocabulary {0} / {1}\n'.
                         format(dashedKeys, len(self.tokenFreqs)))


def addDynamicVersion(tokens, corpus):
    if not configuration['embedding']['dynamicVocab'] or not tokens or len(tokens) <= 1:
        return None
    shouldDynamize = [True if t.getLemma() in corpus.importantFrequentWords else False for t in tokens]
    if False in shouldDynamize and True in shouldDynamize:
        return '_'.join(
            t.getTokenOrLemma() if t.getLemma() in corpus.importantFrequentWords else unk for t in tokens)
    return None


def getFrequencyDics(corpus, freqTaux=1):
    dynamicVocab = set()
    tokenVocab, posVocab = {unk: freqTaux + 1, empty: freqTaux + 1}, {unk: freqTaux + 1, empty: freqTaux + 1}
    for sent in corpus.trainingSents:
        trans = sent.initialTransition
        while trans:
            if trans.configuration.stack:
                tokens = getTokens(trans.configuration.stack[-1])
                if tokens:
                    tokenTxt, posTxt = attachTokens(tokens)
                    for c in tokenTxt:
                        if c.isdigit():
                            tokenTxt = number
                    tokenVocab[tokenTxt] = 1 if tokenTxt not in tokenVocab else tokenVocab[tokenTxt] + 1
                    posVocab[posTxt] = 1 if posTxt not in posVocab else posVocab[posTxt] + 1
                    tokenTxt = addDynamicVersion(tokens, corpus)
                    if tokenTxt:
                        dynamicVocab.add(tokenTxt)
                        tokenVocab[tokenTxt] = 1 if tokenTxt not in tokenVocab else tokenVocab[tokenTxt] + 1
            trans = trans.next

    tokenVocab = cleanTokenVocab(tokenVocab, corpus, freqTaux=freqTaux)
    # if configuration['others']['verbose']:
    #     sys.stdout.write(tabs + 'Dynamic tokens:' + doubleSep)
    #     for i in range(10):
    #         idx = random.randint(0, len(dynamicVocab))
    #         print list(dynamicVocab)[idx]
    return tokenVocab, posVocab


def cleanTokenVocab(tokenVocab, corpus, freqTaux=1):
    if configuration['embedding']['compactVocab']:
        if configuration['others']['verbose']:
            sys.stdout.write(tabs + 'Compact Vocabulary cleaning:' + doubleSep)
            sys.stdout.write(tabs + 'Before : {0}\n'.format(len(tokenVocab)))
        for k in tokenVocab.keys():
            if k not in [empty, unk, number] and k.lower() not in corpus.mweTokenDictionary and '_' not in k:
                del tokenVocab[k]
        if configuration['others']['verbose']:
            sys.stdout.write(tabs + 'After : {0}\n'.format(len(tokenVocab)))

    else:
        if configuration['others']['verbose']:
            sys.stdout.write(tabs + 'Non frequent word cleaning:' + doubleSep)
            sys.stdout.write(tabs + 'Before : {0}\n'.format(len(tokenVocab)))
        for k in tokenVocab.keys():
            if tokenVocab[k] <= freqTaux and '_' not in k and k.lower() not in corpus.mweTokenDictionary:
                if uniform(0, 1) < configuration['constants']['alpha']:
                    del tokenVocab[k]
        if configuration['others']['verbose']:
            sys.stdout.write(tabs + 'After : {0}\n'.format(len(tokenVocab)))

    return tokenVocab


def attachTokens(tokens, dynamicVocab=False, parse=False):
    tokenTxt, posTxt = '', ''
    global importantFrequentWordDic
    if dynamicVocab:
        for t in tokens:
            if parse:
                if len(tokens) > 1:
                    if t.getLemma() in importantFrequentWordDic:
                        tokenTxt += t.getTokenOrLemma() + '_'
                    else:
                        tokenTxt += unk + '_'
                else:
                    tokenTxt += t.getTokenOrLemma() + '_'
            else:
                if t.getLemma() in importantFrequentWordDic:
                    tokenTxt += t.getTokenOrLemma() + '_'
                else:
                    tokenTxt += unk + '_'
        tokenTxt = tokenTxt[:-1]
    else:
        tokenTxt = '_'.join(t.getTokenOrLemma() for t in tokens)
    posTxt = '_'.join(t.posTag for t in tokens)
    return tokenTxt, posTxt.lower()


def indexateDic(dic):
    res = dict()
    r = range(len(dic))
    for i, k in enumerate(dic):
        res[k] = r[i]
    return res


def padSequence(seq, label, emptyIdx):
    padConf = configuration['mlpNonLexicl']
    return np.asarray(pad_sequences([seq], maxlen=padConf[label], value=emptyIdx))[0]
