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
import re

time_num = 2000
case_num = 512
batch_size = 10
nb_epoch = 20
loss = 'categorical_crossentropy'
optimizer = 'adam'

def train_text_to_arr(song_start, song_end, melody, drum):
    print('process text to ndarray')

    x_train_data = None
    y_train_data = None
    # range(len(song_start))
    for i in tqdm(range(len(song_start))):
        length = song_end[i] - song_start[i] - 1
        x_train = np.zeros((1, time_num, case_num), dtype=np.bool)    
        y_train = np.zeros((1, time_num, case_num), dtype=np.bool)

        melody_dic = {0:0, 1:0}
        drum_dic = {0:0}
        
        word_index = song_start[i]
        for j in range(time_num):
            word_index += 1
            if word_index < song_end[i]:
                # melody part
                case_num_index = int(melody[word_index])
                if case_num_index != 0:
                    x_train[0][j][1] = 1
                    melody_dic[1] += 1 
                else:
                    x_train[0][j][0] = 1
                    melody_dic[0] += 1 
                
                # drum part
                case_num_index = 0
                for char_index, char in enumerate(drum[word_index]):
                    if char == '1':
                        case_num_index += 2 ** (8-char_index)
                y_train[0][j][case_num_index] = 1
                if case_num_index in drum_dic:
                    drum_dic[case_num_index] += 1
                else:
                    drum_dic[case_num_index] = 1
            else:
                x_train[0][j][0] = 1
                y_train[0][j][0] = 1
                melody_dic[0] += 1 
                drum_dic[0] += 1

        print('train data arr result')
        melody_count = 0
        drum_count = 0
        for key in melody_dic:
            melody_count += melody_dic[key]
        for key in drum_dic:
            drum_count += drum_dic[key]
        print(melody_dic, melody_count)
        print(drum_dic, drum_count)
        
        if type(x_train_data) != type(x_train):
            x_train_data = x_train
            y_train_data = y_train
        else:
            x_train_data = np.append(x_train_data, x_train, axis=0)
            y_train_data = np.append(y_train_data, y_train, axis=0)

    return x_train_data, y_train_data

def pred_to_drum_track():
    pass

def get_model(song_num, x_train, y_train):
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

    dic = {}
    for i in range(0, time_num):
        time = preds[0][i]
        max_index = np.argmax(time)
        if max_index in dic:
            dic[max_index] += 1
        else:
            dic[max_index] = 1

        for j in range(0, case_num):
            if j == max_index:
                preds[0][i][j] = 1    
            else:
                preds[0][i][j] = 0
    print('predicted result')
    print(dic)
    return preds

def initial(drum_file_name):
    p = re.compile(r'\D*(?P<num>\d*)[.]txt')
    m = p.match(drum_file_name)
    num = m.group('num')
    print(num)

    melody_fd = open('./train/melody_train' + num + '.txt')
    melody_txt = melody_fd.read()
    melody = melody_txt.split(' ')[:-1]
    melody_fd.close()

    drum_fd = open(drum_file_name)
    drum_txt = drum_fd.read()
    drum = drum_txt.split(' ')[:-1]
    drum_fd.close()

    if len(drum) != len(melody):
        print(drum_file_name)
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

    return song_start, song_end, song_num, melody, drum


if __name__=='__main__':
    folder = './train/'
    drum_file_list = os.listdir(folder)
    drum_file_list = [f for f in drum_file_list if f.startswith('drum')]
    for f in tqdm(drum_file_list):    
        song_start, song_end, song_num, melody, drum = initial(folder + f)
        x_train, y_train = train_text_to_arr(song_start, song_end, melody, drum)

        print(x_train.shape)
        print('get x_train, y_train')
        if not os.path.exists('./model.json') or not os.path.exists('./model.h5'):
            print('start get_model')
            get_model(song_num, x_train, y_train)
            print('end get_model')
        else:
            print('start update_model')
            update_model(x_train, y_train)
            print('end update_model')