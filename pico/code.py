import digitalio
import board
import usb_hid
import time
import storage
from adafruit_hid.keyboard import Keyboard
#from adafruit_hid.mouse import Mouse
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

print("== Pi Pico multifunction knob 2.0 ==")
#
# IMOPRTANT FOR EDITING
# Press down the knob while plugging in to be able to edit the code.
#
# As an alternative you can type the following two commands:
# import storage
# storage.remount("/", readonly=False)
#
debug = False

CLK_PIN = board.GP4
DT_PIN = board.GP3
SW_PIN = board.GP2
rotateDelay = False
count = 0
totalMode = 1
currentMode = 0

cc = ConsumerControl(usb_hid.devices)
#mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)


clk = digitalio.DigitalInOut(CLK_PIN)
clk.direction = digitalio.Direction.INPUT

dt = digitalio.DigitalInOut(DT_PIN)
dt.direction = digitalio.Direction.INPUT

sw = digitalio.DigitalInOut(SW_PIN)
sw.direction = digitalio.Direction.INPUT
sw.pull = digitalio.Pull.UP

def millis():
    return time.monotonic() * 1000

def log(message):
    if debug:
        print(message)

def ccw():
    log("left")
    
    if currentMode == 0:
        # Volume decrement
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        
def cw():
    log("right")
    
    if currentMode == 0:
        # Volume increment
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)

        

        
def long_press():
    #Mac sleep: CMD + OPT + EJECT
    log("long-press")
    
def short_press():
    log("short-press")
    if currentMode == 0:
        cc.send(ConsumerControlCode.PLAY_PAUSE)
    
# Fix not working after wakeup (windows sleep)
def resetKeyboard(force = False):
    global keyboard, cc
    
    if force:
        time.sleep(1)
        log("Resetting keyboard..")
        cc = ConsumerControl(usb_hid.devices)
        keyboard = Keyboard(usb_hid.devices)
    else:
        if cc == None:
            time.sleep(1)
            log("ConsumerControl not initialized. Trying again..")
            cc = ConsumerControl(usb_hid.devices)
        if keyboard == None:
            time.sleep(1)
            log("Keyboard not initialized. Trying again..")
            keyboard = Keyboard(usb_hid.devices)
            
    
def loop():
    global rotateDelay
    
    currentState = clk.value
    # Rotation
    if currentState == False:
        if not rotateDelay:
            resetKeyboard()
            try:
                if dt.value != currentState:
                    cw()
                else:
                    ccw()
            except Exception:
                resetKeyboard(true)
            
            rotateDelay = True
    else:
        rotateDelay = False
    
    # Press
    if sw.value == 0:
        pressTime = millis()
        time.sleep(0.2)
        longPress = False
        resetKeyboard()
        try:
            while(sw.value == 0):
                if(millis() - pressTime > 1000 and not longPress):
                    longPress = True
                    long_press()
                
            if(not longPress):
                short_press()
        except Exception:
            resetKeyboard(true)


if __name__ == "__main__":
    # Mount storage when knob is pressed while plugging in
    if(sw.value == 0):
        storage.remount("/", readonly=False)

        
        
    if debug:
        while True:
            loop()
    else:
        while True:
            try:
                loop()
            except Exception:
                # log("An error occurred: {}".format(e))
                resetKeyboard(true)

