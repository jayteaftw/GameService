from pyboy import PyBoy
from pyboy import WindowEvent


pyboy = PyBoy('ROMs/Pokemon Red (UE) [S][!].gb')
pyboy.set_emulation_speed(1)
bot = pyboy.botsupport_manager()
screen_bot = bot.screen()

while not pyboy.tick():
    pass