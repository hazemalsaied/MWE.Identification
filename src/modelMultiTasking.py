import copy
import random
from random import uniform

import keras
import numpy as np
from imblearn.over_sampling import RandomOverSampler
from keras import optimizers
from keras.callbacks import EarlyStopping
from keras.layers import Input, Dense, Flatten, Embedding
from keras.models import Model
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from nltk.parse import DependencyEvaluator
from nltk.parse.transitionparser import TransitionParser, Transition, Configuration

import reports
from corpus import Token
from corpus import getRelevantModelAndNormalizer
from corpus import getTokens, getLemmaString
from modelLinear import getFeatures
from parser import parse
from reports import *
from transitions import TransitionType
from wordEmbLoader import empty
from wordEmbLoader import unk, number

enableCategorization = False

importantFrequentWordDic = dict()

global idenInputArrNum, taggingInputArray, depParserInuptArrNum

mtParams = configuration['multitasking']
trainParams = configuration['nn']


class Network:
    def __init__(self, corpus):
        global idenInputArrNum, taggingInputArray, depParserInuptArrNum
        self.depLabelDic = dict()
        taggingInputArray = 2 + int(mtParams['useCapitalization']) + int(mtParams['useSymbols'])
        idenInputArrNum = taggingInputArray * (3 + mtParams['useB1'] + mtParams['useBx'])
        depParserInuptArrNum = taggingInputArray * 18 + 1
        self.vocabulary = Vocabulary(corpus)
        if configuration['tmp']['trainDepParser'] or configuration['tmp']['trainJointly'] or configuration['tmp'][
            'trainInTransfert']:
            self.depParserData, self.depParserLabels, self.depLabelDic = SynDataFactory.getData(corpus, self.vocabulary)

        self.taggingModel, self.idenModel, self.depParsingModel = Builder.build(self.vocabulary, len(self.depLabelDic))

    def trainAll(self, corpus):
        taggingData, taggingLbls = TaggingDataFactory.getTaggingData(self.vocabulary, corpus)
        taggingLbls = to_categorical(taggingLbls, num_classes=len(self.vocabulary.posIndices))
        idenData, idenLbls = self.getIdenData(corpus)
        idenData, idenLbls = DataFactory.overSample(idenData, idenLbls)
        sys.stdout.write('POS Tagging data = {0}\n'.format(len(taggingLbls)))
        sys.stdout.write('Iden data = {0}\n'.format(len(idenLbls)))
        sys.stdout.write('Dependency parsing = {0}\n'.format(len(self.depParserLabels)))
        idenLbls = to_categorical(idenLbls, num_classes=4)
        depParserLabels = to_categorical(self.depParserLabels, num_classes=len(self.depLabelDic))
        historyList, depIdx = [], 1
        sys.stdout.write('Dependency Parsing: {0}\n'.format(depIdx))
        self.depParsingModel.fit(self.depParserData, depParserLabels,
                                 validation_split=trainParams['validationSplit'],
                                 batch_size=trainParams['depParserBatchSize'],
                                 verbose=2)
        for x in range(trainParams['initialEpochs']):
            sys.stdout.write('POS tagging: {0}\n'.format(x + 1))
            self.taggingModel.fit(taggingData, taggingLbls,
                                  batch_size=trainParams['taggingBatchSize'],
                                  verbose=2)

        posIdx, idenIdx = trainParams['initialEpochs'] + 1, 1
        sys.stdout.write('Train start {0}'.format(datetime.datetime.now()))
        for x in range(trainParams['jointLearningEpochs']):
            t = datetime.datetime.now()
            alpha = random.uniform(0, 1)
            if alpha < .33:
                sys.stdout.write(
                    'POS tagging: {0}\n'.format(posIdx))
                self.taggingModel.fit(taggingData, taggingLbls,
                                      verbose=2,
                                      batch_size=trainParams['taggingBatchSize'])
                posIdx += 1
            elif .66 > alpha >= .33:
                depIdx += 1
                sys.stdout.write('Dependency Parsing: {0}\n'.format(depIdx))
                self.depParsingModel.fit(self.depParserData, depParserLabels,
                                         validation_split=trainParams['validationSplit'],
                                         batch_size=trainParams['depParserBatchSize'],
                                         verbose=2)

            else:
                sys.stdout.write('MWE identification: {0}\n'.format(idenIdx))
                his = self.idenModel.fit(idenData, idenLbls,
                                         validation_split=trainParams['validationSplit'],
                                         verbose=2,
                                         batch_size=trainParams['identBatchSize'])
                historyList.append(his)
                if Network.shouldStopLearning(historyList):
                    break
                idenIdx += 1
            STDOutTools.getExcutionTime('Training time', t)

    def trainInTransfert(self, corpus):
        self.trainTagging(corpus)
        configuration['multitasking']['testOnToken'] = True
        self.testTagging(corpus)
        configuration['multitasking']['testOnToken'] = False
        self.testTagging(corpus, title='POS tagging accuracy (MWEs)')
        configuration['multitasking']['testOnToken'] = True

        self.trainIden(corpus)
        parse(corpus.testingSents, self, None)
        self.trainDepParser()
        self.evaluateDepParsing(corpus)

    def train(self, corpus):
        epochNumber = 100
        taggingData, taggingLbls = TaggingDataFactory.getTaggingData(self.vocabulary, corpus)
        idenData, idenLbls = self.getIdenData(corpus)
        trainParams = configuration['nn']
        self.taggingModel.fit(taggingData, taggingLbls,
                              validation_split=trainParams['validationSplit'],
                              epochs=1,
                              batch_size=trainParams['taggingBatchSize'],
                              verbose=2)
        idenLoss, taggingLoss = [], []
        for i in range(epochNumber):
            if uniform(0, 1) > .5:
                history = self.taggingModel.fit(taggingData, taggingLbls,
                                                validation_split=trainParams['validationSplit'],
                                                epochs=1,
                                                batch_size=trainParams['taggingBatchSize'],
                                                verbose=2)
                taggingLoss.append(history.history['loss'])
            else:
                history = self.idenModel.fit(idenData, idenLbls,
                                             validation_split=trainParams['validationSplit'],
                                             epochs=1,
                                             batch_size=trainParams['taggingBatchSize'],
                                             verbose=2)
                idenLoss.append(history.history['loss'])
                # TODO check the early stopping

    def trainDepParser(self):
        depParserLabels = to_categorical(self.depParserLabels, num_classes=len(self.depLabelDic))
        sys.stdout.write('Dependency parsing = {0}\n'.format(len(self.depParserLabels)))
        self.depParsingModel.fit(self.depParserData, depParserLabels,
                                 validation_split=trainParams['validationSplit'],
                                 epochs=trainParams['epochs'],
                                 batch_size=trainParams['depParserBatchSize'],
                                 verbose=2,
                                 callbacks=Network.getCallBacks())

    def evaluateDepParsing(self, corpus):
        result = self.parse(corpus)
        de = DependencyEvaluator(result, corpus.testDepGraphs)
        sys.stdout.write('UAS = {0}\nLAS = {1}'.format(round(de.eval()[0] * 100, 1), round(de.eval()[1] * 100, 1)))

    def predictDepParsing(self, conf, sent):
        inputs = SynDataFactory.getDataEntry(conf, sent, self.vocabulary)
        inputs = [np.asarray([d]) for d in inputs]
        probVectors = self.depParsingModel.predict(inputs, batch_size=1)
        return probVectors[0]

    def parse(self, corpus):
        result = []
        transParser = TransitionParser(TransitionParser.ARC_STANDARD)
        operation = Transition(transParser.ARC_STANDARD)
        for i in range(len(corpus.testingSents)):
            sent = corpus.testingSents[i]
            depGraph = copy.deepcopy(corpus.testDepGraphs[i])
            for n in depGraph.nodes:
                depGraph.nodes[n]['rel'] = ''
                depGraph.nodes[n]['head'] = None
            conf = Configuration(depGraph)
            # print sent.text
            while len(conf.buffer) > 0:
                probVector = self.predictDepParsing(conf, sent)
                trans = sorted(range(len(probVector)), key=lambda k: probVector[k], reverse=True)[0]
                for k, v in self.depLabelDic.items():
                    if trans == v:
                        baseTransition = k.split(":")[0]
                        # print baseTransition
                        if baseTransition[:4].lower() == Transition.LEFT_ARC[:4].lower():
                            if operation.left_arc(conf, k.split(":")[1]) != -1:
                                break
                        elif baseTransition[:4].lower() == Transition.RIGHT_ARC[:4].lower():
                            if operation.right_arc(conf, k.split(":")[1]) != -1:
                                break
                        elif baseTransition[:4].lower() == Transition.SHIFT[:4].lower():
                            if operation.shift(conf) != -1:
                                break
            for (head, rel, child) in conf.arcs:
                c_node = depGraph.nodes[child]
                c_node['head'] = head
                c_node['rel'] = rel
            result.append(depGraph)
        return result

    def trainIden(self, corpus):
        trainParams = configuration['nn']
        idenData, idenLbls = self.getIdenData(corpus)
        idenData, idenLbls = DataFactory.overSample(idenData, idenLbls)
        idenLbls = to_categorical(idenLbls, num_classes=4)
        sys.stdout.write('Iden data = {0}\n'.format(len(idenLbls)))
        self.idenModel.fit(idenData, idenLbls, validation_split=trainParams['validationSplit'],
                           epochs=trainParams['epochs'],
                           batch_size=trainParams['identBatchSize'],
                           verbose=2,
                           callbacks=Network.getCallBacks())

    def trainTagging(self, corpus):
        taggingData, taggingLbls = TaggingDataFactory.getTaggingData(self.vocabulary, corpus)
        taggingLbls = to_categorical(taggingLbls, num_classes=len(self.vocabulary.posIndices))
        sys.stdout.write('POS Tagging data = {0}\n'.format(len(taggingLbls)))
        self.taggingModel.fit(taggingData, taggingLbls,
                              validation_split=.2,
                              epochs=100,
                              batch_size=configuration['nn']['taggingBatchSize'],
                              verbose=2,
                              callbacks=Network.getCallBacks())

    def trainTaggerAndIdentifier(self, corpus):
        taggingData, taggingLbls = TaggingDataFactory.getTaggingData(self.vocabulary, corpus)
        taggingLbls = to_categorical(taggingLbls, num_classes=len(self.vocabulary.posIndices))
        idenData, idenLbls = self.getIdenData(corpus)
        if configuration['sampling']['overSampling']:
            idenData, idenLbls = DataFactory.overSample(idenData, idenLbls)
        sys.stdout.write('Iden data = {0}\n'.format(len(idenLbls)))
        sys.stdout.write('POS Tagging data = {0}\n'.format(len(taggingLbls)))
        idenLbls = to_categorical(idenLbls, num_classes=4)
        historyList = []
        for x in range(mtParams['initialEpochs']):
            sys.stdout.write('POS tagging: {0}\n'.format(x + 1))
            self.taggingModel.fit(taggingData, taggingLbls,
                                  batch_size=configuration['nn']['taggingBatchSize'],
                                  verbose=2)
        for x in range(configuration['nn']['jointLearningEpochs']):
            if x % 2 == 0:
                sys.stdout.write(
                    'POS tagging: {0}\n'.format(int(x / 2) + 1 + mtParams['initialEpochs']))
                self.taggingModel.fit(taggingData, taggingLbls,
                                      verbose=2,
                                      batch_size=configuration['nn']['taggingBatchSize'])
            else:
                sys.stdout.write('MWE identification: {0}\n'.format(int(x / 2) + 1))
                his = self.idenModel.fit(idenData, idenLbls,
                                         verbose=2,
                                         batch_size=mtParams['identBatchSize'])
                historyList.append(his)
                if Network.shouldStopLearning(historyList):
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
        taggingData, taggingLbls = TaggingDataFactory.getTaggingData(self.vocabulary, corpus, train=False)
        taggingLbls = to_categorical(taggingLbls, num_classes=len(self.vocabulary.posIndices))
        results = self.taggingModel.evaluate(taggingData, taggingLbls, batch_size=32, verbose=0)
        sys.stdout.write('{0} = {1}\n'.format(title, round(results[1] * 100, 1)))

    def getPredData(self, trans, sent):
        data = []
        for i in range(idenInputArrNum):
            data.append([])
        focusedElems = DataFactory.getIdenTransData(trans)
        for i in range(len(focusedElems)):
            taggingEntry = self.vocabulary.getTaggingEntry(focusedElems[i], sent)
            for j in range(len(taggingEntry) - 1):  # i*4, i*4 + 4):
                data[i * taggingInputArray + j].append(np.asarray(taggingEntry[j]))
        return [np.asarray(data[i]) for i in range(idenInputArrNum)]

    def getIdenData(self, corpus, train=True):
        data, labels = [[] for _ in range(idenInputArrNum)], []
        for sent in corpus.trainingSents if train else corpus.testingSents:
            if train and not sent.vMWEs:
                continue
            trans = sent.initialTransition
            while trans and trans.next:
                focusedElems = DataFactory.getIdenTransData(trans)
                for i in range(len(focusedElems)):
                    taggingEntry = self.vocabulary.getTaggingEntry(focusedElems[i], sent)
                    for j in range(len(taggingEntry) - 1):
                        data[i * taggingInputArray + j].append(np.asarray(taggingEntry[j]))
                labels.append(trans.next.type.value if trans.next.type.value <= 2 else 3)
                trans = trans.next
        return [np.asarray(data[i]) for i in range(idenInputArrNum)], labels

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
        s0elems = DataFactory.padSequence(s0elems, 's0Padding', emptyIdx)
        s1elems = DataFactory.padSequence(s1elems, 's1Padding', emptyIdx)
        if trans.configuration.buffer:
            bTokens = trans.configuration.buffer[:2]
            belems = self.vocabulary.getIndices(bTokens)
        belems = DataFactory.padSequence(belems, 'bPadding', emptyIdx)
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
            if mtParams['useB1']:
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
            if mtParams['useB1']:
                tokenIdxs.append(emptyTokenIdx)
                posIdxs.append(emptyPosIdx)
        if mtParams['useBx']:
            if trans.configuration.reduced:
                tokenIdx, posIdx = self.vocabulary.getIndices([trans.configuration.reduced], dynamicVocab=dynamicVocab,
                                                              parse=parse)
                tokenIdxs.append(tokenIdx)
                posIdxs.append(posIdx)
            else:
                tokenIdxs.append(emptyTokenIdx)
                posIdxs.append(emptyPosIdx)

        return np.asarray(tokenIdxs), np.asarray(posIdxs)

    @staticmethod
    def getOptimizer(key):
        if configuration['others']['verbose']:
            sys.stdout.write(reports.seperator + reports.tabs +
                             'Optimizer : Adagrad,  learning rate = {0}'.format(configuration['nn'][key])
                             + reports.seperator)
        return optimizers.Adagrad(lr=configuration['nn'][key], epsilon=None, decay=0.0)

    @staticmethod
    def getCallBacks():
        trainParams = configuration['nn']
        es = EarlyStopping(monitor=trainParams['monitor'],
                           min_delta=trainParams['minDelta'],
                           patience=trainParams['patience'],
                           verbose=configuration['others']['verbose'])
        return [es]

    @staticmethod
    def shouldStopLearning(historyList,
                           patience=configuration['nn']['patience'],
                           minDelta=configuration['nn']['minDelta']):
        if len(historyList) <= patience:
            return False
        key = 'loss' if configuration['nn']['monitor'] == 'val_loss' else 'acc'
        sys.stdout.write('Should stop early?\n')
        for i in range(patience):
            if len(historyList) - i - 1 > 0 and historyList[len(historyList) - i - 1].history[key][0] - \
                    historyList[len(historyList) - i - 2].history[key][0] <= minDelta:
                continue
            else:
                return False
        sys.stdout.write('Early stopping applied\n')
        return True


