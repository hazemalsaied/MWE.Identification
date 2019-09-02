#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import datetime
import os
import sys
from random import randint
from random import shuffle

import torch
import torch.nn as nn
import torch.nn.functional as f
import torch.optim as optim

import config
import evaluation
import facebookEmb
# from config import configuration
from corpus import getTokens
from parser import parse
from reports import seperator, doubleSep, tabs

device = 'cpu'
dtype = torch.float

enableCategorization = False

configuration = config.configuration
unk = configuration['constants']['unk']
empty = configuration['constants']['empty']
number = configuration['constants']['number']


class TransitionClassifier(nn.Module):
    """
    version avec embeddings / lstm sur tous les mots de la phrase, et calcul de perte sur
    toutes les transitions de la phrase.
    """

    def __init__(self, corpus):
        """
        if use_pretrained_w_emb, the indices.w_embeddings_matrix will be used
        """
        super(TransitionClassifier, self).__init__()
        self.tokenVocab, self.posVocab = corpus.toVocabulary()
        self.p_embeddings = nn.Embedding(len(self.posVocab), configuration['kiperwasser']['posDim'])
        self.w_embeddings = nn.Embedding(len(self.tokenVocab), configuration['kiperwasser']['wordDim'])
        if configuration['kiperwasser']['pretrained']:
            self.tokenVocab, embeddingMatrix = facebookEmb.getEmbMatrix(corpus.langName, self.tokenVocab.keys())
            self.w_embeddings.load_state_dict({'weight': torch.FloatTensor(embeddingMatrix)})
        embeddingDim = configuration['kiperwasser']['wordDim'] + configuration['kiperwasser']['posDim']
        if configuration['kiperwasser']['gru']:
            self.rnn = nn.GRU(embeddingDim,
                              configuration['kiperwasser']['rnnUnitNum'],
                              bidirectional=True,
                              num_layers=configuration['kiperwasser']['rnnLayerNum'],
                              dropout=configuration['kiperwasser']['rnnDropout'] if configuration['kiperwasser'][
                                                                                        'rnnLayerNum'] > 1 else 0)
        else:
            self.rnn = nn.LSTM(embeddingDim,
                               configuration['kiperwasser']['rnnUnitNum'],
                               bidirectional=True,
                               num_layers=configuration['kiperwasser']['rnnLayerNum'],
                               dropout=configuration['kiperwasser']['rnnDropout'] if configuration['kiperwasser'][
                                                                                         'rnnLayerNum'] > 1 else 0)
        # init hidden and cell states h0 c0
        self.hiddenRnn = initHiddenRnn()
        # * 2 because bidirectional
        self.linear1 = nn.Linear(
            configuration['kiperwasser']['focusedElemNum'] * configuration['kiperwasser']['rnnUnitNum'] * 2,
            configuration['kiperwasser']['dense1'])
        # dropout here is very detrimental
        self.dropout1 = nn.Dropout(p=configuration['kiperwasser']['denseDropout'])
        self.linear2 = nn.Linear(configuration['kiperwasser']['dense1'], 8 if enableCategorization else 4)

    def forward(self, sentEmbs, activeElemIdxs):
        """ propagation avant, pour prediction d'une transition
        input =
        - embeddings as output from compute_contextualized_embeddings
        (contextualized with lstm layer)
        - the list of the lidxs of the nodes to focus on, according to current configuration
        """
        # select the contextualized embeddings for the focused_elements (given configuration)
        activeElems = selectRows(sentEmbs, activeElemIdxs).view((1, -1))
        out = f.relu(self.linear1(activeElems)) if configuration['kiperwasser'][
                                                       'denseActivation'] == 'relu' else f.tanh(
            self.linear1(activeElems))
        if configuration['kiperwasser']['denseDropout']:
            out = self.dropout1(out)
        out = self.linear2(out)
        scores = f.log_softmax(out, dim=1)
        return scores

    def predict(self, trans, sentEmbs):
        """
        prediction of score vector (for each transition)
        Returns sorted score list / corresponding class id list
        """
        activeElemIdxs = getFocusedElems(trans.configuration)
        # cet appel comprend l'appel de self.forward
        scores = self.forward(sentEmbs, activeElemIdxs)
        # on obtient par ex, si 3 transitions: tensor([[-1.3893, -1.6119, -0.5956]])
        # (cf. minibatch de 1)
        _, sortedIndices = torch.sort(scores[0], descending=True)
        return sortedIndices

    def getContextualizedEmbs(self, tokenIdxs, posIdxs):
        """
        input = sequence of word ids / sequence of pos ids of the sentence
        as output by get_sequence_feats_for_whole_sentence)

        (each are a LongTensor( list of ids )
        and contain as first element the not_existing_node, and the ROOT as second element,
        then all positions of the sentence

        output = tensor of shape (sequence length, self.embedding_dim)
        with lstm-contextualized vectors for each position, computed over non-contextualized embeddings
        """
        tokenEmbed = self.w_embeddings(tokenIdxs).to(device)
        posEmbed = self.p_embeddings(posIdxs).to(device)
        sentEmbed = torch.cat([tokenEmbed, posEmbed], 1).to(device)
        # self.hiddenRnn = initHiddenRnn()
        rnnOutput, self.hiddenRnn = self.rnn(sentEmbed.view(len(tokenIdxs), 1, -1), self.hiddenRnn)
        return rnnOutput.view(len(tokenIdxs), -1)

    def getIdxs(self, sent):
        tokenIdxs, POSIdxs = [], []
        for token in sent.tokens:
            isDigit = False
            for c in token.getTokenOrLemma():
                if c.isdigit():
                    isDigit = True
            if token.getTokenOrLemma() in self.tokenVocab:
                tokenIdxs.append(self.tokenVocab[token.getTokenOrLemma()])
            elif isDigit:
                tokenIdxs.append(self.tokenVocab[number])
            else:
                tokenIdxs.append(self.tokenVocab[unk])

            if token.posTag.lower() in self.posVocab:
                POSIdxs.append(self.posVocab[token.posTag.lower()])
            else:
                POSIdxs.append(self.posVocab[unk])
        return torch.LongTensor(tokenIdxs).to(device), torch.LongTensor(POSIdxs).to(device)

    def getIdxsAsList(self, sent):
        tokenIdxs, POSIdxs = [], []
        for token in sent.tokens:
            isDigit = False
            for c in token.getTokenOrLemma():
                if c.isdigit():
                    isDigit = True
            if token.getTokenOrLemma() in self.tokenVocab:
                tokenIdxs.append(self.tokenVocab[token.getTokenOrLemma()])
            elif isDigit:
                tokenIdxs.append(self.tokenVocab[number])
            else:
                tokenIdxs.append(self.tokenVocab[unk])

            if token.posTag.lower() in self.posVocab:
                POSIdxs.append(self.posVocab[token.posTag.lower()])
            else:
                POSIdxs.append(self.posVocab[unk])
        return tokenIdxs, POSIdxs


