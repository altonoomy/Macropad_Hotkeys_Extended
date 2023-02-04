# Macropad_Hotkeys_Extended
An extension of Adafruit Macropad_Hotkeys for the Macropad RP2040.

# Additions
- Automatic macro switching. Macros now switch depending on the window focus. 
- Rotary encoder now functions as a volume control knob. Pressing the switch locks the current macro to prevent switching.
- Able to detect browser tab information which allows for website specific macros.
- Option for default macros to fall back on if no application macro is available.

# Installation
**Make sure to backup any files and macros before continuing!**
1. If you have not installed CircuitPython onto your board, install it per [Adafruit's Macropad CircuitPython guide](https://learn.adafruit.com/adafruit-macropad-rp2040/circuitpython). If you have CircuitPython installed, simply drag `code.py` and `boot.py` into your CIRCUITPYTHON directory, replacing the files if you had Macropad_Hotkeys already installed. Ensure contents of `lib/` are also present.
2. Install `xdotool` with your preferred package manager e.g. `apt-get install xdotool`. See [xdotool](https://github.com/jordansissel/xdotool) for more information. 

# Usage
Run `python3 getWindow.py` in a terminal and plug in your board, or vice versa. The current application and the application focus will now be displayed.

# Macro names
Macros will switch depending on the name of the current program in use. Both the macro name (not file name!) and the application name **must** be the same for switching to occur. Refer to stdout of `getWindow.py` to get the name of your application.
For browser tab switching, ensure that you name your macros according to the following standard:

` Browser/Website ` e.g. `Firefox/Youtube`, `Brave/Plex`, etc. 

(The full name, e.g. 'Mozilla Firefox' or 'Google Chrome', is not necessary, as it would not fit on the display.) 

Default macros are recommended in case no application macro is available. The "desktop" default should be named to whatever the application name is while on your desktop (refer to `getWindow.py`). For browser default, simply name to `Browser/Default`. 

# Configuration
Due to the arbitrary nature of website titles, it is difficult to predict how tab names will be displayed. Currently, the program looks for any dashes seperated by spaces to differentiate between the website name and any additional information the designer chose to include. The program may be changed to include different seperators, but for most sites, seperating by dash is sufficient. If a tab name is 'Subscriptions - Youtube', 'YouTube' will be what the program looks for and switches to. 

# Compatibility
This has only been tested on Linux using X11 and likely does not work with Wayland. Compatibility will depend on whether `xdotool` or an equivalent program exists for the system. 
