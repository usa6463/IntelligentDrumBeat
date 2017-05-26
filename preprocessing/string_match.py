import csv # This script save data to csv file as flat text file\
from tqdm import tqdm

protocol = {
	'udp' : 0,
	'icmp' : 1,
	'tcp' : 2
}

service = {
	'gopher' : 0,
	'pop_3' : 1,
	'eco_i' : 2,
	'rje' : 3,
	'urp_i' : 4,
	'private' : 5,
	'imap4' : 6,
	'csnet_ns' : 7,
	'red_i' : 8,
	'exec' : 9,
	'netbios_ssn' : 10,
	'netbios_dgm' : 11,
	'klogin' : 12,
	'ecr_i' : 13,
	'printer' : 14,
	'smtp' : 15,
	'nntp' : 16,
	'supdup' : 17,
	'login' : 18,
	'http_8001' : 19,
	'icmp' : 20,
	'uucp_path' : 21,
	'kshell' : 22,
	'name' : 23,
	'harvest' : 24,
	'pop_2' : 25,
	'pm_dump' : 26,
	'IRC' : 27,
	'X11' : 28,
	'shell' : 29,
	'link' : 30,
	'ctf' : 31,
	'ntp_u' : 32,
	'discard' : 33,
	'tim_i' : 34,
	'tftp_u' : 35,
	'sql_net' : 36,
	'auth' : 37,
	'sunrpc' : 38,
	'time' : 39,
	'whois' : 40,
	'systat' : 41,
	'finger' : 42,
	'ssh' : 43,
	'Z39_50' : 44,
	'http_2784' : 45,
	'aol' : 46,
	'vmnet' : 47,
	'domain' : 48,
	'http' : 49,
	'domain_u' : 50,
	'courier' : 51,
	'daytime' : 52,
	'uucp' : 53,
	'hostnames' : 54,
	'telnet' : 55,
	'netbios_ns' : 56,
	'iso_tsap' : 57,
	'http_443' : 58,
	'remote_job' : 59,
	'other' : 60,
	'efs' : 61,
	'bgp' : 62,
	'ftp_data' : 63,
	'mtp' : 64,
	'echo' : 65,
	'ftp' : 66,
	'urh_i' : 67,
	'nnsp' : 68,
	'ldap' : 69,
	'netstat' : 70
}

flag = {
	'OTH' : 0,
	'REJ' : 1,
	'RSTO' : 2,
	'SF' : 3,
	'S3' : 4,
	'S1' : 5,
	'RSTR' : 6,
	'S2' : 7,
	'RSTOS0' : 8,
	'SH' : 9,
	'S0' : 10
}

result = {
	'back' : 0,
	'buffer_overflow' : 1,
	'ftp_write' : 2,
	'guess_passwd' : 3,
	'imap' : 4,
	'ipsweep' : 5,
	'land' : 6,
	'loadmodule' : 7,
	'multihop' : 8,
	'neptune' : 9,
	'nmap' : 10,
	'normal' : 11,
	'perl' : 12,
	'phf' : 13,
	'pod' : 14,
	'portsweep' : 15,
	'rootkit' : 16,
	'satan' : 17,
	'smurf' : 18,
	'spy' : 19,
	'teardrop' : 20,
	'warezclient' : 21,
	'warezmaster' : 22
}

test_file = 'C:\\Users\\ISK\\Desktop\\kdd\\test\\kddcup.data_10_percent_corrected'
train_file = 'C:\\Users\\ISK\\Desktop\\kdd\\train\\kddcup.data.corrected'

train_csvfile = open(train_file, 'r', newline = '')
test_csvfile = open(test_file, 'r', newline = '')

write_train_csvfile = open('train.csv', 'w', newline = '')
write_test_csvfile = open('test.csv', 'w', newline = '')

train_reader = csv.reader(train_csvfile)
test_reader = csv.reader(test_csvfile)

train_writer = csv.writer(write_train_csvfile)
test_writer = csv.writer(write_test_csvfile)

for test in tqdm(train_reader):
	test[1] = protocol[test[1]]
	test[2] = service[test[2]]
	test[3] = flag[test[3]]
	test[-1] = result[test[-1][:-1]]
	train_writer.writerow(test)

for test in tqdm(test_reader):
	test[1] = protocol[test[1]]
	test[2] = service[test[2]]
	test[3] = flag[test[3]]
	test[-1] = result[test[-1][:-1]]
	test_writer.writerow(test)

