from random import uniform

import keras
import numpy as np
from imblearn.over_sampling import RandomOverSampler
from keras import optimizers
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import Input, Dense, Flatten, Embedding
from keras.models import Model
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from nltk.parse.transitionparser import TransitionParser, Transition, Configuration

import reports
from corpus import Token
from corpus import getRelevantModelAndNormalizer
from corpus import getTokens, getLemmaString
from modelLinear import getFeatures
from reports import *
from transitions import TransitionType
from wordEmbLoader import empty
from wordEmbLoader import unk, number

# unk = configuration['constants']['unk']
# empty = configuration['constants']['empty']


enableCategorization = False

importantFrequentWordDic = dict()

# global idenInputArrNum

global idenInputArrNum, taggingInputArray, depParserInuptArrNum


class Network:
    def __init__(self, corpus):
        global idenInputArrNum, taggingInputArray, depParserInuptArrNum
        self.depLabelDic = dict()
        taggingInputArray = 2 + int(configuration['multitasking']['useCapitalization']) \
                            + int(configuration['multitasking']['useSymbols'])
        idenInputArrNum = taggingInputArray * 3 + (taggingInputArray * configuration['multitasking']['useB1']) + (
                taggingInputArray * configuration['multitasking']['useBx'])
        depParserInuptArrNum = taggingInputArray * 18 + 1
        self.vocabulary = Vocabulary(corpus)

        if configuration['tmp']['trainDepParser']:
            self.parser = TransParser('arc-standard')
            self.depParserData, self.depParserLabels, self.depLabelDic = \
                self.parser.getTrainData(corpus, self)

        self.taggingModel, self.idenModel, self.depParsingModel = createTheModel(self.vocabulary, len(self.depLabelDic))

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
                history = self.taggingModel.fit(taggingData, taggingLbls, validation_split=.2,
                                                epochs=1,
                                                batch_size=taggingBatchSize, verbose=2)
                taggingLoss.append(history.history['loss'])
            else:
                history = self.idenModel.fit(idenData, idenLbls, validation_split=.2, epochs=1,
                                             batch_size=taggingBatchSize, verbose=2)
                idenLoss.append(history.history['loss'])
                # TODO check the early stopping

    def trainDepParser(self):
        es = EarlyStopping(monitor='val_loss',
                           min_delta=configuration['nn']['minDelta'],
                           patience=configuration['nn']['patience'],
                           verbose=configuration['others']['verbose'])

        # if configuration['sampling']['overSampling']:
        #     depParserData, depParserLabels = overSample(depParserData, depParserLabels)
        depParserLabels = to_categorical(self.depParserLabels, num_classes=len(self.depLabelDic))
        self.depParsingModel.fit(self.depParserData, depParserLabels,
                                 validation_split=.2,
                                 epochs=100,
                                 batch_size=configuration['multitasking']['depParserBatchSize'],
                                 verbose=2,
                                 callbacks=[es])

    def testDepParser(self, corpus):
        depParserData, depParserLabels, depLabelDic = self.parser.getTrainData(corpus, self)
        depParserLabels = to_categorical(depParserLabels, num_classes=len(self.depLabelDic))
        results = self.depParsingModel.evaluate(depParserData, depParserLabels, batch_size=32, verbose=0)
        sys.stdout.write('Dep Parsing accuracy = {0}\nLoss = {1}, \n'.format(
            round(results[1] * 100, 1), round(results[0], 3)))

    def trainIden(self, corpus):
        idenData, idenLbls = self.getIdenData(corpus)
        if configuration['sampling']['overSampling']:
            idenData, idenLbls = overSample(idenData, idenLbls)
        idenLbls = to_categorical(idenLbls, num_classes=4)
        self.idenModel.fit(idenData, idenLbls, validation_split=.2,
                           epochs=100,
                           batch_size=configuration['multitasking']['identBatchSize'],
                           verbose=2,
                           callbacks=[
                               EarlyStopping(monitor='val_loss',
                                             min_delta=configuration['nn']['minDelta'],
                                             patience=configuration['nn']['patience'],
                                             verbose=configuration['others']['verbose'])
                           ])

    def trainTagging(self, corpus):
        taggingData, taggingLbls = self.getTaggingData(corpus)
        taggingLbls = to_categorical(taggingLbls, num_classes=len(self.vocabulary.posIndices))
        es = EarlyStopping(monitor='val_loss',
                           min_delta=configuration['nn']['minDelta'],
                           patience=configuration['nn']['patience'],
                           verbose=configuration['others']['verbose'])
        self.taggingModel.fit(taggingData, taggingLbls,
                              validation_split=.2,
                              epochs=100,
                              batch_size=configuration['multitasking']['taggingBatchSize'],
                              verbose=2,
                              callbacks=[es])

    def trainTaggerAndIdentifier(self, corpus):
        taggingData, taggingLbls = self.getTaggingData(corpus)
        taggingLbls = to_categorical(taggingLbls, num_classes=len(self.vocabulary.posIndices))
        idenData, idenLbls = self.getIdenData(corpus)
        if configuration['sampling']['overSampling']:
            idenData, idenLbls = overSample(idenData, idenLbls)
        sys.stdout.write('Identication data = {0}\n'.format(len(idenLbls)))
        sys.stdout.write('POS Tagging data = {0}\n'.format(len(taggingLbls)))
        idenLbls = to_categorical(idenLbls, num_classes=4)
        historyList = []
        for x in range(configuration['multitasking']['initialEpochs']):
            sys.stdout.write('POS tagging: {0}\n'.format(x + 1))
            self.taggingModel.fit(taggingData, taggingLbls,
                                  batch_size=configuration['multitasking']['taggingBatchSize'],
                                  verbose=2)
        for x in range(configuration['multitasking']['jointLearningEpochs']):
            if x % 2 == 0:
                sys.stdout.write(
                    'POS tagging: {0}\n'.format(int(x / 2) + 1 + configuration['multitasking']['initialEpochs']))
                self.taggingModel.fit(taggingData, taggingLbls,
                                      verbose=2,
                                      batch_size=configuration['multitasking']['taggingBatchSize'])
            else:
                sys.stdout.write('MWE identification: {0}\n'.format(int(x / 2) + 1))
                his = self.idenModel.fit(idenData, idenLbls,
                                         verbose=2,
                                         batch_size=configuration['multitasking']['identBatchSize'])
                historyList.append(his)
                if shouldStopLearning(historyList):
                    break

    def predictIdent(self, trans, sent):
        inputs = self.getPredData(trans, sent)
        oneHotRep = self.idenModel.predict(inputs, batch_size=1,
                                           verbose=configuration['nn']['predictVerbose'])
        return oneHotRep[0]

    def testIden(self, corpus):
        IdenData, IdenLbls = self.getIdenData(corpus, train=False)
        IdenLbls = to_categorical(IdenLbls, num_classes=4)
        results = self.idenModel.evaluate(IdenData, IdenLbls, batch_size=32, verbose=0)
        sys.stdout.write('Loss = {0}, Accuracy = {1}'.format(round(results[0], 3), round(results[1] * 100, 1)))

    def testTagging(self, corpus, title='POS tagging accuracy'):
        taggingData, taggingLbls = self.getTaggingData(corpus, train=False)
        taggingLbls = to_categorical(taggingLbls, num_classes=len(self.vocabulary.posIndices))
        results = self.taggingModel.evaluate(taggingData, taggingLbls, batch_size=32, verbose=0)
        sys.stdout.write('{0} = {1}\nLoss = {2}, \n'.format(title,
                                                            round(results[1] * 100, 1), round(results[0], 3)))

    def getTaggingData(self, corpus, train=True):
        data, lbls = [[] for _ in range(taggingInputArray)], []
        for s in corpus.allTrainingSents if train else corpus.testingSents:
            for item in s.tokens + s.vMWEs:
                if not train and not configuration['multitasking']['testOnToken'] and \
                        str(item.__class__).endswith('corpus.Token'):
                    continue
                tokens = [item] if str(item.__class__).endswith('corpus.Token') else item.tokens
                outputs = self.getTaggingEntry(tokens, s)
                for i in range(len(outputs) - 1):
                    data[i].append(outputs[i])
                lbls.append(outputs[-1])
        return [np.asarray(d) for d in data], lbls

    def getPredData(self, trans, sent):
        data = []
        for i in range(idenInputArrNum):
            data.append([])
        focusedElems = getIdenTransData(trans)
        for i in range(len(focusedElems)):
            taggingEntry = self.getTaggingEntry(focusedElems[i], sent)
            for j in range(len(taggingEntry) - 1):  # i*4, i*4 + 4):
                data[i * taggingInputArray + j].append(np.asarray(taggingEntry[j]))
        return [np.asarray(data[i]) for i in range(idenInputArrNum)]

    def getIdenData(self, corpus, train=True):
        data, labels = [[] for _ in range(idenInputArrNum)], []
        for sent in corpus.trainingSents if train else corpus.testingSents:
            trans = sent.initialTransition
            while trans and trans.next:
                focusedElems = getIdenTransData(trans)
                for i in range(len(focusedElems)):
                    taggingEntry = self.getTaggingEntry(focusedElems[i], sent)
                    for j in range(len(taggingEntry) - 1):
                        data[i * taggingInputArray + j].append(np.asarray(taggingEntry[j]))
                labels.append(trans.next.type.value if trans.next.type.value <= 2 else 3)
                trans = trans.next
        return [np.asarray(data[i]) for i in range(idenInputArrNum)], labels

    def getAffixeIndices(self, tokens, s):
        affixes = []
        txts = getContextTexts(tokens, s)
        for txt in txts:
            txt = txt.lower()
            if len(txt) > 2:
                if txt[:2] in self.vocabulary.affixeIndices:
                    affixes.append(self.vocabulary.affixeIndices[txt[:2]])
                    if len(txt) > 2 and txt[:3] in self.vocabulary.affixeIndices:
                        affixes.append(self.vocabulary.affixeIndices[txt[:3]])
                    else:
                        affixes.append(self.vocabulary.affixeIndices[unk])
                else:
                    affixes.append(self.vocabulary.affixeIndices[unk])
                    affixes.append(self.vocabulary.affixeIndices[unk])
                if txt[-2:] in self.vocabulary.affixeIndices:
                    affixes.append(self.vocabulary.affixeIndices[txt[-2:]])
                    if len(txt) > 2 and txt[-3:] in self.vocabulary.affixeIndices:
                        affixes.append(self.vocabulary.affixeIndices[txt[-3:]])
                    else:
                        affixes.append(self.vocabulary.affixeIndices[unk])
                else:
                    affixes.append(self.vocabulary.affixeIndices[unk])
                    affixes.append(self.vocabulary.affixeIndices[unk])
            else:
                affixes += [self.vocabulary.affixeIndices[unk]] * 4
        return affixes

    def getTaggingEntry(self, tokens, s):
        outputs = []
        if tokens == [None]:
            outputs = [[self.vocabulary.tokenIndices[unk]] * (configuration['multitasking']['windowSize'] * 2 + 1), \
                       [self.vocabulary.affixeIndices[unk]] * 12]
            if configuration['multitasking']['useCapitalization']:
                outputs.append([2] * 3)
            if configuration['multitasking']['useSymbols']:
                outputs.append([0])
            outputs.append(self.vocabulary.posIndices[unk])
            return outputs
        if tokens == ['empty']:
            outputs = [[self.vocabulary.tokenIndices[empty]] * (configuration['multitasking']['windowSize'] * 2 + 1), \
                       [self.vocabulary.affixeIndices[empty]] * 12]
            if configuration['multitasking']['useCapitalization']:
                outputs.append([2] * 3)
            if configuration['multitasking']['useSymbols']:
                outputs.append([0])
            outputs.append(self.vocabulary.posIndices[empty])
            return outputs
        if tokens == ['root']:
            outputs = [[self.vocabulary.tokenIndices['root']] * (configuration['multitasking']['windowSize'] * 2 + 1), \
                       [self.vocabulary.affixeIndices[unk]] * 12]
            if configuration['multitasking']['useCapitalization']:
                outputs.append([2] * 3)
            if configuration['multitasking']['useSymbols']:
                outputs.append([0])
            outputs.append(self.vocabulary.posIndices['root'])
            return outputs
        tokenIdxs = self.getTokenIdxs(tokens, s)
        outputs.append(tokenIdxs)
        affixes = self.getAffixeIndices(tokens, s)
        outputs.append(affixes)
        if configuration['multitasking']['useCapitalization']:
            capitalIdx = getCapitalizationInfo(tokens, s)
            outputs.append(capitalIdx)
        if configuration['multitasking']['useSymbols']:
            symbols = getSymbolInfo(tokens)
            outputs.append(symbols)
        attachedPos = '_'.join(t.posTag.lower() for t in tokens)
        posIdx = self.vocabulary.posIndices[attachedPos.lower() if attachedPos in self.vocabulary.posIndices else unk]
        outputs.append(posIdx)
        return outputs

    def getTokenIdxs(self, tokens, s):
        windowSize = configuration['multitasking']['windowSize']
        positions = [int(t.position) - 1 for t in tokens]
        minPos, maxPos, tokenIdxs = min(positions), max(positions), []
        res = getLemmaString(tokens) + ' ' + str(minPos) + ' ' + str(maxPos) + ' '
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
        xStr = getLemmaString(tokens).replace(' ', '_')
        if xStr in self.vocabulary.tokenIndices:
            tokenIdxs.append(self.vocabulary.tokenIndices[xStr])
            res += ' ' + xStr
        else:
            tokenIdxs.append(self.vocabulary.tokenIndices[unk])
            res += ' unk'
        return tokenIdxs

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
            if configuration['multitasking']['useB1']:
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
            if configuration['multitasking']['useB1']:
                tokenIdxs.append(emptyTokenIdx)
                posIdxs.append(emptyPosIdx)
        if configuration['multitasking']['useBx']:
            if trans.configuration.reduced:
                tokenIdx, posIdx = self.vocabulary.getIndices([trans.configuration.reduced], dynamicVocab=dynamicVocab,
                                                              parse=parse)
                tokenIdxs.append(tokenIdx)
                posIdxs.append(posIdx)
            else:
                tokenIdxs.append(emptyTokenIdx)
                posIdxs.append(emptyPosIdx)

        return np.asarray(tokenIdxs), np.asarray(posIdxs)


