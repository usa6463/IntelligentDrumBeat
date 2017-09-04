# -*-coding:utf-8 -*-
import os
import pretty_midi
from config import *
from tqdm import tqdm

separate_power = 16

def drum_text_to_midi(drum_dir, f, midi_dir):
    global separate_power

    for file_name in f:
        midi_data = pretty_midi.PrettyMIDI(midi_dir + '/' + file_name[:-4] + '.mid')
        extracted_drum = pretty_midi.PrettyMIDI()
        generated_drum = pretty_midi.Instrument(program=0)
        generated_drum.is_drum = True

        fd = open(drum_dir+file_name, 'r')
        txt = fd.read()
        txt_list = txt.split(' ')[1:-2]

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
                txt_part = txt_list[i*separate_power+time_i]
                for char_i in range(len(txt_part)):
                    if txt_part[char_i] == '1':
                        new_note = pretty_midi.Note(velocity=100,
                            pitch=allowed_pitch[char_i],
                            start=part[time_i],
                            end=part[time_i]+.3)
                        generated_drum.notes.append(new_note)

        extracted_drum.instruments.append(generated_drum)
        extracted_drum.write('test/' + file_name[:-4] + '_drum.mid')
        fd.close()

def melody_text_to_midi(melody_dir, f, midi_dir):
    global separate_power

    for file_name in f:
        midi_data = pretty_midi.PrettyMIDI(midi_dir + '/' + file_name[:-4] + '.mid')
        extracted_melody = pretty_midi.PrettyMIDI()
        generated_melody = pretty_midi.Instrument(program=1)
        generated_melody.is_drum = False

        fd = open(melody_dir+file_name, 'r')
        txt = fd.read()
        txt_list = txt.split(' ')[1:-2]

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
                txt_part = txt_list[i*separate_power+time_i]
                if txt_part != '0':
                    new_note = pretty_midi.Note(velocity=100,
                        pitch=int(txt_part),
                        start=part[time_i],
                        end=part[time_i]+.3)
                    generated_melody.notes.append(new_note)

        extracted_melody.instruments.append(generated_melody)
        extracted_melody.write('test/' + file_name[:-4] + '_melody.mid')
        fd.close()       

def extract_drum(midi_dir, f):
    global separate_power
    midi_data = pretty_midi.PrettyMIDI(midi_dir + '/' + f)
    extracted_drum = pretty_midi.PrettyMIDI()
    generated_drum = pretty_midi.Instrument(program=0)
    generated_drum.is_drum = True

    drums = []
    for inst in midi_data.instruments:
        if inst.is_drum:
            drums.append(inst)
    
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
            for drum in drums:
                for note in drum.notes:
                    if (note.start >= part[time_i]) and (note.start <= part[time_i+1]):
                        new_note = pretty_midi.Note(velocity=100,
                            pitch=note.pitch,
                            start=part[time_i],
                            end=part[time_i]+.3)
                        generated_drum.notes.append(new_note)

    extracted_drum.instruments.append(generated_drum)
    extracted_drum.write('drum/' + f[:-4] + '.mid')


def drum_midi_to_text(midi_dir, f, fd):
    global separate_power

    midi_data = pretty_midi.PrettyMIDI(midi_dir + '/' + f)

    extracted_drum = pretty_midi.PrettyMIDI()
    generated_drum = pretty_midi.Instrument(program=0)
    generated_drum.is_drum = True

    fd.write('start ')
    drums = []
    for inst in midi_data.instruments:
        if inst.is_drum:
            drums.append(inst)
    
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
            text = '000000000'
            note_list = []
            for drum in drums:
                for note in drum.notes:
                    if (note.start >= part[time_i]) and (note.start <= part[time_i+1]):
                        note_list.append(note.pitch)

            for pitch in note_list:
                if pitch in drum_conversion:
                    note_list.append(drum_conversion[pitch])
                    note_list.remove(pitch)
            note_list = set(note_list)
            for pitch in note_list:
                if pitch in allowed_pitch:
                    new_note = pretty_midi.Note(velocity=100,
                        pitch=pitch,
                        start=part[time_i],
                        end=part[time_i]+.3)
                    generated_drum.notes.append(new_note)
                    idx = allowed_pitch.index(pitch)
                    lst = list(text)
                    lst[idx] = '1'
                    text = ''.join(lst)
            fd.write(text + ' ')

    extracted_drum.instruments.append(generated_drum)
    extracted_drum.write('drum/' + f[:-4] + '.mid')
    fd.write('end ')


