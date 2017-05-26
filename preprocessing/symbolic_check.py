"""
duration: continuous.
protocol_type: symbolic.
service: symbolic.
flag: symbolic.
src_bytes: continuous.
dst_bytes: continuous.
land: symbolic.
wrong_fragment: continuous.
urgent: continuous.
hot: continuous.
num_failed_logins: continuous.
logged_in: symbolic.
num_compromised: continuous.
root_shell: continuous.
su_attempted: continuous.
num_root: continuous.
num_file_creations: continuous.
num_shells: continuous.
num_access_files: continuous.
num_outbound_cmds: continuous.
is_host_login: symbolic.
is_guest_login: symbolic.
count: continuous.
srv_count: continuous.
serror_rate: continuous.
srv_serror_rate: continuous.
rerror_rate: continuous.
srv_rerror_rate: continuous.
same_srv_rate: continuous.
diff_srv_rate: continuous.
srv_diff_host_rate: continuous.
dst_host_count: continuous.
dst_host_srv_count: continuous.
dst_host_same_srv_rate: continuous.
dst_host_diff_srv_rate: continuous.
dst_host_same_src_port_rate: continuous.
dst_host_srv_diff_host_rate: continuous.
dst_host_serror_rate: continuous.
dst_host_srv_serror_rate: continuous.
dst_host_rerror_rate: continuous.
dst_host_srv_rerror_rate: continuous.
back,buffer_overflow,ftp_write,guess_passwd,imap,ipsweep,land,loadmodule,multihop,neptune,nmap,normal,perl,phf,pod,portsweep,rootkit,satan,smurf,spy,teardrop,warezclient,warezmaster.
"""

import csv # This script save data to csv file as flat text file\
from tqdm import tqdm

test_file = 'C:\\Users\\ISK\\Desktop\\kdd\\test\\kddcup.testdata.unlabeled'
train_file = 'C:\\Users\\ISK\\Desktop\\kdd\\train\\kddcup.data.corrected'
train_csvfile = open(train_file, 'r', newline = '')
test_csvfile = open(test_file, 'r', newline = '')

train_reader = csv.reader(train_csvfile)
test_reader = csv.reader(test_csvfile)

diction_protocol = {}
diction_service = {}
diction_flag = {}
diction_land = {}
diction_logged = {}
diction_host = {}
diction_guest = {}

for test in tqdm(train_reader):
	if not test[1] in diction_protocol:
		diction_protocol[test[1]] = [test]
	if not test[2] in diction_service:
		diction_service[test[2]] = [test]
	if not test[3] in diction_flag:
		diction_flag[test[3]] = [test]
	if not test[6] in diction_land:
		diction_land[test[6]] = [test]
	if not test[11] in diction_logged:
		diction_logged[test[11]] = [test]
	if not test[20] in diction_host:
		diction_host[test[20]] = [test]
	if not test[21] in diction_guest:
		diction_guest[test[21]] = [test]

for test in tqdm(test_reader):
	if not test[1] in diction_protocol:
		diction_protocol[test[1]] = [test]
	if not test[2] in diction_service:
		diction_service[test[2]] = [test]
	if not test[3] in diction_flag:
		diction_flag[test[3]] = [test]
	if not test[6] in diction_land:
		diction_land[test[6]] = [test]
	if not test[11] in diction_logged:
		diction_logged[test[11]] = [test]
	if not test[20] in diction_host:
		diction_host[test[20]] = [test]
	if not test[21] in diction_guest:
		diction_guest[test[21]] = [test]

print(diction_protocol.keys())
print(diction_service.keys())
print(diction_flag.keys())
print(diction_land.keys())
print(diction_logged.keys())
print(diction_host.keys())
print(diction_guest.keys())

