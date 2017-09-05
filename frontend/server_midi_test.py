#!/usr/bin/env python

#python3
# https://pythonprogramming.net/client-server-python-sockets/

import socket               # Websocket 
import sys                  # 
from thread import *       # Used for multi-threading      The thread module has been renamed to _thread in Python 3.
import time                 # Used to create delays

# ******* WEBSOCKET VARIABLES *******
numberClients = 0
host = 'localhost'
PORT = 2223
# ******* WEBSOCKET VARIABLES *******

# ************************** FUNCTIONS **************************
def threaded_client(conn,address):      # receive as parameters, the connection object (conn), and the address object that contains the ip and port
    global numberClients
    conn.send(str.encode('Welcome, type your info\n'))  # data should be bytes
    numberClients = numberClients + 1

    #           CHECK USER USING PASSWORD OR SOMETHING
    if ("192.168" in str(address[0])):
        print ("     VALID CLIENT!!")

        while True:
            data = conn.recv(2048)
            if (data):
                reply = "" + 'Server output: '+ data.decode('utf-8').rstrip() + "\n"
                print(str(address[0]) + " - Clients(" + str(numberClients) + ") -> Data received: >" + data.decode('utf-8').rstrip() + "<")
            if not data:
                #print("no data")
                #break
                foo = 2
            try:
                conn.sendall(str.encode(reply))     # data should be bytes
            except Exception as e:
                foo = 1
        print("Thread connection closed by client: " + address[0])
        conn.close()
        numberClients = numberClients - 1

    else:
        print ("     INVALID CLIENT -> Thread connection closed by USER VALIDATION: " + address[0])
        conn.close()
        numberClients = numberClients - 1
# ************************** FUNCTIONS **************************




# ************************** SETUP **************************
print ("\n----------- Starting Websocket Python Program -----------\n")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # "s" here is being returned a "socket descriptor" by socket.socket.
print(s)

# we are simply attempeting to bind a socket locally, on PORT 5555.
try:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)         # reuse the port number (in case we just got an error and port was not freed)
    s.bind((host, PORT))                # server side - take IN connections
    print ("Server started on port " + str(PORT))
except socket.error as e:
    print(str(e))
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    #sys.exit()
print('Socket bind complete')

s.listen(5)     # the "5" stands for how many incoming connections we're willing to queue before denying any more.

print('Waiting for a connection.')
# ************************** SETUP **************************



# ************************** MAIN LOOP **************************
while True:
    conn, addr = s.accept()         # code will stop here whilst waiting for a new connection. Old connections will be running in the threads
    print('Connected to: '+addr[0]+':'+str(addr[1]))

    start_new_thread(threaded_client,(conn,addr))   
# ************************** MAIN LOOP **************************