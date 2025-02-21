#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import random
import sys
from collections import Counter
from random import shuffle
from random import uniform

import torch
import torch.nn as nn
import torch.nn.functional as f
import torch.optim as optim

import config
# from config import configuration
from corpus import getTokens
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
        self.tokenVocab, self.posVocab = getVocab(corpus)
        kiperConf = configuration['kiperwasser']
        self.p_embeddings = nn.Embedding(len(self.posVocab), kiperConf['posDim'])
        self.w_embeddings = nn.Embedding(len(self.tokenVocab), kiperConf['wordDim'])
        embeddingDim = kiperConf['wordDim'] + kiperConf['posDim']
        self.lstm = nn.LSTM(embeddingDim,
                            kiperConf['rnnUnitNum'],
                            bidirectional=True,
                            num_layers=kiperConf['rnnLayerNum'],
                            dropout=kiperConf['rnnDropout'] if kiperConf['rnnLayerNum'] > 1 else 0)
        self.lstm_hidden_and_cell = init_lstm_hidden_and_cell()
        self.linear1 = nn.Linear(kiperConf['focusedElemNum'] * kiperConf['rnnUnitNum'] * 2, kiperConf['dense1'])
        self.linear2 = nn.Linear(kiperConf['dense1'], 8 if enableCategorization else 4)

    def forward(self, sentEmbs, activeElemIdxs):
        """ propagation avant, pour prediction d'une transition
        input =
        - embeddings as output from compute_contextualized_embeddings
        (contextualized with lstm layer)
        - the list of the lidxs of the nodes to focus on, according to current configuration
        """
        kiperConf = configuration['kiperwasser']
        activeElems = selectRows(sentEmbs, activeElemIdxs).view((1, -1))
        out = f.relu(self.linear1(activeElems)) if kiperConf['denseActivation'] == 'relu' else f.tanh(
            self.linear1(activeElems))
        if kiperConf['denseDropout']:
            out = self.dropout1(out)
        out = self.linear2(out)
        scores = f.log_softmax(out, dim=1)
        return scores

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
        self.lstm_hidden_and_cell = init_lstm_hidden_and_cell()
        lstmHiddenSeq, self.lstm_hidden_and_cell = \
            self.lstm(sentEmbed.view(len(tokenIdxs), 1, -1), self.lstm_hidden_and_cell)
        return lstmHiddenSeq.view(len(tokenIdxs), -1)

    def predict(self, trans, sentEmbs, tokens):
        """
        prediction of score vector (for each transition)
        Returns sorted score list / corresponding class id list
        """
        # tokensTxt = ' '.join(t.text for t in tokens)
        # print(str(trans))
        # print(tokensTxt)
        activeElemIdxs = getFocusedElems(trans.configuration, tokens)
        scores = self.forward(sentEmbs, activeElemIdxs)
        _, sortedIndices = torch.sort(scores[0], descending=True)
        return sortedIndices

    def getIdxs(self, tokens):
        tokenIdxs, POSIdxs = [], []
        for token in tokens:
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
def train(corpus, conf):
    """
    version avec bi-LSTM sur toute la phrase, et mise à jour des paramètres à chaque phrase
    (calcul de la perte pour une phrase complete)
    """
    global configuration
    configuration = conf
    global device
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    kiperConf = configuration['kiperwasser']
    model = TransitionClassifier(corpus).to(device)
    optimizer = optim.Adagrad(model.parameters(), lr=kiperConf['lr'])
    lossFunction = nn.NLLLoss()
    epochLosses, validLosses = [], []
    if kiperConf['verbose']:
        sys.stderr.write(str(model) + doubleSep)
        # sys.stderr.write(tabs + str(optimizer) + doubleSep)
        # sys.stderr.write(tabs + str(lossFunction) + doubleSep)
    # ------------ if validation asked -------------
    validSeuil = configuration['nn']['validationSplit']
    pointer = int(len(corpus.trainingSents) * (1 - validSeuil))
    trainSents = corpus.trainingSents[:pointer]
    validSents = corpus.trainingSents[pointer:]
    # ------------ training ------------------------
    for epoch in range(configuration['nn']['epochs']):
        if kiperConf['verbose']:
            sys.stderr.write(tabs + 'Epoch %d....\n' % epoch)
        epochLoss = 0
        sentRanks = range(len(trainSents))
        shuffle(sentRanks)
        usedSents = 0
        for i in sentRanks:
            sent = trainSents[i]
            if configuration['kiperwasser']['moreTrans'] and len(sent.tokens) > 6:
                tokens = []
                startTokenIdx = random.randint(0, len(sent.tokens) - 6)
                for tIdx in range(startTokenIdx, startTokenIdx + 6):
                    tokens.append(sent.tokens[tIdx])
                orphalineTokens = True
                positions = []
                for t in tokens:
                    if t.parentMWEs:
                        orphalineTokens = False
                        break
                    positions.append(t.position)
                if sent.vMWEs and orphalineTokens:
                    firstTokenPosition, lastTokenPosition = min(positions), max(positions)
                    for mwe in sent.vMWEs:
                        mweTokenPos = [t.position for t in mwe.tokens]
                        if firstTokenPosition > min(mweTokenPos) and lastTokenPosition < max(mweTokenPos):
                            orphalineTokens = False
                if orphalineTokens:
                    model.zero_grad()
                    sentLoss = getSentLoss(tokens, sent, model, lossFunction, orphalineTokens=True)
                    if sentLoss:
                        usedSents += 1
                        epochLoss += sentLoss.item()
                        sentLoss.backward()
                        optimizer.step()
            processedMWEs = []
            if sent.vMWEs:
                for mwe in sent.vMWEs:
                    if mwe.isEmbedded or mwe.isInterleaving or mwe.isNested or mwe in processedMWEs:
                        continue
                    for _ in range(1):
                        tokens, processedMWEs = getImportantTokens(mwe, sent, processedMWEs)
                        model.zero_grad()
                        sentLoss = getSentLoss(tokens, sent, model, lossFunction)
                        if sentLoss:
                            usedSents += 1
                            epochLoss += sentLoss.item()
                            sentLoss.backward()
                            optimizer.step()

        epochLosses.append(epochLoss)
        if kiperConf['verbose']:
            # sys.stderr.write('Number of used sentences in train = %d\n' % usedSents)
            sys.stderr.write('Total loss for epoch %d: %f on %d sentences\n' % (epoch, epochLoss, usedSents))
    return model


