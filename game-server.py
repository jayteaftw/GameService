# first of all import the socket library
import socket
import numpy as np
from pyboy import PyBoy
from pyboy import WindowEvent
from io import BytesIO
import pickle
import time
from struct import pack
 

if __name__ == "__main__":
    s = socket.socket()        
    print ("Socket successfully created")
    
    port = 12356              
    
    s.bind(('', port))        
    print ("socket binded to %s" %(port))
    
    s.listen(5)    
    print ("socket is listening")           
    
    while True:
        
        # Establish connection with client.
        c, addr = s.accept()    
        print ('Got connection from', addr )
    
        # send a thank you message to the client. encoding to send byte type.
        c.send('Starting Game Service'.encode())

        pyboy = PyBoy('ROMs/Pokemon Red (UE) [S][!].gb')
        pyboy.set_emulation_speed(5)
        bot = pyboy.botsupport_manager()
        screen_bot = bot.screen()

        button_press, button_release = None, None
        while not pyboy.tick():
            #time.sleep(0.001)

            stream = np.transpose(screen_bot.screen_ndarray(), (1,0,2))

            package = pickle.dumps(stream)
            #print(type(package), len(package))
            
            def send_data(conn, data):
                serialized_data = pickle.dumps(data)
                conn.sendall(pack('>I', len(serialized_data)))
                conn.sendall(serialized_data)
            
            send_data(c, package)

            command = c.recv(10).decode()

            def command_conversion(command):
                if command == "A":      return WindowEvent.PRESS_BUTTON_A      
                if command == "!A":     return WindowEvent.RELEASE_BUTTON_A

                if command == "B":      return WindowEvent.PRESS_BUTTON_A      
                if command == "!B":     return WindowEvent.RELEASE_BUTTON_A
                
                if command == "UP":     return WindowEvent.PRESS_ARROW_UP
                if command == "!UP":    return WindowEvent.RELEASE_ARROW_UP
                
                if command == "DOWN":   return WindowEvent.PRESS_ARROW_DOWN    
                if command == "!DOWN":  return WindowEvent.RELEASE_ARROW_DOWN
                
                if command == "RIGHT":  return WindowEvent.PRESS_ARROW_RIGHT
                if command == "!RIGHT": return WindowEvent.RELEASE_ARROW_RIGHT
                
                if command == "LEFT":   return WindowEvent.PRESS_ARROW_LEFT
                if command == "!LEFT":  return WindowEvent.RELEASE_ARROW_LEFT


            if command == "STOP":
                c.close()
                exit()
            if command != " ":
                print(command)
                command = command_conversion(command)
                pyboy.send_input(command)
                pyboy.tick()
           
            
        

    

    #c.close()

        