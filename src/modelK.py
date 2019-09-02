#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import reports
import sys
from random import shuffle
from imblearn.over_sampling import RandomOverSampler
import torch
import torch.nn as nn
import torch.nn.functional as f
import torch.optim as optim

import evaluation
import facebookEmb
from config import configuration as c
# from config import configuration
from corpus import getTokens
from parser import parse

device = 'cpu'
dtype = torch.float

enableCategorization = False

unk = c['constants']['unk']
empty = c['constants']['empty']
number = c['constants']['number']
maxPhraseLen = 100


class Network(nn.Module):
    """
    version avec embeddings / lstm sur tous les mots de la phrase, et calcul de perte sur
    toutes les transitions de la phrase.
    """

    def __init__(self, corpus):
        """
        if use_pretrained_w_emb, the indices.w_embeddings_matrix will be used
        """
        super(Network, self).__init__()
        self.tokenVocab, self.posVocab = corpus.toVocabulary()
        self.p_embeddings = nn.Embedding(len(self.posVocab), c['kiperwasser']['posDim'])
        self.w_embeddings = nn.Embedding(len(self.tokenVocab), c['kiperwasser']['wordDim'])
        if c['kiperwasser']['pretrained']:
            self.tokenVocab, embeddingMatrix = facebookEmb.getEmbMatrix(corpus.langName, self.tokenVocab.keys())
            self.w_embeddings.load_state_dict({'weight': torch.FloatTensor(embeddingMatrix)})
        embeddingDim = c['kiperwasser']['wordDim'] + c['kiperwasser']['posDim']
        if c['kiperwasser']['gru']:
            self.rnn = nn.GRU(embeddingDim,
                              c['kiperwasser']['rnnUnitNum'],
                              bidirectional=True,
                              num_layers=c['kiperwasser']['rnnLayerNum'],
                              dropout=c['kiperwasser']['rnnDropout'] if c['kiperwasser'][
                                                                            'rnnLayerNum'] > 1 else 0)
        else:
            self.rnn = nn.LSTM(embeddingDim,
                               c['kiperwasser']['rnnUnitNum'],
                               bidirectional=True,
                               num_layers=c['kiperwasser']['rnnLayerNum'],
                               dropout=c['kiperwasser']['rnnDropout'] if c['kiperwasser'][
                                                                             'rnnLayerNum'] > 1 else 0)
        # init hidden and cell states h0 c0
        self.hiddenRnn = initHiddenRnn()
        # * 2 because bidirectional
        # if c['kiperwasser']['useBatches']:
        #     self.linear1 = nn.Linear(
        #         c['kiperwasser']['focusedElemNum'] * c['kiperwasser']['rnnUnitNum'] * 2,
        #         # c['kiperwasser']['batch']),
        #         c['kiperwasser']['dense1'])
        # else:
        self.linear1 = nn.Linear(
            c['kiperwasser']['focusedElemNum'] * c['kiperwasser']['rnnUnitNum'] * 2,
            c['kiperwasser']['dense1'])
        # dropout here is very detrimental
        self.dropout1 = nn.Dropout(p=c['kiperwasser']['denseDropout'])
        self.linear2 = nn.Linear(c['kiperwasser']['dense1'], 4)

    def forward(self, batchTokens, batchPoss, batchActiveTokens, parsing=False):
        batchSize = 1 if parsing else c['kiperwasser']['batch']
        batchTokens = torch.LongTensor(batchTokens).to(device)
        batchPoss = torch.LongTensor(batchPoss).to(device)
        batchActiveTokens = torch.LongTensor(batchActiveTokens).to(device)
        tokenEmbed = self.w_embeddings(batchTokens).to(device)
        posEmbed = self.p_embeddings(batchPoss).to(device)
        sentEmbeds = torch.cat([tokenEmbed, posEmbed], 2).to(device)
        self.hiddenRnn = initHiddenRnn(parsing=parsing)
        rnnOutput, self.hiddenRnn = self.rnn(sentEmbeds.view(len(batchTokens[0]), batchSize, -1), self.hiddenRnn)
        rnnOutput = rnnOutput.to(device)
        activeElems = selectRowsFromTensors(rnnOutput, batchActiveTokens, parsing=parsing).view(1, batchSize, -1).to(device)
        out = f.tanh(self.linear1(activeElems)).to(device)
            # f.relu(self.linear1(activeElems)).to(device) if c['kiperwasser']['denseActivation'] == 'relu' else \
            # f.tanh(self.linear1(activeElems)).to(device)
        if c['kiperwasser']['denseDropout']:
            out = self.dropout1(out).to(device)
        out = self.linear2(out).to(device)
        return out

    def predict(self, trans, sent):
        """
        prediction of score vector (for each transition)
        Returns sorted score list / corresponding class id list
        """
        tokens, poss, idxs = DataFactory.getTransData(trans, sent, self.tokenVocab, self.posVocab)
        # cet appel comprend l'appel de self.forward
        scores = self.forward([tokens], [poss], [idxs], parsing=True)
        # on obtient par ex, si 3 transitions: tensor([[-1.3893, -1.6119, -0.5956]])
        # (cf. minibatch de 1)
        _, sortedIndices = torch.sort(scores[0], descending=True)
        return sortedIndices


