import tkinter as tk
from datetime import datetime
import winsound

# Global flags
start_printed = False
stop_printed = True
done = False
finished = False
stop_clicked = False


class AlarmApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Alarm Clock")
        self.resizable(width=False, height=False)

        # Variables for dropdowns
        self.hr = tk.IntVar(value=12)
        self.min = tk.IntVar(value=0)
        self.ampm = tk.StringVar(value="AM")

        # Dropdown lists
        hours = list(range(1, 13))
        minutes = [f"{y:02d}" for y in range(60)]
        ampmlist = ["AM", "PM"]

        tk.OptionMenu(self, self.hr, *hours).pack(side="left")
        tk.Label(text=":").pack(side="left")
        tk.OptionMenu(self, self.min, *minutes).pack(side="left")
        tk.OptionMenu(self, self.ampm, *ampmlist).pack(side="left")

        # Buttons
        self.alarmbutton = tk.Button(self, text="Set Alarm", command=self.start_clock)
        self.cancelbutton = tk.Button(self, text="Cancel Alarm", command=self.stop_clock, state="disabled")
        self.stopalarmbutton = tk.Button(self, text="Stop Alarm", command=self.stop_audio, state="disabled")

        self.alarmbutton.pack()
        self.cancelbutton.pack()
        self.stopalarmbutton.pack()

        # Digital clock label
        self.clock_label = tk.Label(self, font=("Helvetica", 16))
        self.clock_label.pack(pady=10)
        self.update_clock()  # start updating the clock

    def update_clock(self):
        """Update the digital clock every second."""
        now = datetime.now().strftime("%I:%M:%S %p")
        self.clock_label.config(text=now)
        self.after(1000, self.update_clock)

    def start_clock(self):
        global done, start_printed, stop_printed, stop_clicked
        if not done:
            self.cancelbutton.config(state="active")
            self.alarmbutton.config(state="disabled")

            if not start_printed:
                print(f"Alarm set for {self.hr.get()}:{self.min.get():02d}{self.ampm.get()}")
                start_printed = True
                stop_printed = False

            # Convert to 24-hour format
            if self.ampm.get() == "AM":
                hour_value = self.hr.get() if self.hr.get() != 12 else 0
            else:
                hour_value = self.hr.get() if self.hr.get() == 12 else self.hr.get() + 12

            self.Alarm(f"{hour_value:02d}", f"{self.min.get():02d}")

        if stop_clicked:
            done = False
            start_printed = False
            stop_clicked = False

    def stop_clock(self):
        global done, stop_clicked
        print(f"Alarm set for {self.hr.get()}:{self.min.get():02d}{self.ampm.get()} has been cancelled")
        stop_clicked = True
        done = True
        self.cancelbutton.config(state="disabled")
        self.alarmbutton.config(state="active")

    def stop_audio(self):
        winsound.PlaySound(None, winsound.SND_PURGE)  # stop sound
        self.stopalarmbutton.config(state="disabled")
        self.alarmbutton.config(state="active")

    def Alarm(self, myhour, myminute):
        global done, start_printed, finished
        if not done:
            now = datetime.now()
            hour, minute = f"{now.hour:02d}", f"{now.minute:02d}"

            if hour == myhour and minute == myminute:
                print("Alarm is ringing!")
                winsound.PlaySound("MyAlarm.wav", winsound.SND_FILENAME | winsound.SND_LOOP)
                done = True
                finished = True
                self.cancelbutton.config(state="disabled")
                self.stopalarmbutton.config(state="active")
            else:
                self.after(1000, self.start_clock)

        if finished:
            start_printed = False
            finished = False


if __name__ == "__main__":
    app = AlarmApp()
    app.mainloop()
