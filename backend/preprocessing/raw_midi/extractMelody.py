import os
import sys
import pretty_midi
from tqdm import tqdm

usage = '''
Usage
----------------------------------------------------------------------------------
python extractMelody.py c filename  # for check the program number of instruments
python extractMelody.py s filename indexnumber(can multi num) # make sample  
python extractMelody.py m filename # move extracted midi to ../midi
----------------------------------------------------------------------------------
'''
separate_power = 32

def check(file_name):
    if os.path.exists(file_name) == False:
        print('wrong filename!')
        print(usage)
        exit()

    midi_data = pretty_midi.PrettyMIDI(file_name)
    insts = midi_data.instruments
    for i, inst_info in enumerate(insts):
        if not inst_info.is_drum:
            print('index {} : {}'.format(i, inst_info))

def sample(file_name, indices):
    if os.path.exists(file_name) == False:
        print('wrong filename!')
        print(usage)
        exit()

    midi_data = pretty_midi.PrettyMIDI(file_name)
    extracted_melody = pretty_midi.PrettyMIDI()

    generated_melody = pretty_midi.Instrument(program=1) # Acoustic Grand Piano
    generated_melody.is_drum = False
    generated_melody.name = 'Melody'

    generated_durm = pretty_midi.Instrument(program=0) 
    generated_durm.is_drum = True
    generated_durm.name = 'Drum'

    for inst in midi_data.instruments:
        if inst.is_drum:
            notes = inst.notes
            for note in notes:
                generated_durm.notes.append(note)

    melody_inst = []
    for i in indices:
        melody_inst.append(midi_data.instruments[int(i)])

    for inst in melody_inst:
        notes = inst.notes
        for note in notes:
            generated_melody.notes.append(note)
        
    extracted_melody.instruments.append(generated_melody)
    extracted_melody.instruments.append(generated_durm)
    extracted_melody.write(file_name[:-4] + '_extract' + '.mid')

def move():
    filenames = os.listdir('.')
    sample_filenames = [f for f in filenames if f.endswith('_extract.mid')]
    # original_filenames = [f[:-12] + '.mid' for f in sample_filenames]

    for sample_name in sample_filenames:
        os.rename(sample_name, '../midi/'+sample_name)    
    # for file_name in original_filenames:
    #     if os.path.exists(file_name):
    #         os.remove(file_name)

def findMelody(midi_data):
    candidate = []
    instruments = midi_data.instruments
    for i in range(len(instruments)):
        if not instruments[i].is_drum:
            candidate.append([i, instruments[i], 0])

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
            for inst in candidate:
                for note in inst[1].notes:
                    if (note.start >= part[time_i]) and (note.start <= part[time_i+1]) and (note.pitch >= 30) and (note.pitch <= 80) :
                        inst[2] += 1
                        break
                        
        melody_part_index = None
        max_note_num = -1
        for inst in candidate:
            if max_note_num < inst[2]:
                melody_part_index = inst[0]
                max_note_num = inst[2]

    # for i, inst in enumerate(midi_data.instruments):
    #     print (i, inst)
    # print 'melody index: {}, note_num : {}'.format(melody_part_index, max_note_num)

    return melody_part_index


def auto_extract():
    file_list = os.listdir('.')
    file_list = [f for f in file_list if f.endswith('.mid')]

    if not os.path.exists('../midi'):
        os.makedirs('../midi/')

    for f in tqdm(file_list):
        try:
            midi_data = pretty_midi.PrettyMIDI(f)
            extracted_melody = pretty_midi.PrettyMIDI()

            generated_melody = pretty_midi.Instrument(program=1) # Acoustic Grand Piano
            generated_melody.is_drum = False
            generated_melody.name = 'Melody'

            generated_durm = pretty_midi.Instrument(program=0) 
            generated_durm.is_drum = True
            generated_durm.name = 'Drum'

            for inst in midi_data.instruments:
                if inst.is_drum:
                    notes = inst.notes
                    for note in notes:
                        generated_durm.notes.append(note)

            melody_inst_index = findMelody(midi_data)
            melody_inst = midi_data.instruments[melody_inst_index]
            notes = melody_inst.notes
            for note in notes:
                generated_melody.notes.append(note)
                
            extracted_melody.instruments.append(generated_melody)
            extracted_melody.instruments.append(generated_durm)
            extracted_melody.write('../midi/' + 'extract_' + f  + '.mid')
        except Exception as e:
            print(e)
            print(f + 'has error!')
            if os.path.exists('../midi/' + f + '_extract' + '.mid'):
                os.remove('../midi/' + f + '_extract' + '.mid')


if __name__ == '__main__':
    # if os.path.exists('../midi/') == False:
    #         os.makedirs('../midi/')
    
    # if len(sys.argv) < 2:
    #     print usage
    #     exit()

    # if sys.argv[1] == 'c':
    #     if not sys.argv[2]:
    #         print usage
    #         exit()
    #     file_name = sys.argv[2]
    #     check(file_name)
        
    # elif sys.argv[1] == 's':
    #     if not sys.argv[2] or not sys.argv[3]:
    #         print usage
    #         exit()
    #     file_name = sys.argv[2]
    #     indices = []
    #     for i in range(3, len(sys.argv)):
    #         indices.append(sys.argv[i])
    #     sample(file_name, indices)
        
    # elif sys.argv[1] == 'm':
    #     move()

    # else:
    #     print usage
    auto_extract()
    # move()