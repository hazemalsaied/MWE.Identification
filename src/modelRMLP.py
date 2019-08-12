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

enableCategorization = False

rnnConf = configuration['rnn']
params = configuration['nn']


class Network:
    def __init__(self, corpus):
        global rnnConf
        rnnConf = configuration['rnn']
        global tokenVocab, posVocab, focusedElements
        focusedElements = rnnConf['s0TokenNum'] + rnnConf['s1TokenNum'] + rnnConf['bTokenNum'] + \
                          rnnConf['useB-1']
        tokenVocab, posVocab = getVocab(corpus)
        self.model = Network.build()

    @staticmethod
    def build():

        inputToken = Input((focusedElements,))
        inputPos = Input((focusedElements,))
        inputLayers = [inputToken, inputPos]
        tokenEmb = Embedding(len(tokenVocab), rnnConf['wordDim'])(inputToken)
        posEmb = Embedding(len(posVocab), rnnConf['posDim'])(inputPos)
        if configuration['rnn']['gru']:
            tokenRnn = GRU(rnnConf['wordRnnUnitNum'], return_sequences=rnnConf['rnnSequence'])(tokenEmb)
            posRnn = GRU(rnnConf['posRnnUnitNum'], return_sequences=rnnConf['rnnSequence'])(posEmb)
        else:
            tokenRnn = LSTM(rnnConf['wordRnnUnitNum'], return_sequences=rnnConf['rnnSequence'])(tokenEmb)
            posRnn = LSTM(rnnConf['posRnnUnitNum'], return_sequences=rnnConf['rnnSequence'])(posEmb)

        if rnnConf['rnnSequence']:
            tokenRnn = Flatten()(tokenRnn)
            posRnn = Flatten()(posRnn)

        tokenRnnDrop = Dropout(rnnConf['rnnDropout'])(tokenRnn)
        posRnnDrop = Dropout(rnnConf['rnnDropout'])(posRnn)
        concLayers = [tokenRnnDrop, posRnnDrop]

        lastLayer = keras.layers.concatenate(concLayers)
        if rnnConf['useDense']:
            lastLayer = Dense(rnnConf['denseUnitNum'], activation='relu')(lastLayer)
            lastLayer = Dropout(rnnConf['denseDropout'])(lastLayer)
        softmax = Dense(8 if enableCategorization else 4, activation='softmax')(lastLayer)
        model = Model(inputs=inputLayers, outputs=softmax)
        sys.stdout.write(str(model.summary()))
        return model

    def predict(self, trans):
        tokenIdxs, posIdxs = DataFactory.getIdxs(trans.configuration)
        oneHotRep = self.model.predict([np.asarray([tokenIdxs]), np.asarray([posIdxs])], batch_size=1)
        return oneHotRep[0]

    def train(self, corpus):
        lbls, tokenIdxs, posIdxs = DataFactory.getLearningData(corpus)
        lbls, tokenIdxs, posIdxs = DataFactory.overSample(lbls, tokenIdxs, posIdxs)
        lbls, tokenIdxs, posIdxs = DataFactory.focusedSample(lbls, tokenIdxs, posIdxs, corpus)
        classWeightDic = sampling.getClassWeights(lbls)
        sampleWeights = sampling.getSampleWeightArray(lbls, classWeightDic)
        lbls = to_categorical(lbls, num_classes=8 if enableCategorization else 4)
        if rnnConf['shuffle']:
            lists = sampling.shuffle([lbls, tokenIdxs, posIdxs, sampleWeights]) if configuration['sampling'][
                'sampleWeight'] else \
                sampling.shuffle([lbls, tokenIdxs, posIdxs])
            lbls, tokenIdxs, posIdxs, sampleWeights = np.asarray(lists[0]), np.asarray(lists[1]), np.asarray(
                lists[2]), np.asarray(lists[3]) if len(lists) >= 4 else None
        optimizer = keras.optimizers.Adagrad(lr=rnnConf['lr'], epsilon=None, decay=0.0) \
            if params['optimizer'] == 'adagrad' else keras.optimizers.Adam(lr=rnnConf['lr'])
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

        callbacks = [EarlyStopping(monitor=params['monitor'],
                                   min_delta=params['minDelta'],
                                   patience=params['patience'],
                                   verbose=configuration['others']['verbose'])] if params['earlyStop'] else []
        history = self.model.fit([np.asarray(tokenIdxs), np.asarray(posIdxs)], lbls,
                                 validation_split=params['validationSplit'],
                                 epochs=params['epochs'],
                                 batch_size=params['batchSize'],
                                 callbacks=callbacks,
                                 verbose=2,
                                 sample_weight=sampleWeights)
        return history






def trainValidationData(model, tokenData, posData, labels, classWeightDic, history):
    labels, valTokenData, valPosData = getValidationData(labels, tokenData, posData)
    validationLabelsAsInt = [np.where(r == 1)[0][0] for r in labels]
    sampleWeights = sampling.getSampleWeightArray(validationLabelsAsInt, classWeightDic)
    history = model.fit([np.asarray(valTokenData), np.asarray(valPosData)], np.asarray(labels),
                        epochs=len(history.epoch),
                        batch_size=rnnConf['batchSize'],
                        verbose=0,
                        sample_weight=sampleWeights)
    return history


def getValidationData(labels, tokenData, posData):
    valLabels, valTokenData, valPosData = [], [], []
    for i in range(int(len(labels) * (1 - params['validationSplit'])), len(labels)):
        valTokenData.append(tokenData[i])
        valPosData.append(posData[i])
        valLabels.append(labels[i])
    return valLabels, valTokenData, valPosData
    # return valLabels, [np.asarray(valTokenData), np.asarray(valPosData)]


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
            if t not in corpus.mweTokenDictionary and tokenCounter[t] == 1 and uniform(0, 1) < 0.5:
                del tokenCounter[t]
    tokenCounter.update({unk: 1, number: 1, empty: 1})
    posCounter.update({unk: 1, empty: 1})

    return {w: i for i, w in enumerate(tokenCounter.keys())}, \
           {w: i for i, w in enumerate(posCounter.keys())}


