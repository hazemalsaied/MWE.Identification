from collections import Counter
from random import uniform

import keras
import numpy as np
import sys
from imblearn.over_sampling import RandomOverSampler
from keras.callbacks import EarlyStopping
from keras.layers import Input, Dense, Embedding, Flatten, GRU, TimeDistributed,    Dense, Dropout, LSTM
from keras.models import Model
from keras.utils import to_categorical
from keras.models import Sequential
import reports
import sampling
from config import configuration
from corpus import getTokens
from wordEmbLoader import unk, number, empty

concLayers = []
tokenVocabLength, posVocabLength = 100, 50
tokenEmb, posEmb = 50, 15
maxConfPadding = 10

# input shape: (nb_samples, timesteps, 10)
model = Sequential()
model.add(Input((10,))) # output shape: (nb_samples, timesteps, 10)
model.add(TimeDistributed(Dense(10))) # output shape: (nb_samples, timesteps, 10)
model.add(LSTM(10, return_sequences=True)) # output shape: (nb_samples, timesteps, 10)
model.add(TimeDistributed(Dense(5))) # output shape: (nb_samples, timesteps, 5)
model.add(LSTM(10, return_sequences=False)) # output shape: (nb_samples, 10))
# optimizer = RMSprop(lr=0.001,clipnorm=10)
model.compile(optimizer='sgd', loss='mse')

# model = Sequential()
# model.add(Input((3,)))
# model.add(Embedding(tokenVocabLength, tokenEmb))
# model.add(TimeDistributed(Dense(50)))
# model.add(GRU(50, return_sequences=True))
# model.add(Dense(4, activation='softmax'))


# # inputToken = Input((3,))
# sharedTokenLayer = Embedding(tokenVocabLength, tokenEmb)
# sharedDenseLayer = TimeDistributed(Dense(50))
# inputs, inters = [], []
# for i in range(maxConfPadding):
#     inputToken = Input((3,))
#     inputs.append(inputToken)
#     tmpTokenEmbLayer = sharedTokenLayer(inputToken)
#     tokenFlatten = Flatten()(tmpTokenEmbLayer)
#     tmpDenseLayer = sharedDenseLayer(tokenFlatten)
#     inters.append(tmpDenseLayer)
#
# inter = keras.layers.concatenate(inters) #, axis=0)
# rnnLayer = GRU(maxConfPadding, return_sequences=True)(inters)
# softmax = Dense(4, activation='softmax')(rnnLayer)
# model = Model(inputs=inputs, outputs=softmax)
# model.compile(loss='categorical_crossentropy',
#               optimizer='sgd',
#               metrics=['accuracy'])

sys.stdout.write(str(model.summary()))