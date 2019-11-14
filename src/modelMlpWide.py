from random import uniform

import keras
import numpy as np
from imblearn.over_sampling import RandomOverSampler
from keras import optimizers
from keras.callbacks import EarlyStopping
from keras.layers import Input, Dense, Flatten, Embedding, Dropout
from keras.models import Model
from keras.utils import to_categorical

import reports
import sampling
from corpus import getTokens
from reports import *
from vocabTools import empty
from vocabTools import unk, number

enableCategorization = False

importantFrequentWordDic = dict()


class Network:
    def __init__(self, corpus):
        self.vocabulary = Vocabulary(corpus)
        inputs, output = createTheModel(self.vocabulary)
        self.model = Model(inputs=inputs, outputs=output)
        if configuration['others']['verbose']:
            sys.stdout.write('# Parameters = {0}\n'.format(self.model.count_params()))
            sys.stdout.write(str(self.model.summary()))

    def predict(self, trans):
        inputs = getTransData(trans, self.vocabulary)
        inputs = [np.asarray([i]) for i in inputs]
        oneHotRep = self.model.predict(inputs, batch_size=1, verbose=configuration['nn']['predictVerbose'])
        return oneHotRep[0]

    def train(self, corpus):
        labels, data = getLearningData(corpus, self.vocabulary)
        if configuration['others']['verbose']:
            sys.stdout.write(reports.seperator + reports.tabs + 'Sampling' + reports.doubleSep)
        labels, data = overSample(labels, data)
        if configuration['nn']['earlyStop']:
            # To make sure that we will get a random validation dataset
            labelsAndData = sampling.shuffleArrayInParallel([labels, data[0], data[1]])
            labels = labelsAndData[0]
            data = labelsAndData[1:]
        if configuration['others']['verbose']:
            lblDistribution = Counter(labels)
            sys.stdout.write(tabs + '{0} Labels in train : {1}\n'.format(len(lblDistribution), lblDistribution))
        if configuration['others']['verbose']:
            valDistribution = Counter(labels[int(len(labels) * (1 - configuration['nn']['validationSplit'])):])
            sys.stdout.write(tabs + '{0} Labels in valid : {1}\n'.format(len(valDistribution), valDistribution))
        labels = to_categorical(labels, num_classes=8 if enableCategorization else 4)
        self.model.compile(loss=configuration['nn']['loss'], optimizer=getOptimizer(), metrics=['accuracy'])
        es = EarlyStopping(monitor='val_loss',
                           min_delta=configuration['nn']['minDelta'],
                           patience=configuration['nn']['patience'],
                           verbose=configuration['others']['verbose'])
        history = self.model.fit(data, labels,
                                 validation_split=configuration['nn']['validationSplit'],
                                 epochs=configuration['nn']['epochs'],
                                 batch_size=configuration['mlp']['batchSize'],
                                 verbose=2 if configuration['others']['verbose'] else 0,
                                 callbacks=[es])
        self.trainValidationData(data, labels, history)

    def trainValidationData(self, data, labels, history):
        data, labels = getValidationData(data, labels)
        history = self.model.fit(data, labels,
                                 epochs=len(history.epoch),
                                 batch_size=configuration['mlp']['batchSize'],
                                 verbose=0)
        return history


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


class Vocabulary:
    def __init__(self, corpus):
        self.tokenFreqs, self.posFreqs = getFrequencyDics(corpus)
        self.tokenIndices = indexateDic(self.tokenFreqs)
        self.posIndices = indexateDic(self.posFreqs)

    def getIndices(self, tokens):
        tokenTxt, posTxt = attachTokens(tokens)
        if tokenTxt in self.tokenIndices:
            tokenIdx = self.tokenIndices[tokenTxt]
        else:
            tokenIdx = self.tokenIndices[unk]
        if posTxt in self.posIndices:
            posIdx = self.posIndices[posTxt]
        else:
            posIdx = self.posIndices[unk]
        return tokenIdx, posIdx


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
                    if tokenTxt:
                        tokenVocab[tokenTxt] = 1 if tokenTxt not in tokenVocab else tokenVocab[tokenTxt] + 1

            trans = trans.next
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
    return tokenVocab, posVocab