class DataFactory:
    @staticmethod
    def getLearningData(corpus):
        lbls, tokenIdxs, posIdxs = [], [], []
        for s in corpus.trainingSents:
            t = s.initialTransition
            while t and t.next:
                idxs = DataFactory.getIdxs(t.configuration)
                tokenIdxs.append(idxs[0])
                posIdxs.append(idxs[1])
                lbls.append(3 if t.next.type.value > 2 and not enableCategorization else t.next.type.value)
                t = t.next
        return lbls, tokenIdxs, posIdxs

    @staticmethod
    def overSample(lbls, tokenIdxs, posIdxs, ):
        data = []  # focusedElements =rnnConf['s0TokenNum'] + rnnConf['s1TokenNum'] + rnnConf['bTokenNum']
        if configuration['others']['verbose']:
            sys.stdout.write(reports.doubleSep + reports.tabs + 'Resampling:' + reports.doubleSep)
            sys.stdout.write(reports.tabs + 'data size before sampling = {0}\n'.format(len(lbls)))
        for i in range(len(tokenIdxs)):
            data.append(np.asarray(np.concatenate((tokenIdxs[i], posIdxs[i]))))
        ros = RandomOverSampler(random_state=0)
        data, lbls = ros.fit_sample(data, lbls)
        tokenIdxs, posIdxs = [], []
        for i in range(len(data)):
            tokenIdxs.append(data[i][:focusedElements])
            posIdxs.append(data[i][focusedElements:])
        if configuration['others']['verbose']:
            sys.stdout.write(reports.tabs + 'data size after sampling = {0}\n'.format(len(lbls)))
        return lbls, tokenIdxs, posIdxs

    @staticmethod
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

    @staticmethod
    def getIdxs(config):
        idxs, posIdxs = [], []
        global tokenVocab, posVocab
        DataFactory.getBufferIdxs(config, idxs, posIdxs)
        DataFactory.addEmptyIdx(rnnConf['bTokenNum'], idxs, posIdxs)
        DataFactory.getS0Idxs(config, idxs, posIdxs)
        DataFactory.addEmptyIdx(rnnConf['bTokenNum'] + rnnConf['s0TokenNum'], idxs, posIdxs)
        DataFactory.getS1Idxs(config, idxs, posIdxs)
        DataFactory.addEmptyIdx(rnnConf['bTokenNum'] + rnnConf['s0TokenNum'] + rnnConf['s1TokenNum'], idxs, posIdxs)
        if rnnConf['useB-1']:
            DataFactory.getBxIdxs(config, idxs, posIdxs)
            DataFactory.addEmptyIdx(rnnConf['bTokenNum'] + rnnConf['s0TokenNum'] + rnnConf['s1TokenNum'] + 1, idxs, posIdxs)
        return np.asarray(idxs), np.asarray(posIdxs)

    @staticmethod
    def getS1Idxs(config, idxs, posIdxs):
        if config.stack and len(config.stack) > 1:
            for t in getTokens(config.stack[-2])[:rnnConf['s1TokenNum']]:
                if t.isNumber():
                    idxs.append(tokenVocab[number])
                else:
                    idxs.append(
                        tokenVocab[t.getTokenOrLemma()] if t.getTokenOrLemma() in tokenVocab else tokenVocab[unk])
                posIdxs.append(posVocab[t.posTag.lower()] if t.posTag.lower() in posVocab else posVocab[unk])

    @staticmethod
    def getS0Idxs(config, idxs, posIdxs):
        if config.stack:
            for t in getTokens(config.stack[-1])[:rnnConf['s0TokenNum']]:
                if t.isNumber():
                    idxs.append(tokenVocab[number])
                else:
                    idxs.append(
                        tokenVocab[t.getTokenOrLemma()] if t.getTokenOrLemma() in tokenVocab else tokenVocab[unk])
                posIdxs.append(posVocab[t.posTag.lower()] if t.posTag.lower() in posVocab else posVocab[unk])
        # addEmptyIdx(rnnConf['s0TokenNum'], idxs, posIdxs)

    @staticmethod
    def getBufferIdxs(config, idxs, posIdxs):
        if config.buffer:
            for t in config.buffer[:rnnConf['bTokenNum']]:
                if t.isNumber():
                    idxs.append(tokenVocab[number])
                else:
                    idxs.append(
                        tokenVocab[t.getTokenOrLemma()] if t.getTokenOrLemma() in tokenVocab else tokenVocab[unk])
                posIdxs.append(posVocab[t.posTag.lower()] if t.posTag.lower() in posVocab else posVocab[unk])
        # addEmptyIdx(rnnConf['bTokenNum'], idxs, posIdxs)

    @staticmethod
    def getBxIdxs(config, idxs, posIdxs):
        if rnnConf['useB-1']:
            t = config.reduced
            if t is not None:
                if t.isNumber():
                    idxs.append(tokenVocab[number])
                else:
                    idxs.append(
                        tokenVocab[t.getTokenOrLemma()] if t.getTokenOrLemma() in tokenVocab else tokenVocab[unk])
                posIdxs.append(posVocab[t.posTag.lower()] if t.posTag.lower() in posVocab else posVocab[unk])

    @staticmethod
    def addEmptyIdx(number, idxs, posIdxs):
        while len(idxs) < number:
            idxs.append(tokenVocab[empty])
            posIdxs.append(posVocab[empty])
