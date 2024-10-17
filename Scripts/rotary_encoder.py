# =============================================================================
#  Project: Lambda Cyberdeck
#  License: CC-BY-NC-4.0
#  Repository: https://github.com/CodyTolene/Lambda-Cyberdeck
#  Description: This script reads a rotary encoder and a push button to emulate
#               a mouse scroll wheel and left click. The rotary encoder is
#               connected to GPIO pins 5 and 6, and the push button is connected
#               to GPIO pin 26. The script uses the pigpio library to read the
#               GPIO pins and the evdev library to emulate the mouse input.
# =============================================================================

import pigpio
import time
from evdev import UInput, ecodes as e

# Initialize pigpio library
pi = pigpio.pi()

if not pi.connected:
    exit()

# Set up virtual input device with specific capabilities
capabilities = {
    e.EV_KEY: [e.BTN_LEFT],
    e.EV_REL: [e.REL_WHEEL, e.REL_X, e.REL_Y],
}

ui = UInput(capabilities)

# Debug flag
debug = False

def debug_print(message):
    if debug:
        print(message)

def mouse_scroll_up():
    debug_print("Scrolling up")
    ui.write(e.EV_REL, e.REL_WHEEL, 1)
    ui.syn()

def mouse_scroll_down():
    debug_print("Scrolling down")
    ui.write(e.EV_REL, e.REL_WHEEL, -1)
    ui.syn()

def mouse_left_click():
    debug_print("Left click")
    ui.write(e.EV_KEY, e.BTN_LEFT, 1)
    ui.syn()
    ui.write(e.EV_KEY, e.BTN_LEFT, 0)
    ui.syn()

# State machine variables
last_enc_state = (pi.read(6) << 1) | pi.read(5)
last_time = time.time()
debounce_time = 0.01  # 10 ms debounce time

def rotary_callback(gpio, level, tick):
    global last_enc_state, last_time

    current_time = time.time()
    if current_time - last_time < debounce_time:
        return

    last_time = current_time

    a = pi.read(6)
    b = pi.read(5)

    enc_state = (a << 1) | b  # Combine a and b into a 2-bit state

    if enc_state != last_enc_state:
        if last_enc_state == 0b00 and enc_state == 0b01:
            mouse_scroll_up()
        elif last_enc_state == 0b01 and enc_state == 0b11:
            mouse_scroll_up()
        elif last_enc_state == 0b11 and enc_state == 0b10:
            mouse_scroll_up()
        elif last_enc_state == 0b10 and enc_state == 0b00:
            mouse_scroll_up()
        elif last_enc_state == 0b00 and enc_state == 0b10:
            mouse_scroll_down()
        elif last_enc_state == 0b10 and enc_state == 0b11:
            mouse_scroll_down()
        elif last_enc_state == 0b11 and enc_state == 0b01:
            mouse_scroll_down()
        elif last_enc_state == 0b01 and enc_state == 0b00:
            mouse_scroll_down()

        last_enc_state = enc_state

def button_callback(gpio, level, tick):
    if pi.read(26) == pigpio.LOW:  # Button pressed
        mouse_left_click()

# Configure GPIO pins
pi.set_mode(6, pigpio.INPUT)
pi.set_mode(5, pigpio.INPUT)
pi.set_mode(26, pigpio.INPUT)

pi.set_pull_up_down(6, pigpio.PUD_UP)
pi.set_pull_up_down(5, pigpio.PUD_UP)
pi.set_pull_up_down(26, pigpio.PUD_UP)

# Set up callbacks for edge detection
pi.callback(6, pigpio.EITHER_EDGE, rotary_callback)
pi.callback(5, pigpio.EITHER_EDGE, rotary_callback)
pi.callback(26, pigpio.FALLING_EDGE, button_callback)

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    pi.stop()
    ui.close()