def getSentLoss(tokens, sent, model, lossFunction, orphalineTokens=False):
    """
    returns the whole loss for the sentence in gold_dg
    (return type is that of Torch.nn losses: differentiable Tensor of size 1)

    unless no gold transition sequence could be found
    (e.g. if gold_dg is a non proj tree and the transition set does not handle it)
    in which case returns None
    """
    firstTrans = getFirstTrans(tokens[0], sent)

    if orphalineTokens:
        lastMWEToken = tokens[-3]
    else:
        lastMWEToken = None
        for t in reversed(tokens):
            if t.parentMWEs:
                lastMWEToken = t
                break
    lastTrans = getLastTrans(firstTrans, lastMWEToken)  # tokens[-3])
    transLosses = []
    tokenIdxs, posIdxs = model.getIdxs(tokens)
    sentEmb = model.getContextualizedEmbs(tokenIdxs, posIdxs)
    # tokenStr = ' '.join(t.text for t in tokens)
    # print(tokenStr)
    trans = firstTrans
    while trans and trans != lastTrans:
        # print(trans)
        goldT = 3 if trans.next.type.value > 2 and not enableCategorization else trans.next.type.value
        focusedIdxs = getFocusedElems(trans.configuration, tokens)
        predT = model.forward(sentEmb, focusedIdxs)
        loss = lossFunction(predT, toTensor(goldT))
        transLosses.append(loss)
        trans = trans.next
    return sum(transLosses)


def getFirstTrans(token, sent):
    initT = sent.initialTransition
    trans = initT
    while trans.next:
        if trans.configuration.buffer and int(trans.configuration.buffer[0].position) == int(token.position):
            while trans.next.configuration.buffer and \
                    int(trans.next.configuration.buffer[0].position) == int(token.position):
                trans = trans.next
            return trans
        trans = trans.next
    return None


def getLastTrans(firstTrans, lastMWEToken):
    trans = firstTrans
    while trans:
        if trans.configuration.buffer and \
                trans.configuration.buffer[0].position <= lastMWEToken.position:
            trans = trans.next
            continue
        tokens = []
        if trans.configuration.stack:
            for s in trans.configuration.stack:
                tokens += getTokens(s)
        tokenIdxs = set()
        for t in tokens:
            tokenIdxs.add(int(t.position))
        if lastMWEToken.position not in tokenIdxs:
            return trans.previous
        trans = trans.next
    return None