class TaggingDataFactory:
    @staticmethod
    def getTaggingData(vocab, corpus, train=True):
        data, lbls = [[] for _ in range(taggingInputArray)], []
        for s in corpus.allTrainingSents if train else corpus.testingSents:
            for item in s.tokens + s.vMWEs:
                if not train and not mtParams['testOnToken'] and \
                        str(item.__class__).endswith('corpus.Token'):
                    continue
                tokens = [item] if str(item.__class__).endswith('corpus.Token') else item.tokens
                outputs = vocab.getTaggingEntry(tokens, s)
                for i in range(len(outputs) - 1):
                    data[i].append(outputs[i])
                lbls.append(outputs[-1])
        return [np.asarray(d) for d in data], lbls


class Vocabulary:
    def __init__(self, corpus):
        self.affixeDic = self.getAffixeDic(corpus)
        self.affixeIndices = Vocabulary.indexateDic(self.affixeDic)
        self.tokenFreqs, self.posFreqs, self.sytacticLabels = Vocabulary.getFrequencyDics(corpus)
        self.tokenIndices = Vocabulary.indexateDic(self.tokenFreqs)
        self.posIndices = Vocabulary.indexateDic(self.posFreqs)
        self.syntacticLabelIndices = Vocabulary.indexateDic(self.sytacticLabels)
        if configuration['others']['verbose'] == 1:
            sys.stdout.write(str(self))
            self.verify(corpus)

    def __str__(self):
        res = seperator + tabs + 'Vocabulary' + doubleSep
        res += tabs + 'Tokens := {0} * POS : {1}'.format(len(self.tokenIndices), len(self.posIndices)) \
            if not configuration['xp']['compo'] else ''
        res += seperator
        return res

    def getTaggingEntry(self, tokens, s):
        outputs = []
        if tokens == [None]:
            outputs = [[self.tokenIndices[unk]] * (mtParams['windowSize'] * 2 + 1),
                       [self.affixeIndices[unk]] * 12]
            if mtParams['useCapitalization']:
                outputs.append([2] * 3)
            if mtParams['useSymbols']:
                outputs.append([0])
            outputs.append(self.posIndices[unk])
            return outputs
        if tokens == ['empty']:
            outputs = [[self.tokenIndices[empty]] * (mtParams['windowSize'] * 2 + 1),
                       [self.affixeIndices[empty]] * 12]
            if mtParams['useCapitalization']:
                outputs.append([2] * 3)
            if mtParams['useSymbols']:
                outputs.append([0])
            outputs.append(self.posIndices[empty])
            return outputs
        if tokens == ['root']:
            outputs = [[self.tokenIndices['root']] * (mtParams['windowSize'] * 2 + 1),
                       [self.affixeIndices[unk]] * 12]
            if mtParams['useCapitalization']:
                outputs.append([2] * 3)
            if mtParams['useSymbols']:
                outputs.append([0])
            outputs.append(self.posIndices['root'])
            return outputs
        tokenIdxs = self.getTokenIdxs(tokens, s)
        outputs.append(tokenIdxs)
        affixes = self.getAffixeIndices(tokens, s)
        outputs.append(affixes)
        if mtParams['useCapitalization']:
            capitalIdx = DataFactory.getCapitalizationInfo(tokens, s)
            outputs.append(capitalIdx)
        if mtParams['useSymbols']:
            symbols = DataFactory.getSymbolInfo(tokens)
            outputs.append(symbols)
        attachedPos = '_'.join(t.posTag.lower() for t in tokens)
        posIdx = self.posIndices[attachedPos.lower() if attachedPos in self.posIndices else unk]
        outputs.append(posIdx)
        return outputs

    def getTokenIdxs(self, tokens, s):
        windowSize = mtParams['windowSize']
        positions = [int(t.position) - 1 for t in tokens]
        minPos, maxPos, tokenIdxs = min(positions), max(positions), []
        res = getLemmaString(tokens) + ' ' + str(minPos) + ' ' + str(maxPos) + ' '
        for i in reversed(range(1, windowSize + 1)):
            if minPos - i >= 0:
                currentToken = s.tokens[minPos - i]
                if currentToken.getTokenOrLemma() in self.tokenIndices:
                    tokenIdxs.append(self.tokenIndices[currentToken.getTokenOrLemma()])
                    res += currentToken.getTokenOrLemma() + ' '
                else:
                    tokenIdxs.append(self.tokenIndices[unk])
                    res += 'unk '
            else:
                tokenIdxs.append(self.tokenIndices[empty])
                res += 'emp '
        for i in range(1, windowSize + 1):
            if maxPos + i < len(s.tokens):
                currentToken = s.tokens[maxPos + i]
                if currentToken.getTokenOrLemma() in self.tokenIndices:
                    tokenIdxs.append(self.tokenIndices[currentToken.getTokenOrLemma()])
                    res += currentToken.getTokenOrLemma() + ' '
                else:
                    tokenIdxs.append(self.tokenIndices[unk])
                    res += 'unk '
            else:
                tokenIdxs.append(self.tokenIndices[empty])
                res += 'emp '
        xStr = getLemmaString(tokens).replace(' ', '_')
        if xStr in self.tokenIndices:
            tokenIdxs.append(self.tokenIndices[xStr])
            res += ' ' + xStr
        else:
            tokenIdxs.append(self.tokenIndices[unk])
            res += ' unk'
        return tokenIdxs

    def getAffixeIndices(self, tokens, s):
        affixes = []
        txts = DataFactory.getContextTexts(tokens, s)
        for txt in txts:
            txt = txt.lower()
            if len(txt) > 2:
                if txt[:2] in self.affixeIndices:
                    affixes.append(self.affixeIndices[txt[:2]])
                    if len(txt) > 2 and txt[:3] in self.affixeIndices:
                        affixes.append(self.affixeIndices[txt[:3]])
                    else:
                        affixes.append(self.affixeIndices[unk])
                else:
                    affixes.append(self.affixeIndices[unk])
                    affixes.append(self.affixeIndices[unk])
                if txt[-2:] in self.affixeIndices:
                    affixes.append(self.affixeIndices[txt[-2:]])
                    if len(txt) > 2 and txt[-3:] in self.affixeIndices:
                        affixes.append(self.affixeIndices[txt[-3:]])
                    else:
                        affixes.append(self.affixeIndices[unk])
                else:
                    affixes.append(self.affixeIndices[unk])
                    affixes.append(self.affixeIndices[unk])
            else:
                affixes += [self.affixeIndices[unk]] * 4
        return affixes

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
            tokenTxt, posTxt = Vocabulary.attachTokens(tokens, dynamicVocab=False)
        else:
            tokenTxt, posTxt = Vocabulary.attachTokens(tokens, dynamicVocab=dynamicVocab)
        if tokenTxt in self.tokenIndices:
            tokenIdx = self.tokenIndices[tokenTxt]
        else:
            if dynamicVocab and parse:
                tokenTxt, posTxt = Vocabulary.attachTokens(tokens, dynamicVocab=dynamicVocab, parse=parse)
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

    def printTagging(self, de):
        reversedTokens, reversedAffixes = dict(), dict()
        for i in range(2):
            for k, v in [self.tokenIndices, self.affixeIndices][i]:
                [reversedTokens, reversedAffixes][i][v] = k
        tokens = ' '.join(reversedTokens[e] for e in de[0])
        affixes = ' '.join(reversedAffixes[e] for e in de[1])
        print tokens
        print affixes

    @staticmethod
    def getSynLabels(corpus):
        syntacticLabelVocab = {unk: 5, empty: 5, 'root': 5}
        for depGraph in corpus.trainDepGraphs:
            for n in depGraph.nodes:
                if depGraph.nodes[n]['rel'] is not None:
                    k = depGraph.nodes[n]['rel'].lower()
                    if k not in syntacticLabelVocab:
                        syntacticLabelVocab[k] = 1
                    else:
                        syntacticLabelVocab[k] += 1
        return syntacticLabelVocab

    @staticmethod
    def getFrequencyDics(corpus):
        syntacticLabelVocab = Vocabulary.getSynLabels(corpus)
        tokenVocab = {unk: 5, 'root': 5, empty: 5}
        posVocab = {unk: 5, empty: 5, 'root': 5}

        for sent in corpus.trainingSents:
            trans = sent.initialTransition
            while trans:
                if trans.configuration.stack:
                    tokens = getTokens(trans.configuration.stack[-1])
                    if tokens:
                        tokenTxt, posTxt = Vocabulary.attachTokens(tokens)
                        for c in tokenTxt:
                            if c.isdigit():
                                tokenTxt = number
                        tokenVocab[tokenTxt] = 1 if tokenTxt not in tokenVocab else tokenVocab[tokenTxt] + 1
                        posVocab[posTxt] = 1 if posTxt not in posVocab else posVocab[posTxt] + 1
                        if tokenTxt:
                            tokenVocab[tokenTxt] = 1 if tokenTxt not in tokenVocab else tokenVocab[tokenTxt] + 1

                trans = trans.next
        # Vocabulary.cleanVocab(tokenVocab)
        return tokenVocab, posVocab, syntacticLabelVocab

    @staticmethod
    def cleanVocab(tokenVocab, mweTokenDictionary, freqTaux=0):
        if configuration['others']['verbose']:
            sys.stdout.write(tabs + 'Non frequent word cleaning:' + doubleSep)
            sys.stdout.write(tabs + 'Before : {0}\n'.format(len(tokenVocab)))
        for k in tokenVocab.keys():
            if tokenVocab[k] <= freqTaux and '_' not in k and k.lower() not in mweTokenDictionary:
                if configuration['embedding']['compactVocab']:
                    del tokenVocab[k]
                elif uniform(0, 1) < configuration['constants']['alpha']:
                    del tokenVocab[k]
        if configuration['others']['verbose']:
            sys.stdout.write(tabs + 'After : {0}\n'.format(len(tokenVocab)))
        return tokenVocab

    @staticmethod
    def indexateDic(dic):
        res = dict()
        r = range(len(dic))
        for i, k in enumerate(dic):
            res[k] = r[i]
        return res

    @staticmethod
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


