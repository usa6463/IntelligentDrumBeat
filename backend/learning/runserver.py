import model
import pretty_midi
import numpy as np
import socket
import time

separate_power = model.time_num

def concat_repeat(midi_data_name, arr):
    midi_data = pretty_midi.PrettyMIDI(midi_data_name)
    allowed_pitch = [36, 38, 42, 46, 41, 45, 48, 51, 49]
    generated_drum = pretty_midi.Instrument(program=0)
    generated_drum.is_drum = True

    for inst in midi_data.instruments:
        if inst.is_drum == True:
            inst.notes = []

    beats = midi_data.get_downbeats()
    for i in range(len(beats)-1):
        start = beats[i]
        end = beats[i+1]
        interval = float((end-start)) / separate_power
        
        part = []
        for j in range(separate_power):
            part.append(start)
            start += interval
        part.append(end)
        
        for time_i in range(len(part)-1):
            one_index = list(arr[i][time_i]).index(1)
            range_list = [8,7,6,5,4,3,2,1,0]
            for k in range_list:
                if one_index >= 2**k:
                    new_note = pretty_midi.Note(velocity=100,
                        pitch=allowed_pitch[8-k],
                        start=part[time_i],
                        end=part[time_i]+.3)
                    generated_drum.notes.append(new_note)
                    one_index -= 2**k

    midi_data.instruments.append(generated_drum)
    midi_data.write('test2.mid')


def separate(file_name):
    midi_data = pretty_midi.PrettyMIDI(file_name)
    arr = np.zeros((1, model.time_num, model.case_num), dtype=np.bool)

    # melody select
    melody_inst = None
    for inst in midi_data.instruments:
        if not inst.is_drum :
            melody_inst = inst

    beats = midi_data.get_downbeats()
    x_train = np.zeros((len(beats)-1, model.time_num, model.case_num), dtype=np.bool)

    pitch_sum = 0
    pitch_count = 0
    for note in melody_inst.notes:
        if note.pitch != '0':
            pitch_count += 1
            pitch_sum += note.pitch
    pitch_avg = (pitch_sum / pitch_count)
    pitch_low = pitch_avg - 6
    pitch_high = pitch_avg + 6
    
    for i in range(len(beats)-1): # bar
        start = beats[i]
        end = beats[i+1]
        interval = float((end-start)) / separate_power
        extracted_melody_dic = {0:0, 1:0, 2:0, 3:0}
        
        part = []
        for j in range(separate_power):
            part.append(start)
            start += interval
        part.append(end)
        
        for time_i in range(len(part)-1): # bar / 32
            # only 1 pitch allowed
            min_pitch = 200
            check = False

            for note in melody_inst.notes:
                if (note.start >= part[time_i]) and (note.start <= part[time_i+1]) and (note.pitch<min_pitch):
                    check = True
                    min_pitch = note.pitch

            if check:
                if min_pitch >= pitch_high :
                    x_train[0][j][3] = 1
                    extracted_melody_dic[3] += 1 
                elif min_pitch <= pitch_low:
                    x_train[0][j][1] = 1
                    extracted_melody_dic[1] += 1 
                else:
                    x_train[0][j][2] = 1
                    extracted_melody_dic[2] += 1 

                # x_train[i][time_i][1] = 1
                # extracted_melody_dic[1] += 1
            else:
                x_train[i][time_i][0] = 1
                extracted_melody_dic[0] += 1
        
        count = 0
        for key in extracted_melody_dic:
            count += extracted_melody_dic[key]
        print(str(i) + 'th ' + 'extracted melody')
        print(extracted_melody_dic, count)

    print('---------------------------------x_train shape----------------------------')
    print(x_train.shape)
    print(x_train)
    return x_train, len(beats)-1