def getImportantTokens(mwe, sent, processedMWEs):
    tokenPositions = [int(t.position) for t in mwe.tokens]
    if mwe.isAttached:
        attachedMwes = []
        for m in sent.vMWEs:
            if m is not mwe and (m.tokens[0].position == mwe.tokens[-1].position + 1 or
                                 m.tokens[0].position == mwe.tokens[-1].position + 2):
                attachedMwes.append(m)
                processedMWEs.append(m)
        for m in attachedMwes:
            tokenPositions += [t.position for t in m.tokens]

    startTokenPos, endTokenPos = min(tokenPositions), max(tokenPositions)
    if startTokenPos > 1 and not sent.tokens[startTokenPos - 2].parentMWEs:
        startTokenPos -= 1
    for i in range(2):
        if endTokenPos < len(sent.tokens) and not sent.tokens[endTokenPos].parentMWEs:
            endTokenPos += 1
    tokens = []
    for t in sent.tokens:
        if endTokenPos >= t.position >= startTokenPos:
            tokens.append(t)
    return tokens, processedMWEs


def getCorpusLoss(sents, model, lossFunction):
    """
    returns the loss for a list of gold dgs
    """
    loss = 0
    for sent in sents:
        sentLoss = getSentLoss(sent, model, lossFunction)
        loss += sentLoss.item() if sentLoss else 0.
    return loss


def getFocusedElems(config, tokens):
    idxs = []
    if config.stack and len(config.stack) > 1:
        for t in getTokens(config.stack[-2])[:2]:
            # if t in tokens:
            idxs.append(tokens.index(t))
    while len(idxs) < 2:
        idxs = idxs + [-1]

    if config.stack:
        for t in getTokens(config.stack[-1])[:4]:
            # if t in tokens:
            idxs.append(tokens.index(t))
    while len(idxs) < 6:
        idxs = idxs + [-1]

    if config.buffer:
        for t in config.buffer[:2]:
            idxs.append(tokens.index(t))

    while len(idxs) < 8:
        idxs = idxs + [-1]

    return idxs


def selectRows(sentEmbeds, idxs):
    """
    extract given rows (= axis 0) from a given 2 dim tensor
    """
    results = []
    for idx in idxs:
        if idx == -1:
            results.append(torch.zeros((1, 2 * configuration['kiperwasser']['rnnUnitNum']), dtype=dtype).to(device))
        else:
            results.append(sentEmbeds[idx].view(1, -1).to(device))
    return torch.cat(results)


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
            if tokenCounter[t] == 1 and uniform(0, 1) < configuration['constants']['alpha']:
                del tokenCounter[t]
    tokenCounter.update({unk: 1, number: 1})
    posCounter.update({unk: 1})
    printVocabReport(tokenCounter, posCounter)
    return {w: i for i, w in enumerate(tokenCounter.keys())}, {w: i for i, w in enumerate(posCounter.keys())}





def printVocabReport(tokenCounter, posCounter):
    res = seperator + tabs + 'Vocabulary' + doubleSep
    res += tabs + 'Tokens := {0} * POS : {1}'.format(len(tokenCounter), len(posCounter)) \
        if not configuration['xp']['compo'] else ''
    res += seperator
    return res


def toTensor(label):
    """
    cree un Tensor de shape (1,); i.e. on crée le label gold pour un mini-batch de 1
    """
    return torch.LongTensor([label]).to(device)


def init_lstm_hidden_and_cell():
    """
    Before we've done anything, we dont have any hidden state.
    The axes semantics are (num_layers, minibatch_size, hidden_dim)
    h_0 is of shape (num_layers * num_directions, batch, hidden_size):
                    tensor containing the initial hidden state for each element in the batch
    same for c_0 = initial cell state
    here num_directions = 2 (bidirectional), batch = 1
    :return:
    """
    return torch.zeros(configuration['kiperwasser']['rnnLayerNum'] * 2, configuration['kiperwasser']['batch'],
                       configuration['kiperwasser']['rnnUnitNum']).to(device), \
           torch.zeros(configuration['kiperwasser']['rnnLayerNum'] * 2, configuration['kiperwasser']['batch'],
                       configuration['kiperwasser']['rnnUnitNum']).to(device)