def getTrainData(corpus, model):
    pointer = int(len(corpus.trainingSents) * (1 - configuration['nn']['validationSplit']))
    trainSents = corpus.trainingSents[:pointer]
    sentRanks = range(len(trainSents))
    shuffle(sentRanks)
    labels, data = [], [[], [], []]

    for i in sentRanks:
        sent = trainSents[i]
        trans = sent.initialTransition
        transNum = 0
        while trans and trans.next:
            goldT = 3 if trans.next.type.value > 2 and not enableCategorization else trans.next.type.value
            labels.append(goldT)
            tokenIdxs, posIdxs = model.getIdxsAsList(sent)
            focusedIdxs = getFocusedElems(trans.configuration)
            data[0].append(tokenIdxs)
            data[1].append(posIdxs)
            data[2].append(focusedIdxs)
            if configuration['kiperwasser']['sampling'] and trans.isImportantTrans() \
                    and transNum < configuration['kiperwasser']['samplingTaux']:
                transNum += 1
            else:
                trans = trans.next

    return data, labels


def train2(corpus):
    """
    version avec bi-LSTM sur toute la phrase, et mise à jour des paramètres à chaque phrase
    (calcul de la perte pour une phrase complete)
    """
    global device
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    # nb of sentence positions taken to build input vector representing a parse configuration
    model = TransitionClassifier(corpus).to(device)
    optimizer = getOptimizer(model.parameters())
    lossFunction = nn.NLLLoss()
    data, labels = getTrainData(corpus, model)
    batchNum = int(len(data[0]) / configuration['kiperwasser']['batch']) - 1
    batchSize = configuration['kiperwasser']['batch']
    for epoch in range(configuration['nn']['epochs']):
        for i in range(batchNum):
            # Local batches and labels
            batchTokens = data[0][i * batchSize:(i + 1) * batchSize]
            batchPoss = data[1][i * batchSize:(i + 1) * batchSize]
            batchActiveTokens = data[2][i * batchSize:(i + 1) * batchSize]
            batchLabels = labels[i * batchSize:(i + 1) * batchSize]

            transLosses, retain_graph = [], True
            tokenEmbed = model.w_embeddings(torch.LongTensor(batchTokens)).to(device)
            posEmbed = model.p_embeddings(torch.LongTensor(batchPoss)).to(device)
            sentEmbeds = torch.cat([tokenEmbed, posEmbed], 2).to(device)
            model.hiddenRnn = initHiddenRnn()
            rnnOutput, model.hiddenRnn = model.rnn(sentEmbeds.view(len(batchTokens[0]),
                                                    configuration['kiperwasser']['batch'], -1),
                                                    model.hiddenRnn)
            # rnnOutput = rnnOutput.view(len(batchTokens), -1)
            activeElems = selectRowsFromTensors(rnnOutput, batchActiveTokens).view((1, -1))
            out = f.relu(model.linear1(activeElems)) \
                if configuration['kiperwasser']['denseActivation'] == 'relu' else \
                f.tanh(model.linear1(activeElems))
            if configuration['kiperwasser']['denseDropout']:
                out = model.dropout1(out)
            out = model.linear2(out)
            predT = f.log_softmax(out, dim=1)
            loss = lossFunction(predT, toTensor(batchLabels))
            loss.backward(retain_graph=retain_graph)
            optimizer.step()


