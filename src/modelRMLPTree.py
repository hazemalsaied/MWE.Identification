import sys
from collections import Counter
from random import uniform

import keras
import numpy as np
from imblearn.over_sampling import RandomOverSampler
from keras.callbacks import EarlyStopping
from keras.layers import Input, Dense, Embedding, Flatten, GRU, Dropout, LSTM
from keras.models import Model
from keras.utils import to_categorical

import reports
import sampling
from config import configuration
from corpus import getTokens
from wordEmbLoader import unk, number, empty

# from keras.utils import plot_model

enableCategorization = False


class Network:

    def __init__(self, corpus):
        global tokenVocab, posVocab
        tokenVocab, posVocab = getVocab(corpus)
        buffElements = 1 + configuration['embedding']['useB1'] + configuration['embedding']['useB-1']
        inputLayers, concLayers = [], []
        bufTokens = Input((buffElements,), name='B_toks')
        buffPoss = Input((buffElements,), name='B_Pos')
        inputLayers.append(bufTokens)
        inputLayers.append(buffPoss)
        buffTokEmb = Embedding(len(tokenVocab), configuration['rmlpTree']['tokenEmb'], name='B_toksEmb')(bufTokens)
        buffPosEmb = Embedding(len(posVocab), configuration['rmlpTree']['posEmb'], name='B_PosEmb')(buffPoss)
        buffTokEmb = Flatten(name='B_toksFlat')(buffTokEmb)
        buffPosEmb = Flatten(name='B_PosFlat')(buffPosEmb)

        s0Tokens = Input((configuration['rmlpTree']['stackPadding'],), name='S0_toks')
        s0Poss = Input((configuration['rmlpTree']['stackPadding'],), name='S0_Pos')
        inputLayers.append(s0Tokens)
        inputLayers.append(s0Poss)
        s0TokEmb = Embedding(len(tokenVocab), configuration['rmlpTree']['tokenEmb'], name='S0_toksEmb')(s0Tokens)
        s0PosEmb = Embedding(len(posVocab), configuration['rmlpTree']['posEmb'], name='S0_tPosEmb')(s0Poss)
        s0Emb = keras.layers.concatenate([s0TokEmb, s0PosEmb])
        s1Tokens = Input((configuration['rmlpTree']['stackPadding'],), name='S1_toks')
        s1Poss = Input((configuration['rmlpTree']['stackPadding'],), name='S1_Pos')
        inputLayers.append(s1Tokens)
        inputLayers.append(s1Poss)
        s1TokEmb = Embedding(len(tokenVocab), configuration['rmlpTree']['tokenEmb'], name='S1_toksEmb')(s1Tokens)
        s1PosEmb = Embedding(len(posVocab), configuration['rmlpTree']['posEmb'], name='S1_PosEmb')(s1Poss)
        s1Emb = keras.layers.concatenate([s1TokEmb, s1PosEmb])
        if configuration['rmlpTree']['gru']:
            s0Rnn = GRU(configuration['rmlpTree']['wordRnnUnitNum'], return_sequences=configuration['rmlpTree']['rnnSequence'],
                        name='s0Rnn')(s0Emb)
            s1Rnn = GRU(configuration['rmlpTree']['wordRnnUnitNum'], return_sequences=configuration['rmlpTree']['rnnSequence'],
                        name='s1Rnn')(s1Emb)
        else:
            s0Rnn = LSTM(configuration['rmlpTree']['wordRnnUnitNum'], return_sequences=configuration['rmlpTree']['rnnSequence'],
                         name='s0Rnn')(s0Emb)
            s1Rnn = LSTM(configuration['rmlpTree']['wordRnnUnitNum'], return_sequences=configuration['rmlpTree']['rnnSequence'],
                         name='s1Rnn')(s1Emb)
        if configuration['rmlpTree']['rnnSequence']:
            s0Rnn = Flatten()(s0Rnn)
            s1Rnn = Flatten()(s1Rnn)
        s0Rnn = Dropout(configuration['rmlpTree']['rnnDropout'])(s0Rnn)
        s1Rnn = Dropout(configuration['rmlpTree']['rnnDropout'])(s1Rnn)
        lastLayer = keras.layers.concatenate([buffTokEmb, buffPosEmb, s0Rnn, s1Rnn])
        lastLayer = Dense(configuration['rmlpTree']['denseUnitNumber'], activation='relu')(lastLayer)
        lastLayer = Dropout(configuration['rmlpTree']['denseDropout'])(lastLayer)
        softmax = Dense(8 if enableCategorization else 4, activation='softmax')(lastLayer)
        self.model = Model(inputs=inputLayers, outputs=softmax)
        sys.stdout.write(str(self.model.summary()))


    def predict(self, trans):
        newIdxs = [np.asarray([idx]) for idx in getIdxs(trans.configuration)]
        oneHotRep = self.model.predict(newIdxs, batch_size=1)
        return oneHotRep[0]