class Vocabulary:
    def __init__(self, corpus):
        self.affixeDic = self.getAffixeDic(corpus)
        self.affixeIndices = indexateDic(self.affixeDic)
        self.tokenFreqs, self.posFreqs, self.sytacticLabels = getFrequencyDics(corpus)
        self.tokenIndices = indexateDic(self.tokenFreqs)
        self.posIndices = indexateDic(self.posFreqs)
        self.syntacticLabelIndices = indexateDic(self.sytacticLabels)
        if configuration['others']['verbose'] == 1:
            sys.stdout.write(str(self))
            self.verify(corpus)

    def __str__(self):
        res = seperator + tabs + 'Vocabulary' + doubleSep
        res += tabs + 'Tokens := {0} * POS : {1}'.format(len(self.tokenIndices), len(self.posIndices)) \
            if not configuration['xp']['compo'] else ''
        res += seperator
        return res

    def getAffixeDic(self, corpus):
        affixeDic = dict()
        for s in corpus.trainingSents:
            for t in s.tokens:
                if len(t.text) >= 2:
                    affixeDic[t.text[-2:].lower()] = 0
                    affixeDic[t.text[:2].lower()] = 0
                    if len(t.text) > 2:
                        affixeDic[t.text[-3:].lower()] = 0
                        affixeDic[t.text[:3].lower()] = 0
        affixeDic[unk] = 0
        affixeDic[empty] = 0
        return affixeDic

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


