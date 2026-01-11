import time
import threading
import tkinter as tk
from tkinter import ttk, PhotoImage


class PomodoroTimer:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x300")
        self.root.title("Pomodoro Timer")
        self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file='pomodoro_icon.png'))
        self.root.resizable(False, False)

        self.s = ttk.Style()
        self.s.configure("TNotebook.Tab", font=("Ubuntu", 16))
        self.s.configure("TButton", font=("Ubuntu", 16))

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", pady=10, expand=True)

        self.tab1 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab2 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab3 = ttk.Frame(self.tabs, width=600, height=100)

        self.pomodoro_timer_label = ttk.Label(self.tab1, text='25.00', font=('Ubuntu', 48))
        self.pomodoro_timer_label.pack(pady=20)

        self.short_break_timer = ttk.Label(self.tab2, text='5.00', font=('Ubuntu', 48))
        self.short_break_timer.pack(pady=20)

        self.pomodoro_timer_label = ttk.Label(self.tab3, text='15.00', font=('Ubuntu', 48))
        self.pomodoro_timer_label.pack(pady=20)

        self.tabs.add(self.tab1, text="Pomodoro")
        self.tabs.add(self.tab2, text="Short Break")
        self.tabs.add(self.tab3, text="Long Break")

        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=10)

        self.start_button = ttk.Button(self.grid_layout, text="Start", command=self.start_timer_thread)
        self.start_button.grid(row=0, column=0)

        self.skip_button = ttk.Button(self.grid_layout, text="Skip", command=self.skip_clock)
        self.skip_button.grid(row=0, column=1)

        self.reset_button = ttk.Button(self.grid_layout, text="Reset", command=self.reset_clock)
        self.reset_button.grid(row=0, column=2)



        self.root.mainloop()

    def start_timer_thread(self):
        pass
    def start_timer(self):
        pass
    def reset_clock(self):
        pass
    def skip_clock(self):
        pass
PomodoroTimer()