import random

from keras.callbacks import EarlyStopping
from keras.layers import Input, Dense
from keras.models import Model
from keras.utils import to_categorical
import numpy as np
input1 = Input((1,))
input2 = Input((1,))
taggingDense = Dense(50, activation='relu')

dense1 = taggingDense(input1)
dense2 = taggingDense(input2)

softmax1 = Dense(5, activation='softmax')(dense1)
softmax2 = Dense(6, activation='softmax')(dense2)

model1 = Model(inputs=input1, outputs=softmax1)
model2 = Model(inputs=input2, outputs=softmax2)

model1.compile(loss='categorical_crossentropy',
               optimizer='adagrad',
               metrics=['accuracy'])
model2.compile(loss='categorical_crossentropy',
               optimizer='adagrad',
               metrics=['accuracy'])

print model1.summary()

print model2.summary()

data1 = [random.randint(0, 4) for _ in range(2000)]
label1 = data1
label1 = to_categorical(label1, num_classes=5)

data2 = [random.randint(0, 5) for _ in range(8000)]
label2 = data2
label2 = to_categorical(label2, num_classes=6)

model1.fit(data1, label1,
           validation_split=.2,
           epochs=100,
           batch_size=8,
           verbose=2,
           callbacks=[EarlyStopping(monitor='val_loss',
                                    min_delta=.2,
                                    patience=2,
                                    verbose=2)])
model2.fit(data2, label2,
           validation_split=.2,
           epochs=100,
           batch_size=8,
           verbose=2,
            callbacks=[EarlyStopping(monitor='val_loss',
                                       min_delta=.2,
                                       patience=2,
                                       verbose=2)])

m1P, m2P = 0, 0
for _ in range(100):
    x = random.randint(0, 4)
    props = model1.predict([x],batch_size=1)
    # print 'm1: ', x, np.where(props[0] == max(props[0]))
    if x == int(np.where(props[0] == max(props[0]))[0]):
        m1P += 1
    x = random.randint(0, 5)
    props = model2.predict([x], batch_size=1)
    # print 'm2: ', x, np.where(props[0] == max(props[0]))
    if x == int(np.where(props[0] == max(props[0]))[0]):
        m2P += 1
print 'P1: ', round(m1P/100.,2)
print 'P2: ', round(m2P/100.,2)