import model
import pretty_midi
import numpy as np

separate_power = 32

def melody_midi_to_arr(file_name):
    midi_data = pretty_midi.PrettyMIDI(file_name)
    arr = np.zeros((1, model.time_num, model.case_num), dtype=np.bool)

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
                return arr

            for note in melody_inst.notes:
                if (note.start >= part[time_i]) and (note.start <= part[time_i+1]) and (note.pitch<min_pitch):
                    check = True
                    min_pitch = note.pitch
                    
            if check:
                arr[0][i*separate_power+time_i][min_pitch] = 1

    return arr


def concat_arr_to_midi(file_name, arr):
    pass


if __name__ == '__main__':
    # download MIDI file from client using socket. 
    # save MIDI file with name as 'test.mid'

    midi_data_name = 'test.mid'
    arr = melody_midi_to_arr(midi_data_name)
    # pred = model.predict(arr)
    # concat_arr_to_midi(midi_data_name, pred)

    # send 'test.mid' to client
    # os.remove(midi_data_name)
    