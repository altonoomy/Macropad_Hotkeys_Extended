"""
A macro/hotkey program for Adafruit MACROPAD. Macro setups are stored in the
/macros folder (configurable below), load up just the ones you're likely to
use. Plug into computer's USB port, use dial to select an application macro
set, press MACROPAD keys to send key sequences and other USB protocols.
"""

#pylint: disable=import-error, unused-import, too-few-public-methods

import os
import time
import displayio
import terminalio
import usb_cdc
import json
import re
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad

# Bug found: https://www.youtube.com/watch?v=wrKQhOvMm1g ; this video splits tab weirdly as 'uTube'. idk y lol
def splitStringByHyphen(s):
    pattern = re.compile(r"\s-\s")
    start = 0
    result = []
    while True:
        match = pattern.search(s, start)
        if match is None:
            result.append(s[start:].strip())
            break
        else:
            result.append(s[start:match.start()].strip())
            start = match.end()
    return result


# CONFIGURABLES ------------------------

MACRO_FOLDER = '/macros'

# Potential applications
browsers = ['Firefox', 'Chrome', 'Brave', 'Edge', 'Opera', 'Safari', 'Vivaldi', 'Pale Moon', 'Orion', 'Chromium']
websites = ['YouTube', 'Twitch']

# CLASSES AND FUNCTIONS ----------------

class App:
    """ Class representing a host-side application, for which we have a set
        of macro sequences. Project code was originally more complex and
        this was helpful, but maybe it's excessive now?"""
    def __init__(self, appdata):
        self.name = appdata['name']
        self.macros = appdata['macros']

    def switch(self):
        """ Activate application settings; update OLED labels and LED
            colors. """
        group[13].text = self.name   # Application name
        for i in range(12):
            if i < len(self.macros):  # Key in use, set label + LED color
                macropad.pixels[i] = self.macros[i][0]
                group[i].text = self.macros[i][1]
            else:  # Key not in use, no label or LED
                macropad.pixels[i] = 0
                group[i].text = ''
        macropad.keyboard.release_all()
        macropad.consumer_control.release()
        macropad.mouse.release_all()
        macropad.stop_tone()
        macropad.pixels.show()
        macropad.display.refresh()


# INITIALIZATION -----------------------

macropad = MacroPad()
macropad.display.auto_refresh = False
macropad.pixels.auto_write = False
# If encoder switch pressed, locks the macrokeys, used in the main loop
macro_locked = False

# Set up displayio group with all the labels
group = displayio.Group()

for key_index in range(12):
    x = key_index % 3
    y = key_index // 3
    group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF,
                             anchored_position=((macropad.display.width - 1) * x / 2,
                                                macropad.display.height - 1 -
                                                (3 - y) * 12),
                             anchor_point=(x / 2, 1.0)))
