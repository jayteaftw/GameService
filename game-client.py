# Import socket module
import socket 
import pygame
import numpy as np  
from io import BytesIO     
import pickle 
import time   
 
# Create a socket object
s = socket.socket()        
 
# Define the port on which you want to connect
port = 12356              
 
# connect to the server on local computer
s.connect(('127.0.0.1', port))
 
# receive data from the server and decoding to get the string.
print (s.recv(1024).decode())


pygame.init()
FACTOR = 5
size = (160*FACTOR, 144*FACTOR)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)

count = 0
while True:
    time.sleep(0.01)
    recieved = s.recv(69283)
    length = s.recv(100)
    if str(length) != f"b'{str(len(recieved))}'":
        #print(length, len(recieved) )
        count += 1
        print("Drop Count:",count)
        continue
    
    stream = pickle.loads(recieved)
    #print("recieved:",recieved)

    #print(stream.shape, type(stream))
    #print("okay")

    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            size = (event.w, event.h)

    org_pic = pygame.surfarray.make_surface(stream)
    pic = pygame.transform.scale(org_pic, size)

    #print("stream:",stream.shape, "\n screen1", screen.get_size())
    
    BLACK = (0, 0, 0)
    screen.fill(BLACK)
    
    screen.blit(pic, (0,0))
    
    #pygame.display.flip()
    pygame.display.update()


# close the connection
s.close()  