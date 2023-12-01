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
# IMPORTANT FOR EDITING THIS SCRIPT
# Press down the knob while plugging in to be able to edit the code.
#
# As an alternative you can type the following two commands:
# import storage
# storage.remount("/", readonly=False)
#
# Debug
debug = False

# Pins
CLK_PIN = board.GP4
DT_PIN = board.GP3
SW_PIN = board.GP2

rotateDelay = False
totalModes = 1
currentMode = 0

cc = ConsumerControl(usb_hid.devices)
# mouse = Mouse(usb_hid.devices)
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
    log("Knob: turned left")

    if currentMode == 0:
        # Volume decrement
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)


def cw():
    log("Knob: turned right")

    if currentMode == 0:
        # Volume increment
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)


def long_press():
    # Mac sleep: CMD + OPT + EJECT
    log("Knob: long press detected")


def short_press():
    log("Knob: short press detected")
    if currentMode == 0:
        cc.send(ConsumerControlCode.PLAY_PAUSE)


def reset_keyboard(force=False):
    global keyboard, cc

    if force:
        time.sleep(1)
        log("Resetting keyboard..")
        cc = ConsumerControl(usb_hid.devices)
        keyboard = Keyboard(usb_hid.devices)
    else:
        if cc is None:
            time.sleep(1)
            log("ConsumerControl not initialized. Trying again..")
            cc = ConsumerControl(usb_hid.devices)
        if keyboard is None:
            time.sleep(1)
            log("Keyboard not initialized. Trying again..")
            keyboard = Keyboard(usb_hid.devices)


def loop():
    global rotateDelay

    current_state = clk.value
    # Rotation
    if not current_state:
        if not rotateDelay:
            reset_keyboard()
            try:
                if dt.value != current_state:
                    cw()
                else:
                    ccw()
            except Exception as e:
                print("An error occurred: {}".format(e))
                reset_keyboard(True)

            rotateDelay = True
    else:
        rotateDelay = False

    # Press
    if sw.value == 0:
        press_time = millis()
        time.sleep(0.2)
        long_pressed = False
        reset_keyboard()
        try:
            while sw.value == 0:
                if millis() - press_time > 1000 and not long_pressed:
                    long_pressed = True
                    long_press()

            if not long_pressed:
                short_press()

        except Exception as e:
            print("An error occurred: {}".format(e))
            reset_keyboard(True)


if __name__ == "__main__":
    # Mount storage when knob is pressed while plugging in
    if sw.value == 0:
        storage.remount("/", readonly=False)

    while True:
        # try except just in case there are any errors that might occur for any reason. Make sure it keeps running.
        try:
            loop()
        except Exception as e2:
            print("An error in the loop occurred: {}".format(e2))
            reset_keyboard(True)