def melody_midi_to_arr(file_name):
    midi_data = pretty_midi.PrettyMIDI(file_name)
    arr = np.zeros((1, model.time_num, model.case_num), dtype=np.bool)

    extracted_melody_dic = [0, 0]

    # melody select
    melody_inst = None
    for inst in midi_data.instruments:
        if not inst.is_drum :
            melody_inst = inst

    last_index = 0
    beats = midi_data.get_downbeats()
    for i in range(len(beats)-1):
        start = beats[i]
        end = beats[i+1]
        interval = float((end-start)) / separate_power
        
        part = []
        for j in range(separate_power):
            part.append(start)
            start += interval
        part.append(end)
        
        for time_i in range(len(part)-1):
            total_time_i = i*separate_power+time_i

            # only 1 pitch allowed
            min_pitch = 200
            check = False

            if total_time_i >= model.time_num:
                return arr, extracted_melody_dic

            for note in melody_inst.notes:
                if (note.start >= part[time_i]) and (note.start <= part[time_i+1]) and (note.pitch<min_pitch):
                    check = True
                    min_pitch = note.pitch
                    
            if check:
                arr[0][i*separate_power+time_i][1] = 1
                extracted_melody_dic[1] += 1
            else:
                arr[0][i*separate_power+time_i][0] = 1
                extracted_melody_dic[0] += 1
            last_index = i*separate_power+time_i

    for i in range(last_index+1, model.time_num):
        arr[0][i][0] = 1
        extracted_melody_dic[0] += 1

    return arr, extracted_melody_dic


def concat_arr_to_midi(midi_data_name, arr):
    midi_data = pretty_midi.PrettyMIDI(midi_data_name)
    allowed_pitch = [36, 38, 42, 46, 41, 45, 48, 51, 49]
    generated_drum = pretty_midi.Instrument(program=0)
    generated_drum.is_drum = True

    beats = midi_data.get_downbeats()
    for i in range(len(beats)-1):
        start = beats[i]
        end = beats[i+1]
        interval = float((end-start)) / separate_power
        
        part = []
        for j in range(separate_power):
            part.append(start)
            start += interval
        part.append(end)
        
        for time_i in range(len(part)-1):
            total_time_i = i*separate_power+time_i
            if total_time_i >= model.time_num:
                break
            one_index = list(arr[0][total_time_i]).index(1)
            range_list = [8,7,6,5,4,3,2,1,0]
            for k in range_list:
                if one_index >= 2**k:
                    new_note = pretty_midi.Note(velocity=100,
                        pitch=allowed_pitch[8-k],
                        start=part[time_i],
                        end=part[time_i]+.3)
                    generated_drum.notes.append(new_note)
                    one_index -= 2**k

    midi_data.instruments.append(generated_drum)
    midi_data.write('test_drum_added.mid')


def cutting(pred):
    for bar_i in range(len(pred)-1): # except last one
        current_bar = pred[bar_i]
        next_bar = pred[bar_i+1]
        
        current_dic = {}
        current_count = 0
        next_dic = {}
        next_count = 0

        for part in current_bar:
            index = list(part).index(1)
            if not index in current_dic:
                current_dic[index] = 1
            else:
                current_dic[index] += 1

            if index != 0:
                current_count += 1
        
        for part in next_bar:
            index = list(part).index(1)
            if not index in next_dic:
                next_dic[index] = 1
            else:
                next_dic[index] += 1

            if index != 0:
                next_count += 1

        current_key_list = list(current_dic.keys())
        next_key_list = list(next_dic.keys())

        if (current_key_list != next_key_list):
            pass
        elif current_count != next_count:
            pass
        else:
            print(str(bar_i+1) + ' th bar changed')
            next_bar = current_bar

if __name__ == '__main__':

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind( ('127.0.0.1', 9001))
    server_sock.listen(10)

    while True:
        client_sock, addr = server_sock.accept()
        data = client_sock.recv(200000)
        # print(data)
        f = open("test.mid",'wb');
        f.write(data);
        f.close();

        midi_data_name = 'test.mid'
        arr, bar_num = separate(midi_data_name)
        pred = model.predict(arr)
        cutting(pred)
        concat_repeat(midi_data_name, pred)

        f2 = open("./test2.mid", 'rb')
        print("Sending...")
        data2 = f2.read(200000)
        print(data2)
        client_sock.send(data2)
        f2.close();

        client_sock.close()

    
        # send 'test.mid' to client
        # os.remove(midi_data_name)
    