def attachTokens(tokens):
    tokenTxt, posTxt = '', ''
    global importantFrequentWordDic
    for t in tokens:
        tokenTxt += t.getTokenOrLemma() + '_'
        posTxt += t.posTag + '_'
    return tokenTxt[:-1], posTxt[:-1].lower()


def indexateDic(dic):
    res = dict()
    r = range(len(dic))
    for i, k in enumerate(dic):
        res[k] = r[i]
    return res


def getLearningData(corpus, vocab):
    labels, data = [], []
    global importantFrequentWordDic
    for sent in corpus.trainingSents:
        trans = sent.initialTransition
        while trans and trans.next:
            tokenIdxs, posIdxs = getTransData(trans, vocab)
            data.append(np.asarray(np.concatenate((tokenIdxs, posIdxs))))
            labels.append(trans.next.type.value if trans.next.type.value <= 2 else (
                trans.next.type.value if enableCategorization else 3))
            trans = trans.next
    return labels, data


def getTransData(trans, vocabulary, window=configuration['mlp']['posWindow']):
    tokenIdxs, posIdxs, emptyTokenIdx = [], [], vocabulary.tokenIndices[empty]
    if trans.configuration.stack:
        s0Tokens = getTokens(trans.configuration.stack[-1])
        tokenIdx, posIdx = vocabulary.getIndices(s0Tokens)
        tokenIdxs.append(tokenIdx)
        getPosTags(trans.sent, s0Tokens, vocabulary.posIndices, posIdxs, window=window)
        if len(trans.configuration.stack) > 1:
            s1Tokens = getTokens(trans.configuration.stack[-2])
            tokenIdx, posIdx = vocabulary.getIndices(s1Tokens)
            tokenIdxs.append(tokenIdx)
            getPosTags(trans.sent, s0Tokens, vocabulary.posIndices, posIdxs, window=window)
        else:
            tokenIdxs.append(emptyTokenIdx)
            getPosTags(trans.sent, [], vocabulary.posIndices, posIdxs, window=window)
    else:
        tokenIdxs.append(emptyTokenIdx)
        tokenIdxs.append(emptyTokenIdx)
        getPosTags(trans.sent, [], vocabulary.posIndices, posIdxs, window=window)
        getPosTags(trans.sent, [], vocabulary.posIndices, posIdxs, window=window)

    if trans.configuration.buffer:
        tokenIdx, posIdx = vocabulary.getIndices([trans.configuration.buffer[0]],
                                                 )
        tokenIdxs.append(tokenIdx)
        getPosTags(trans.sent, [trans.configuration.buffer[0]], vocabulary.posIndices, posIdxs,
                   window=window)
        if configuration['embedding']['useB1']:
            if len(trans.configuration.buffer) > 1:
                tokenIdx, posIdx = vocabulary.getIndices([trans.configuration.buffer[1]],
                                                         )
                tokenIdxs.append(tokenIdx)
                getPosTags(trans.sent, [trans.configuration.buffer[1]], vocabulary.posIndices, posIdxs,
                           window=window)
            else:
                tokenIdxs.append(emptyTokenIdx)
                for _ in range(window * 2 + 1):
                    posIdxs.append(vocabulary.posIndices[empty])
    else:
        tokenIdxs.append(emptyTokenIdx)
        getPosTags(trans.sent, [], vocabulary.posIndices, posIdxs, window=window)
        if configuration['embedding']['useB1']:
            tokenIdxs.append(emptyTokenIdx)
            getPosTags(trans.sent, [], vocabulary.posIndices, posIdxs, window=window)
    if configuration['embedding']['useB-1']:
        if trans.configuration.reduced:
            tokenIdx, posIdx = vocabulary.getIndices([trans.configuration.reduced],
                                                     )
            tokenIdxs.append(tokenIdx)
            getPosTags(trans.sent, [trans.configuration.reduced], vocabulary.posIndices, posIdxs,
                       window=window)
        else:
            tokenIdxs.append(emptyTokenIdx)
            getPosTags(trans.sent, [], vocabulary.posIndices, posIdxs, window=window)

    return np.asarray(tokenIdxs), np.asarray(posIdxs)