def run(corpus):
    """
    version avec bi-LSTM sur toute la phrase, et mise à jour des paramètres à chaque phrase
    (calcul de la perte pour une phrase complete)
    """
    global device
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    model = Network(corpus).to(device)
    # nb of sentence positions taken to build input vector representing a parse configuration
    optimizer = optim.Adagrad(model.parameters(), lr=c['kiperwasser']['lr'])
    sys.stdout.write('Learning rate = {0}\n'.format(c['kiperwasser']['lr']))
    lossFunction = nn.NLLLoss()
    data, labels = DataFactory.getData(corpus, model.tokenVocab, model.posVocab)
    data, labels = DataFactory.overSample(data, labels)
    valData, valLabels = DataFactory.getData(corpus, model.tokenVocab, model.posVocab, validation=True)
    batchNum = int(len(data[0]) / c['kiperwasser']['batch']) - 1
    valBatchNum = int(len(valData[0]) / c['kiperwasser']['batch']) - 1
    batchSize, epochLosses, batchId = c['kiperwasser']['batch'], [], 0
    for epoch in range(c['nn']['epochs']):
        for i in range(batchNum):
            batchId += 1
            sys.stdout.write('{0}.'.format(batchId))
            # Local batches and labels
            batchTokens = data[0][i * batchSize:(i + 1) * batchSize]
            batchPoss = data[1][i * batchSize:(i + 1) * batchSize]
            batchActiveTokens = data[2][i * batchSize:(i + 1) * batchSize]
            batchLabels = labels[i * batchSize:(i + 1) * batchSize]
            batchLabels = torch.LongTensor([batchLabels]).to(device).view(c['kiperwasser']['batch'])
            out = model(batchTokens, batchPoss, batchActiveTokens)
            predT = f.log_softmax(out, dim=1)
            loss = lossFunction(predT.view(c['kiperwasser']['batch'], 4), batchLabels)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        valLosses = 0
        for i in range(valBatchNum):
            # Local batches and labels
            batchTokens = valData[0][i * batchSize:(i + 1) * batchSize]
            batchPoss = valData[1][i * batchSize:(i + 1) * batchSize]
            batchActiveTokens = valData[2][i * batchSize:(i + 1) * batchSize]
            batchLabels = valLabels[i * batchSize:(i + 1) * batchSize]
            batchLabels = torch.LongTensor([batchLabels]).to(device).view(c['kiperwasser']['batch'])
            out = model(batchTokens, batchPoss, batchActiveTokens)
            predT = f.log_softmax(out, dim=1)
            loss = lossFunction(predT.view(c['kiperwasser']['batch'], 4), batchLabels)
            valLosses += loss.item()
        epochLosses.append(valLosses/batchSize)
        sys.stdout.write('\nEpoch {0}: Val loss:{1}\n'.format(epoch, round(valLosses / batchSize, 6)))
        if shouldStopLearning(epochLosses):
            break

    return model


def shouldStopLearning(epochLosses,
                       patience=c['nn']['patience'] + 1,
                       minDelta=c['nn']['minDelta']):
        if len(epochLosses) <= patience:
            return False
        for i in range(patience):
            if epochLosses[len(epochLosses) - i - 1] - epochLosses[len(epochLosses) - i - 2] <= minDelta:
                continue
            else:
                return False
        sys.stdout.write('Early stopping applied\n')
        return True


def evaluate(sents, model):
    parse(sents, model, None)
    return evaluation.evaluate(sents, loggingg=False)[1]


def initHiddenRnn(parsing=False):
    """
    Before we've done anything, we dont have any hidden state.
    The axes semantics are (num_layers, minibatch_size, hidden_dim)
    h_0 is of shape (num_layers * num_directions, batch, hidden_size):
                    tensor containing the initial hidden state for each element in the batch
    same for c_0 = initial cell state
    here num_directions = 2 (bidirectional), batch = 1
    :return:
    """
    batchSize = 1 if parsing else c['kiperwasser']['batch']
    if c['kiperwasser']['gru']:
        return torch.zeros(c['kiperwasser']['rnnLayerNum'] * 2,
                           batchSize,
                           c['kiperwasser']['rnnUnitNum']).to(device)
    else:
        return (torch.zeros(c['kiperwasser']['rnnLayerNum'] * 2,
                            batchSize,
                            c['kiperwasser']['rnnUnitNum']).to(device),\
                torch.zeros(c['kiperwasser']['rnnLayerNum'] * 2,
                            batchSize,
                            c['kiperwasser']['rnnUnitNum']).to(device))