class TransParser(TransitionParser):
    """
    Class for transition based parser. Implement 2 algorithms which are "arc-standard" and "arc-eager"
    """

    def getTrainDataOld(self, depgraphs, sents, vocab, network):
        """
        Create the training example in the libsvm format and write it to the input_file.
        Reference : Page 32, Chapter 3. Dependency Parsing by Sandra Kubler, Ryan McDonal and Joakim Nivre (2009)
        """
        operation = Transition(self.ARC_STANDARD)
        count_proj = 0
        data, labels, labelDic = [[] for _ in range(depParserInuptArrNum)], [], dict()
        for i in range(len(sents)):
            depgraph = depgraphs[i]
            sent = sents[i]
            if not self._is_projective(depgraph):
                continue
            count_proj += 1
            conf = Configuration(depgraph)
            while len(conf.buffer) > 0:
                b0 = conf.buffer[0]
                dataEntry = getDataEntry(conf, vocab, sent, network)
                for i in range(depParserInuptArrNum):
                    data[i].append(dataEntry[i])
                if len(conf.stack) > 0:
                    s0 = conf.stack[len(conf.stack) - 1]
                    # Left-arc operation
                    rel = self._get_dep_relation(b0, s0, depgraph)
                    if rel is not None:
                        key = Transition.LEFT_ARC + ':' + rel
                        if key not in labelDic:
                            labelDic[key] = len(labelDic)
                        operation.left_arc(conf, rel)
                        labels.append(labelDic[key])
                        continue
                    # Right-arc operation
                    rel = self._get_dep_relation(s0, b0, depgraph)
                    if rel is not None:
                        precondition = True
                        # Get the max-index of buffer
                        maxID = conf._max_address
                        for w in range(maxID + 1):
                            if w != b0:
                                relw = self._get_dep_relation(b0, w, depgraph)
                                if relw is not None:
                                    if (b0, relw, w) not in conf.arcs:
                                        precondition = False
                        if precondition:
                            key = Transition.RIGHT_ARC + ':' + rel
                            operation.right_arc(conf, rel)
                            if key not in labelDic:
                                labelDic[key] = len(labelDic)
                            labels.append(labelDic[key])
                            continue
                # Shift operation as the default
                key = Transition.SHIFT
                if key not in labelDic:
                    labelDic[key] = len(labelDic)
                operation.shift(conf)
                labels.append(labelDic[key])
        print(" Number of training examples : " + str(len(depgraphs)))
        print(" Number of valid (projective) examples : " + str(count_proj))
        return [np.asarray(data[i]) for i in range(depParserInuptArrNum)], labels, labelDic

    def getTrainData(self, corpus, network):
        """
        Create the training example in the libsvm format and write it to the input_file.
        Reference : Page 32, Chapter 3. Dependency Parsing by Sandra Kubler, Ryan McDonal and Joakim Nivre (2009)
        """
        operation = Transition(self.ARC_STANDARD)
        count_proj = 0
        data, labels, labelDic = [[] for _ in range(depParserInuptArrNum)], [], dict()
        for i in range(len(corpus.trainingSents)):
            depgraph = corpus.trainDepGraphs[i]
            sent = corpus.trainingSents[i]
            if not self._is_projective(depgraph):
                continue
            count_proj += 1
            conf = Configuration(depgraph)
            while len(conf.buffer) > 0:
                b0 = conf.buffer[0]
                dataEntry = getDataEntry(conf, sent, network)
                if len(dataEntry) != 73:
                    print conf
                for i in range(depParserInuptArrNum):
                    data[i].append(dataEntry[i])
                if len(conf.stack) > 0:
                    s0 = conf.stack[len(conf.stack) - 1]
                    # Left-arc operation
                    rel = self._get_dep_relation(b0, s0, depgraph)
                    if rel is not None:
                        if conf.stack[-1] - 1 >= 0 and conf.buffer[0] - 1 >= 0:
                            sent.tokens[conf.stack[-1] - 1].dependencyParent = sent.tokens[conf.buffer[0] - 1]
                        sent.tokens[conf.stack[-1] - 1].dependencyLabel = rel
                        key = Transition.LEFT_ARC + ':' + rel
                        if key not in labelDic:
                            labelDic[key] = len(labelDic)
                        operation.left_arc(conf, rel)
                        labels.append(labelDic[key])

                        continue
                    # Right-arc operation
                    rel = self._get_dep_relation(s0, b0, depgraph)
                    if rel is not None:
                        precondition = True
                        # Get the max-index of buffer
                        maxID = conf._max_address
                        for w in range(maxID + 1):
                            if w != b0:
                                relw = self._get_dep_relation(b0, w, depgraph)
                                if relw is not None:
                                    if (b0, relw, w) not in conf.arcs:
                                        precondition = False
                        if precondition:
                            key = Transition.RIGHT_ARC + ':' + rel
                            if conf.stack[-1] - 1 >= 0 and conf.buffer[0] - 1 >= 0:
                                sent.tokens[conf.buffer[0] - 1].dependencyParent = sent.tokens[conf.stack[-1] - 1]
                            else:
                                sent.tokens[conf.buffer[0] - 1].dependencyParent = None
                            sent.tokens[conf.buffer[0] - 1].dependencyLabel = rel
                            operation.right_arc(conf, rel)
                            if key not in labelDic:
                                labelDic[key] = len(labelDic)
                            labels.append(labelDic[key])
                            continue
                # Shift operation as the default
                key = Transition.SHIFT
                if key not in labelDic:
                    labelDic[key] = len(labelDic)
                operation.shift(conf)
                labels.append(labelDic[key])
        print(" Number of training examples : " + str(len(corpus.trainDepGraphs)))
        print(" Number of valid (projective) examples : " + str(count_proj))
        return [np.asarray(data[i]) for i in range(depParserInuptArrNum)], labels, labelDic