def createTheModel(vocabulary, window=configuration['mlp']['posWindow']):
    inputLayers, interLayers = [], []
    inputToken = Input((3 + configuration['embedding']['useB1'] + configuration['embedding']['useB-1'],))
    inputLayers.append(inputToken)
    tokenEmb = Embedding(len(vocabulary.tokenIndices), configuration['mlp']['tokenEmb'],
                         trainable=configuration['mlp']['trainable'])(inputToken)
    tokenFlatten = Flatten()(tokenEmb)
    interLayers.append(tokenFlatten)
    posNum = (2 * window + 1) * (3 + configuration['embedding']['useB1'] + configuration['embedding']['useB-1'])
    inputPos = Input((posNum,))
    inputLayers.append(inputPos)
    posEmb = Embedding(len(vocabulary.posIndices), configuration['mlp']['posEmb'],
                       trainable=configuration['mlp']['trainable'])(inputPos)
    posFlatten = Flatten()(posEmb)
    interLayers.append(posFlatten)

    interLayers = keras.layers.concatenate(interLayers)
    lastLayer = Dense(configuration['mlp']['dense1UnitNumber'],
                      activation=configuration['nn']['dense1Activation'])(interLayers)
    # dropout=configuration['mlp']['dense1Dropout'])(interLayers)
    lastLayer = Dropout(configuration['mlp']['dense1Dropout'])(lastLayer)
    softmaxLayer = Dense(8 if enableCategorization else 4, activation='softmax')(lastLayer)
    return inputLayers, softmaxLayer


def overSample(labels, data):
    tokenData, posData = [], []
    tokenNum = 3 + configuration['embedding']['useB1'] + configuration['embedding']['useB-1']
    if configuration['others']['verbose']:
        sys.stdout.write(reports.doubleSep + reports.tabs + 'Resampling:' + reports.doubleSep)
        sys.stdout.write(reports.tabs + 'data size before sampling = {0}\n'.format(len(labels)))
    ros = RandomOverSampler(random_state=0)
    data, labels = ros.fit_sample(data, labels)
    for item in data:
        tokenData.append(np.asarray(item[:tokenNum]))
        posData.append(np.asarray(item[tokenNum:]))
    if configuration['others']['verbose']:
        sys.stdout.write(reports.tabs + 'data size after sampling = {0}\n'.format(len(labels)))
    return np.asarray(labels), [np.asarray(tokenData), np.asarray(posData)]


def getPosTags(sent, tokens, vocab, posTags, window=configuration['mlp']['posWindow']):
    if not tokens:
        for _ in range(window * 2 + 1):
            posTags.append(vocab[empty])
        return
    positions = [t.position for t in tokens]
    minPos, maxPos = min(positions) - 1, max(positions) - 1
    for i in reversed(range(1, window + 1)):
        if minPos - i >= 0:
            token = sent.tokens[minPos - i]
            if token.posTag.lower() in vocab:
                posTags.append(vocab[token.posTag.lower()])
            else:
                posTags.append(vocab[unk])
        else:
            posTags.append(vocab[empty])
    if len(tokens) == 1:
        if tokens[0].posTag.lower() in vocab:
            posTags.append(vocab[tokens[0].posTag.lower()])
        else:
            posTags.append(vocab[unk])
    else:
        posTag = '_'.join(t.posTag.lower() for t in tokens)
        if posTag in vocab:
            posTags.append(vocab[posTag])
        else:
            posTags.append(vocab[unk])

    for i in range(1, window + 1):
        if maxPos + i < len(sent.tokens):
            token = sent.tokens[maxPos + i]
            if token.posTag.lower() in vocab:
                posTags.append(vocab[token.posTag.lower()])
            else:
                posTags.append(vocab[unk])
        else:
            posTags.append(vocab[empty])
    return posTags
