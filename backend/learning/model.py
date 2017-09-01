from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.utils.data_utils import get_file
import keras
import numpy as np
import random
import sys
import os

time_num = 5000
case_num = 512

def train_text_to_arr(time_num, case_num):
    melody_fd = open('../preprocessing/melody_train.txt')
    melody_txt = melody_fd.read()
    melody = melody_txt.split(' ')[:-1]
    melody_fd.close()

    drum_fd = open('../preprocessing/drum_train.txt')
    drum_txt = drum_fd.read()
    drum = drum_txt.split(' ')[:-1]
    drum_fd.close()

    if len(drum) != len(melody):
        print('train file has the problem')

    song_start = []
    song_end = []
    print('trying to count song num...')
    for i in range(len(melody)):
        if melody[i] == 'start':
            song_start.append(i)
        if melody[i] == 'end':
            song_end.append(i)
    song_num = len(song_start)
    print('train song num : {}'.format(song_num))

    x_train_data = None
    y_train_data = None
    for i in range(song_num):
        length = song_end[i] - song_start[i] - 1
        x_train = np.zeros((1, time_num, case_num), dtype=np.bool)    
        y_train = np.zeros((1, time_num, case_num), dtype=np.bool)
        
        word_index = song_start[i]
        for j in range(5000):
            word_index += 1
            if word_index < song_end[i]:
                # melody part
                case_num_index = int(melody[word_index])
                x_train[0][j][case_num_index] = 1
                
                # drum part
                case_num_index = 0
                for char_index, char in enumerate(drum[word_index]):
                    if char == '1':
                        case_num_index += 2 ** (8-char_index)
                y_train[0][j][case_num_index] = 1
            else:
                x_train[0][j][0] = 1
                y_train[0][j][0] = 1
        
        if type(x_train_data) != type(x_train):
            x_train_data = x_train
            y_train_data = y_train
        else:
            x_train_data = np.append(x_train_data, x_train, axis=0)
            y_train_data = np.append(y_train_data, y_train, axis=0)

    return x_train_data, y_train_data, song_num

def pred_to_drum_track():
    pass

def get_model(song_num, time_num, case_num, x_train, y_train):

    model = Sequential()
    model.add(LSTM(song_num, return_sequences=True, input_shape=(time_num, case_num)))
    model.add(Dropout(0.2))
    model.add(LSTM(song_num, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(Dense(case_num))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    x_test = np.zeros((1, time_num, case_num), dtype=np.bool)

    result = model.fit(x_train, y_train, batch_size=10, nb_epoch=10)

    preds = model.predict(x_test, verbose=0)
    print(preds)
    print(preds.shape)

if __name__=='__main__':
    x_train, y_train, song_num = train_text_to_arr(time_num, case_num)
    get_model(song_num, time_num, case_num, x_train, y_train)