def train(cls, corpus):
    data, lbls = getLearningData(corpus)
    newData = []
    for d in data:
        newD = []
        for i in range(6):
            newD = np.concatenate((newD, d[i]))
        newData.append(newD)
    newData, lbls = overSample(newData, lbls)
    if configuration['rmlpTree']['shuffle']:
        lblAndData = sampling.shuffle([lbls, newData])
        lbls, newData = np.asarray(lblAndData[0]), lblAndData[1]
    data = []
    stackElems = configuration['rmlpTree']['stackPadding']
    buffElems = 1 + configuration['embedding']['useB1'] + configuration['embedding']['useB-1']
    for i in range(6):
        data.append([])
    for d in newData:
        data[0].append(np.asarray(d[0:buffElems]))
        data[1].append(np.asarray(d[buffElems: buffElems * 2]))
        data[2].append(np.asarray(d[buffElems * 2: (buffElems * 2) + stackElems]))
        data[3].append(np.asarray(d[(buffElems * 2) + stackElems:(buffElems * 2) + (2 * stackElems)]))
        data[4].append(np.asarray(d[(buffElems * 2) + (2 * stackElems):(buffElems * 2) + (3 * stackElems)]))
        data[5].append(np.asarray(d[(buffElems * 2) + (3 * stackElems):]))
    for i in range(6):
        data[i] = np.asarray(data[i])

    lbls = to_categorical(lbls, num_classes=8 if enableCategorization else 4)
    optimizer = keras.optimizers.Adagrad(lr=configuration['rmlpTree']['lr'], epsilon=None, decay=0.0)
    cls.model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    es = EarlyStopping(monitor='val_loss',
                       min_delta=configuration['nn']['minDelta'],
                       patience=configuration['nn']['patience'],
                       verbose=configuration['others']['verbose'])
    callbacks = [es] if configuration['nn']['earlyStop'] else []
    history = cls.model.fit(data, lbls,
                            validation_split=configuration['nn']['validationSplit'],
                            epochs=configuration['nn']['epochs'],
                            batch_size=configuration['nn']['batchSize'],
                            callbacks=callbacks,
                            verbose=2 if configuration['others']['verbose'] else 0)
    # trainValidationData(cls.model, data, lbls, history)
    return history


def getLearningData(corpus):
    lbls, data = [], []
    for s in corpus.trainingSents:
        t = s.initialTransition
        while t and t.next:
            data.append(getIdxs(t.configuration))
            lbls.append(3 if t.next.type.value > 2 and not enableCategorization else t.next.type.value)
            t = t.next
    return data, lbls


def overSample(data, lbls):
    if configuration['others']['verbose']:
        sys.stdout.write(reports.doubleSep + reports.tabs + 'Resampling:' + reports.doubleSep)
        sys.stdout.write(reports.tabs + 'data size before sampling = {0}\n'.format(len(lbls)))
    ros = RandomOverSampler(random_state=0)
    data, lbls = ros.fit_sample(data, lbls)
    if configuration['others']['verbose']:
        sys.stdout.write(reports.tabs + 'data size after sampling = {0}\n'.format(len(lbls)))
    return data, lbls


def focusedSample(labels, tokenData, posData, corpus):
    if not configuration['sampling']['focused']:
        return labels, tokenData, posData
    newLabels, newTokens, newPOS, traitedMWEs = [], [], [], set()
    oversamplingTaux = configuration['sampling']['mweRepeition']
    mWEDicAsIdxs = getMWEDicAsIdxs(corpus)
    for i in range(len(labels)):
        if labels[i] > 2:
            mweIdx = ''
            for st in tokenData[i][2:6]:
                if st != tokenVocab[empty]:
                    mweIdx += '.{0}.'.format(st)
            if mweIdx in mWEDicAsIdxs and mweIdx not in traitedMWEs:
                traitedMWEs.add(mweIdx)
                mwe = mWEDicAsIdxs[mweIdx]
                mweLength = len(mwe.split(' '))
                if mwe == 'estar com febre':
                    pass
                if mwe in corpus.mweDictionary:
                    mweOccurrence = corpus.mweDictionary[mwe]
                else:
                    pass
                    mweOccurrence = 0
                if mweOccurrence < oversamplingTaux:
                    for underProcessingTransIdx in range(i - (2 * mweLength - 1) + 1, i + 1):
                        for j in range(oversamplingTaux - mweOccurrence):
                            newTokens.append(tokenData[underProcessingTransIdx])
                            newPOS.append(posData[underProcessingTransIdx])
                            newLabels.append(labels[underProcessingTransIdx])
    sys.stdout.write(reports.tabs + 'data size before focused sampling = {0}\n'.format(len(labels)))
    labels = np.concatenate((labels, newLabels))
    sys.stdout.write(reports.tabs + 'data size after focused sampling = {0}\n'.format(len(labels)))
    tokenData = np.concatenate((tokenData, newTokens))
    posData = np.concatenate((posData, newPOS))
    return labels, tokenData, posData


