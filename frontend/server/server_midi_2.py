import socket
import time

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind( ('127.0.0.1', 9001))
server_sock.listen(10)

client_sock, addr = server_sock.accept()

data = client_sock.recv(200000)
print(data)
f = open("save_test.mid",'wb');
f.write(data);
f.close();

time.sleep(20)


f2 = open("./Complete/complete.mid", 'rb')
print("Sending...")
data2 = f2.read(200000)
print(data2)


client_sock.send(data2)

f2.close();

