import urllib2
import re
import os

mid_regex = r'a href=".*[.]mid"'

web_root = ['http://bhs.minor9.com/midi/assortment/A-F/',
    'http://bhs.minor9.com/midi/assortment/G-Q/',
    'http://bhs.minor9.com/midi/assortment/R-Z/']

for url in web_root:
    html = urllib2.urlopen(url)
    result = html.read()

    p = re.compile(mid_regex)
    m = p.findall(result)
    midi_file_list = [file_name[8:-1] for file_name in m]

    folder = './' + url[-4:]
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    for midi in midi_file_list:
        midi_file = urllib2.urlopen(url+midi)
        with open(folder + midi, 'wb') as fd:
            fd.write(midi_file.read())

# mp3file = urllib2.urlopen('http://bhs.minor9.com/midi/assortment/A-F/Billy%20Joel%20-%20PianoMan%202.mid')
# with open('b.mid','wb') as output:
#   output.write(mp3file.read())