def train(corpus, conf, trainedModel=None, trainValidation=False):
    """
    version avec bi-LSTM sur toute la phrase, et mise à jour des paramètres à chaque phrase
    (calcul de la perte pour une phrase complete)
    """
    global configuration
    configuration = conf
    global device
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    if configuration['kiperwasser']['verbose'] and trainValidation:
        sys.stdout.write(tabs + 'Training validation set!' + seperator)
    # nb of sentence positions taken to build input vector representing a parse configuration
    model = TransitionClassifier(corpus).to(device) if not trainValidation else trainedModel
    optimizer = getOptimizer(model.parameters())
    lossFunction = nn.NLLLoss()
    if not trainValidation:
        fileNum = randint(0, 500)
        filePath = os.path.join(configuration['path']['projectPath'], 'Reports',
                                str(fileNum) + '.' + configuration['kiperwasser']['file'])
        sys.stdout.write('\n' + tabs + 'Best model path: ' + '/'.join(filePath.split('/')[-2:]) + seperator)
    # losses of validation set for each epoch
    epochLosses, validLosses, validAccuracies = [], [], []
    if not trainValidation and configuration['kiperwasser']['verbose']:
        sys.stdout.write(tabs + str(model) + doubleSep)
        sys.stdout.write(tabs + str(optimizer) + doubleSep)
    # ------------ if validation asked -------------
    validSeuil = configuration['nn']['validationSplit']
    pointer = int(len(corpus.trainingSents) * (1 - validSeuil))
    validSents = corpus.trainingSents[pointer:]
    trainSents = corpus.trainingSents[:pointer] if not trainValidation else validSents
    for epoch in range(configuration['nn']['epochs']):
        start, epochLoss, usedSents = datetime.datetime.now(), 0, 0
        # shuffle sentences
        sentRanks = range(len(trainSents))
        shuffle(sentRanks)
        for i in sentRanks:
            sent = trainSents[i]
            model.zero_grad()
            sentLoss = getSentLoss(sent, model, lossFunction, optimizer)
            if sentLoss:
                usedSents += 1
                epochLoss += sentLoss.item()
                if not configuration['kiperwasser']['eager']:
                    sentLoss.backward()
                    optimizer.step()
        epochLosses.append(epochLoss)
        sys.stdout.write('Epoch %d:  Total loss = %f on %d\n' % (epoch, epochLoss, usedSents)
                         if configuration['kiperwasser']['verbose'] and not trainValidation else '')
        if not trainValidation:
            valLoss = getCorpusLoss(validSents, model, lossFunction, optimizer)
            validAcc = evaluate(validSents, model)
            sys.stdout.write('Validation loss: %f, Identification accuracy: %f\n' % (valLoss, validAcc)
                             if configuration['kiperwasser']['verbose'] and not trainValidation else '')
            # save model if validation loss has decreased
            # if validLosses and valLoss <= validLosses[-1]:
            if configuration['nn']['earlyStop'] and validAccuracies and validAcc > max(validAccuracies):
                torch.save(model, filePath)
            # early stopping
            elif configuration['nn']['earlyStop'] and \
                    epoch > configuration['nn']['patience'] and \
                    validAcc < max(validAccuracies) and os.path.isfile(filePath):
                model = torch.load(filePath)
                sys.stdout.write(tabs + 'identification accuracy has decreased (), '
                                        'stop and retrain using %d epochs\n' % (epoch - 1))
                if configuration['kiperwasser']['trainValidationSet']:
                    configuration['nn']['epochs'] = epoch - 1  # (cf. epoch est décalé de 1)
                    return train(corpus, configuration, model, trainValidation=True)
                return model
            validLosses.append(valLoss)
            validAccuracies.append(validAcc)
    if not trainValidation and configuration['kiperwasser']['trainValidationSet']:
        return train(corpus, configuration, model, trainValidation=True)

    return model


