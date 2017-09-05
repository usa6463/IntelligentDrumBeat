# IntelligentDrumBeat
System which make drum beat using tensorflow

## deploy (Linux)
- `virtualenv env`
- `source env/bin/activate`
- `pip install -r requirements.txt`

## preprocessing
- put the raw midi files to `\backend\preprocessing\raw_midi` 
- `python extractMelody.py`
- then you can get the extracted midi files in `\backend\preprocessing\midi`

- In `\backend\preprocessing\`, command `python preprocess.py`
- then you can get .txt files as train data in `\backend\preprocessing\`
- also `\backend\preprocessing\drum` and `\backend\preprocessing\melody` will be generated. Each directory have only drum or melody MIDI file

## train
- need to install keras, tensorflow
- go to `\backend\learning\`
- move the train data to `\backend\learning\train`
- command `python model.py .`. then you can get `model.h5`, `model.json`

## run server
- need to install keras, tensorflow
- `python runserver.py`
