#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import threading

class SocketClient(threading.Thread):

    # Constructor
    def __init__(self):
        # Threading init
        threading.Thread.__init__(self)
        self.setName = "SocketClient"
        self.daemon = True
        self.alive = False

        # Init socket
        self.HOST = '192.168.1.113'
        self.PORT = 4242
        self.sock = None #Socket object

    # Destructor
    def __del__(self):
        self.close()

    # Kill the thread gracefully
    def kill(self):
        self.alive = False
        self.sock.shutdown(socket.SHUT_WR) #Force the socket to stop listening

    # Start point of thread execution
    def run(self):
        self.alive = True
        self.setupSocket()
        while(self.alive):
            pass

    # Socket initiation
    def setupSocket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORT))
        print "Setup socket successfull"

    # Send message over active socket
    def send(self, msg):
        totalsent = 0
        # Sends the message in chunks until the whole message has been sent
        while totalsent < len(msg):
            sent = self.sock.sendto(msg[totalsent:], (self.HOST, self.PORT))
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    # Make sure the socket closes properly
    def close(self):
        if(self.sock != None):
            self.sock.close()
            self.sock = None

    # Receive one message of 1024 bytes
    def recieve(self):
        return self.sock.recv(1024) # Blocking receive
