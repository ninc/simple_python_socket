#!/usr/bin/python
# -*- coding: utf-8 -*-

import Queue
import time
from SocketClient import SocketClient
from SocketServer import SocketServer


def handleMessages(messages):
    while(not messages.empty()):
        currentMessage = messages.get() # Remove item from queue
        print currentMessage # TODO Do something more interesting than to print the content

def main():

    # Init socket comm
    socketServer = SocketServer()
    socketClient = SocketClient()


    # Start threads
    socketServer.start() # Always start the server before the client
    socketClient.start()
    

    time.sleep(1) # Allow the sockets to be setup before using them

    try:    
        receivedMessages = Queue.Queue() # Init a queue to store received messages in

        # Send/Recv example
        while(True):
            socketClient.send("Hasse gillar kaffe \n") # VERY IMPORTANT!!!! ALWAYS PROVIDE A NEWLINE AT THE END OF THE MESSAGE OR THE RECV FUNCTION WILL NEVER STOP!
            time.sleep(1) # Make sure that our message has been received (Remove in real code)
            receivedMessages = socketServer.getMessages()

            handleMessages(receivedMessages)

    except (KeyboardInterrupt, SystemExit):
        raise

    finally:

        # Let threads die gracefully
        socketClient.kill()
        socketServer.kill()

        # Wait until threads die
        socketClient.join()
        socketServer.join()

main()