def createTheModel(vocab, depParserClassNum):
    taggingModel, sharedLayers = createTaggingModel(vocab)
    if configuration['tmp']['trainIden'] or configuration['tmp']['trainJointly']:
        idenModel = createIdenModel(sharedLayers)
    else:
        idenModel = None
    if configuration['tmp']['trainDepParser']:
        depParsingModel = createDepParsingModel(sharedLayers, depParserClassNum, vocab)
    else:
        depParsingModel = None
    return taggingModel, idenModel, depParsingModel


def createTaggingModel(vocab):
    inputToks = Input((configuration['multitasking']['windowSize'] * 2 + 1,), dtype='int32', name='tokens')
    inputAffixe = Input((12,), dtype='int32', name='affixes')
    inputLayers = [inputToks, inputAffixe]
    sharedTokEmb = Embedding(len(vocab.tokenIndices), configuration['multitasking']['tokenDim'], name='tokenEmb')
    sharedAffixeEmb = Embedding(len(vocab.affixeIndices), configuration['multitasking']['affixeDim'],
                                name='affixeseEmb')

    taggingFlatten = Flatten()(sharedTokEmb(inputToks))
    taggingAffixeFlatten = Flatten()(sharedAffixeEmb(inputAffixe))
    concFlatten = [taggingFlatten, taggingAffixeFlatten]
    sharedLayers = [sharedTokEmb, sharedAffixeEmb]
    addCapitalizationLayer(inputLayers, concFlatten, sharedLayers)
    addSymbolLayer(inputLayers, concFlatten, sharedLayers)
    concFlatten = keras.layers.concatenate(concFlatten)
    sharedDense = Dense(configuration['multitasking']['taggingDenseUnits'], activation='relu', name='posDense')
    sharedLayers = [sharedDense] + sharedLayers
    taggingDense = sharedDense(concFlatten)

    taggingSoftmax = Dense(len(vocab.posIndices), activation='softmax')(taggingDense)
    taggingModel = Model(inputs=inputLayers, outputs=taggingSoftmax)
    taggingModel.compile(loss=configuration['nn']['loss'],
                         optimizer=getOptimizer(),
                         metrics=['accuracy'])
    if configuration['others']['verbose']:
        sys.stdout.write(str(taggingModel.summary()) + doubleSep)
    return taggingModel, sharedLayers