class Builder:
    @staticmethod
    def build(vocab, depParserClassNum):
        taggingModel, sharedLayers = Builder.buildTaggingModel(vocab)
        if configuration['tmp']['trainIden'] or configuration['tmp']['trainJointly'] or configuration['tmp'][
            'trainInTransfert']:
            idenModel = Builder.buildIdenModel(sharedLayers)
        else:
            idenModel = None
        if configuration['tmp']['trainDepParser'] or configuration['tmp']['trainJointly'] or configuration['tmp'][
            'trainInTransfert']:
            depParsingModel = Builder.buildDepParsingModel(sharedLayers, depParserClassNum, vocab)
        else:
            depParsingModel = None
        return taggingModel, idenModel, depParsingModel

    @staticmethod
    def buildTaggingModel(vocab):
        inputToks = Input((mtParams['windowSize'] * 2 + 1,), dtype='int32', name='tokens')
        inputAffixe = Input((12,), dtype='int32', name='affixes')
        inputLayers = [inputToks, inputAffixe]
        sharedTokEmb = Embedding(len(vocab.tokenIndices), mtParams['tokenDim'], name='tokenEmb')
        sharedAffixeEmb = Embedding(len(vocab.affixeIndices), mtParams['affixeDim'],
                                    name='affixeseEmb')

        taggingFlatten = Flatten()(sharedTokEmb(inputToks))
        taggingAffixeFlatten = Flatten()(sharedAffixeEmb(inputAffixe))
        concFlatten = [taggingFlatten, taggingAffixeFlatten]
        sharedLayers = [sharedTokEmb, sharedAffixeEmb]
        Builder.addCapitalizationLayer(inputLayers, concFlatten, sharedLayers)
        Builder.addSymbolLayer(inputLayers, concFlatten, sharedLayers)
        concFlatten = keras.layers.concatenate(concFlatten)
        sharedDense = Dense(mtParams['taggingDenseUnits'], activation='relu', name='posDense')
        sharedLayers = [sharedDense] + sharedLayers
        taggingDense = sharedDense(concFlatten)

        taggingSoftmax = Dense(len(vocab.posIndices), activation='softmax')(taggingDense)
        taggingModel = Model(inputs=inputLayers, outputs=taggingSoftmax)
        taggingModel.compile(loss=configuration['nn']['loss'],
                             optimizer=Network.getOptimizer('taggingLR'),
                             metrics=['accuracy'])
        if False and configuration['others']['verbose']:
            sys.stdout.write(str(taggingModel.summary()) + doubleSep)
        return taggingModel, sharedLayers

    @staticmethod
    def buildDepParsingModel(sharedLayers, classNum, vocab):
        depParsingLayers, depParsingDenseLayers = [], []
        # for i in ['b0', 's0', 's1']:
        for i in ['b0', 'b1', 'b2', 's0', 's1', 's2',
                  'LM1(S1)', 'LM2(S1)', 'LM1(S0)', 'LM2(S0)',
                  'RM1(S1)', 'RM2(S1)', 'RM1(S0)', 'RM2(S0)',
                  'LMLM(S1)', 'RMRM(S1)', 'LMLM(S0)', 'RMRM(S0)']:
            inputLayers, denseLayer = Builder.buildPosModule(sharedLayers, i)
            depParsingLayers += inputLayers
            depParsingDenseLayers.append(denseLayer)

        synLblInput = Input((12,), dtype='int32', name='SyntacticLabels')
        depParsingLayers = [synLblInput] + depParsingLayers  # .append(synLblInput)
        synLblEmb = Embedding(len(vocab.syntacticLabelIndices), mtParams['sytacticLabelDim'],
                              name='SyntacticLabelEmb')(synLblInput)
        synLblFlatten = Flatten()(synLblEmb)
        depParsingDenseLayers = [synLblFlatten] + depParsingDenseLayers
        # depParsingDenseLayers.append(synLblFlatten)

        concDense = keras.layers.concatenate(depParsingDenseLayers)
        depParsingDense = Dense(mtParams['depParsingDenseUnits'],
                                activation='relu',
                                name='depParsingDense')(concDense)
        depParsingSoftmax = Dense(classNum, activation='softmax', name='depParsingSoftMax')(depParsingDense)
        depParsingModel = Model(inputs=depParsingLayers, outputs=depParsingSoftmax)
        depParsingModel.compile(loss=configuration['nn']['loss'],
                                optimizer=Network.getOptimizer('depParsingLR'),
                                metrics=['accuracy'])

        if configuration['others']['verbose']:
            sys.stdout.write(str(depParsingModel.summary()) + doubleSep)
        return depParsingModel

    @staticmethod
    def buildIdenModel(sharedLayers):
        idenInputLayers, idenDenseLayers = [], []
        focusedElements = ['b0', 's0', 's1']
        if mtParams['useB1']:
            focusedElements = ['b1'] + focusedElements
        if mtParams['useBx']:
            focusedElements = ['bx'] + focusedElements
        for i in focusedElements:
            inputLayers, denseLayer = Builder.buildPosModule(sharedLayers, i)
            idenInputLayers += inputLayers
            idenDenseLayers.append(denseLayer)

        concDense = keras.layers.concatenate(idenDenseLayers)
        idenDense = Dense(mtParams['idenDenseUnits'], activation='relu', name='idenDense')(
            concDense)
        idenSoftmax = Dense(4, activation='softmax', name='idenSoftMax')(idenDense)
        idenModel = Model(inputs=idenInputLayers, outputs=idenSoftmax)
        idenModel.compile(loss=configuration['nn']['loss'],
                          optimizer=Network.getOptimizer('idenLR'),
                          metrics=['accuracy'])

        if False and configuration['others']['verbose']:
            sys.stdout.write(str(idenModel.summary()) + doubleSep)
        return idenModel

    @staticmethod
    def buildPosModule(sharedLayers, title):
        inputSize, tokenEmb = mtParams['windowSize'] * 2 + 1, \
                              mtParams['tokenDim']
        inputToks = Input((inputSize,), dtype='int32', name=title + 'Tokens')
        inputAffixe = Input((12,), dtype='int32', name=title + 'Affixes')
        inputLayers = [inputToks, inputAffixe]
        taggingTokEmb = sharedLayers[1](inputToks)
        taggingFlatten = Flatten()(taggingTokEmb)
        taggingAffixeEmb = sharedLayers[2](inputAffixe)
        taggingAffixeFlatten = Flatten()(taggingAffixeEmb)
        concFlatten = [taggingFlatten, taggingAffixeFlatten]
        if mtParams['useCapitalization']:
            inputCapital = Input((3,), dtype='int32', name=title + 'Capitalization')
            inputLayers.append(inputCapital)
            capitalEmb = sharedLayers[3](inputCapital)
            capitalFlatten = Flatten()(capitalEmb)
            concFlatten.append(capitalFlatten)
        if mtParams['useSymbols']:
            inputSymbol = Input((1,), dtype='int32', name=title + 'Symbols')
            inputLayers.append(inputSymbol)
            symbolEmb = sharedLayers[-1](inputSymbol)
            symbolFlatten = Flatten()(symbolEmb)
            concFlatten.append(symbolFlatten)
        concFlatten = keras.layers.concatenate(concFlatten)
        taggingDense = sharedLayers[0](concFlatten)
        return inputLayers, taggingDense

    @staticmethod
    def addCapitalizationLayer(inputLayers, concFlatten, sharedLayers):
        sharedCapitalEmb = Embedding(4, mtParams['capitalDim'], name='capitalizationEmb')
        if mtParams['useCapitalization']:
            inputCapital = Input((3,), dtype='int32', name='capitalization')
            inputLayers.append(inputCapital)
            capitalEmb = sharedCapitalEmb(inputCapital)
            capitalFlatten = Flatten()(capitalEmb)
            concFlatten.append(capitalFlatten)
            sharedLayers.append(sharedCapitalEmb)

    @staticmethod
    def addSymbolLayer(inputLayers, concFlatten, sharedLayers):
        sharedSymbolEmb = Embedding(20, mtParams['symbolDim'], name='symbolsEmb')
        if mtParams['useSymbols']:
            inputSymbol = Input((1,), dtype='int32', name='symbol')
            inputLayers.append(inputSymbol)
            symbolEmb = sharedSymbolEmb(inputSymbol)
            symbolFlatten = Flatten()(symbolEmb)
            concFlatten.append(symbolFlatten)
            sharedLayers.append(sharedSymbolEmb)