def extract_melody(midi_dir, f):
    global separate_power
    midi_data = pretty_midi.PrettyMIDI(midi_dir + '/' + f)
    extracted_melody = pretty_midi.PrettyMIDI()
    generated_melody = pretty_midi.Instrument(program=1) # Acoustic Grand Piano
    generated_melody.is_drum = False

    melody_inst = None
    for inst in midi_data.instruments:
        if not inst.is_drum :
            melody_inst = inst

    print (f, melody_inst.name, melody_inst.program)
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
            min_pitch = 200
            check = False
            for note in melody_inst.notes:
                if (note.start >= part[time_i]) and (note.start <= part[time_i+1]) and (note.pitch < min_pitch):
                    check = True
                    min_pitch = note.pitch
            if check:
                new_note = pretty_midi.Note(velocity=100,
                    pitch=min_pitch,
                    start=part[time_i],
                    end=part[time_i]+.3)
                generated_melody.notes.append(new_note)

    extracted_melody.instruments.append(generated_melody)
    extracted_melody.write('melody/' + f[:-4] + '.mid')


def melody_midi_to_text(midi_dir, f, fd):
    global separate_power
    midi_data = pretty_midi.PrettyMIDI(midi_dir + '/' + f)
    extracted_melody = pretty_midi.PrettyMIDI()
    generated_melody = pretty_midi.Instrument(program=1) # Acoustic Grand Piano
    generated_melody.is_drum = False

    fd.write('start ')

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
            min_pitch = 200
            check = False
            for note in melody_inst.notes:
                if (note.start >= part[time_i]) and (note.start <= part[time_i+1]) and (note.pitch<min_pitch):
                    check = True
                    min_pitch = note.pitch
            if check:
                new_note = pretty_midi.Note(velocity=100,
                    pitch=min_pitch,
                    start=part[time_i],
                    end=part[time_i]+.3)
                generated_melody.notes.append(new_note)
                fd.write(str(min_pitch) + ' ')
            else:
                fd.write(str(0) + ' ')

    extracted_melody.instruments.append(generated_melody)
    extracted_melody.write('melody/' + f[:-4] + '.mid')
    fd.write('end ')


if __name__ == '__main__':
    if os.path.exists('./drum/') == False:
        os.makedirs('./drum/')
    if os.path.exists('./melody/') == False:
        os.makedirs('./melody/')
    if os.path.exists('./midi/') == False:
        os.makedirs('./midi/')
        print 'please input .mid files to ./midi directory!'
        exit()

    midi_dir = 'midi'
    midi_filenames = os.listdir(midi_dir)

    midi_filenames = [f for f in midi_filenames if f.endswith('.mid')]
    midi_filenames = [f for f in midi_filenames if os.path.getsize(midi_dir + '/' + f) != 0]

    drum_fd = open('drum_train.txt', 'w')
    melody_fd = open('melody_train.txt', 'w')

    for f in tqdm(midi_filenames):
        midi_data = pretty_midi.PrettyMIDI(midi_dir + '/' + f)
        inst = midi_data.instruments
        if len(inst) != 2:
            print 'instrument problem'
            continue
        if (len(inst[0].notes) < 100) or (len(inst[1].notes) < 100):
            print 'note num problem'
            continue

        print f

        drum_midi_to_text(midi_dir, f, drum_fd)
        melody_midi_to_text(midi_dir, f, melody_fd)

    drum_fd.close()
    melody_fd.close()
    # text to midi part

    # drum_dir = 'drum/'
    # drum_text_filenames = os.listdir(drum_dir)
    # drum_text_filenames = [f for f in drum_text_filenames if f.endswith('.txt')]
    
    # melody_dir = 'melody/'
    # melody_text_filenames = os.listdir(melody_dir)
    # melody_text_filenames = [f for f in melody_text_filenames if f.endswith('.txt')]
    
    # for f in drum_text_filenames:
    #     drum_text_to_midi(drum_dir, drum_text_filenames, midi_dir)

    # for f in melody_text_filenames:
    #     melody_text_to_midi(melody_dir, melody_text_filenames, midi_dir)

    print 'done! for %d files' % len(midi_filenames)