def addCapitalizationLayer(inputLayers, concFlatten, sharedLayers):
    sharedCapitalEmb = Embedding(4, configuration['multitasking']['capitalDim'], name='capitalizationEmb')
    if configuration['multitasking']['useCapitalization']:
        inputCapital = Input((3,), dtype='int32', name='capitalization')
        inputLayers.append(inputCapital)
        capitalEmb = sharedCapitalEmb(inputCapital)
        capitalFlatten = Flatten()(capitalEmb)
        concFlatten.append(capitalFlatten)
        sharedLayers.append(sharedCapitalEmb)


def addSymbolLayer(inputLayers, concFlatten, sharedLayers):
    sharedSymbolEmb = Embedding(20, configuration['multitasking']['symbolDim'], name='symbolsEmb')
    if configuration['multitasking']['useSymbols']:
        inputSymbol = Input((1,), dtype='int32', name='symbol')
        inputLayers.append(inputSymbol)
        symbolEmb = sharedSymbolEmb(inputSymbol)
        symbolFlatten = Flatten()(symbolEmb)
        concFlatten.append(symbolFlatten)
        sharedLayers.append(sharedSymbolEmb)


def createDepParsingModel(sharedLayers, classNum, vocab):
    depParsingLayers, depParsingDenseLayers = [], []
    # for i in ['b0', 's0', 's1']:
    for i in ['b0', 'b1', 'b2', 's0', 's1', 's2',
              's1_LM1', 's1_LM2', 's0_LM1', 's0_LM2',
              's1_RM1', 's1_RM2', 's0_RM1', 's0_RM2',
              's1_LM_LM', 's1_RM_RM', 's0_LM_LM', 's0_RM_RM']:
        inputLayers, denseLayer = createPosModule(sharedLayers, i)
        depParsingLayers += inputLayers
        depParsingDenseLayers.append(denseLayer)

    synLblInput = Input((12,), dtype='int32', name='SyntacticLabels')
    depParsingLayers.append(synLblInput)
    synLblEmb = Embedding(len(vocab.syntacticLabelIndices), configuration['multitasking']['sytacticLabelDim'],
                          name='SyntacticLabelEmb')(synLblInput)
    synLblFlatten = Flatten()(synLblEmb)
    depParsingDenseLayers.append(synLblFlatten)

    concDense = keras.layers.concatenate(depParsingDenseLayers)
    depParsingDense = Dense(configuration['multitasking']['depParsingDenseUnitNumber'],
                            activation='relu',
                            name='depParsingDense')(concDense)
    depParsingSoftmax = Dense(classNum, activation='softmax', name='depParsingSoftMax')(depParsingDense)
    depParsingModel = Model(inputs=depParsingLayers, outputs=depParsingSoftmax)
    depParsingModel.compile(loss=configuration['nn']['loss'],
                            optimizer=getOptimizer(),
                            metrics=['accuracy'])

    if configuration['others']['verbose']:
        sys.stdout.write(str(depParsingModel.summary()) + doubleSep)
    return depParsingModel


def createIdenModel(sharedLayers):
    idenInputLayers, idenDenseLayers = [], []
    focusedElements = ['b0', 's0', 's1']
    if configuration['multitasking']['useB1']:
        focusedElements = ['b1'] + focusedElements
    if configuration['multitasking']['useBx']:
        focusedElements = ['bx'] + focusedElements
    for i in focusedElements:
        inputLayers, denseLayer = createPosModule(sharedLayers, i)
        idenInputLayers += inputLayers
        idenDenseLayers.append(denseLayer)

    concDense = keras.layers.concatenate(idenDenseLayers)
    idenDense = Dense(configuration['multitasking']['IdenDenseUnitNumber'], activation='relu', name='idenDense')(
        concDense)
    idenSoftmax = Dense(4, activation='softmax', name='idenSoftMax')(idenDense)
    idenModel = Model(inputs=idenInputLayers, outputs=idenSoftmax)
    idenModel.compile(loss=configuration['nn']['loss'],
                      optimizer=getOptimizer(),
                      metrics=['accuracy'])

    if configuration['others']['verbose']:
        sys.stdout.write(str(idenModel.summary()) + doubleSep)
    return idenModel


