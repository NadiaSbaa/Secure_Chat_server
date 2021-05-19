import socket
import os
from _thread import *

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection):
    connection.send(str.encode('Welcome to the Server'))
    while True:
        data = connection.recv(2048)
        #We get the data username and passwd combined
        #We check them
        #We send the certificate
        print("data",data.decode('utf-8'))
        informations = data.decode('utf-8').split('|')
        print("informations", informations)
        if len(informations) > 0:
            #Inscription
            if informations[0] == "Ins":
                print("Inscription Request")
                #I create a certificate
                #PWD doit etre encode en sha256
                #I save the client in the data base
                #I return the certificate
                resp = "123##"
            if informations[0] == "Con":
                print("Connection Request")
                #I connect to the database
                #I verify the login, pwd, certificate
                resp = "Yes"

        else:
            resp = ""
        if not data:
            break
        connection.sendall(str.encode(resp))
    connection.close()

while (ThreadCount < 5):
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Client: ' + str(ThreadCount))
ServerSocket.close()