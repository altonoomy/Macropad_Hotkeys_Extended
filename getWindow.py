import subprocess
import time
import io
import serial
import json
import adafruit_board_toolkit.circuitpython_serial


def getCurrentWindow():
    # Using xdotool to get the active window name. getactivewindow is used rather than getwindowfocus as it is more reliable.
    try:
        window = subprocess.run(['xdotool', 'getactivewindow', 'getwindowname'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    except BaseException as error:
        print(f"An exception occured: {error}")
    try:
         # What we will send to the board
        windowComponents = {'application': None, 'applicationFocus': None}
        windowSplit = window.split("—")
        browser = False
        if len(windowSplit) == 1:
            for x in windowSplit:
                if "-" in x.strip():
                    appComponent = x.split("-")
                    windowComponents["application"] = appComponent[-1].strip()
                    windowComponents["applicationFocus"] = "".join(appComponent[0:-1]).strip()
                    browser = True
            if not browser:
                windowComponents['application'] = windowSplit[0]
                windowComponents['applicationFocus'] = windowSplit[1]
        elif len(windowSplit) > 1:
            windowComponents["application"] = windowSplit[-1].strip()
            windowComponents['applicationFocus'] = "".join(windowSplit[0:-1]).strip()
    except IndexError:
        pass
    return windowComponents

def getPort():
    while True:
        print("Looking for data port...")
        if adafruit_board_toolkit.circuitpython_serial.data_comports():
            print("Port found!")
            # sleep to allow time for connection to be made
            time.sleep(0.1)
            for port in adafruit_board_toolkit.circuitpython_serial.data_comports():
                return port
        else:
            print("No port found.")
            time.sleep(1)

# Set up serial channel and set timeout
def getChannel(port):
    channel = serial.Serial(port)
    channel.timeout = 0.03 # originally 0.05
    return channel
                               
def startWindowWatch():
    while True:           
        channelPort = getPort()
        channel = getChannel(channelPort.device)
        while True:
            windowComponents = getCurrentWindow()
            print(f"App: {windowComponents['application']} | Tab: {windowComponents['applicationFocus']}")
            # Send data to the serial port
            try:
                channel.write(json.dumps(windowComponents).encode())
                channel.write(b"\r\n")
            except serial.serialutil.SerialException:
                break
        print(f"{channelPort.product} disconnected.")
            #channel.close()

if __name__ == "__main__":
    startWindowWatch()