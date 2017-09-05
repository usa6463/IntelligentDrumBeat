import pretty_midi

    
extracted_drum = pretty_midi.PrettyMIDI()
generated_drum = pretty_midi.Instrument(program=1)
generated_drum.is_drum = False

for i in range(10):
    new_note = pretty_midi.Note(velocity=110,
        pitch=35,
        start=i*2,
        end=i*2+.3)
    generated_drum.notes.append(new_note)
extracted_drum.instruments.append(generated_drum)
extracted_drum.write('pitch_test.mid')

# 25 ~ 85