def getIdenTransData(trans):
    focusedElems = [[trans.configuration.reduced]] if configuration['multitasking']['useBx'] else []
    if configuration['multitasking']['useB1']:
        focusedElems.append([trans.configuration.buffer[1]] if len(trans.configuration.buffer) > 1 else [None])
    focusedElems.append([trans.configuration.buffer[0]] if len(trans.configuration.buffer) > 0 else [None])
    focusedElems.append(
        getTokens(trans.configuration.stack[-1]) if len(trans.configuration.stack) > 0 else [None])
    focusedElems.append(
        getTokens(trans.configuration.stack[-2]) if len(trans.configuration.stack) > 1 else [None])
    return focusedElems


def createPosModule(sharedLayers, title):
    inputSize, tokenEmb = configuration['multitasking']['windowSize'] * 2 + 1, \
                          configuration['multitasking']['tokenDim']
    inputToks = Input((inputSize,), dtype='int32', name=title + 'Tokens')
    inputAffixe = Input((12,), dtype='int32', name=title + 'Affixes')
    inputLayers = [inputToks, inputAffixe]
    taggingTokEmb = sharedLayers[1](inputToks)
    taggingFlatten = Flatten()(taggingTokEmb)
    taggingAffixeEmb = sharedLayers[2](inputAffixe)
    taggingAffixeFlatten = Flatten()(taggingAffixeEmb)
    concFlatten = [taggingFlatten, taggingAffixeFlatten]
    if configuration['multitasking']['useCapitalization']:
        inputCapital = Input((3,), dtype='int32', name=title + 'Capitalization')
        inputLayers.append(inputCapital)
        capitalEmb = sharedLayers[3](inputCapital)
        capitalFlatten = Flatten()(capitalEmb)
        concFlatten.append(capitalFlatten)
    if configuration['multitasking']['useSymbols']:
        inputSymbol = Input((1,), dtype='int32', name=title + 'Symbols')
        inputLayers.append(inputSymbol)
        symbolEmb = sharedLayers[-1](inputSymbol)
        symbolFlatten = Flatten()(symbolEmb)
        concFlatten.append(symbolFlatten)
    concFlatten = keras.layers.concatenate(concFlatten)
    taggingDense = sharedLayers[0](concFlatten)
    return inputLayers, taggingDense


def getValidationData(data, labels):
    validationData = []
    for dataTensor in data:
        validationData.append(dataTensor[int(len(dataTensor) * (1 - configuration['nn']['validationSplit'])):])
    validationLabel = labels[int(len(labels) * (1 - configuration['nn']['validationSplit'])):]
    return validationData, validationLabel


def getOptimizer():
    if configuration['others']['verbose']:
        sys.stdout.write(reports.seperator + reports.tabs +
                         'Optimizer : Adagrad,  learning rate = {0}'.format(configuration['multitasking']['lr'])
                         + reports.seperator)
    return optimizers.Adagrad(lr=configuration['multitasking']['lr'], epsilon=None, decay=0.0)


def getCallBacks():
    bestWeightPath = reports.getBestWeightFilePath()
    callbacks = [
        ModelCheckpoint(bestWeightPath, monitor='val_loss', verbose=1, save_best_only=True, mode='max')
    ] if bestWeightPath else []
    es = EarlyStopping(monitor='val_loss',
                       min_delta=configuration['nn']['minDelta'],
                       patience=configuration['nn']['patience'],
                       verbose=configuration['others']['verbose'])
    if configuration['nn']['earlyStop']:
        callbacks.append(es)
    if configuration['nn']['checkPoint']:
        mc = ModelCheckpoint(
            os.path.join(configuration['path']['projectPath'], 'Reports', configuration['path']['checkPointPath']),
            monitor='val_acc', mode='max', verbose=1, save_best_only=True)
        callbacks.append(mc)
    return callbacks


def overSample(idenData, idenLbls):
    newIdenData = []
    for i in range(len(idenData[0])):
        newIdenDataEntry = []
        for j in range(idenInputArrNum):
            newIdenDataEntry += list(idenData[j][i])
        newIdenData.append(newIdenDataEntry)
    ros = RandomOverSampler(random_state=0)
    newIdenData, newIdenLbls = ros.fit_sample(newIdenData, idenLbls)
    idenData = []
    dataDivision = [2 * configuration['multitasking']['windowSize'] + 1, 12]
    if configuration['multitasking']['useCapitalization']:
        dataDivision.append(3)
    if configuration['multitasking']['useSymbols']:
        dataDivision.append(1)

    dataDivision = dataDivision * (3 + (1 if configuration['multitasking']['useB1'] else 0) +
                                   (1 if configuration['multitasking']['useBx'] else 0))
    for i in range(idenInputArrNum):
        idenData.append([])
    for i in range(len(newIdenData)):
        for j in range(idenInputArrNum):
            end = sum(dataDivision[:j + 1])
            start = end - dataDivision[j]
            idenData[j].append(np.asarray(newIdenData[i][start:end]))
    for i in range(idenInputArrNum):
        idenData[i] = np.asarray(idenData[i])
    return idenData, newIdenLbls


def addDynamicVersion(tokens, corpus):
    if not configuration['embedding']['dynamicVocab'] or not tokens or len(tokens) <= 1:
        return None
    shouldDynamize = [True if t.getLemma() in corpus.importantFrequentWords else False for t in tokens]
    if False in shouldDynamize and True in shouldDynamize:
        return '_'.join(
            t.getTokenOrLemma() if t.getLemma() in corpus.importantFrequentWords else unk for t in tokens)
    return None


