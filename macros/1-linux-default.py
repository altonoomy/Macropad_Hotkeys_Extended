# MACROPAD Hotkeys example: Custom Windows configuration.

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
from adafruit_hid.consumer_control_code import ConsumerControlCode

app = {                    # REQUIRED dict, must be named 'app'
    'name' : 'Desktop',  # Application name
    'macros' : [           # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x000000, 'Kill', [0.2, Keycode.ALT, Keycode.F4]),
        (0x000000, 'Minimize', [Keycode.WINDOWS, Keycode.PAGE_DOWN]),
        (0x000000, 'Mute', [[ConsumerControlCode.MUTE]]),
        # 2nd row ----------
        (0x000000, 'Prev', [[ConsumerControlCode.SCAN_PREVIOUS_TRACK]]),
        (0x000000, 'Play/Pause', [[ConsumerControlCode.PLAY_PAUSE]]),
        (0x000000, 'Next', [[ConsumerControlCode.SCAN_NEXT_TRACK]]),
        # 3rd row ----------
        (0x000000, 'Lock', [Keycode.WINDOWS, 'l']),
        (0x000000, 'AlTab', [Keycode.ALT, Keycode.TAB]),
        (0x000000, 'TTY', [Keycode.CONTROL, Keycode.ALT, 't']), #opens terminal
        # 4th row ----------
        (0x000000, 'Save', [Keycode.LEFT_CONTROL, 'S']),   # ctrl+s
        (0x000000, 'Copy', [Keycode.CONTROL, 'c']),   # ctrl+c
        (0x000000, 'Paste', [Keycode.LEFT_CONTROL, 'v']),  # ctrl+v
        # Encoder button ---
        (0xe50e00, 'SOUND', []) # Close window/tab
    ]
}
