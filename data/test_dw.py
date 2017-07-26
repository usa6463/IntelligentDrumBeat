import urllib3
import os
import sys
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
			,'Cookie':'PHPSESSID=c6ce8b64b6a31ace4645b0225ceb4e7c'
			,'Referer':'http://guitarprotabs.org/a/a_dominique/au_22_bar_33/'
			,'connection': 'keep-alive'
			,'accept-encoding': 'gzip,deflate'
	  		,'Host':'guitarprotabs.org'};
http = urllib3.PoolManager();

r = http.request('GET', 'http://guitarprotabs.org/a/a_dominique/au_22_bar_33/download/ HTTP/1.1',headers=headers);

r.data;
#cookies = {'Cookie':'PHPSESSID=c6ce8b64b6a31ace4645b0225ceb4e7c'};