def getFrequencyDics(corpus, freqTaux=0):
    tokenVocab = {unk: 5, 'root': 5, empty: 5}
    posVocab = {unk: 5, empty: 5, 'root': 5}
    syntacticLabelVocab = {unk: 5, empty: 5}
    for depGraph in corpus.trainDepGraphs:
        for n in depGraph.nodes:
            k = depGraph.nodes[n]['ctag'].lower()
            if k not in syntacticLabelVocab:
                syntacticLabelVocab[k] = 1
            else:
                syntacticLabelVocab[k] += 1

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
            if configuration['embedding']['compactVocab']:
                del tokenVocab[k]
            elif uniform(0, 1) < configuration['constants']['alpha']:
                del tokenVocab[k]
    if configuration['others']['verbose']:
        sys.stdout.write(tabs + 'After : {0}\n'.format(len(tokenVocab)))
    return tokenVocab, posVocab, syntacticLabelVocab


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


def getContextTexts(tokens, s):
    if str(tokens.__class__).endswith('corpus.Token'):
        txts = [tokens.text]
        txts += [s.tokens[tokens.position - 2].text] if tokens.position > 1 else ['']
        txts += [s.tokens[tokens.position].text] if tokens.position < len(s.tokens) else ['']
    else:
        positions = [i.position - 1 for i in tokens]
        minPos, maxPos = min(positions), max(positions)
        txts = [getLemmaString(tokens).replace(' ', '_')]
        if minPos > 0:
            token = s.tokens[minPos - 1]
            txts += [token.text] if token.position > 1 else ['']
        else:
            txts += ['']
        if maxPos < len(s.tokens) - 1:
            token = s.tokens[maxPos + 1]
            txts += [token.text] if token.position < len(s.tokens) else ['']
        else:
            txts += ['']
    return txts


def getSymbolInfo(tokens):
    hasDigit, hasHyphen, hasPunctuation = False, False, False
    txt = ' '.join(t.text for t in tokens)
    idx = 0
    for c in txt:
        if c.isdigit():
            if not hasDigit:
                idx += 3
            hasDigit = True
        if c == '-' or c == '_':
            if not hasHyphen:
                idx += 5
            hasHyphen = True
        if c in ["'", ',', '.', '#', '@', '!', '?']:
            if not hasPunctuation:
                idx += 7
            hasPunctuation = True
    return [int(idx)]


def getCapitalizationInfo(tokens, s):
    txts = getContextTexts(tokens, s)
    capitalization = []
    for txt in txts:
        isWord = True
        for c in txt:
            if not c.isalpha():
                isWord = False
                capitalization.append(2)
                break
        if isWord:
            if txt == txt.upper():
                capitalization.append(0)
            elif txt[0] == txt[0].upper():
                capitalization.append(1)
            else:
                capitalization.append(2)
    return capitalization


def indexateDic(dic):
    res = dict()
    r = range(len(dic))
    for i, k in enumerate(dic):
        res[k] = r[i]
    return res


def padSequence(seq, label, emptyIdx):
    padConf = configuration['mlpNonLexicl']
    return np.asarray(pad_sequences([seq], maxlen=padConf[label], value=emptyIdx))[0]


def getBufferTokens(conf, sent, vocab, network, dataEntry):
    for i in range(3):
        if i < len(conf.buffer):
            bi = conf.buffer[i] - 1
            addTokenTaggingEntries(sent.tokens[bi], sent, dataEntry, vocab, network)
        else:
            addTokenTaggingEntries(None, sent, dataEntry, vocab, network)


def getStackTokens(conf, sent, vocab, network, dataEntry):
    for i in range(1, 4):
        if i < len(conf.stack):
            si = conf.stack[-i] - 1
            if si == -1:
                addTokenTaggingEntries('root', sent, dataEntry, vocab, network)
            else:
                addTokenTaggingEntries(sent.tokens[si], sent, dataEntry, vocab, network)
        else:
            addTokenTaggingEntries(None, sent, dataEntry, vocab, network)


def getSyntacticLabelIndice(t, vocab):
    if t:
        k = t.dependencyLabel.lower()
        if k in vocab:
            return vocab[k]
        return vocab[unk]
    return vocab[empty]


def getStackLeftMosts(conf, sent, vocab, synVocab, network, dataEntry):
    syntacticLabels = []
    for i in range(2):
        if len(conf.stack) >= 2 - i:
            if conf.stack[i - 2] > 0:
                si = sent.tokens[conf.stack[i - 2] - 1]
                leftMostChildren = getLeftMostChildren(si, sent)
                for t in leftMostChildren[:2]:
                    addTokenTaggingEntries(t, sent, dataEntry, vocab, network)
                    syntacticLabels.append(getSyntacticLabelIndice(t, synVocab))
                for _ in range(2 - len(leftMostChildren)):
                    addTokenTaggingEntries(None, sent, dataEntry, vocab, network)
                    syntacticLabels.append(getSyntacticLabelIndice(None, synVocab))
            else:
                addTokenTaggingEntries(None, sent, dataEntry, vocab, network)
                syntacticLabels.append(getSyntacticLabelIndice(None, synVocab))
                addTokenTaggingEntries(None, sent, dataEntry, vocab, network)
                syntacticLabels.append(getSyntacticLabelIndice(None, synVocab))
        else:
            addTokenTaggingEntries(None, sent, dataEntry, vocab, network)
            syntacticLabels.append(getSyntacticLabelIndice(None, synVocab))
            addTokenTaggingEntries(None, sent, dataEntry, vocab, network)
            syntacticLabels.append(getSyntacticLabelIndice(None, synVocab))
    return syntacticLabels


