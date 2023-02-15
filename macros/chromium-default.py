# MACROPAD Hotkeys example: Custom Windows configuration.

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
from adafruit_hid.consumer_control_code import ConsumerControlCode

app = {                    # REQUIRED dict, must be named 'app'
    'name' : 'Chromium/Default',  # Application name
    'macros' : [           # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0xbf2dff, '-Tab', [Keycode.CONTROL, 'w']),
        (0x000000, 'Reopen', [Keycode.CONTROL, Keycode.SHIFT, 't']),
        (0xbf2dff, '+Tab', [Keycode.CONTROL, 't']),
        # 2nd row ----------
        (0xbf2dff, 'Prev', [[ConsumerControlCode.SCAN_PREVIOUS_TRACK]]),
        (0x000000, 'Play/Pause', [[ConsumerControlCode.PLAY_PAUSE]]),
        (0xbf2dff, 'Next', [[ConsumerControlCode.SCAN_NEXT_TRACK]]),
        # 3rd row ----------
        (0xbf2dff, '<-Tab', [Keycode.CONTROL, Keycode.SHIFT, Keycode.TAB]),
        (0x000000, 'Mute', ['m']),
        (0xbf2dff, 'Tab->', [Keycode.CONTROL, Keycode.TAB]),
        # 4th row ----------
        (0xbf2dff, 'Enter', [Keycode.ENTER]),   # ctrl+s
        (0x000000, 'Copy', [Keycode.CONTROL,'c']),   # ctrl+c
        (0xbf2dff, 'Paste', [Keycode.CONTROL, 'v']),  # ctrl+v
        # Encoder button ---
        (0x000000, 'SOUND', []) # Close window/tab
    ]
}
