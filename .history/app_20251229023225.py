from collections import defaultdict
import msvcrt
import time
import win32api
import win32con
import win32process
import win32gui



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

time_tracking = defaultdict(float)

# Main loop for the processes to count the number of seconds

def print_time_tracking(time_tracking):
    print("End of Day Time Tracking:")
    for key, value in time_tracking.items():
        t = time.gmtime(value)
        values = time.strftime("%H:%M:%S", t)
        print("{} ({})".format(key, values))

# def changing_names(time_tracking):

def timed_process():
    process = activeWindow()
    start = time.time()
    running = True

    while running:
        time.sleep(1)
        new_process = activeWindow()
        
        if new_process != process:
            end = time.time()
            total = end - start
            time_tracking[process] += total
            process = activeWindow()
            start = time.time()

        if msvcrt.kbhit():
            user_input = input().strip().lower()
            if user_input == "exit":
                end = time.time()
                total = end - start
                time_tracking[process] += total
                print_time_tracking(time_tracking)
                running = False
                pass

        elif new_process is None:
            end = time.time()
            total = end - start
            time_tracking[process] += total
            process = activeWindow()
            start = time.time()


if __name__ == "__main__":
    timed_process()
