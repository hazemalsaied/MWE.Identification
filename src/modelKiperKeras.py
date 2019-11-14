from random import shuffle

import numpy as np
from keras.callbacks import EarlyStopping
from keras.layers import Input, Dense, Embedding, GRU, Flatten
from keras.models import Model
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.backend import gather
from corpus import getTokens
from reports import *
from vocabTools import empty
from vocabTools import unk, number

tokenNum = 100
vocabSize = 1000
tokenDim = 50
trainable = True
wordRnnUnitNum = 10
focusedElems = 8
dense1UnitNumber = 25
from keras.layers import Layer, Masking


class VectorMasking(Masking):
    def __init__(self, mask_value=0., **kwargs):
        super(VectorMasking, self).__init__(**kwargs)
        self.supports_masking = True
        self.mask_value = mask_value

    def compute_mask(self, inputs, mask=None):
        output_mask = K.any(K.not_equal(inputs, self.mask_value), axis=-1)
        return output_mask

    def call(self, inputs):
        boolean_mask = K.any(K.not_equal(inputs, self.mask_value),
                             axis=-1, keepdims=True)
        return inputs * K.cast(boolean_mask, K.dtype(inputs))

    def get_config(self):
        config = {'mask_value': self.mask_value}
        base_config = super(Masking, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

    def compute_output_shape(self, input_shape):
        return input_shape


from keras import backend as K


class DynamicSelection(Layer):
    """Layer that concatenates a list of inputs.
    It takes as input a list of tensors,
    all of the same shape except for the concatenation axis,
    and returns a single tensor, the concatenation of all inputs.
    # Arguments
        axis: Axis along which to concatenate.
        **kwargs: standard layer keyword arguments.
    """

    def __init__(self, **kwargs):
        super(DynamicSelection, self).__init__(**kwargs)

    def call(self, inputs, **kwargs):
        return gather(Flatten(inputs[0]), list(inputs[0]))
        # return inputs[0]
        # results = []
        # for idx in range(focusedElems):
        #     if inputs[1][idx] != -1:
        #         results.append(np.zeros(wordRnnUnitNum))
        #         # results = results + inputs[0][idx]
        #     else:
        #         # results = results + ([0] * wordRnnUnitNum)
        #         results.append(np.zeros(wordRnnUnitNum))
        #         # results.append(inputs[0][idx])
        # results = K.variable(value=np.asarray(results), dtype='float64')
        # return results  # K.concatenate(results) # results

    def compute_output_shape(self, input_shape):
        # return (None,wordRnnUnitNum)
        return (None, focusedElems * wordRnnUnitNum)
        # return (focusedElems, wordRnnUnitNum)


phraseMaxLength = 100


class Network:
    def __init__(self, corpus):
        self.tokenVocab, self.posVocab = corpus.toVocabulary()
        vocabSize = len(self.tokenVocab)
        self.model = Network.build()
        sys.stdout.write(str(self.model.summary()))
        self.train(corpus)

    @staticmethod
    def build():
        inputToken = Input((tokenNum,))
        embToken = Embedding(vocabSize, tokenDim, trainable=trainable)(inputToken)
        rnnLayer = GRU(wordRnnUnitNum, return_sequences=True, name='phraseRnn')(embToken)
        inputIdxs = Input((focusedElems,))
        # gatherLayer = gather(rnnLayer, inputIdxs)
        dynamicSelector = DynamicSelection()([rnnLayer, inputIdxs])
        # dynamicSelector = Flatten()(dynamicSelector)
        denseLayer = Dense(dense1UnitNumber, activation='relu')(dynamicSelector)
        # denseLayer = Dense(dense1UnitNumber, activation='relu')(gatherLayer)
        softmaxLayer = Dense(4, activation='softmax')(denseLayer)
        model = Model(inputs=[inputToken, inputIdxs], outputs=softmaxLayer)
        model.compile(loss=configuration['nn']['loss'], optimizer='adagrad', metrics=['accuracy'])
        return model

    def getIdxs(self, sent):
        tokenIdxs, POSIdxs = [], []
        for token in sent.tokens:
            isDigit = False
            for c in token.getTokenOrLemma():
                if c.isdigit():
                    isDigit = True
            if isDigit:
                tokenIdxs.append(self.tokenVocab[number])
            elif token.getTokenOrLemma() in self.tokenVocab:
                tokenIdxs.append(self.tokenVocab[token.getTokenOrLemma()])
            else:
                tokenIdxs.append(self.tokenVocab[unk])

            if token.posTag.lower() in self.posVocab:
                POSIdxs.append(self.posVocab[token.posTag.lower()])
            else:
                POSIdxs.append(self.posVocab[unk])
        return np.asarray(tokenIdxs), np.asarray(POSIdxs)

    def train(self, corpus):
        data, labels = self.getTrainData(corpus)
        labels = to_categorical(labels, 4)
        es = EarlyStopping(monitor='val_loss',
                           min_delta=configuration['nn']['minDelta'],
                           patience=configuration['nn']['patience'],
                           verbose=configuration['others']['verbose'])
        self.model.fit(data, labels,
                       validation_split=configuration['nn']['validationSplit'],
                       epochs=configuration['nn']['epochs'],
                       batch_size=configuration['mlp']['batchSize'],
                       verbose=2 if configuration['others']['verbose'] else 0,
                       callbacks=[es])

    def getTrainData(self, corpus, extendedVectors=False):
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
                goldT = 3 if trans.next.type.value > 2 else trans.next.type.value
                labels.append(goldT)
                tokenIdxs, posIdxs = self.getIdxs(sent)
                focusedIdxs = getFocusedElems(trans.configuration)
                tokenIdxs = np.asarray(pad_sequences([tokenIdxs], maxlen=phraseMaxLength,
                                                     value=self.tokenVocab[empty]))[0]
                posIdxs = np.asarray(pad_sequences([posIdxs], maxlen=phraseMaxLength,
                                                   value=self.posVocab[empty]))[0]
                data[0].append(tokenIdxs)
                data[1].append(posIdxs)
                if extendedVectors:
                    newFocusedIdxs = []
                    for t in sent.tokens:
                        if t.position in focusedIdxs:
                            newFocusedIdxs.append(np.ones(wordRnnUnitNum))
                        else:
                            newFocusedIdxs.append(np.zeros(wordRnnUnitNum))
                    newFocusedIdxs = newFocusedIdxs[:phraseMaxLength]
                    while len(newFocusedIdxs) < phraseMaxLength:
                        newFocusedIdxs.append(np.zeros(wordRnnUnitNum))
                    data[2].append(np.asarray(newFocusedIdxs))
                else:
                    data[2].append(focusedIdxs)
                if configuration['kiperwasser']['sampling'] and trans.isImportantTrans() \
                        and transNum < configuration['kiperwasser']['samplingTaux']:
                    transNum += 1
                else:
                    trans = trans.next
        return [data[0], data[2]], labels
        # return data, labels


# def getFocusedElemsAsVectors(config, sent):
#     idxs = []
#     if config.stack and len(config.stack) > 1:
#         for t in getTokens(config.stack[-2])[:2]:
#             idxs.append(t.position)
#     while len(idxs) < 2:
#         idxs = idxs + [-1]
#
#     if config.stack:
#         for t in getTokens(config.stack[-1])[:4]:
#             idxs.append(t.position)
#     while len(idxs) < 6:
#         idxs = idxs + [-1]
#
#     if config.buffer:
#         for t in config.buffer[:2]:
#             idxs.append(t.position)
#
#     while len(idxs) < 8:
#         idxs = idxs + [-1]
#     for t in sent.tokens:
#         if t.position
#     return idxs


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
