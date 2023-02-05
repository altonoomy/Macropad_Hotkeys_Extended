# MACROPAD Hotkeys example: Custom Windows configuration.

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
from adafruit_hid.consumer_control_code import ConsumerControlCode

app = {                    # REQUIRED dict, must be named 'app'
    'name' : 'Konsole',  # Application name
    'macros' : [           # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x000000, '-Tab', [Keycode.CONTROL, Keycode.SHIFT, 'W']),
        (0x000000, 'Minimize', [Keycode.WINDOWS, Keycode.PAGE_DOWN]),
        (0x000000, '+Tab', [Keycode.CONTROL, Keycode.SHIFT, 'T']),
        # 2nd row ----------
        (0x000000, '<-Tab', [Keycode.SHIFT, Keycode.LEFT_ARROW]),
        (0x000000, 'Update', ['sudo apt update && sudo apt upgrade -y', Keycode.ENTER]),
        (0x000000, 'Tab->', [Keycode.SHIFT, Keycode.RIGHT_ARROW]),
        # 3rd row ----------
        (0x000000, 'Kill', [Keycode.CONTROL, 'C']),
        (0x000000, 'Clear', [Keycode.LEFT_CONTROL, 'l']), #opens windows task manager
        (0x000000, '-Line', [Keycode.ALT, Keycode.BACKSPACE]), #opens task manager
        # 4th row ----------
        (0x000000, 'Enter', [Keycode.ENTER]),   # ctrl+s

        (0x000000, 'Copy', [Keycode.CONTROL, Keycode.SHIFT, 'C']),   # ctrl+c
        (0x000000, 'Paste', [Keycode.CONTROL, Keycode.SHIFT, 'V']),  # ctrl+v
        # Encoder button ---
        (0x000000, 'SOUND', []) # Close window/tab
    ]
}
