# Circuit python program for Adafruit Neokey 1x4 
#
# Sets up the keys to send F13 - F16 keycodes when pressed.
# Use the ConsumerControl in the adafruit_hid library to add multimedia controls like volume, fwd, pause, etc.
#
# I use AutoHotkey (https://www.autohotkey.com/) to run macros on my Windows machine to action the F13-16 keypresses.
#
# Finally I was running into memory issues trying to use the QT Py or other smaller devices with limited memory (memerror).
#
import board
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_neokey.neokey1x4 import NeoKey1x4
neokey = NeoKey1x4(board.I2C())

# set up hid
kbd = Keyboard(usb_hid.devices)

RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (153,0,153)
WHITE = (255,255,255)
PINK = (255,51,153)
ORANGE = (255,140,0)

keys = [
    [neokey, 0, 0xFF0000, False],
    [neokey, 1, 0xFF0000, False],
    [neokey, 2, 0xFF0000, False],
    [neokey, 3, 0xFF0000, False],
]

colors = [YELLOW,GREEN,BLUE,PURPLE,WHITE,PINK,ORANGE]

# insert a small pause after keypress
def qpause():
    time.sleep(0.2)

# Send key code character
def sendKeyCode(key):
    if key==0:
        kbd.send(Keycode.F13)
    if key==1:
        kbd.send(Keycode.F14)
    if key==2:
        kbd.send(Keycode.F15)
    if key==3:
        kbd.send(Keycode.F16)

    #qpause()  # Uncomment to add delay after keypress

# * * * Main code * * * 

n = 0
initial = time.monotonic() + 6

while True:
    # change color of keys over time
    now = time.monotonic()
    if now - initial > 5:
        initial = now
        n = n + 1
        if n > len(colors)-1:
            n = 0
        for x in range(4):
            neokey.pixels[x] = colors[n]

    # check for key press
    for i in range(4):
        neokey, key_number, color, active = keys[i]
        if neokey[key_number]:
            neokey.pixels[key_number] = color
            keys[i][3]=True
            sendKeyCode(i)

        elif active==True:
            neokey.pixels[key_number] = colors[n]
            keys[i][3]=False
