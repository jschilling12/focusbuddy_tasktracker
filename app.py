from collections import defaultdict
import time
import win32api
import win32con
import win32process
import win32gui

time_tracking = defaultdict(float)


def activeWindow():
    try:
        window = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(window)
        # Request only PROCESS_QUERY_LIMITED_INFORMATION
        handle = win32api.OpenProcess(win32con.PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        # ... perform operations with the handle ...
        active_window_path = win32process.GetModuleFileNameEx(handle, 0)
        win32api.CloseHandle(handle)
        return active_window_path
    except win32api.error as e:
        if e.winerror == 5:  # ERROR_ACCESS_DENIED
            print(f"Access Denied: {e}")
        else:
            raise


process = activeWindow()
start = time.time()
    
while True:
    time.sleep(1)

    new_process = activeWindow()

    if new_process != process:
        end = time.time()
        total = end - start
        time_tracking[process] += total
        process = activeWindow()
        start = time.time()

    elif new_process is None:
        end = time.time()
        total = end - start
        time_tracking[process] += total
        process = activeWindow()
        start = time.time()


