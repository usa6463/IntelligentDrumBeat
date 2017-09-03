from tqdm import tqdm
melody_fd = open('melody_train.txt')
melody_txt = melody_fd.read()
melody = melody_txt.split(' ')[:-1]
melody_fd.close()

drum_fd = open('drum_train.txt')
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

step = 100
for i in tqdm(range(0, song_num, step)):
    end = 0
    if i+step >= song_num:
        end = song_num
    else:
        end = i+step-1
    folder = '../learning/train/'
    melody_fd = open(folder + 'melody_train' + str(i) + '.txt', 'w')
    drum_fd = open(folder + 'drum_train' + str(i) + '.txt', 'w')
    for j in range(song_start[i], song_end[end]+1):
        melody_fd.write(melody[j]+' ')
        drum_fd.write(drum[j]+' ')