class DataFactory:
    @staticmethod
    def getIdenTransData(trans):
        focusedElems = [[trans.configuration.reduced]] if mtParams['useBx'] else []
        if mtParams['useB1']:
            focusedElems.append([trans.configuration.buffer[1]] if len(trans.configuration.buffer) > 1 else [None])
        focusedElems.append([trans.configuration.buffer[0]] if len(trans.configuration.buffer) > 0 else [None])
        focusedElems.append(
            getTokens(trans.configuration.stack[-1]) if len(trans.configuration.stack) > 0 else [None])
        focusedElems.append(
            getTokens(trans.configuration.stack[-2]) if len(trans.configuration.stack) > 1 else [None])
        return focusedElems

    @staticmethod
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
        dataDivision = [2 * mtParams['windowSize'] + 1, 12]
        if mtParams['useCapitalization']:
            dataDivision.append(3)
        if mtParams['useSymbols']:
            dataDivision.append(1)

        dataDivision = dataDivision * (3 + (1 if mtParams['useB1'] else 0) +
                                       (1 if mtParams['useBx'] else 0))
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

    @staticmethod
    def getValidationData(data, labels):
        validationData = []
        for dataTensor in data:
            validationData.append(dataTensor[int(len(dataTensor) * (1 - configuration['nn']['validationSplit'])):])
        validationLabel = labels[int(len(labels) * (1 - configuration['nn']['validationSplit'])):]
        return validationData, validationLabel

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def getCapitalizationInfo(tokens, s):
        txts = DataFactory.getContextTexts(tokens, s)
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

    @staticmethod
    def padSequence(seq, label, emptyIdx):
        padConf = configuration['mlpNonLexicl']
        return np.asarray(pad_sequences([seq], maxlen=padConf[label], value=emptyIdx))[0]

    @staticmethod
    def addTokenTaggingEntries(token, sent, dataEntry, vocab):
        if token and isinstance(token, Token) and token.getTokenOrLemma() in vocab.tokenIndices:
            taggingEntries = vocab.getTaggingEntry([token], sent)
            for j in range(len(taggingEntries) - 1):
                dataEntry.append(taggingEntries[j])
                # dataEntry.append(vocab[sent.tokens[b0].getTokenOrLemma()])
        else:
            if not token:
                taggingEntries = vocab.getTaggingEntry(['empty'], sent)
                for j in range(len(taggingEntries) - 1):
                    dataEntry.append(taggingEntries[j])
            else:
                taggingEntries = vocab.getTaggingEntry([token], sent)
                for j in range(len(taggingEntries) - 1):
                    dataEntry.append(taggingEntries[j])


