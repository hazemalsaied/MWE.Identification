#!/usr/bin/env python
# -*- coding: utf-8 -
import sys
from collections import Counter

import numpy as np
from imblearn.over_sampling import RandomOverSampler
from keras import optimizers
from keras.callbacks import EarlyStopping
from keras.layers import Input, Dense, Embedding, Flatten, GRU, LSTM, concatenate
from keras.models import Model
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical

import reports
import sampling
from config import configuration
from corpus import getTokens
from modelMLP import Vocabulary
from reports import tabs
from vocabTools import empty, unk


class Network:
    def __init__(self, vocab, model):
        self.vocabulary = vocab
        self.model = model

    def predict(self, trans):
        inputs = getTransData(trans, self.vocabulary)
        newInputs = [np.asarray([i]) for i in inputs]
        oneHotRep = self.model.predict(newInputs, batch_size=1, verbose=configuration['nn']['predictVerbose'])
        return oneHotRep[0]


def createTheModel(tokenVocab, posVocab):
    mlpPhraseConf = configuration['mlpPhrase']
    phraseTokens = Input((mlpPhraseConf['phraseMaxLength'],), name='phraseTokens')
    phrasePoss = Input((mlpPhraseConf['phraseMaxLength'],), name='phrasePoss')
    phraseTokEmb = Embedding(len(tokenVocab), configuration['mlpPhrase']['phraseTokenEmb'], name='phraseTokenEmb')(
        phraseTokens)
    phrasePosEmb = Embedding(len(posVocab), configuration['mlpPhrase']['phrasePosEmb'], name='phrasePosEmb')(phrasePoss)
    phraseEmb = concatenate([phraseTokEmb, phrasePosEmb])

    if mlpPhraseConf['gru']:
        phraseRnn = GRU(mlpPhraseConf['wordRnnUnitNum'], name='phraseRnn')(phraseEmb)
    else:
        phraseRnn = LSTM(mlpPhraseConf['wordRnnUnitNum'], name='phraseRnn')(phraseEmb)

    tranTokNum = 3 + mlpPhraseConf['useB1'] + mlpPhraseConf['useB-1']
    transTokens = Input((tranTokNum,), name='transTokens')
    transPoss = Input((tranTokNum,), name='transPoss')
    transTokEmb = Embedding(len(tokenVocab), mlpPhraseConf['transTokenEmb'], name='transTokenEmb')(
        transTokens)
    transPosEmb = Embedding(len(posVocab), mlpPhraseConf['transPosEmb'], name='transPosEmb')(transPoss)
    transTokEmb = Flatten(name='transTokenFlat')(transTokEmb)
    transPosEmb = Flatten(name='transPosFlat')(transPosEmb)
    transEmb = concatenate([transTokEmb, transPosEmb])
    inputEmb = concatenate([phraseRnn, transEmb])
    denseLayer = Dense(mlpPhraseConf['denseUnitNumber'], activation='relu')(inputEmb)
    softmax = Dense(4, activation='softmax')(denseLayer)
    model = Model(inputs=[transTokens, transPoss, phraseTokens, phrasePoss], outputs=softmax)
    sys.stdout.write(str(model.summary()))
    return model


def train(corpus):
    vocab = Vocabulary(corpus)
    model = createTheModel(vocab.tokenIndices, vocab.posIndices)
    labels, data = getLearningData(corpus, vocab)

    if configuration['others']['verbose']:
        sys.stdout.write(reports.seperator + reports.tabs + 'Sampling' + reports.doubleSep)
    labels, data = overSample(labels, data)
    if configuration['nn']['earlyStop']:
        # To make sure that we will get a random validation dataset
        labelsAndData = sampling.shuffleArrayInParallel([labels, data[0], data[1], data[2], data[3]])
        labels = labelsAndData[0]
        data = labelsAndData[1:]
    if configuration['others']['verbose']:
        lblDistribution = Counter(labels)
        sys.stdout.write(tabs + '{0} Labels in train : {1}\n'.format(len(lblDistribution), lblDistribution))
    if configuration['others']['verbose']:
        valDistribution = Counter(labels[int(len(labels) * (1 - configuration['nn']['validationSplit'])):])
        sys.stdout.write(tabs + '{0} Labels in valid : {1}\n'.format(len(valDistribution), valDistribution))
    labels = to_categorical(labels, num_classes=4)

    optim = optimizers.Adagrad(lr=configuration['mlpPhrase']['lr'], epsilon=None, decay=0.0)
    es = EarlyStopping(monitor='val_loss',
                       min_delta=configuration['nn']['minDelta'],
                       patience=configuration['nn']['patience'],
                       verbose=configuration['others']['verbose'])
    model.compile(loss=configuration['nn']['loss'], optimizer=optim, metrics=['accuracy'])
    model.fit(data, labels,
              validation_split=configuration['nn']['validationSplit'],
              epochs=configuration['nn']['epochs'],
              batch_size=configuration['mlp']['batchSize'],
              verbose=2 if configuration['others']['verbose'] else 0,
              callbacks=[es])
    return Network(vocab, model)


