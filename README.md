# Pomodoro_tracker

A process time tracking, and pomodoro timer. In an effort to review the week ensuring focus is key and using the pomodoro to avoid burn out.

## DevLogs

Devlogs from the conception of this tool can be found here.

[**Dev Logs**](https://jordanschilling.me/focus-buddy.html)

## Key Features

- **Pomodoro Timer** - Pomodoro timer to maintain focused work while avoiding burnout.
- **Process Time Tracker** - Automatic process tracker for Windows systems.
- **CSV Export** - Save your tracked time data for review

## Installation

```bash
# Clone the repository
git clone https://github.com/jschilling12/focusbuddy_tasktracker.git
cd focusbuddy_tasktracker

# Install dependencies
pip install pywin32 schedule
```

## Usage

```bash
python app.py
```

## Build as Executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name FocusBuddy app.py
```

The executable will be in the `dist/` folder.

## Project Structure

```
focusbuddy_tasktracker/
├── app.py              # Main entry point, time tracking logic
├── pomodoro_timer.py   # Tkinter GUI for pomodoro timer
├── saves.py            # CSV save/load utilities
├── db.py               # Database utilities
└── README.md
```

## Disclaimer

This is made with little to no AI. Hand written code credit to Jordan Schilling 