def getStackRightMosts(conf, sent, vocab, synVocab, network, dataEntry):
    syntacticLabels = []
    for i in range(2):
        if len(conf.stack) >= 2 - i:
            if conf.stack[i - 2] > 0:
                si = sent.tokens[conf.stack[i - 2] - 1]
                rightMostChildren = getRightMostChildren(si, sent)
                for t in rightMostChildren[:2]:
                    addTokenTaggingEntries(t, sent, dataEntry, vocab, network)
                    syntacticLabels.append(getSyntacticLabelIndice(t, synVocab))
                for _ in range(2 - len(rightMostChildren)):
                    addTokenTaggingEntries(None, sent, dataEntry, vocab, network)
                    syntacticLabels.append(getSyntacticLabelIndice(None, synVocab))
            else:
                addTokenTaggingEntries(None, sent, dataEntry, vocab, network)
                syntacticLabels.append(getSyntacticLabelIndice(None, synVocab))
                addTokenTaggingEntries(None, sent, dataEntry, vocab, network)
                syntacticLabels.append(getSyntacticLabelIndice(None, synVocab))
        else:
            addTokenTaggingEntries(None, sent, dataEntry, vocab, network)
            syntacticLabels.append(getSyntacticLabelIndice(None, synVocab))
            addTokenTaggingEntries(None, sent, dataEntry, vocab, network)
            syntacticLabels.append(getSyntacticLabelIndice(None, synVocab))
    return syntacticLabels


def getStackLeftAndRightMostOfLeftAndRightMosts(conf, sent, vocab, synVocab, network, dataEntry):
    syntacticLabels = []
    for i in range(2):
        if len(conf.stack) >= 2 - i and conf.stack[i - 2] > 0:
            si = sent.tokens[conf.stack[i - 2] - 1]
            leftMostOfLeftMostChild = getLeftMostOfLeftMostChildren(si, sent)
            addTokenTaggingEntries(leftMostOfLeftMostChild, sent, dataEntry, vocab, network)
            syntacticLabels.append(getSyntacticLabelIndice(leftMostOfLeftMostChild, synVocab))
            rightMostOfRightMostChild = getRightMostOfRightMostChildren(si, sent)
            addTokenTaggingEntries(rightMostOfRightMostChild, sent, dataEntry, vocab, network)
            syntacticLabels.append(getSyntacticLabelIndice(rightMostOfRightMostChild, synVocab))
        else:
            addTokenTaggingEntries(None, sent, dataEntry, vocab, network)
            syntacticLabels.append(getSyntacticLabelIndice(None, synVocab))
            addTokenTaggingEntries(None, sent, dataEntry, vocab, network)
            syntacticLabels.append(getSyntacticLabelIndice(None, synVocab))
    return syntacticLabels


def getLeftMostChildren(token, sent):
    leftMostChildren = []
    for t in sent.tokens[:token.position - 1]:
        if t.dependencyParent == token.position:
            leftMostChildren.append(t)
    return leftMostChildren


def getLeftMostOfLeftMostChildren(token, sent):
    leftMostChildren = []
    for t in sent.tokens[:token.position - 1]:
        if t.dependencyParent == token.position:
            leftMostChildren.append(t)
            break
    if leftMostChildren:
        return getLeftMostChildren(leftMostChildren[0], sent)[0]
    return None


def getRightMostOfRightMostChildren(token, sent):
    rightMostChildren = []
    for t in sent.tokens[:token.position - 1]:
        if t.dependencyParent == token.position:
            rightMostChildren.append(t)
            break
    if rightMostChildren:
        return getRightMostChildren(rightMostChildren[0], sent)[0]
    return None


def getRightMostChildren(token, sent):
    rightMostChildren = []
    for t in reversed(sent.tokens[token.position:]):
        if t.dependencyParent == token.position:
            rightMostChildren.append(t)
    return rightMostChildren


def addTokenTaggingEntries(token, sent, dataEntry, vocab, network):
    if token and isinstance(token, Token) and token.getTokenOrLemma() in vocab:
        taggingEntry = network.getTaggingEntry([token], sent)
        for j in range(len(taggingEntry) - 1):
            dataEntry.append(taggingEntry[j])
            # dataEntry.append(vocab[sent.tokens[b0].getTokenOrLemma()])
    else:
        if not token:
            taggingEntry = network.getTaggingEntry(['empty'], sent)
            for j in range(len(taggingEntry) - 1):
                dataEntry.append(taggingEntry[j])
        else:
            taggingEntry = network.getTaggingEntry([token], sent)
            for j in range(len(taggingEntry) - 1):
                dataEntry.append(taggingEntry[j])


def getDataEntry(conf, sent, network):
    tokenVocab = network.vocabulary.tokenIndices
    syntacticLabelVocab = network.vocabulary.syntacticLabelIndices
    dataEntry = []
    getBufferTokens(conf, sent, tokenVocab, network, dataEntry)
    getStackTokens(conf, sent, tokenVocab, network, dataEntry)
    syntacticLabels = getStackLeftMosts(conf, sent, tokenVocab, syntacticLabelVocab, network, dataEntry)
    syntacticLabels += getStackRightMosts(conf, sent, tokenVocab, syntacticLabelVocab, network, dataEntry)
    syntacticLabels += getStackLeftAndRightMostOfLeftAndRightMosts(conf, sent, tokenVocab,syntacticLabelVocab, network, dataEntry)
    dataEntry.append(syntacticLabels)
    return dataEntry


def shouldStopLearning(historyList, patience=4, minDelta=.1):
    if len(historyList) <= patience:
        return False
    for i in range(patience):
        if historyList[len(historyList) - i - 1].history['loss'][0] - \
                historyList[len(historyList) - i - 2].history['loss'][0] <= minDelta:
            continue
        else:
            return False
    return True
