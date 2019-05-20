from random import uniform

import keras
import numpy as np
from keras import optimizers
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import Input, Dense, Flatten, Embedding
from keras.models import Model
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from numpy import zeros

import reports
from corpus import getRelevantModelAndNormalizer
from corpus import getTokens
from modelLinear import getFeatures
from reports import *
from transitions import TransitionType
from wordEmbLoader import empty
from wordEmbLoader import unk, number

enableCategorization = False

importantFrequentWordDic = dict()


class Network:
    def __init__(self, corpus):
        self.vocabulary = Vocabulary(corpus)
        self.taggingModel, self.idenModel = createTheModel(self.vocabulary)

    def predict(self, trans, linearModels=None, linearVecs=None):
        pass
        # inputs = []
        # tokenIdxs, posIdxs = self.getAttachedIndices(trans, dynamicVocab=configuration['embedding']['dynamicVocab'],
        #                                              parse=True)
        # inputs.append(np.asarray([tokenIdxs]))
        # inputs.append(np.asarray([posIdxs]))
        # if linearModels and linearVecs:
        #     linearModel, linearVec = getRelevantModelAndNormalizer(trans.sent, None, linearModels, linearVecs, True)
        #     featDic = getFeatures(trans, trans.sent)
        #     predTrans = linearModel.predict(linearVec.transform(featDic))[0]
        #     predVec = [1 if t.value == predTrans else 0 for t in TransitionType]
        #     inputs.append(np.asarray([predVec]))
        # if configuration['mlp2']['features']:
        #     features = np.asarray(self.nnExtractor.vectorize(trans))
        #     inputs.append(np.asarray([features]))
        # oneHotRep = self.model.predict(inputs, batch_size=1,
        #                                verbose=configuration['nn']['predictVerbose'])
        # return oneHotRep[0]

    def train(self, corpus):
        epochNumber = 100
        taggingBatchSize = 32
        taggingData, taggingLbls = self.getTaggingData(corpus)
        idenData, idenLbls = self.getIdenData(corpus)
        self.taggingModel.fit(taggingData, taggingLbls, validation_split=.2, epochs=1,
                              batch_size=taggingBatchSize, verbose=2)
        idenLoss, taggingLoss = [], []
        for i in range(epochNumber):
            if uniform(0, 1) > .5:
                history = self.taggingModel.fit(taggingData, taggingLbls, validation_split=.2, epochs=1,
                                                batch_size=taggingBatchSize, verbose=2)
                taggingLoss.append(history.history['loss'])
            else:
                history = self.idenModel.fit(idenData, idenLbls, validation_split=.2, epochs=1,
                                             batch_size=taggingBatchSize, verbose=2)
                idenLoss.append(history.history['loss'])
            # TODO check the early stopping

    def trainTagging(self, corpus):
        taggingBatchSize = 32
        taggingData, taggingLbls = self.getTaggingData(corpus)
        taggingLbls = to_categorical(taggingLbls, num_classes=len(self.vocabulary.posIndices))
        self.taggingModel.fit(taggingData, taggingLbls, validation_split=.2, epochs=100,
                              batch_size=taggingBatchSize, verbose=2, callbacks=[
                                EarlyStopping(  monitor='val_loss',
                                                min_delta=configuration['nn']['minDelta'],
                                                patience=configuration['nn']['patience'],
                                                verbose=configuration['others']['verbose'])])


    def testTagging(self, corpus):
        taggingData, taggingLbls =  self.getTaggingData(corpus, train=False)
        taggingLbls = to_categorical(taggingLbls, num_classes=len(self.vocabulary.posIndices))
        results = self.taggingModel.evaluate(taggingData, taggingLbls, batch_size=32, verbose=0)
        sys.stdout.write('Loss = {0}, Accuracy = {1}'.format(round(results[0],3), round(results[1] * 100, 1)))

    def getTaggingData(self, corpus, train=True):
        data, lbls = [], []
        for s in corpus.trainingSents if train else corpus.testingSents:
            for t in s.tokens:
                d, lbl = self.getTokenWindow(t, s)
                data.append(np.asarray(d))
                lbls.append(lbl)
            for w in s.vMWEs:
                d, lbl = self.getMWEWindow(w, s)
                data.append(np.asarray(d))
                lbls.append(lbl)
        return np.asarray(data), lbls

    def getIdenData(self, corpus, linearModels=None, linearNormalizers=None):
        labels, data = [], []
        global importantFrequentWordDic
        importantFrequentWordDic = corpus.importantFrequentWords
        for sent in corpus.trainingSents:
            trans = sent.initialTransition
            while trans and trans.next:
                self.addTransData(trans, sent, corpus, labels, data, linearModels=linearModels,
                                  linearNormalizers=linearNormalizers)
                trans = trans.next
        return labels, data

    def getTokenWindow(self, t, s):
        windowSize = configuration['multitasking']['windowSize']
        tIdx = s.tokens.index(t)
        tokenIdxs = []
        res = t.text + ' ' + str(tIdx)
        for c in [1, -1]:
            for i in reversed(range(1, windowSize + 1)) if c == 1 else range(1, windowSize + 1):
                if len(s.tokens) > tIdx - i * c >= 0:
                    currentToken = s.tokens[tIdx - i * c]
                    if currentToken.getTokenOrLemma() in self.vocabulary.tokenIndices:
                        tokenIdxs.append(self.vocabulary.tokenIndices[currentToken.getTokenOrLemma()])
                        res += ' ' + currentToken.getTokenOrLemma()
                    else:
                        tokenIdxs.append(self.vocabulary.tokenIndices[unk])
                        res += ' unk'
                else:
                    tokenIdxs.append(self.vocabulary.tokenIndices[empty])
                    res += ' empty'
        if t.getTokenOrLemma() in self.vocabulary.tokenIndices:
            tokenIdxs.append(self.vocabulary.tokenIndices[t.getTokenOrLemma()])
            res += ' ' + t.getTokenOrLemma()
        else:
            tokenIdxs.append(self.vocabulary.tokenIndices[unk])
            res += ' unk'
        return tokenIdxs, self.vocabulary.posIndices[
            t.posTag.lower() if t.posTag.lower() in self.vocabulary.posIndices else unk]

    def getMWEWindow(self, w, s):
        windowSize = configuration['multitasking']['windowSize']
        positions = [int(t.position) - 1 for t in w.tokens]
        minPos, maxPos, tokenIdxs = min(positions), max(positions), []
        res = w.getLemmaString() + ' ' + str(minPos) + ' ' + str(maxPos) + ' '
        if minPos < 5 or maxPos > len(s.tokens) - 5:
            pass
        for i in reversed(range(1, windowSize + 1)):
            if minPos - i >= 0:
                currentToken = s.tokens[minPos - i]
                if currentToken.getTokenOrLemma() in self.vocabulary.tokenIndices:
                    tokenIdxs.append(self.vocabulary.tokenIndices[currentToken.getTokenOrLemma()])
                    res += currentToken.getTokenOrLemma() + ' '
                else:
                    tokenIdxs.append(self.vocabulary.tokenIndices[unk])
                    res += 'unk '
            else:
                tokenIdxs.append(self.vocabulary.tokenIndices[empty])
                res += 'emp '
        for i in range(1, windowSize + 1):
            if maxPos + i < len(s.tokens):
                currentToken = s.tokens[maxPos + i]
                if currentToken.getTokenOrLemma() in self.vocabulary.tokenIndices:
                    tokenIdxs.append(self.vocabulary.tokenIndices[currentToken.getTokenOrLemma()])
                    res += currentToken.getTokenOrLemma() + ' '
                else:
                    tokenIdxs.append(self.vocabulary.tokenIndices[unk])
                    res += 'unk '
            else:
                tokenIdxs.append(self.vocabulary.tokenIndices[empty])
                res += 'emp '
        attachedPos = '_'.join(t.posTag.lower() for t in w.tokens)
        posIdx = self.vocabulary.posIndices[attachedPos.lower()
        if attachedPos in self.vocabulary.posIndices else unk]
        xStr = w.getLemmaString().replace(' ', '_')
        if xStr in self.vocabulary.tokenIndices:
            tokenIdxs.append(self.vocabulary.tokenIndices[xStr])
            res += ' ' + xStr
        else:
            tokenIdxs.append(self.vocabulary.tokenIndices[unk])
            res += ' unk'
        return tokenIdxs, posIdx

    # def getWeightMatrix(self, tokenVocab, lang):
    #     if configuration['embedding']['pretrained']:
    #         self.vocabulary.tokenIndices, embeddingMatrix = facebookEmb.getEmbMatrix(lang, tokenVocab.keys())
    #         return [embeddingMatrix]
    #     elif configuration['embedding']['manual']:
    #         return [initEmbMatrix(tokenVocab)]
    #     else:
    #         return None

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

    # def train(self, corpus, linearModels=None, linearNormalizers=None):
    #     labels, data = self.getLearningData(corpus, linearModels=linearModels,
    #                                         linearNormalizers=linearNormalizers)
    #     if configuration['others']['verbose']:
    #         sys.stdout.write(reports.seperator + reports.tabs + 'Sampling' + reports.doubleSep)
    #     if configuration['sampling']['focused']:
    #         data, labels = sampling.overSampleImporTrans(data, labels, corpus, self.vocabulary)
    #     labels, data = sampling.overSample(labels, data, linearInMlp=True)
    #     if configuration['nn']['earlyStop']:
    #         # To make sure that we will get a random validation dataset
    #         labelsAndData = sampling.shuffleArrayInParallel(
    #             [labels, data[0], data[1], data[2]] if linearModels else [labels, data[0], data[1]])
    #         labels = labelsAndData[0]
    #         data = labelsAndData[1:]
    #     if configuration['others']['verbose']:
    #         lblDistribution = Counter(labels)
    #         sys.stdout.write(tabs + '{0} Labels in train : {1}\n'.format(len(lblDistribution), lblDistribution))
    #     if configuration['others']['verbose']:
    #         valDistribution = Counter(labels[int(len(labels) * (1 - configuration['nn']['validationSplit'])):])
    #         sys.stdout.write(tabs + '{0} Labels in valid : {1}\n'.format(len(valDistribution), valDistribution))
    #     self.classWeightDic = sampling.getClassWeights(labels)
    #     sampleWeights = sampling.getSampleWeightArray(labels, self.classWeightDic)
    #     labels = to_categorical(labels, num_classes=8 if enableCategorization else 4)
    #     self.model.compile(loss=configuration['nn']['loss'], optimizer=getOptimizer(), metrics=['accuracy'])
    #     history = self.model.fit(data, labels,
    #                              validation_split=configuration['nn']['validationSplit'],
    #                              epochs=configuration['nn']['epochs'],
    #                              batch_size=configuration['mlp']['batchSize'],
    #                              verbose=2 if configuration['others']['verbose'] else 0,
    #                              callbacks=getCallBacks(),
    #                              sample_weight=sampleWeights)
    #     if configuration['nn']['checkPoint']:
    #         self.model = load_model(
    #             os.path.join(configuration['path']['projectPath'],
    #               'Reports', configuration['path']['checkPointPath']))
    #     # if configuration['others']['verbose']:
    #     #    sys.stdout.write('Epoch Losses = ' + str(history.history['loss']))
    #     self.trainValidationData(data, labels, history)

    # def trainValidationData(self, data, labels, history):
    #     data, labels = getValidationData(data, labels)
    #     validationLabelsAsInt = [np.where(r == 1)[0][0] for r in labels]
    #     sampleWeights = sampling.getSampleWeightArray(validationLabelsAsInt, self.classWeightDic)
    #     history = self.model.fit(data, labels,
    #                              epochs=len(history.epoch),
    #                              batch_size=configuration['mlp']['batchSize'],
    #                              verbose=0,
    #                              sample_weight=sampleWeights)
    #     return history


