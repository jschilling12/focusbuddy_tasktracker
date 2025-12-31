from collections import defaultdict
import csv
import datetime
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

def print_time_tracking(time_tracking):
    print("End of Day Time Tracking:")
    for key, value in time_tracking.items():
        t = time.gmtime(value)
        values = time.strftime("%H:%M:%S", t)
        print("{} ({})".format(key, values))

def save_time_tracking(time_tracking):
    fields = ['Run Time', 'Application Path', 'Time']
    filename = "time_tracking.csv"
    today = str(datetime.date.today())

    '''
     for key, value in time_tracking.items():
        t = time.gmtime(value)
        values = time.strftime("%H:%M:%S", t)
        rows.append([today, key, values])   
    '''
    with open(filename, 'w') as csvfile:
        fields = ['Run Time', 'Application Path', 'Time']
        csvwriter = csv.DictWriter(csvfile, fieldnames=fields)
        csvwriter.writeheader()
        csvwriter.writerow({'Run Time': {today}})
        for key, value in time_tracking.items():
            t = time.gmtime(value)
            values = time.strftime("%H:%M:%S", t)
            csvwriter.writerow({'Application Path': {key}})
            csvwriter.writerow({'Application Path': {values}})
    return True



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
                running = False

        elif new_process is None:
            end = time.time()
            total = end - start
            time_tracking[process] += total
            process = activeWindow()
            start = time.time()
    return save_time_tracking(time_tracking)


if __name__ == "__main__":
    print(timed_process())