def selectRowsFromTensors(sentEmbeds, idxss, parsing=False):
    """
    extract given rows (= axis 0) from a given 2 dim tensor
    """
    batchSize = 1 if parsing else c['kiperwasser']['batch']
    results = torch.zeros((c['kiperwasser']['focusedElemNum'],
                           batchSize,
                           2 * c['kiperwasser']['rnnUnitNum']), dtype=dtype)

    for batchIdx in range(batchSize):
        idx = 0
        for selectedIdx in idxss[batchIdx]:
            if selectedIdx != -1 and selectedIdx < 100:
                results[idx][batchIdx] = sentEmbeds[selectedIdx - 1][batchIdx]
            idx += 1
    return results


class DataFactory:
    @staticmethod
    def padSeq(seq, vocab, pos=False):
        seq = seq[:maxPhraseLen]
        for _ in range(maxPhraseLen - len(seq)):
            if pos:
                seq.append(vocab[empty])
            else:
                seq.append(vocab[empty])
        return seq

    @staticmethod
    def getData(corpus, tokenVocab, posVocab, validation=False):
        pointer = int(len(corpus.trainingSents) * (1 - c['nn']['validationSplit']))
        trainSents = corpus.trainingSents[pointer:] if validation else corpus.trainingSents[:pointer]
        sentRanks = range(len(trainSents))
        shuffle(sentRanks)
        labels, data = [], [[], [], []]
        for i in sentRanks:
            sent = trainSents[i]
            trans = sent.initialTransition
            transNum = 0
            while trans and trans.next:
                labels.append(3 if trans.next.type.value > 2 else trans.next.type.value)
                dEntry = DataFactory.getTransData(trans, sent, tokenVocab, posVocab)
                for i in range(3):
                    data[i].append(dEntry[i])
                if c['kiperwasser']['sampling'] and trans.isImportantTrans() \
                        and transNum < c['kiperwasser']['samplingTaux']:
                    transNum += 1
                else:
                    trans = trans.next
        return data, labels

    @staticmethod
    def getTransData(trans, sent, tokenVocab, posVocab):
        tokenIdxs, POSIdxs = DataFactory.getSentData(sent, tokenVocab, posVocab)
        selectedIdxs = DataFactory.getSelectedIdxs(trans.configuration)
        return tokenIdxs, POSIdxs, selectedIdxs

    @staticmethod
    def getSentData(sent, tokenVocab, posVocab):
        tokenIdxs, POSIdxs = [], []
        for token in sent.tokens:
            isDigit = False
            for c in token.getTokenOrLemma():
                if c.isdigit():
                    isDigit = True
            if token.getTokenOrLemma() in tokenVocab:
                tokenIdxs.append(tokenVocab[token.getTokenOrLemma()])
            elif isDigit:
                tokenIdxs.append(tokenVocab[number])
            else:
                tokenIdxs.append(tokenVocab[unk])

            if token.posTag.lower() in posVocab:
                POSIdxs.append(posVocab[token.posTag.lower()])
            else:
                POSIdxs.append(posVocab[unk])
        return DataFactory.padSeq(tokenIdxs, tokenVocab), DataFactory.padSeq(POSIdxs, posVocab, pos=True)

    @staticmethod
    def getSelectedIdxs(config):
        idxs = []
        if config.stack and len(config.stack) > 1:
            for t in getTokens(config.stack[-2])[:2]:
                idxs.append(t.position)
        while len(idxs) < 2:
            idxs = idxs + [-1]

        if config.stack:
            for t in getTokens(config.stack[-1])[:4]:
                idxs.append(t.position)
        while len(idxs) < 6:
            idxs = idxs + [-1]

        if config.buffer:
            for t in config.buffer[:2]:
                idxs.append(t.position)

        while len(idxs) < 8:
            idxs = idxs + [-1]

        return idxs
    @staticmethod
    def overSample(data, labels):
        newData = []
        for i in range(len(data[0])):
            newData.append(data[0][i] + data[1][i] + data[2][i])
        tokenData, posData, selectedIdxs = [], [], []
        if c['others']['verbose']:
            sys.stdout.write(reports.doubleSep + reports.tabs + 'Resampling:' + reports.doubleSep)
            sys.stdout.write(reports.tabs + 'data size before sampling = {0}\n'.format(len(labels)))
        ros = RandomOverSampler(random_state=0)
        data, labels = ros.fit_sample(newData, labels)
        tokens, poss, idxs = [], [], []
        for item in data:
            tokens.append(item[:maxPhraseLen])
            poss.append(item[maxPhraseLen: maxPhraseLen *2 ])
            idxs.append(item[maxPhraseLen *2:])
        if c['others']['verbose']:
            sys.stdout.write(reports.tabs + 'data size after sampling = {0}\n'.format(len(labels)))
        return [tokenData, posData, idxs], labels

