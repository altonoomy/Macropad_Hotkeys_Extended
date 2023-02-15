
# MACROPAD Hotkeys example: Firefox web browser for Windows

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
from adafruit_hid.consumer_control_code import ConsumerControlCode
app = {                       # REQUIRED dict, must be named 'app'
    'name' : 'Firefox/YouTube', # Application name
    'macros' : [              # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x00d3ff , '-Speed', [Keycode.SHIFT, ',']),
        (0x000000, 'FS', ['f']),
        (0x00d3ff, '+Speed', [Keycode.SHIFT, '.']),
        # 2nd row ----------
        (0x000000, 'Prev', [Keycode.SHIFT, 'p']),
        (0x000000, 'Play/Stop', ['k']),
        (0x000000, 'Next', [Keycode.SHIFT, 'n']),                     # Scroll down
        # 3rd row ----------
        (0x000000, '-Seek', ['j']),
        (0x000000, 'CC', ['c']), #twitch specific starts here
        (0x000000, '+Seek', ['l']),
        # 4th row ----------
        (0x00d3ff, '-Vol', [Keycode.DOWN_ARROW]), # twitch following
        (0x000000, 'Mute', ['m']),     # dev mode
        (0x00d3ff, '+Vol', [Keycode.UP_ARROW]),     # digikey in a new tab
        # Encoder button ---
        (0x000000, '', []) # Close window/tab
    ]
}