class SynDataFactory(object):
    @staticmethod
    def getData(corpus, vocabulary, train=True):
        """
        Create the training example in the libsvm format and write it to the input_file.
        Reference : Page 32, Chapter 3. Dependency Parsing by Sandra Kubler, Ryan McDonal and Joakim Nivre (2009)
        """
        transParser = TransitionParser(TransitionParser.ARC_STANDARD)
        transition = Transition(transParser.ARC_STANDARD)
        count_proj = 0
        data, labels, labelDic = [[] for _ in range(depParserInuptArrNum)], [], dict()
        sents = corpus.allTrainingSents if train else corpus.testingSents
        depGraphs = corpus.trainDepGraphs if train else corpus.testDepGraphs
        for i in range(len(sents)):
            depgraph = depGraphs[i]
            sent = sents[i]
            if not transParser._is_projective(depgraph):
                continue
            count_proj += 1
            conf = Configuration(depgraph)
            while len(conf.buffer) > 0:
                dataEntry = SynDataFactory.getDataEntry(conf, sent, vocabulary)
                for i in range(depParserInuptArrNum):
                    data[i].append(dataEntry[i])
                # SynDataFactory.printDataEntry(dataEntry, vocabulary, conf, sent)
                b0 = conf.buffer[0]
                if len(conf.stack) > 0:
                    s0 = conf.stack[len(conf.stack) - 1]
                    # Left-arc operation
                    rel = transParser._get_dep_relation(b0, s0, depgraph)
                    if rel is not None:
                        if conf.stack[-1] - 1 >= 0 and conf.buffer[0] - 1 >= 0:
                            sent.tokens[conf.stack[-1] - 1].predictedDepParent = sent.tokens[conf.buffer[0] - 1]
                            sent.tokens[conf.stack[-1] - 1].predictedDepLabel = rel
                        key = Transition.LEFT_ARC + ':' + rel
                        if key not in labelDic:
                            labelDic[key] = len(labelDic)
                        transition.left_arc(conf, rel)
                        # print 'LEFT_ARC'
                        labels.append(labelDic[key])
                        continue
                    # Right-arc operation
                    rel = transParser._get_dep_relation(s0, b0, depgraph)
                    if rel is not None:
                        precondition = True
                        # Get the max-index of buffer
                        maxID = conf._max_address
                        for w in range(maxID + 1):
                            if w != b0:
                                relw = transParser._get_dep_relation(b0, w, depgraph)
                                if relw is not None:
                                    if (b0, relw, w) not in conf.arcs:
                                        precondition = False
                        if precondition:
                            key = Transition.RIGHT_ARC + ':' + rel
                            if conf.stack[-1] - 1 >= 0 and conf.buffer[0] - 1 >= 0:
                                sent.tokens[conf.buffer[0] - 1].predictedDepParent = sent.tokens[conf.stack[-1] - 1]
                            else:
                                sent.tokens[conf.buffer[0] - 1].predictedDepParent = None
                            if conf.buffer[0] - 1 >= 0:
                                sent.tokens[conf.buffer[0] - 1].predictedDepLabel = rel
                            transition.right_arc(conf, rel)
                            # print 'RIGHT_ARC'
                            if key not in labelDic:
                                labelDic[key] = len(labelDic)
                            labels.append(labelDic[key])
                            continue
                # Shift operation as the default
                key = Transition.SHIFT
                if key not in labelDic:
                    labelDic[key] = len(labelDic)
                transition.shift(conf)
                # print 'SHIFT'
                labels.append(labelDic[key])

        exNum = len(corpus.trainDepGraphs) if train else len(corpus.testDepGraphs)
        print(" Number of {0} examples : {1}".format('training' if train else 'evaluation', exNum))
        print(" Number of projective examples : " + str(count_proj))
        return [np.asarray(d) for d in data], labels, labelDic

    @staticmethod
    def getDataEntry(conf, sent, vocab):
        dataEntry = [[]]
        SynDataFactory.getBufferTokens(conf, sent, vocab, dataEntry)
        SynDataFactory.getStackTokens(conf, sent, vocab, dataEntry)
        SynDataFactory.getStackLeftMosts(conf, sent, vocab, dataEntry)
        SynDataFactory.getStackRightMosts(conf, sent, vocab, dataEntry)
        SynDataFactory.getStackLeftAndRightMostOfLeftAndRightMosts(conf, sent, vocab, dataEntry)
        return dataEntry

    @staticmethod
    def getStackLeftMosts(conf, sent, vocab, dataEntry):
        syntacticLabels = []
        for i in range(2):
            if len(conf.stack) >= 2 - i:
                if conf.stack[i - 2] > 0:
                    si = sent.tokens[conf.stack[i - 2] - 1]
                    leftMostChildren = SynDataFactory.getLeftMostChildren(si, sent)
                    for t in leftMostChildren[:2]:
                        SynDataFactory.addAllIdxs(t, sent, vocab, dataEntry)
                    for _ in range(2 - len(leftMostChildren)):
                        SynDataFactory.addAllIdxs(None, sent, vocab, dataEntry)
                else:
                    SynDataFactory.addAllIdxs(None, sent, vocab, dataEntry)
                    SynDataFactory.addAllIdxs(None, sent, vocab, dataEntry)
            else:
                SynDataFactory.addAllIdxs(None, sent, vocab, dataEntry)
                SynDataFactory.addAllIdxs(None, sent, vocab, dataEntry)
        return syntacticLabels

    @staticmethod
    def getStackRightMosts(conf, sent, vocab, dataEntry):
        for i in range(2):
            if len(conf.stack) >= 2 - i:
                if conf.stack[i - 2] > 0:
                    si = sent.tokens[conf.stack[i - 2] - 1]
                    rightMostChildren = SynDataFactory.getRightMostChildren(si, sent)
                    for t in rightMostChildren[:2]:
                        SynDataFactory.addAllIdxs(t, sent, vocab, dataEntry)
                    for _ in range(2 - len(rightMostChildren)):
                        SynDataFactory.addAllIdxs(None, sent, vocab, dataEntry)
                else:
                    SynDataFactory.addAllIdxs(None, sent, vocab, dataEntry)
                    SynDataFactory.addAllIdxs(None, sent, vocab, dataEntry)
            else:
                SynDataFactory.addAllIdxs(None, sent, vocab, dataEntry)
                SynDataFactory.addAllIdxs(None, sent, vocab, dataEntry)

    @staticmethod
    def getStackLeftAndRightMostOfLeftAndRightMosts(conf, sent, vocab, dataEntry):
        for i in range(2):
            if len(conf.stack) >= 2 - i and conf.stack[i - 2] > 0:
                si = sent.tokens[conf.stack[i - 2] - 1]
                leftMostOfLeftMostChild = SynDataFactory.getLeftMostOfLeftMostChildren(si, sent)
                SynDataFactory.addAllIdxs(leftMostOfLeftMostChild, sent, vocab, dataEntry)
                rightMostOfRightMostChild = SynDataFactory.getRightMostOfRightMostChildren(si, sent)
                SynDataFactory.addAllIdxs(rightMostOfRightMostChild, sent, vocab, dataEntry)
            else:
                SynDataFactory.addAllIdxs(None, sent, vocab, dataEntry)
                SynDataFactory.addAllIdxs(None, sent, vocab, dataEntry)

    @staticmethod
    def getLeftMostChildren(token, sent):
        leftMostChildren = []
        if token.position - 1 > 0:
            for t in sent.tokens[:token.position - 1]:
                if t.predictedDepParent and t.predictedDepParent.position == token.position:
                    leftMostChildren.append(t)
        return leftMostChildren

    @staticmethod
    def getLeftMostOfLeftMostChildren(token, sent):
        leftMostChildren = SynDataFactory.getLeftMostChildren(token, sent)

        if leftMostChildren:
            leftMostOfLeftMost = SynDataFactory.getLeftMostChildren(leftMostChildren[0], sent)
            if leftMostOfLeftMost:
                return leftMostOfLeftMost[0]
        return None

    @staticmethod
    def getRightMostOfRightMostChildren(token, sent):
        rightMostChildren = SynDataFactory.getRightMostChildren(token, sent)
        if rightMostChildren:
            rightMostOfRightMost = SynDataFactory.getRightMostChildren(rightMostChildren[0], sent)
            if rightMostOfRightMost:
                return rightMostOfRightMost[0]
        return None

    @staticmethod
    def getRightMostChildren(token, sent):
        rightMostChildren = []
        for t in reversed(sent.tokens[token.position:]):
            if t.predictedDepParent and t.predictedDepParent.position == token.position:
                rightMostChildren.append(t)
        return rightMostChildren

    @staticmethod
    def addAllIdxs(t, sent, vocab, dataEntry):
        DataFactory.addTokenTaggingEntries(t, sent, dataEntry, vocab)
        SynDataFactory.addSynLabelIdx(t, vocab, dataEntry)

    @staticmethod
    def addSynLabelIdx(t, vocab, dataEntry):
        if t is not None:
            if t == 'root':
                dataEntry[0].append(vocab.syntacticLabelIndices['root'])
            elif t.predictedDepLabel.lower() in vocab.syntacticLabelIndices:
                dataEntry[0].append(vocab.syntacticLabelIndices[t.predictedDepLabel.lower()])
            else:
                dataEntry[0].append(vocab.syntacticLabelIndices[unk])
        else:
            dataEntry[0].append(vocab.syntacticLabelIndices[empty])

    @staticmethod
    def getBufferTokens(conf, sent, vocab, dataEntry):
        for i in range(3):
            if i < len(conf.buffer):
                bi = conf.buffer[i] - 1
                if bi >= 0 and bi < len(sent.tokens):
                    biToken = sent.tokens[bi]
                    DataFactory.addTokenTaggingEntries(biToken, sent, dataEntry, vocab)
                else:
                    DataFactory.addTokenTaggingEntries('root', sent, dataEntry, vocab)
            else:
                DataFactory.addTokenTaggingEntries(None, sent, dataEntry, vocab)

    @staticmethod
    def getStackTokens(conf, sent, vocab, dataEntry):
        for i in range(1, 4):
            if conf.stack and i <= len(conf.stack):
                si = conf.stack[-i] - 1
                if si == -1:
                    DataFactory.addTokenTaggingEntries('root', sent, dataEntry, vocab)
                else:
                    siToken = sent.tokens[si]
                    DataFactory.addTokenTaggingEntries(siToken, sent, dataEntry, vocab)
            else:
                DataFactory.addTokenTaggingEntries(None, sent, dataEntry, vocab)

    @staticmethod
    def getSyntacticLabelIndice(t, vocab):
        if t:
            k = t.predictedDepLabel.lower()
            if k in vocab:
                return vocab[k]
            return vocab[unk]
        return vocab[empty]
