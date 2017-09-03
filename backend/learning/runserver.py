import model
import pretty_midi
import numpy as np

separate_power = 32

def melody_midi_to_arr(file_name):
    midi_data = pretty_midi.PrettyMIDI(file_name)
    arr = np.zeros((1, model.time_num, model.case_num), dtype=np.bool)

    extracted_melody_dic = [0, 0]

    # melody select
    melody_inst = None
    for inst in midi_data.instruments:
        if not inst.is_drum :
            melody_inst = inst

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


if __name__ == '__main__':
    # download MIDI file from client using socket. 
    # save MIDI file with name as 'test.mid'

    midi_data_name = 'test.mid'
    
    arr, extracted_melody_dic = melody_midi_to_arr(midi_data_name)
    print('extracted_melody_dic result')
    print(extracted_melody_dic)

    pred = model.predict(arr)
    
    concat_arr_to_midi(midi_data_name, pred)

    # send 'test.mid' to client
    # os.remove(midi_data_name)
    