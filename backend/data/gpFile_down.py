import urllib3
import os
import sys
import json
from bs4 import BeautifulSoup
import re

headers = {'accept-encoding': 'gzip,deflate'
			,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
			,'Cookie':'PHPSESSID=310a9a726e5ac3e04bd85f8e1e0081ef'
			,'Referer':'http://guitarprotabs.org/a/a_dominique/au_22_bar_33/'
			,'connection': 'keep-alive'
			,'Host':'guitarprotabs.org'};
http = urllib3.PoolManager();
host = 'http://guitarprotabs.org'
get_url = '/a/a_dominique/au_22_bar_33/download/ HTTP/1.1'
root = 'D:/capstone/data/'
print('실행');
list_number = 1;

alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'];
for alpha_list in alpha:  
	#print(list_number); #debug
	#alpha = chr(alpha_int);
	str_list_num = str(list_number);
	Parser_url = host + '/' + alpha_list + '/';
	print(Parser_url)	#debug
	url_temp = Parser_url + str_list_num +'/';
	print(url_temp)		#debug
	html_page = http.request('GET', url_temp);
	'''
	print(html_page.status)	#debug
	if(html_page.status != 200):
			continue;
	'''
	page_txt = html_page.data;
	bs = BeautifulSoup(page_txt,'html.parser');
	try:
		test_list = bs.find(class_="pagination").get_text();
	except:
		test_list = '1';

	string = re.sub('[^0-9]', '', test_list)
	#print("debug")
	#print (string)

	for i in string:
		print(i);
		url_temp = Parser_url + i +'/';
		html_page = http.request('GET', url_temp);
		print(html_page.status)	#debug
		if(html_page.status != 200):
			continue;
			print("continue");
		page_txt2 = html_page.data;
		bs_temp = BeautifulSoup(page_txt2,'html.parser');
	#print("------------");
	#while(1):
		'''
		str_list_num = str(list_number);
		Parser_url = host + '/' + alpha_list + '/';
		url_temp = Parser_url + str_list_num;
		print(url_temp+'\n');		
		html_page = http.request('GET', url_temp);
		if(html_page.status != 200):
			break;
		page_txt = html_page.data;
		bs = BeautifulSoup(page_txt,'html.parser');
		list_number = list_number + 1;
		'''
		

		try :
			bs_list = bs_temp.tbody.find_all('a');
			for test in bs_list:
					url_temp2 = test.get('href');
					html_page_temp = http.request('GET',url_temp2);
					page_txt2 = html_page_temp.data;
					bs2 = BeautifulSoup(page_txt2,'html.parser');
					try:
						for test2 in bs2.tbody.find_all('a'):
							download_url = test2.get('href');
							file_name = test2.get_text();
							get_url = download_url+'download/ HTTP/1.1';
							print (file_name + '  ' + get_url) ;
						
							r = http.request('GET', get_url, headers=headers);
							try:
								for test3 in bs2.tbody.find_all('td')[1]:
									if os.path.exists(root) == False:
										os.makedirs(root);
									fp = open(root+file_name+test3,'wb');
									fp.write(r.data);
									fp.close();
							except:
								continue;
								print("continue");
					except:
						continue;
						print("continue");

		except :
			continue;
			print("continue");
'''
r = http.request('GET', host+get_url ,headers=headers);
if os.path.exists(root) == False:
	os.makedirs(root);
fp = open(root+'test.gp3','wb');
fp.write(r.data);
r.data;
'''
