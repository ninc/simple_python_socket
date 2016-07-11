#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import threading
import Queue
import sys
import time

class SocketServer(threading.Thread):

    # Constructor
    def __init__(self):
        # Threading init
        threading.Thread.__init__(self)
        self.setName = "SocketServer"
        self.daemon = True
        self.alive = False

        # Init socket
        self.HOST = ''
        self.PORT = 4242
        self.sock = None

        self.eventQueue = Queue.Queue()
        self.eventQueueLock = threading.Lock()

    # Destructor
    def __del__(self):
        self.close()


    # Start point of thread execution
    def run(self):
        self.alive = True
        self.listenToSocket()

    # Kill the thread gracefully
    def kill(self):
        self.alive = False
        self.sock.shutdown(socket.SHUT_WR) #Force the socket to stop listening

    # Make sure the socket closes properly
    def close(self):
        if(self.sock != None):
            self.sock.close()
            self.sock = None

    # Closes the client socket
    def closeClientSocket(self, client):
        if(client != None):
            client.close()
            client = None
   
    # Setup UDP socket
    def setupUDP(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Bind socket to program
            self.sock.bind((self.HOST, self.PORT))
            self.sock.listen(1)
            print "Successfully setup UDP socket in Server"
        except socket.error, msg:
            self.close()
            print msg
            self.alive = False
            print "Failed to setup UDP in Server"

    # Listens to the socket for client connections
    def listenToSocket(self):
        # Initialize socket
        self.setupUDP()

        try:
            # Listen to socket
            while(self.alive):
                print "Waiting for connection request on PORT: " + str(self.PORT)
                client, clientAddr = self.sock.accept() # Waiting for connection request
                while(client != None):
                    clientData = client.recv(1024) # Receiving 1024 bytes.
                    if not clientData:
                        self.closeClientSocket(client) # End of message
                        break
                    self.handleClientData(clientData) # MESSAGE RECEIVED -> HANDLE IT
        except (KeyboardInterrupt, SystemExit):
            raise
            
    # Handles Client messages
    def handleClientData(self, clientData):
        # INSERT CODE HERE

        # FOR EXAMPLE SAVE ALL MESSAGES TO AN EVENT QUEUE
        self.eventQueueLock.acquire()
        try:
            self.eventQueue.put(clientData)
        finally:
            self.eventQueueLock.release() # Release lock no matter what


    # Fetch received messages (CALL FROM MAIN THREAD)
    def getMessages(self):
        eventQueue = Queue.Queue()
        self.eventQueueLock.acquire()
        try:
            eventQueue = self.eventQueue #Swap queue
            self.eventQueue = Queue.Queue() #Empty queue
        finally:
            self.eventQueueLock.release() # Release lock no matter what
        return eventQueue