def trainValidationData(model, data, labels, history):
    labels, data = getValidationData(labels, data)
    history = model.fit(data, np.asarray(labels),
                        epochs=len(history.epoch),
                        batch_size=configuration['rmlpTree']['batchSize'],
                        verbose=0)
    return history


def getValidationData(labels, data):
    valLabels, valData = [], []
    for i in range(6):
        valData.append([])
    for i in range(int(len(labels) * (1 - configuration['nn']['validationSplit'])), len(labels)):
        for j in range(6):
            valData[j].append(data[j][i])
            # print valData
        valLabels.append(labels[i])
    for i in range(6):
        valData[i] = np.asarray(valData[i])
    return valLabels, valData


def getMWEDicAsIdxs(corpus):
    result = dict()
    for s in corpus.trainingSents:
        for v in s.vMWEs:
            if v.isRecognizable:
                vIdxs = ''
                for t in v.tokens:
                    if t.getTokenOrLemma() in tokenVocab.keys():
                        vIdxs += '.{0}.'.format(tokenVocab[t.getTokenOrLemma()])
                    elif t.isNumber():
                        vIdxs += '.{0}.'.format(tokenVocab[number])
                    else:
                        vIdxs += '.{0}.'.format(tokenVocab[unk])
                value = ' '.join(t.lemma.lower() for t in v.tokens)
                result[vIdxs] = value
                if value == 'estar com febre':
                    pass
    return result


def getVocab(corpus):
    tokenCounter, posCounter = Counter(), Counter()
    for s in corpus.trainingSents:
        for t in s.tokens:
            tokenCounter.update({t.getTokenOrLemma(): 1})
            posCounter.update({t.posTag.lower(): 1})
    if configuration['embedding']['compactVocab']:
        for t in tokenCounter.keys():
            if t not in corpus.mweTokenDictionary:
                del tokenCounter[t]
    else:
        for t in tokenCounter.keys():
            if tokenCounter[t] == 1 and uniform(0, 1) < 0.5:
                del tokenCounter[t]
    tokenCounter.update({unk: 1, number: 1, empty: 1})
    posCounter.update({unk: 1, empty: 1})

    return {w: i for i, w in enumerate(tokenCounter.keys())}, \
           {w: i for i, w in enumerate(posCounter.keys())}


def addTokenIdxs(t, buffIdxs, buffPosIdxs):
    if t.isNumber():
        buffIdxs.append(tokenVocab[number])
    else:
        buffIdxs.append(tokenVocab[t.getTokenOrLemma()] if t.getTokenOrLemma() in tokenVocab else tokenVocab[unk])
    buffPosIdxs.append(posVocab[t.posTag.lower()] if t.posTag.lower() in posVocab else posVocab[unk])


def addEmptyIdxs(idxs, posIdxs, lenght):
    while len(idxs) < lenght:
        idxs += [tokenVocab[empty]]
        posIdxs += [posVocab[empty]]


def getIdxs(config):
    global tokenVocab, posVocab
    buffIdxs, buffPosIdxs, s0Idxs, s0PosIdxs, s1Idxs, s1PosIdxs = [], [], [], [], [], []
    buffElements = 1 + configuration['embedding']['useB1'] + configuration['embedding']['useB-1']
    stackElements = configuration['rmlpTree']['stackPadding']
    if config.buffer:
        addTokenIdxs(config.buffer[0], buffIdxs, buffPosIdxs)
        if configuration['embedding']['useB1']:
            addTokenIdxs(config.buffer[0], buffIdxs, buffPosIdxs)
    addEmptyIdxs(buffIdxs, buffPosIdxs, buffElements - 1)
    if configuration['embedding']['useB-1'] and config.reduced:
        addTokenIdxs(config.reduced, buffIdxs, buffPosIdxs)
    addEmptyIdxs(buffIdxs, buffPosIdxs, buffElements)

    if config.stack:
        for t in getTokens(config.stack[-1])[:stackElements]:
            addTokenIdxs(t, s0Idxs, s0PosIdxs)
        addEmptyIdxs(s0Idxs, s0PosIdxs, stackElements)
        if len(config.stack) > 1:
            for t in getTokens(config.stack[-2])[:stackElements]:
                addTokenIdxs(t, s1Idxs, s1PosIdxs)
        addEmptyIdxs(s1Idxs, s1PosIdxs, stackElements)
    else:
        addEmptyIdxs(s0Idxs, s0PosIdxs, stackElements)
        addEmptyIdxs(s1Idxs, s1PosIdxs, stackElements)
    return np.asarray(buffIdxs), np.asarray(buffPosIdxs), np.asarray(s0Idxs), np.asarray(s0PosIdxs), \
           np.asarray(s1Idxs), np.asarray(s1PosIdxs)