def overSample(labels, data):
    elementNumber = 3 + configuration['mlpPhrase']['useB1'] + configuration['mlpPhrase']['useB-1']
    newData = []
    for i in range(len(data[0])):
        newData.append(np.concatenate((data[0][i], data[1][i], data[2][i], data[3][i])))
    if configuration['others']['verbose']:
        sys.stdout.write(reports.doubleSep + reports.tabs + 'Resampling:' + reports.doubleSep)
        sys.stdout.write(reports.tabs + 'data size before sampling = {0}\n'.format(len(labels)))
    ros = RandomOverSampler(random_state=0)
    newData, labels = ros.fit_sample(newData, labels)
    tokenData, posData, phraseTokens, phrasePoss = [], [], [], []
    for d in newData:
        tokenData.append(d[:elementNumber])
        posData.append(d[elementNumber:elementNumber * 2])
        phraseTokens.append(d[elementNumber * 2:(len(d) - (elementNumber * 2)) / 2 + elementNumber * 2])
        phrasePoss.append(d[((len(d) - elementNumber * 2) / 2) + elementNumber * 2:])
    if configuration['others']['verbose']:
        sys.stdout.write(reports.tabs + 'data size after sampling = {0}\n'.format(len(labels)))
    return np.asarray(labels), [np.asarray(tokenData), np.asarray(posData), np.asarray(phraseTokens),
                                np.asarray(phrasePoss)]


def getLearningData(corpus, vocab):
    labels, phraseTokenData, phrasePosData, transTokenData, transPosData = [], [], [], [], []
    global importantFrequentWordDic
    importantFrequentWordDic = corpus.importantFrequentWords
    for sent in corpus.trainingSents:
        trans = sent.initialTransition
        while trans and trans.next:
            tokenIdxs, posIdxs, phraseTokens, phrasePoss = getTransData(trans, vocab)
            transTokenData.append(tokenIdxs)
            transPosData.append(posIdxs)
            phraseTokenData.append(phraseTokens)
            phrasePosData.append(phrasePoss)
            labels.append(trans.next.type.value if trans.next.type.value <= 2 else 3)
            trans = trans.next
    return labels, [transTokenData, transPosData, phraseTokenData, phrasePosData]


def getTransData(trans, vocabulary):
    emptyTokenIdx = vocabulary.tokenIndices[empty]
    emptyPosIdx = vocabulary.posIndices[empty]
    tokenIdxs, posIdxs = [], []
    getSIndices(0, trans, vocabulary, tokenIdxs, posIdxs)
    getSIndices(1, trans, vocabulary, tokenIdxs, posIdxs)
    getBIndices(0, trans, vocabulary, tokenIdxs, posIdxs)
    if configuration['mlpPhrase']['useB1']:
        getBIndices(1, trans, vocabulary, tokenIdxs, posIdxs)

    if configuration['mlpPhrase']['useB-1']:
        if trans.configuration.reduced:
            tokenIdx, posIdx = getIdx(vocabulary, [trans.configuration.reduced])
            tokenIdxs.append(tokenIdx)
            posIdxs.append(posIdx)
        else:
            tokenIdxs.append(emptyTokenIdx)
            posIdxs.append(emptyPosIdx)
    phraseTokens, phrasePoss = getPhraseIndices(trans, vocabulary)
    return np.asarray(tokenIdxs), np.asarray(posIdxs), np.asarray(phraseTokens), np.asarray(phrasePoss)


def getPhraseIndices(trans, vocabulary):
    phraseTokens, phrasePoss = [], []
    for t in trans.sent.tokens:
        tokenIdx, posIdx = getIdx(vocabulary, [t])
        phraseTokens.append(tokenIdx)
        phrasePoss.append(posIdx)
    phraseTokens = phraseTokens[:configuration['mlpPhrase']['phraseMaxLength']]
    phrasePoss = phrasePoss[:configuration['mlpPhrase']['phraseMaxLength']]
    if len(phraseTokens) < configuration['mlpPhrase']['phraseMaxLength']:
        phraseTokens = np.asarray(pad_sequences([phraseTokens], maxlen=configuration['mlpPhrase']['phraseMaxLength'],
                                                value=vocabulary.tokenIndices[empty]))[0]
        phrasePoss = np.asarray(pad_sequences([phrasePoss], maxlen=configuration['mlpPhrase']['phraseMaxLength'],
                                              value=vocabulary.posIndices[empty]))[0]
    return phraseTokens, phrasePoss


def getSIndices(sPos, trans, vocabulary, tokenIdxs, posIdxs):
    if trans.configuration.stack and len(trans.configuration.stack) > sPos:
        s0Tokens = getTokens(trans.configuration.stack[len(trans.configuration.stack) - sPos - 1])
        tokenIdx, posIdx = getIdx(vocabulary, s0Tokens)
        tokenIdxs.append(tokenIdx)
        posIdxs.append(posIdx)
    else:
        tokenIdxs.append(vocabulary.tokenIndices[empty])
        posIdxs.append(vocabulary.posIndices[empty])


def getBIndices(bPos, trans, vocabulary, tokenIdxs, posIdxs):
    if trans.configuration.buffer and len(trans.configuration.buffer) > bPos:
        tokenIdx, posIdx = getIdx(vocabulary, [trans.configuration.buffer[bPos]])
        tokenIdxs.append(tokenIdx)
        posIdxs.append(posIdx)
    else:
        tokenIdxs.append(vocabulary.tokenIndices[empty])
        posIdxs.append(vocabulary.posIndices[empty])


def getIdx(vocab, tokens):
    tokensStr = '_'.join(t.getTokenOrLemma() for t in tokens)
    posStr = '_'.join(t.posTag.lower() for t in tokens)
    tokenIdx = vocab.tokenIndices[tokensStr] if tokensStr in vocab.tokenIndices else vocab.tokenIndices[unk]
    posIdx = vocab.posIndices[posStr] if posStr in vocab.posIndices else vocab.posIndices[unk]
    return tokenIdx, posIdx
