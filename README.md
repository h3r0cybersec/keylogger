# Introduction
For now there are two different versions of keylogger:

- **v1**
- **v2**

## V1 keylogger version
The **v1** folder contains a keylogger version that make use of **pyxhook** module that allow to build a keylogger that throught Xlib is able to catch all user input comming from the keyboard.

### Pros
- show for each key show also the information about:
    - WindowName
    - ProcName 
- each keys are stored in a buffer that is flushed only when user press **enter** to start a new line, in this way we can see always that has been already pressed on a line instead of multiple lines

### Cons
- need Xserver 
- run only on linux


## V2 keylogger version
The **v2** folder contains a keylogger version that make use of **keyboard** module that allow to build a keylogger that is indipendent from the operative system and from the current display manager.

### Pros
- can run potentially on Windows, Linux, Mac
- indipendent from display manager
- each keys are stored in a buffer that is flushed only when user press **enter** to start a new line, in this way we can see always that has been already pressed on a line instead of multiple lines

### Cons
- Todo

## Usage
You need just to choose your version 

```bash
git clone https://github.com/h3r0cybersec/keylogger.git
cd keylogger/v1 or cd keylogger/v2
```

install all dependenties

```bash
pip3 install -r requirements.txt
```

run as sudo

```bash
# run as daemon
sudo python3 keylogger.py &
```

**NOTE: different version of keylogger could have variation on startup options make sure to take a look at the code if you running in troubles if there's not a README file in the specific version folder.**