def evaluate(sents, model):
    parse(sents, model, None)
    return evaluation.evaluate(sents, loggingg=False)[1]


def initHiddenRnn():
    """
    Before we've done anything, we dont have any hidden state.
    The axes semantics are (num_layers, minibatch_size, hidden_dim)
    h_0 is of shape (num_layers * num_directions, batch, hidden_size):
                    tensor containing the initial hidden state for each element in the batch
    same for c_0 = initial cell state
    here num_directions = 2 (bidirectional), batch = 1
    :return:
    """
    if configuration['kiperwasser']['gru']:
        return torch.zeros(configuration['kiperwasser']['rnnLayerNum'] * 2,
                           configuration['kiperwasser']['batch'],
                           configuration['kiperwasser']['rnnUnitNum']).to(device)
    else:
        return (torch.zeros(configuration['kiperwasser']['rnnLayerNum'] * 2,
                            configuration['kiperwasser']['batch'],
                            configuration['kiperwasser']['rnnUnitNum']).to(device), \
                torch.zeros(configuration['kiperwasser']['rnnLayerNum'] * 2,
                            configuration['kiperwasser']['batch'],
                            configuration['kiperwasser']['rnnUnitNum']).to(device))


def selectRowsFromTensors(sentEmbeds, idxss):
    """
    extract given rows (= axis 0) from a given 2 dim tensor
    """
    results = torch.zeros((configuration['kiperwasser']['focusedElemNum'],
                            configuration['kiperwasser']['batch'],
                            2 * configuration['kiperwasser']['rnnUnitNum']), dtype=dtype)

    for batchIdx in range(configuration['kiperwasser']['batch']):
        for focusedElemIdx in range(configuration['kiperwasser']['focusedElemNum']):# idxss[batchIdx]:
            if idxss[batchIdx][focusedElemIdx] != -1:
                results[batchIdx] = sentEmbeds[idxss[batchIdx][focusedElemIdx] - 1][batchIdx]
    return results
    #
    # results = []
    # for idxs in idxss:
    #     batch = []
    #     for idx in idxs:
    #         if idx == -1:
    #             batch.append(torch.zeros((configuration['kiperwasser']['batch'], 2 * configuration['kiperwasser']['rnnUnitNum']), dtype=dtype).to(device))
    #         else:
    #             batch.append(sentEmbeds[idx - 1].to(device))
    #     results.append(batch)
    # return torch.cat(results, 2)

