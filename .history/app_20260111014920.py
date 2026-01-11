from collections import defaultdict
import csv
import datetime
from logging import root
import msvcrt
from multiprocessing import process
from pathlib import Path
import threading
import time
import tkinter.filedialog
import os
import win32api
import win32con
import win32process
import win32gui
from pomodoro_timer import PomodoroTimer

CONFIG_PATH = Path(os.environ["APPDATA"]) / "pomodoro_tracker" / "empty.txt"
CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

def job(): 
    running = False
    return running

def activeWindow():
    try:
        window = win32gui.GetForegroundWindow()
        if not window:
            return None
        _, pid = win32process.GetWindowThreadProcessId(window)
        if not pid or pid == 0:
            return None
        # Request only PROCESS_QUERY_LIMITED_INFORMATION
        handle = win32api.OpenProcess(win32con.PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not handle:
            return None
        # ... perform operations with the handle ...
        active_window_path = win32process.GetModuleFileNameEx(handle, 0)
        win32api.CloseHandle(handle)
        return active_window_path
    except win32api.error as e:
        if e.winerror == 5:  # ERROR_ACCESS_DENIED
            print(f"Access Denied: {e}")
        else:
            raise
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

class saveFiles:
    def save_folder(self, config_path: Path):
        # Prompt a file dialog for directory selection.
        PathFileName = str(Path(tkinter.filedialog.askdirectory(mustexist=True, title="Select Directory to Save Time Tracking CSV")))
        if PathFileName:
            config_path.write_text(PathFileName)
        # Save the selected directory path for future use.
        # Check on subsequent launches if a path is already saved.

    def save_time_tracking(self, txt, time_tracking):

        fields = ['Run Time', 'Application Path', 'Time']
        today = str(datetime.date.today())
        file_name = '{today}.csv'.format(today=today)
        file = os.path.join(txt, file_name)

        '''
        for key, value in time_tracking.items():
            t = time.gmtime(value)
            values = time.strftime("%H:%M:%S", t)
            rows.append([today, key, values])   
        '''
        
        with open(file, 'w') as csvfile:
            fields = ['Run Time', 'Application Path', 'Time']
            csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
            csvwriter.writeheader()
            csvwriter.writerow({'Run Time': {today}})
            for key, value in time_tracking.items():
                t = time.gmtime(value)
                values = time.strftime("%H:%M:%S", t)
                csvwriter.writerow({
                    "Run Time": today,
                    "Application Path": key,
                    "Time": time.strftime("%H:%M:%S", time.gmtime(value))
                })
        return True

class timeTracker:
    def __init__(self):
        self.time_tracking = defaultdict(float)
        self.running = True
        self.last_autosave = time.time()

    def print_time_tracking(self, time_tracking):
        print("End of Day Time Tracking:")
        for key, value in time_tracking.items():
            t = time.gmtime(value)
            values = time.strftime("%H:%M:%S", t)
            print("{} ({})".format(key, values))

    # def changing_names(time_tracking):

    def stop(self):
        self.running = False

    def timed_process(self):
        process = activeWindow()
        start = time.time()

        while self.running:
            time.sleep(1)
            new_process = activeWindow()

            if time.time() - self.last_autosave >= 300:
                try:
                    if txt:
                        saves.save_time_tracking(txt, self.time_tracking)
                except Exception as e:
                        print(f"Autosave failed: {e}")      
                self.last_autosave = time.time()
            if new_process != process:
                end = time.time()
                total = end - start
                self.time_tracking[process] += total
                process = activeWindow()
                start = time.time()

            if new_process is None:
                continue
        end = time.time()
        total = end - start
        if process:
            self.time_tracking[process] += total
    
    def on_close():
        tracker.stop()
        saves.save_time_tracking(txt, tracker.time_tracking)
        root.destroy()


# t = Timer(30.0, hello)

if __name__ == "__main__":
    tracker = timeTracker()
    saves = saveFiles()

    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text("")

    txt = CONFIG_PATH.read_text().strip()

    if txt == "":
        saves.save_folder(CONFIG_PATH)
        txt = CONFIG_PATH.read_text().strip()

    app = PomodoroTimer()  # creates root, but doesn't start mainloop yet

    tracking_thread = threading.Thread(target=tracker.timed_process, daemon=True)
    tracking_thread.start()

    def on_close():
        tracker.stop()
        saves.save_time_tracking(txt, tracker.time_tracking)
        app.root.destroy()

    app.root.protocol("WM_DELETE_WINDOW", on_close)
    app.run()
