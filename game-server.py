# first of all import the socket library
import socket
import numpy as np
from pyboy import PyBoy
from pyboy import WindowEvent
from io import BytesIO
import pickle
 
# next create a socket object
s = socket.socket()        
print ("Socket successfully created")
 
# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12356              
 
# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))        
print ("socket binded to %s" %(port))
 
# put the socket into listening mode
s.listen(5)    
print ("socket is listening")           
 
# a forever loop until we interrupt it or
# an error occurs
while True:
 
    # Establish connection with client.
    c, addr = s.accept()    
    print ('Got connection from', addr )
 
    # send a thank you message to the client. encoding to send byte type.
    c.send('Starting Game Service'.encode())

    

    pyboy = PyBoy('ROMs/Pokemon Red (UE) [S][!].gb')
    pyboy.set_emulation_speed(1)
    bot = pyboy.botsupport_manager()
    screen_bot = bot.screen()

    while not pyboy.tick():

        stream = np.transpose(screen_bot.screen_ndarray(), (1,0,2))

        package = pickle.dumps(stream)
        print(type(package), len(package))
        c.send(package)
        c.send(str(len(package)).encode())
        

        """  #message = c.recv(1024).decode()
        message = c.recv(1024)
        print(message, type(message))

        # Close the connection with the client
        if message == "close":
            print("Closing Server")
            break """

        pass
    

    message = c.recv(1024).decode()
    print(message, type(message))

    c.close()

    # Close the connection with the client
    if message == "close":
        print("Closing Server")
        break
        