def selectRows(sentEmbeds, idxs):
    """
    extract given rows (= axis 0) from a given 2 dim tensor
    """
    results = []
    for idx in idxs:
        if idx == -1:
            results.append(torch.zeros((1, 2 * configuration['kiperwasser']['rnnUnitNum']), dtype=dtype).to(device))
        else:
            results.append(sentEmbeds[idx - 1].view(1, -1).to(device))
    return torch.cat(results)


def getCorpusLoss(sents, model, lossFunction, optimizer):
    """
    returns the loss for a list of gold dgs
    """
    loss = 0
    for sent in sents:
        sentLoss = getSentLoss(sent, model, lossFunction, optimizer)
        loss += sentLoss.item() if sentLoss else 0.
    return loss


def getFocusedElems(config):
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


def getSentLoss(sent, model, lossFunction, optimizer):
    """
    returns the whole loss for the sentence in gold_dg
    (return type is that of Torch.nn losses: differentiable Tensor of size 1)

    unless no gold transition sequence could be found
    (e.g. if gold_dg is a non proj tree and the transition set does not handle it)
    in which case returns None
    """
    # list of losses after each decision (transition) for the sentence
    transLosses, retain_graph = [], True
    tokenIdxs, posIdxs = model.getIdxs(sent)
    sentEmb = model.getContextualizedEmbs(tokenIdxs, posIdxs)
    trans = sent.initialTransition
    transNum = 0
    while trans and trans.next:
        if configuration['kiperwasser']['eager']:
            model.zero_grad()
            model.hiddenRnn = initHiddenRnn()
            sentEmb = model.getContextualizedEmbs(tokenIdxs, posIdxs)
        # Used to reduce the number of used transitions by replacing all Mark as transition by Mark as OTH
        goldT = 3 if trans.next.type.value > 2 and not enableCategorization else trans.next.type.value
        focusedIdxs = getFocusedElems(trans.configuration)
        predT = model.forward(sentEmb, focusedIdxs)
        loss = lossFunction(predT, toTensor(goldT))
        transLosses.append(loss)
        if configuration['kiperwasser']['eager']:
            loss.backward(retain_graph=retain_graph)
            optimizer.step()
            retain_graph = False
        if configuration['kiperwasser']['sampling'] and trans.isImportantTrans() \
                and transNum < configuration['kiperwasser']['samplingTaux']:
            transNum += 1
        else:
            trans = trans.next
    return sum(transLosses)


def getOptimizer(params):
    sys.stdout.write('# Network optimizer = Adagrad, learning rate = {0}\n'.format(configuration['kiperwasser']['lr']))
    return optim.Adagrad(params, lr=configuration['kiperwasser']['lr'])


def toTensor(label):
    """
    cree un Tensor de shape (1,); i.e. on crée le label gold pour un mini-batch de 1
    """
    return torch.LongTensor([label]).to(device)
