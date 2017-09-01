from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.utils.data_utils import get_file
import keras
import numpy as np
import random
import sys
import os

def get_model(song_num, time_num, case_num, drum_txt, melody_txt):

    model = Sequential()
    model.add(LSTM(song_num, return_sequences=True, input_shape=(time_num, case_num)))
    model.add(Dropout(0.2))
    model.add(LSTM(song_num, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(Dense(case_num))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    x_train = np.random.random((song_num, time_num, case_num))
    y_train = np.random.random((song_num, time_num, case_num))

    x_test = np.random.random((1, time_num, case_num))
    
    result = model.fit(x_train, y_train, batch_size=10, nb_epoch=1)

    preds = model.predict(x_test, verbose=0)
    print(preds)
    print(preds.shape)

if __name__=='__main__':
    get_model(100, 100, 100, '', '')