def createTheModel(vocab):
    inputSize, parsingInfoDim, tokenEmb = configuration['multitasking']['windowSize']*2 + 1, 1000, configuration['multitasking']['tokenDim']
    inputTagging = Input((inputSize,))
    sharedEmb = Embedding(len(vocab.tokenIndices), tokenEmb)
    # weights=self.getWeightMatrix(self.vocabulary.tokenIndices, lang))
    taggingEmb = sharedEmb(inputTagging)
    taggingFlatten = Flatten()(taggingEmb)
    taggingDense = Dense(100, activation='relu')(taggingFlatten)
    taggingSoftmax = Dense(len(vocab.posIndices), activation='softmax')(taggingDense)
    taggingModel = Model(inputs=inputTagging, outputs=taggingSoftmax)
    taggingModel.compile(loss=configuration['nn']['loss'],
                         optimizer=getOptimizer(),
                         metrics=['accuracy'])
    if configuration['others']['verbose']:
        sys.stdout.write(str(taggingModel.summary()) + doubleSep)
    inputBx = Input((inputSize,))
    inputB1 = Input((inputSize,))
    inputB0 = Input((inputSize,))
    inputS0 = Input((inputSize,))
    inputS1 = Input((inputSize,))
    inputLayers = [inputBx, inputB1, inputB0, inputS0, inputS1]
    bxEmb = sharedEmb(inputBx)
    b1Emb = sharedEmb(inputB1)
    b0Emb = sharedEmb(inputB0)
    s0Emb = sharedEmb(inputS0)
    s1Emb = sharedEmb(inputS1)

    bxDense = Dense(50, activation='relu')(bxEmb)
    b1Dense = Dense(50, activation='relu')(b1Emb)
    b0Dense = Dense(50, activation='relu')(b0Emb)
    s0Dense = Dense(50, activation='relu')(s0Emb)
    s1Dense = Dense(50, activation='relu')(s1Emb)

    concDense = keras.layers.concatenate([bxDense, b1Dense, b0Dense, s0Dense, s1Dense])
    idenDense = Dense(500, activation='relu')(concDense)
    idenSoftmax = Dense(4, activation='softmax')(idenDense)
    idenModel = Model(inputs=inputLayers, outputs=idenSoftmax)
    idenModel.compile(loss=configuration['nn']['loss'],
                      optimizer=getOptimizer(),
                      metrics=['accuracy'])

    if configuration['others']['verbose']:
        sys.stdout.write(str(idenModel.summary()) + doubleSep)
    return taggingModel, idenModel


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
    bestWeightPath = reports.getBestWeightFilePath()
    callbacks = [
        ModelCheckpoint(bestWeightPath, monitor='val_loss', verbose=1, save_best_only=True, mode='max')
    ] if bestWeightPath else []
    if configuration['nn']['earlyStop']:
        callbacks.append(
            EarlyStopping(monitor='val_loss',
                          min_delta=configuration['nn']['minDelta'],
                          patience=configuration['nn']['patience'],
                          verbose=configuration['others']['verbose']))
    if configuration['nn']['checkPoint']:
        mc = ModelCheckpoint(
            os.path.join(configuration['path']['projectPath'], 'Reports', configuration['path']['checkPointPath']),
            monitor='val_acc', mode='max', verbose=1, save_best_only=True)
        callbacks.append(mc)
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
                        tokenVocab[tokenTxt] = 1 if tokenTxt not in tokenVocab else tokenVocab[tokenTxt] + 1

            trans = trans.next
    if configuration['others']['verbose']:
        sys.stdout.write(tabs + 'Non frequent word cleaning:' + doubleSep)
        sys.stdout.write(tabs + 'Before : {0}\n'.format(len(tokenVocab)))
    for k in tokenVocab.keys():
        if tokenVocab[k] <= freqTaux and '_' not in k and k.lower() not in corpus.mweTokenDictionary:
            if uniform(0, 1) < configuration['constants']['alpha']:
                del tokenVocab[k]
    if configuration['others']['verbose']:
        sys.stdout.write(tabs + 'After : {0}\n'.format(len(tokenVocab)))
    return tokenVocab, posVocab


def attachTokens(tokens, dynamicVocab=False, parse=False):
    tokenTxt, posTxt = '', ''
    global importantFrequentWordDic
    for t in tokens:
        if dynamicVocab:
            if parse:
                if len(tokens) > 1:
                    # for tt in tokens:
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
        else:
            tokenTxt += t.getTokenOrLemma() + '_'
        posTxt += t.posTag + '_'
    return tokenTxt[:-1], posTxt[:-1].lower()


def indexateDic(dic):
    res = dict()
    r = range(len(dic))
    for i, k in enumerate(dic):
        res[k] = r[i]
    return res


def padSequence(seq, label, emptyIdx):
    padConf = configuration['mlpNonLexicl']
    return np.asarray(pad_sequences([seq], maxlen=padConf[label], value=emptyIdx))[0]
