import ctypes
from datetime import datetime, timedelta
import signal
import sys
from time import sleep
import winsound

NOTE_C = 523
NOTE_D = 587
NOTE_E = 659
NOTE_DURATION_MS = 500

SLEEP_DURATION_SEC = 0.02

WORK_TIME_MIN = 20
REST_TIME_MIN = 5

def sigint_handler(sig, frame):
    print("Done. Have a nice day :)")
    sys.exit(1)

class TimePeriod:
    def __init__(self, time_min, icon, title, description, sound_asc=True):
        self.time_sec = time_min * 60
        self.icon = icon
        self.title = title
        self.description = description
        self.sound_ascending = sound_asc

    def __str__(self):
        ret = "=== " + self.title + "===" + "\n"
        ret += "Time: " + self.prettyDelta(timedelta(seconds=self.time_sec)) + "\n"
        ret += self.description
        return ret

    def sleep(self):
        start = datetime.now()
        end = start + timedelta(seconds=self.time_sec)

        print("Time started at", start.strftime("%I:%M:%S %p"))
        while datetime.now() < end:
            remaining = end - datetime.now()
            print(self.prettyDelta(remaining), "\r", end="")
            sleep(SLEEP_DURATION_SEC)

        print()
        self.beep()

    def beep(self):
        notes = (NOTE_C, NOTE_D, NOTE_E)
        if not self.sound_ascending:
            notes = reversed(notes)

        for note in notes:
            winsound.Beep(note, NOTE_DURATION_MS)

    def prettyDelta(self, delta):
        rem_mins = int(delta.seconds / 60)
        rem_secs = delta.seconds % 60
        return str(rem_mins).zfill(2) + ":" + str(rem_secs).zfill(2)

MB_ICONINFORMATION = 0x0040
MB_ICONSTOP = 0x0010
MB_SETFOREGROUND = 0x0001000
MB_TOPMOST = 0x00040000

WORK = TimePeriod(WORK_TIME_MIN, MB_ICONINFORMATION, "Work", "Go back to work", False)
REST = TimePeriod(REST_TIME_MIN, MB_ICONSTOP, "Rest", "Stop working, take a rest", True)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)

    print("Pomodoro!", WORK_TIME_MIN, "minutes of work,",
          REST_TIME_MIN, "minutes of rest.")
    winsound.Beep(NOTE_C, NOTE_DURATION_MS)
    while (True):
        for period in (WORK, REST):
            print()
            print(period)
            ctypes.windll.user32.MessageBoxW(0, period.description,
                                             period.title,
                                             period.icon) # | MB_TOPMOST)# | MB_SETFOREGROUND)
            period.sleep()

# FIXME input 20/5
# FIXME messagebox in background

# EOF
