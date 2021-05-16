# Keylogger 
This is just a simplified version of a system keylogger. Could be configure on a system to be able to run on start up and potentialy start logging all the current user activity.

For now it's only work on Unix like systems but as soon as possibile the windows part will be implemented! 

As it is, depends on Xlib **python3-xlib** and works by relying on the X server but for the future this will be an option because it should be able to work without gui library.

## Command Line option

OPTION | INFO | DEFAULT
|---|---|---|
| -s | start the keylogger | True
| -k | kill the keylogger | False
| -o | store collected data in a different location | /var/log/keylogger.log
| -v | show keylogger version | 
| -h | show usage information |

## Start the keylogger

```bash
python3 keylogger.py
```

or 

```bash
python3 keylogger.py -s
```

## Change log output on a different file

```bash
python3 keylogger.py -o test.log
```

## Kill the keylogger 

```bash
python3 keylogger.py -k
```

When it start automatically store main thread PID informations so when you give this command it retrive current PID and kill the program. 
