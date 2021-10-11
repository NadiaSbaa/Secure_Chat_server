import socket
import os
import pymongo
from _thread import *
from hashlib import sha256
from utils_INSAT_PKI import createRequest, createCertificate
from OpenSSL import crypto
from server import server_chat
from hashlib import sha256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as INSAT_PKI
import base64
from datetime import datetime, timedelta

def create_connection_db():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["python_chat"]
    return  mydb

def insert_client(carteid, firstname, lastname, login, password, certifR, certif):
    mydb = create_connection_db()
    mycol = mydb["clients"]
    client = { "carteid": carteid, "firstname": firstname , "lastname": lastname, "login": login, "password": password , "certifRequest": certifR, "certif": certif}
    x = mycol.insert_one(client)
    return x

def list_clients():
    print("Clients existants dans la base de données maintenant: ")
    mydb = create_connection_db()
    mycol = mydb["clients"]
    for x in mycol.find():
        print("Login : ",x["login"], " , Password : ", x["password"], " , Certif : ", x["certif"])

def check_client_exists(login, password):
    mydb = create_connection_db()
    mycol = mydb["clients"]
    for x in mycol.find({"login": login, "password": password},{"certif"}):
        return x

def check_client_is_certified(login, password):
    mydb = create_connection_db()
    mycol = mydb["clients"]
    date = datetime.now()
    print("check function :login ", login, "pwd", password)
    for x in mycol.find({"login": login, "password": password},{"certif", "certifExpirationDate"}):
        print("x", x)
        if ((x['certif'] != '') and (date < x['certifExpirationDate'])):
            return "ClientAndCertified"
        else:
            return "ClientAndNotCertified"

def add_certif_to_client(login, password, certifR, certif):
    mydb = create_connection_db()
    mycol = mydb["clients"]
    myquery = { "login": login, "password": password}
    date = datetime.now()
    expire_date = date + timedelta(days=365)
    newvalues = { "$set": { "certifRequest": certifR, "certif": certif, "certifCreationDate": date,"certifExpirationDate": expire_date} }
    mycol.update_one(myquery, newvalues)


def encrypt(message, origin):
    filename = '../Client/keys/' + str(origin)
    f = open(filename + '.cert','r')
    key = RSA.import_key(f.read())
    cipher = INSAT_PKI.new(key)
    ciphertext = cipher.encrypt(message.encode('utf8'))
    encrypted = base64.b64encode(ciphertext).decode('ascii')
    return encrypted


def threaded_client(connection):
    while True:
        data = connection.recv(2048)
        #We get the data username and passwd combined
        #We check them
        #We send the certificate
        informations = data.decode('utf-8').split('|')
        resp = ""
        if len(informations) > 0:
            #Inscription
            if informations[0] == "Ins":
                print("Inscription Request")
                #I save the client in the data base
                #I return the certificate
                resp = "You should send a certificate request if you want to join the INSAT_CHAT!"
                #PWD doit etre encode en sha256
                password = sha256(informations[5].encode('utf_8')).hexdigest()
                insert_client(informations[1], informations[2], informations[3], informations[4], password, '', '')
            
            if informations[0] == "Con":
                print("Connection Request")
                #I connect to the database
                #I verify the login, pwd
                #If you dont have a certificate we tell you " you need to do a certifciate request"
                #If you have a certificate we tell you " you log to the chat"
                print("information 2", informations[2])
                password = sha256(informations[2].encode('utf_8')).hexdigest()
                print("passw information 2", password)
                check_c = check_client_is_certified(informations[1], password)
                print("check_c", check_c)
                if (check_c== 'ClientAndCertified'):
                    resp = "ClientAndCertified"
                    server_chat("127.0.0.1", 1060)
                else:
                    if (check_c== 'ClientAndNotCertified'):
                        print(informations[1], "exists Nadia")
                        resp = "ClientAndNotCertified"
                    else:
                        resp = "NotClient"

            if informations[0] == "Req":
                print("Certificate Request from", informations[1])
                ckey, creq = createRequest(informations[1])
                ccert = createCertificate(creq, creq, ckey, 0, 0, 60*60*24*365*1) # 1 year
                open('../client/keys/' + str(informations[1]) + '.cert', 'wb').write(crypto.dump_certificate(crypto.FILETYPE_PEM, ccert))
                password = sha256(informations[2].encode('utf_8')).hexdigest()
                add_certif_to_client(informations[1], password, "exists", "exists")
                resp = "ClientAndCertified"
                server_chat("127.0.0.1", 1060)

        else:
            resp = ""
        if not data:
            break
        connection.sendall(str.encode(resp))
    connection.close()


def accept_connexion():
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

    while (ThreadCount < 10):
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        list_clients()
        start_new_thread(threaded_client, (Client, ))
        ThreadCount += 1
        print('Client: ' + str(ThreadCount))
    ServerSocket.close()
    
accept_connexion()