group.append(Rect(0, 0, macropad.display.width, 12, fill=0xFFFFFF))
group.append(label.Label(terminalio.FONT, text='', color=0x000000,
                         anchored_position=(macropad.display.width//2, -2),
                         anchor_point=(0.5, 0.0)))
macropad.display.show(group)

# Load all the macro key setups from .py files in MACRO_FOLDER
apps = []


files = os.listdir(MACRO_FOLDER)
files.sort()
for filename in files:
    if filename.endswith('.py'):
        try:
            module = __import__(MACRO_FOLDER + '/' + filename[:-3])
            apps.append(App(module.app))
        except (SyntaxError, ImportError, AttributeError, KeyError, NameError,
                IndexError, TypeError) as err:
            pass

if not apps:
    group[13].text = 'NO MACRO FILES FOUND'
    macropad.display.refresh()
    while True:
        pass
app_names = []
for app in apps:
    app_names.append(app.name)
default_app_index = 0

last_position = 0
last_encoder_switch = macropad.encoder_switch_debounced.pressed
app_index = 0
apps[app_index].switch()

# setup data serial comms
serial = usb_cdc.data

current_macro = apps[app_index].name.split('/')
time_sleep_interval = 0.15

# MAIN LOOP ----------------------------
while True:
    # Init switching variables
    browser = False
    # Read the current application in use to change macros on the fly
    if serial.in_waiting > 0:
        data_in = serial.readline()
        data = None
        if data_in:
            try:
                data = json.loads(data_in)
            except ValueError:
                pass
        if isinstance(data, dict):
            if data.get("application") is not None:
                window_program = data["application"]
                # Check if program is a browser for faster switching
                for b in browsers:
                    if window_program.endswith(b):
                        browser = True
                        window_program = window_program.split(" ")[-1]
                        break
            else:
                window_program = None
            if data.get("applicationFocus") is not None:
                window_program_focus = data["applicationFocus"]
                window_program_focus = splitStringByHyphen(window_program_focus)
            else:
                window_program_focus = None
            # If macro_locked, no macros will be switched until deactivated
            if not macro_locked:
                # If program is running and detected, and we haven't switched to that program macro
                if not browser and window_program and current_macro[0] != window_program:
                    for app in apps:
                        # If we have a corresponding macro for the app, switch to it
                        if window_program in app.name:
                            app_index = app_names.index(app.name)
                            apps[app_index].switch()
                            time.sleep(time_sleep_interval)
                            current_macro = app.name.split('/')
                            break
                    else:
                        # If we don't have corresponding macro, go to default macro i.e. first macro in macro/ directory
                        # also don't switch if we are already in default
                        if app_index != 0:
                            app_index = 0
                            apps[app_index].switch()
                            time.sleep(time_sleep_interval)
                            current_macro = apps[0].name.split('/')
                # If program is a browser, and current macro isn't already switched to, detect for tab changes
                if browser and (current_macro[0] != window_program or current_macro[-1] != window_program_focus):
                    # Some browsers like FF leave home page tab as None, others as New tab
                    # Check tab name, if it changed...
                    if window_program_focus is not None and current_macro[-1] != window_program_focus[-1]:
                        for app in apps:
                            # Check if tab name has corresponding macro. If so, switch.
                            if window_program_focus[-1] in app.name:
                                app_index = app_names.index(app.name)
                                apps[app_index].switch()
                                time.sleep(time_sleep_interval)
                                current_macro = app.name.split('/')
                                break
                        # If no corresponding macro, switch to default
                        else:
                            if app_index != app_names.index(window_program + "/Default"):
                                app_index = app_names.index(window_program + "/Default")
                                apps[app_index].switch()
                                time.sleep(time_sleep_interval)
                                current_macro = apps[app_index].name.split('/')
                    # In case of tab name being None, switch to default
                    elif window_program_focus is None and current_macro[-1] != "Default":
                        app_index = app_names.index(window_program + "/Default")
                        apps[app_index].switch()
                        time.sleep(time_sleep_interval)
                        current_macro = apps[app_index].name.split('/')
    # Read encoder position. If it's changed, switch apps.
    position = macropad.encoder
    if macropad.encoder != last_position and macropad.encoder > last_position:
        macropad.consumer_control.send(macropad.ConsumerControlCode.VOLUME_INCREMENT)
        print("Encoder: {}".format(macropad.encoder))
    elif macropad.encoder < last_position and macropad.encoder < last_position:
        macropad.consumer_control.send(macropad.ConsumerControlCode.VOLUME_DECREMENT)
        print("Encoder: {}".format(macropad.encoder))
    last_position = position

    # Handle encoder button. If state has changed, lock macro to the current setup
    macropad.encoder_switch_debounced.update()
    encoder_switch = macropad.encoder_switch_debounced.pressed
    if encoder_switch != last_encoder_switch:
        macro_locked = not macro_locked
        key_number = 12
        pressed = encoder_switch
    else:
        event = macropad.keys.events.get()
        if not event or event.key_number >= len(apps[app_index].macros):
            continue  # No key events, or no corresponding macro, resume loop
        key_number = event.key_number
        pressed = event.pressed
    # If code reaches here, a key or the encoder button WAS pressed/released
    # and there IS a corresponding macro available for it...other situations
    # are avoided by 'continue' statements above which resume the loop.

    sequence = apps[app_index].macros[key_number][2]
    if pressed:
        # 'sequence' is an arbitrary-length list, each item is one of:
        # Positive integer (e.g. Keycode.KEYPAD_MINUS): key pressed
        # Negative integer: (absolute value) key released
        # Float (e.g. 0.25): delay in seconds
        # String (e.g. "Foo"): corresponding keys pressed & released
        # List []: one or more Consumer Control codes (can also do float delay)
        # Dict {}: mouse buttons/motion (might extend in future)
        if key_number < 12:  # No pixel for encoder button
            macropad.pixels[key_number] = 0xFFFFFF
            macropad.pixels.show()
        # if macro_locked True, light pixels red to signify locked. If off, switch back to og color config.
        if key_number == 12 and macro_locked:
            #for key in range(12):
            macropad.pixels[0] = 0xFF0000
            macropad.pixels[2] = 0xFF0000
            macropad.pixels.show()
        else:
            macropad.pixels[0] = apps[app_index].macros[0][0]
            macropad.pixels[2] = apps[app_index].macros[2][0]
            macropad.pixels.show()

        for item in sequence:
            if isinstance(item, int):
                if item >= 0:
                    macropad.keyboard.press(item)
                else:
                    macropad.keyboard.release(-item)
            elif isinstance(item, float):
                time.sleep(item)
            elif isinstance(item, str):
                macropad.keyboard_layout.write(item)
            elif isinstance(item, list):
                for code in item:
                    if isinstance(code, int):
                        macropad.consumer_control.release()
                        macropad.consumer_control.press(code)
                    if isinstance(code, float):
                        time.sleep(code)
            elif isinstance(item, dict):
                if 'buttons' in item:
                    if item['buttons'] >= 0:
                        macropad.mouse.press(item['buttons'])
                    else:
                        macropad.mouse.release(-item['buttons'])
                macropad.mouse.move(item['x'] if 'x' in item else 0,
                                    item['y'] if 'y' in item else 0,
                                    item['wheel'] if 'wheel' in item else 0)
                if 'tone' in item:
                    if item['tone'] > 0:
                        macropad.stop_tone()
                        macropad.start_tone(item['tone'])
                    else:
                        macropad.stop_tone()
                elif 'play' in item:
                    macropad.play_file(item['play'])
    else:
        # Release any still-pressed keys, consumer codes, mouse buttons
        # Keys and mouse buttons are individually released this way (rather
        # than release_all()) because pad supports multi-key rollover, e.g.
        # could have a meta key or right-mouse held down by one macro and
        # press/release keys/buttons with others. Navigate popups, etc.
        for item in sequence:
            if isinstance(item, int):
                if item >= 0:
                    macropad.keyboard.release(item)
            elif isinstance(item, dict):
                if 'buttons' in item:
                    if item['buttons'] >= 0:
                        macropad.mouse.release(item['buttons'])
                elif 'tone' in item:
                    macropad.stop_tone()
        macropad.consumer_control.release()
        if key_number < 12:  # No pixel for encoder button
            macropad.pixels[key_number] = apps[app_index].macros[key_number][0]
            macropad.pixels.show()
    time.sleep(0.01)


