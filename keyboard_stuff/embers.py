#!//usr/bin/env python3

import threading
import subprocess
import random
import time

#BACKGROUND = '1c1c61' # Dark blue
#STARLIGHT = 'ffe400' # Yellow

BACKGROUND = '332200' # Black
STARLIGHT = 'ffbb22' # Orange

# Set keyboard background color to simulate night sky
subprocess.call('g810-led -dv 046d -dp c33c -tuk 1 -a ' + BACKGROUND, shell=True)

# Each key is illuminated separately as its own thread.
class newThread (threading.Thread):
    def __init__(self, threadID, keyName, counter):
        threading.Thread.__init__(self) 
        self.threadID = threadID 
        self.keyName = keyName
        self.counter = counter


    def run(self):
        print('Starting: ' + self.keyName)

        fadeColor(self.keyName, self.counter, 1, STARLIGHT, True)
        fadeColor(self.keyName, self.counter, 1, STARLIGHT, False)

        print('Exiting: ' + self.keyName)


# Convert hex string into separate RGB values
def hexToRGB(color):
    return list(int(color[i:i+2], 16) for i in (0, 2, 4))

# -----------------------------------------------------------------------
# Fade key color in to STARLIGHT value.
# -----------------------------------------------------------------------
# fadeDir is fade direction.
# True = fade in from BACKGROUND color to STARLIGHT color
# False = fade out from starlight color to BACKGROUND color
# -----------------------------------------------------------------------
def fadeColor(keyName, delay, step, color, fadeDir):
    step = 1


    # Convert hex STARLIGHT color to RGB
    keyRGB = hexToRGB(color)

    # Convert hex BACKGROUND color to RGB
    backRGB = hexToRGB(BACKGROUND)


    # Fade in
    if fadeDir:

        # Start at BACKGROUND
        newRed = backRGB[0]
        newGreen = backRGB[1]
        newBlue = backRGB[2]

        # Stop at STARLIGHT
        stopRed = keyRGB[0]
        stopGreen = keyRGB[1]
        stopBlue = keyRGB[2]


    # Fade out
    else:

        # Start at STARLIGHT
        newRed = keyRGB[0]
        newGreen = keyRGB[1]
        newBlue = keyRGB[2]

        # Stop at Background
        stopRed = backRGB[0]
        stopGreen = backRGB[1]
        stopBlue = backRGB[2]


    newColor = False
    stopColor = False

    if fadeDir:
        stopColor = STARLIGHT
    else:
        stopColor = BACKGROUND

    # Form new hex color
    while not newColor == stopColor:

        newColor = '{0:02x}{1:02x}{2:02x}'.format(newRed, newGreen, newBlue)
    
        subprocess.call('g810-led -dv 046d -dp c33c -tuk 1 -k ' + keyName + ' ' + newColor, shell=True)

        # adjust color values. Increment color if less than, decrement if greater than
        if newRed < stopRed:
            newRed += step
        elif newRed > stopRed:
            newRed -= step
    
        if newGreen < stopGreen:
            newGreen += step
        elif newGreen > stopGreen:
            newGreen -= step
    
        if newBlue < stopBlue:
            newBlue += step
        elif newBlue > stopBlue:
            newBlue -= step

# ------------------------------------------------------------
# List of keys to affect
# ------------------------------------------------------------
keys = [
'esc',

# Function F1-F12
'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',

# Print Screen, Scroll Lock, Pause
'printscr', 'scrolllock', 'pause',

'ins', 'del', 'home', 'end', 'pageup', 'pagedown',

# Arrow keys
'top', 'right', 'bottom', 'left',

# Numpad
'numlock', 'numslash', 'numasterisk', 'numminus', 'numplus', 'numenter',
'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'num.',

'tilde', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'minus', 'equal', 'backspace',
'tab', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
's', 't', 'u', 'v', 'u', 'w', 'x', 'y', 'z', 'comma', 'period', 'slash', 'semicolon',
'quote', 'open_bracket', 'close_bracket', 'backslash', 'enter', 'shiftright', 'shiftleft',
'caps', 'winright', 'winleft', 'menu', 'space', 'capslock', 'ctrlleft', 'ctrlright',
'altleft', 'altright',

'gamemode', 'capsindicator'
]


# Store active keys.
threadList = {}

try:
    while True:

        # Prevent too many threads in dictionary
        if len(threadList) > 5:
            for key in threadList:
                threadList[key].join()
            threadList = {} # Reset
    
        for key in random.sample(keys, 5):
            if not key in threadList:
                threadList[key] = newThread(key, key, 1) # Use keyname as dictionary key
                threadList[key].handled = True
                threadList[key].start()
                time.sleep(random.random() * 1.5)
            else: 
                # Must wait for thread to finish and remove
                threadList[key].join()
                threadList.pop(key, None)

except KeyboardInterrupt: # Handle CTRL+C
    for key in threadList:
        threadList[key].join()
    subprocess.call('g810-led -dv 046d -dp c33c -tuk 1 -a ' + BACKGROUND, shell=True)
