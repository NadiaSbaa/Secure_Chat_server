import threading
import socket
import argparse
import os
from hashlib import sha256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as INSAT_PKI
import base64

class Server(threading.Thread):
    """
    Supports management of server connections.
    Attributes:
        connections (list): A list of ServerSocket objects representing the active connections.
        host (str): The IP address of the listening socket.
        port (int): The port number of the listening socket.
    """
    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.host = host
        self.port = port
        self.clients_connected = []
    
    def run(self):
        """
        Creates the listening socket. The listening socket will use the SO_REUSEADDR option to
        allow binding to a previously-used socket address. This is a small-scale application which
        only supports one waiting connection at a time. 
        For each new connection, a ServerSocket thread is started to facilitate communications with
        that particular client. All ServerSocket objects are stored in the connections attribute.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))

        sock.listen(1)
        print('Listening at', sock.getsockname())

        while True:

            # Accept new connection
            sc, sockname = sock.accept()
            print('Accepted a new connection from {} to {}'.format(sc.getpeername(), sc.getsockname()))

            # Create new thread
            server_socket = ServerSocket(sc, sockname, self)
            
            # Start new thread
            server_socket.start()

            # Add thread to active connections
            self.connections.append(server_socket)
            print('Ready to receive messages from', sc.getpeername())


    def encrypt(self, message, origin):
            filename = '../Client/keys/' + str(origin)
            f = open(filename + '.cert','r')
            key = RSA.import_key(f.read())
            cipher = INSAT_PKI.new(key)
            ciphertext = cipher.encrypt(message.encode('utf8'))
            encrypted = base64.b64encode(ciphertext).decode('ascii')
            return encrypted

    def broadcast(self, message, source, origineName):
        """
        Sends a message to all connected clients, except the source of the message.
        Args:
            message (str): The message to broadcast.
            source (tuple): The socket address of the source client.
        """
        for connection in self.connections:
            # Send to all connected clients except the source client
            if connection.sockname != source:
                #Decryption
                m = self.encrypt(message, connection.origin)
                connection.send(m)
    
    def remove_connection(self, connection):
        """
        Removes a ServerSocket thread from the connections attribute.
        Args:
            connection (ServerSocket): The ServerSocket thread to remove.
        """
        self.connections.remove(connection)


class ServerSocket(threading.Thread):
    """
    Supports communications with a connected client.
    Attributes:
        sc (socket.socket): The connected socket.
        sockname (tuple): The client socket address.
        server (Server): The parent thread.
    """
    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.server = server
        self.origin = ''
    
    def run(self):
        """
        Receives data from the connected client and broadcasts the message to all other clients.
        If the client has left the connection, closes the connected socket and removes itself
        from the list of ServerSocket threads in the parent Server thread.
        """
        while True:
            message = self.sc.recv(1024).decode('ascii')
            if message:
                informations = message.split(':')
                self.server.clients_connected.append(informations[0])
                self.server.clients_connected = list(set(self.server.clients_connected))
                self.origin = informations[0]
                print('{} says {!r}'.format(self.sockname, message))
                self.server.broadcast(message, self.sockname, informations[0])
            else:
                # Client has closed the socket, exit the thread
                print('{} has closed the connection'.format(self.sockname))
                self.sc.close()
                self.server.remove_connection(self)
                return
    
    def send(self, message):
        """
        Sends a message to the connected server.
        Args:
            message (str): The message to be sent.
        """
        self.sc.sendall(message.encode('ascii'))


def exitt(server):
    """
    Allows the server administrator to shut down the server.
    Typing 'q' in the command line will close all active connections and exit the application.
    """
    while True:
        ipt = input('')
        if ipt == 'q':
            print('Closing all connections...')
            for connection in server.connections:
                connection.sc.close()
            print('Shutting down the server...')
            os._exit(0)



def server_chat(host, p):
    # Create and start server thread
    server = Server(host, p)
    server.start()
    exit = threading.Thread(target = exitt, args = (server,))
    exit.start()
