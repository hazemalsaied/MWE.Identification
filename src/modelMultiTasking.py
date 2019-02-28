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

import reports
from corpus import getRelevantModelAndNormalizer
from corpus import getTokens, getLemmaString
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
                history = self.taggingModel.fit(taggingData, taggingLbls, validation_split=.2,
                                                epochs=1,
                                                batch_size=taggingBatchSize, verbose=2)
                taggingLoss.append(history.history['loss'])
            else:
                history = self.idenModel.fit(idenData, idenLbls, validation_split=.2, epochs=1,
                                             batch_size=taggingBatchSize, verbose=2)
                idenLoss.append(history.history['loss'])
            # TODO check the early stopping

    def trainIden(self, corpus):
        idenBatchSize = 32
        idenData, idenLbls = self.getIdenData(corpus)
        # idenData, idenLbls = overSample(idenData, idenLbls)
        idenLbls = to_categorical(idenLbls, num_classes=4)
        self.idenModel.fit(idenData, idenLbls, validation_split=.2,
                           epochs=100,
                           batch_size=idenBatchSize, verbose=2, callbacks=[
                EarlyStopping(monitor='val_loss',
                              min_delta=configuration['nn']['minDelta'],
                              patience=configuration['nn']['patience'],
                              verbose=configuration['others']['verbose'])])

    def trainTagging(self, corpus):
        taggingBatchSize = 32
        taggingData, taggingLbls = self.getTaggingData(corpus)
        taggingLbls = to_categorical(taggingLbls, num_classes=len(self.vocabulary.posIndices))
        self.taggingModel.fit(taggingData, taggingLbls, validation_split=.2,
                              epochs=100,
                              batch_size=taggingBatchSize, verbose=2, callbacks=[
                EarlyStopping(monitor='val_loss',
                              min_delta=configuration['nn']['minDelta'],
                              patience=configuration['nn']['patience'],
                              verbose=configuration['others']['verbose'])])

    def testIden(self, corpus):
        IdenData, IdenLbls = self.getIdenData(corpus, train=False)
        IdenLbls = to_categorical(IdenLbls, num_classes=4)
        results = self.idenModel.evaluate(IdenData, IdenLbls, batch_size=32, verbose=0)
        sys.stdout.write('Loss = {0}, Accuracy = {1}'.format(round(results[0], 3), round(results[1] * 100, 1)))

    def testTagging(self, corpus):
        taggingData, taggingLbls = self.getTaggingData(corpus, train=False)
        taggingLbls = to_categorical(taggingLbls, num_classes=len(self.vocabulary.posIndices))
        results = self.taggingModel.evaluate(taggingData, taggingLbls, batch_size=32, verbose=0)
        sys.stdout.write('Loss = {0}, Accuracy = {1}'.format(round(results[0], 3), round(results[1] * 100, 1)))

    def getTaggingData(self, corpus, train=True):
        data1, data2, data3, data4, lbls = [], [], [], [], []
        for s in corpus.trainingSents if train else corpus.testingSents:
            for item in s.tokens + s.vMWEs:
                if not train and not configuration['multitasking']['testOnToken'] and \
                        str(item.__class__).endswith('corpus.Token'):
                    continue
                tokens = [item] if str(item.__class__).endswith('corpus.Token') else item.tokens
                d1, d2, d3, d4, lbl = self.getTaggingEntry(tokens, s)
                data1.append(np.asarray(d1))
                data2.append(np.asarray(d2))
                data3.append(np.asarray(d3))
                data4.append(np.asarray(d4))
                lbls.append(lbl)
        if configuration['multitasking']['useCapitalization'] and configuration['multitasking']['useSymbols']:
            return [np.asarray(data1), np.asarray(data2), np.asarray(data3), np.asarray(data4)], lbls
        if configuration['multitasking']['useCapitalization']:
            return [np.asarray(data1), np.asarray(data2), np.asarray(data3)], lbls
        if configuration['multitasking']['useSymbols']:
            return [np.asarray(data1), np.asarray(data2), np.asarray(data4)], lbls
        return [np.asarray(data1), np.asarray(data2)], lbls

    def getIdenData(self, corpus, train=True):
        labels, data = [], []  # , data = [], [[]] * 20
        for i in range(20):
            data.append([])
        for sent in corpus.trainingSents if train else corpus.testingSents:
            trans = sent.initialTransition
            while trans and trans.next:
                focusedElems = [[trans.configuration.reduced]]
                focusedElems.append([trans.configuration.buffer[1]] if len(trans.configuration.buffer) > 1 else [None])
                focusedElems.append([trans.configuration.buffer[0]] if len(trans.configuration.buffer) > 0 else [None])
                focusedElems.append(
                    getTokens(trans.configuration.stack[-1]) if len(trans.configuration.stack) > 0 else [None])
                focusedElems.append(
                    getTokens(trans.configuration.stack[-2]) if len(trans.configuration.stack) > 1 else [None])
                for i in range(len(focusedElems)):
                    taggingEntry = self.getTaggingEntry(focusedElems[i], sent)
                    for j in range(4):  # i*4, i*4 + 4):
                        data[i * 4 + j].append(np.asarray(taggingEntry[j]))
                labels.append(trans.next.type.value if trans.next.type.value <= 2 else 3)
                trans = trans.next
        for i in range(20):
            data[i] = np.asarray(data[i])
        return data, labels

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
        if tokens == [None]:
            return [self.vocabulary.tokenIndices[unk]] * (configuration['multitasking']['windowSize'] * 2 + 1), \
                   [self.vocabulary.affixeIndices[unk]] * 12, \
                   [2] * 3, [0], self.vocabulary.posIndices[unk]
        tokenIdxs = self.getTokenIdxs(tokens, s)
        affixes = self.getAffixeIndices(tokens, s)
        capitalIdx = getCapitalizationInfo(tokens, s)
        symbols = getSymbolInfo(tokens)
        attachedPos = '_'.join(t.posTag.lower() for t in tokens)
        posIdx = self.vocabulary.posIndices[attachedPos.lower() if attachedPos in self.vocabulary.posIndices else unk]
        return tokenIdxs, affixes, capitalIdx, symbols, posIdx

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
    inputSize, parsingInfoDim, tokenEmb = configuration['multitasking']['windowSize'] * 2 + 1, 1000, \
                                          configuration['multitasking']['tokenDim']
    affixeEmb = configuration['multitasking']['affixeDim']
    inputToks = Input((inputSize,), dtype='int32', name='tokens')
    inputAffixe = Input((12,), dtype='int32', name='affixes')
    inputLayers = [inputToks, inputAffixe]
    sharedTokEmb = Embedding(len(vocab.tokenIndices), tokenEmb, name='tokenEmb')
    sharedAffixeEmb = Embedding(len(vocab.affixeIndices), affixeEmb, name='affixeseEmb')

    taggingTokEmb = sharedTokEmb(inputToks)
    taggingFlatten = Flatten()(taggingTokEmb)
    taggingAffixeEmb = sharedAffixeEmb(inputAffixe)
    taggingAffixeFlatten = Flatten()(taggingAffixeEmb)
    concFlatten = [taggingFlatten, taggingAffixeFlatten]
    sharedCapitalEmb = Embedding(4, configuration['multitasking']['capitalDim'], name='capitalizationEmb')
    sharedSymbolEmb = Embedding(20, configuration['multitasking']['symbolDim'], name='symbolsEmb')
    sharedLayers = [sharedTokEmb, sharedAffixeEmb]
    if configuration['multitasking']['useCapitalization']:
        inputCapital = Input((3,), dtype='int32', name='capitalization')
        inputLayers.append(inputCapital)
        capitalEmb = sharedCapitalEmb(inputCapital)
        capitalFlatten = Flatten()(capitalEmb)
        concFlatten.append(capitalFlatten)
        sharedLayers.append(sharedCapitalEmb)
    if configuration['multitasking']['useSymbols']:
        inputSymbol = Input((1,), dtype='int32', name='symbol')
        inputLayers.append(inputSymbol)
        symbolEmb = sharedSymbolEmb(inputSymbol)
        symbolFlatten = Flatten()(symbolEmb)
        concFlatten.append(symbolFlatten)
        sharedLayers.append(sharedSymbolEmb)
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
    idenInputLayers, idenDenseLayers = [], []
    for i in ['bx', 'b1', 'b0', 's0', 's1']:
        inputLayers, denseLayer = createPosModule(sharedLayers, i)
        idenInputLayers += inputLayers
        idenDenseLayers.append(denseLayer)

    concDense = keras.layers.concatenate(idenDenseLayers)
    idenDense = Dense(500, activation='relu', name='idenDense')(concDense)
    idenSoftmax = Dense(4, activation='softmax', name='idenSoftMax')(idenDense)
    idenModel = Model(inputs=idenInputLayers, outputs=idenSoftmax)
    idenModel.compile(loss=configuration['nn']['loss'],
                      optimizer=getOptimizer(),
                      metrics=['accuracy'])

    if configuration['others']['verbose']:
        sys.stdout.write(str(idenModel.summary()) + doubleSep)
    return taggingModel, idenModel


def createPosModule(sharedLayers, title):
    inputSize, parsingInfoDim, tokenEmb = configuration['multitasking']['windowSize'] * 2 + 1, 1000, \
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
            EarlyStopping(monitor='val_loss', min_delta=configuration['nn']['minDelta'],
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
        self.affixeDic = self.getAffixeDic(corpus)
        self.affixeIndices = indexateDic(self.affixeDic)
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


def overSample(idenData, idenLbls):
    newIdenData = []
    for i in range(len(idenData[0])):
        newIdenDataEntry = []
        for j in range(20):
            newIdenDataEntry += list(idenData[j][i])
        newIdenData.append(newIdenDataEntry)
    ros = RandomOverSampler(random_state=0)
    newIdenData, newIdenLbls = ros.fit_sample(newIdenData, idenLbls)
    idenData = []
    dataDivision = [2 * configuration['multitasking']['windowSize'] + 1, 12, 3, 1] * 5
    for i in range(20):
        idenData.append([])
    for i in range(len(newIdenData)):
        for j in range(20):
            end = sum(dataDivision[:j + 1])
            start = end - dataDivision[j]
            idenData[j].append(np.asarray(newIdenData[i][start:end]))
    for i in range(20):
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
