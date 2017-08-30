import os
import sys
import pretty_midi

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
        print 'wrong filename!'
        print usage
        exit()

    midi_data = pretty_midi.PrettyMIDI(file_name)
    insts = midi_data.instruments
    for i, inst_info in enumerate(insts):
        if not inst_info.is_drum:
            print 'index {} : {}'.format(i, inst_info)

def sample(file_name, indices):
    if os.path.exists(file_name) == False:
        print 'wrong filename!'
        print usage
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
    original_filenames = [f[:-12] + '.mid' for f in sample_filenames]

    for sample_name in sample_filenames:
        os.rename(sample_name, '../midi/'+sample_name)    
    for file_name in original_filenames:
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == '__main__':
    if os.path.exists('../midi/') == False:
            os.makedirs('../midi/')
    
    if len(sys.argv) < 2:
        print usage
        exit()

    if sys.argv[1] == 'c':
        if not sys.argv[2]:
            print usage
            exit()
        file_name = sys.argv[2]
        check(file_name)
        
    elif sys.argv[1] == 's':
        if not sys.argv[2] or not sys.argv[3]:
            print usage
            exit()
        file_name = sys.argv[2]
        indices = []
        for i in range(3, len(sys.argv)):
            indices.append(sys.argv[i])
        sample(file_name, indices)
        
    elif sys.argv[1] == 'm':
        move()

    else:
        print usage