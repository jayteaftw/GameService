# Import socket module
import socket 
import pygame
import numpy as np  
from io import BytesIO     
import pickle 
import time
import sys
from struct import unpack   
 
def streaming_game(size):
    # Create a socket object
    s = socket.socket()        

    # Define the port on which you want to connect
    port = 12356              

    # connect to the server on local computer
    s.connect(('127.0.0.1', port))

    # receive data from the server and decoding to get the string.
    print (s.recv(1024).decode())
    count = 0
    running = True
    events_to_send = " "
    while running:
        
        #time.sleep(.1)
        
        def receive_data(conn):
            data_size = unpack('>I', conn.recv(4))[0]
            received_payload = b""
            reamining_payload_size = data_size
            while reamining_payload_size != 0:
                received_payload += conn.recv(reamining_payload_size)
                reamining_payload_size = data_size - len(received_payload)
            data = pickle.loads(received_payload)

            return data
        
        recieved = receive_data(s)

        s.send(events_to_send.encode())
        if events_to_send == "STOP":
            s.close()  
            return
        
        stream = pickle.loads(recieved)

        def command_conversion(command):
            if command == pygame.K_ESCAPE:  return "STOP"
            if command == pygame.K_a:       return "A"
            if command == pygame.K_b:       return "B"  
            if command == pygame.K_UP:      return "UP"
            if command == pygame.K_DOWN:    return "DOWN"
            if command == pygame.K_LEFT:    return "LEFT"
            if command == pygame.K_RIGHT:   return "RIGHT"

        events_to_send = " "
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                size = (event.w, event.h)
            if event.type == pygame.KEYDOWN:
                events_to_send = command_conversion(event.key)
                print(f"You pressed {events_to_send}")
            if event.type == pygame.KEYUP:
                events_to_send = "!"+command_conversion(event.key)
                print(f"You Released {events_to_send}")

                
                

        org_pic = pygame.surfarray.make_surface(stream)
        pic = pygame.transform.scale(org_pic, size)
        
        BLACK = (0, 0, 0)
        screen.fill(BLACK)
        
        screen.blit(pic, (0,0))
        
        #pygame.display.flip()
        pygame.display.update()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu(mainClock, size):

    click = False
    while True:

        screen.fill((0,0,0))
        draw_text('main menu', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                streaming_game(size)
        if button_2.collidepoint((mx, my)):
            if click:
                pass
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


if __name__ == "__main__":
    

    
    main_clock = pygame.time.Clock()
    pygame.init()
    FACTOR = 5
    size = (160*FACTOR, 144*FACTOR)
    pygame.display.set_caption('Pokemon')
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    font = pygame.font.SysFont(None, 20)
    main_menu(main_clock, size)
    #streaming_game(size)

