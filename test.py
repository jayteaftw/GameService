import numpy as np
from pyboy import PyBoy
from pyboy import WindowEvent
#import cv2
import time
import pygame


pyboy = PyBoy('ROMs/Pokemon Red (UE) [S][!].gb')
pyboy.set_emulation_speed(1)
bot = pyboy.botsupport_manager()
screen_bot = bot.screen()

pygame.init()
size = (160, 144)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)

while not pyboy.tick():
    #print(screen_bot.screen_ndarray()[0][0], size)
    stream = np.transpose(screen_bot.screen_ndarray(), (1,0,2))
    
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            size = (event.w, event.h)

    org_pic = pygame.surfarray.make_surface(stream)
    pic = pygame.transform.scale(org_pic, size)

    print("stream:",stream.shape, "\n screen1", screen.get_size())
    
    BLACK = (0, 0, 0)
    screen.fill(BLACK)
    
    screen.blit(pic, (0,0))
    
    #pygame.display.flip()
    pygame.display.update()

    pass