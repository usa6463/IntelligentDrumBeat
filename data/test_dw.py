import urllib3
import os
import sys
import json
from bs4 import BeautifulSoup

headers = {'accept-encoding': 'gzip,deflate'
			,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
			,'Cookie':'PHPSESSID=c6ce8b64b6a31ace4645b0225ceb4e7c'
			,'Referer':'http://guitarprotabs.org/a/a_dominique/au_22_bar_33/'
			,'connection': 'keep-alive'
			,'Host':'guitarprotabs.org'};
http = urllib3.PoolManager();
host = 'http://guitarprotabs.org'
get_url = '/a/a_dominique/au_22_bar_33/download/ HTTP/1.1'
root = 'C:/Users/Hyunwoo/Desktop/files/';

#alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','n','m','o','p','q','r','s','t','u','v','w','x','y','z'];
for alpha in range(97,121):  #a부터 z까지 
	list_number = 1;
	while(1):
		str_list_num = str(list_number);
		Parser_url = host + '/' + chr(alpha)+ '/';
		url_temp = Parser_url + '/'+ str_list_num;
		html_page = http.request('GET', url_temp);
		if(html_page.status != 200):
			break;
		page_txt = html_page.data;
		bs = BeautifulSoup(page_txt,'html.parser');
		list_number = list_number + 1;
		for test in bs.tbody.find_all('a'):
				url_temp2 = test.get('href');
				html_page_temp = http.request('GET',url_temp2);
				page_txt2 = html_page_temp.data;
				bs2 = BeautifulSoup(page_txt2,'html.parser');
				for test2 in bs2.tbody.find_all('a'):
					download_url = test2.get('href');
					file_name = test2.get_text();
					get_url = download_url+'download/ HTTP/1.1';
					print (file_name + '  ' + get_url) ;
					r = http.request('GET', get_url, headers=headers);
					for test3 in bs2.tbody.find_all('td')[1]:
						if os.path.exists(root) == False:
							os.makedirs(root);
						fp = open(root+file_name+test3,'wb');
						fp.write(r.data);
						fp.close();
#print(soup.find_all("li", {}));
'''
r = http.request('GET', host+get_url ,headers=headers);


if os.path.exists(root) == False:
	os.makedirs(root);
fp = open(root+'test.gp3','wb');
fp.write(r.data);

r.data;
'''
#cookies = {'Cookie':'PHPSESSID=c6ce8b64b6a31ace4645b0225ceb4e7c'};

