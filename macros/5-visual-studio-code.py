# MACROPAD Hotkeys example: Custom Windows configuration.

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
from adafruit_hid.consumer_control_code import ConsumerControlCode

app = {                    # REQUIRED dict, must be named 'app'
    'name' : 'Visual Studio Code',  # Application name
    'macros' : [           # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x000000, 'Close', [Keycode.CONTROL, 'w']),
        (0x000000, 'Minimize', [Keycode.WINDOWS, Keycode.PAGE_DOWN]),
        (0x000000, 'New', [Keycode.CONTROL, 'n']),
        # 2nd row ----------
        (0x000000, 'Prev', [[ConsumerControlCode.SCAN_PREVIOUS_TRACK]]),
        (0x000000, 'Play/Pause', [[ConsumerControlCode.PLAY_PAUSE]]),
        (0x000000, 'Next', [[ConsumerControlCode.SCAN_NEXT_TRACK]]),
        # 3rd row ----------
        (0x000000, 'Run', [Keycode.CONTROL, 'b']),
        (0x000000, 'Kill', [Keycode.CONTROL, 'c']),
        (0x000000, 'Undo', [Keycode.CONTROL, 'z']), #opens terminal
        # 4th row ----------
        (0x000000, 'Save', [Keycode.CONTROL, 's']),   # ctrl+s
        (0x000000, 'Copy', [Keycode.CONTROL, 'c']),   # ctrl+c
        (0x000000, 'Paste', [Keycode.CONTROL, 'v']),  # ctrl+v
        # Encoder button ---
        (0xe50e00, 'SOUND', []) # Close window/tab
    ]
}
