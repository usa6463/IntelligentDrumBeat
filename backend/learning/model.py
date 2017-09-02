from keras.models import Sequential, model_from_json
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.utils.data_utils import get_file
import keras
import numpy as np
import random
import sys
import os
from tqdm import tqdm

time_num = 10
case_num = 512
batch_size = 1
nb_epoch = 1
loss = 'categorical_crossentropy'
optimizer = 'adam'

def train_text_to_arr(time_num, case_num, song_start, song_end):
    print('process text to ndarray')

    x_train_data = None
    y_train_data = None
    for i in tqdm(range(len(song_start))):
        length = song_end[i] - song_start[i] - 1
        x_train = np.zeros((1, time_num, case_num), dtype=np.bool)    
        y_train = np.zeros((1, time_num, case_num), dtype=np.bool)
        
        word_index = song_start[i]
        for j in range(time_num):
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

    return x_train_data, y_train_data

def pred_to_drum_track():
    pass

def get_model(song_num, time_num, case_num, x_train, y_train):
    # function making new model
    model = Sequential()
    model.add(LSTM(song_num, return_sequences=True, input_shape=(time_num, case_num)))
    model.add(Dropout(0.2))
    model.add(LSTM(song_num, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(Dense(case_num))
    model.add(Activation('softmax'))
    model.compile(loss=loss, optimizer=optimizer)

    result = model.fit(x_train, y_train, batch_size=batch_size, nb_epoch=nb_epoch)

    model_json = model.to_json()
    with open('model.json', 'w') as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights('model.h5')
    print('model saved')

def update_model(x_train, y_train):
    if not os.path.exists('./model.json') or not os.path.exists('./model.h5'):
        print('pleas make model first')
        exit()

    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights('model.h5')
    model.compile(loss=loss, optimizer=optimizer)
    print('model loaded')

    result = model.fit(x_train, y_train, batch_size=batch_size, nb_epoch=nb_epoch)
    model_json = model.to_json()
    with open('model.json', 'w') as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights('model.h5')
    print('model updated')


def predict(arr):
    if not os.path.exists('./model.json') or not os.path.exists('./model.h5'):
        print('pleas make model first')
        exit()

    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights('model.h5')
    model.compile(loss=loss, optimizer=optimizer)
    print('model loaded')

    print('predicting...')
    preds = model.predict(arr, verbose=0)

    for i in range(0, time_num):
        time = preds[0][i]
        max_index = np.argmax(time)
        for j in range(0, case_num):
            if j == max_index:
                preds[0][i][j] = 1    
            else:
                preds[0][i][j] = 0

    return preds

if __name__=='__main__':
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

    for i in range(0, song_num, 1):
        x_train, y_train = train_text_to_arr(time_num, case_num, song_start[i:i+1], song_end[i:i+1])
        print(x_train.shape)
        print('get x_train, y_train')
        if not os.path.exists('./model.json') or not os.path.exists('./model.h5'):
            print('start get_model')
            get_model(song_num, time_num, case_num, x_train, y_train)
        else:
            print('start update_model')
            update_model(x_train, y_train)