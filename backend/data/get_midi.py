import urllib2
import re
import os
from tqdm import tqdm

mid_regex = r'a href=".*[.]mid"'

# web_root = ['http://bhs.minor9.com/midi/assortment/A-F/',
#     'http://bhs.minor9.com/midi/assortment/G-Q/',
#     'http://bhs.minor9.com/midi/assortment/R-Z/']
web_root = ['http://bhs.minor9.com/midi/jazzstandards/']

for url in web_root:
    html = urllib2.urlopen(url)
    result = html.read()

    p = re.compile(mid_regex)
    m = p.findall(result)
    midi_file_list = [file_name[8:-1] for file_name in m]

    folder = './' + url[-4:]
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    for midi in tqdm(midi_file_list):
        try:
            midi_file = urllib2.urlopen(url+midi)
            with open(folder + midi, 'wb') as fd:
                fd.write(midi_file.read())
        except Exception as e:
            if os.path.exists(folder + midi):
                os.remove(folder + midi)
            print e