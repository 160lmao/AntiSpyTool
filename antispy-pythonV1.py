from pynput import keyboard
import pyautogui
import time
import threading
import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import pygetwindow as gw
import json
import os
from pathlib import Path

# Define the path to the settings file
settings_file = Path(os.getenv('USERPROFILE')) / 'Desktop' / 'AntiSpy' / 'settings.json'

# Check if the settings file exists
if not settings_file.is_file():
    # If not, create the AntiSpy directory and the settings file
    settings_file.parent.mkdir(parents=True, exist_ok=True)
    with open(settings_file, 'w') as f:
        json.dump({'password': 'default'}, f)

# Load the settings
with open(settings_file) as f:
    settings = json.load(f)

# Now you can use settings['password'] instead of "Dasiel121." in your check_password function
stop_explorer_loop = False

def close_explorer():
    global stop_explorer_loop
    while not stop_explorer_loop:
        os.system("taskkill /f /im explorer.exe")
        time.sleep(1)

# Start the explorer closing loop in a new thread
explorer_thread = threading.Thread(target=close_explorer)
explorer_thread.start()

class TypingDetector:
    def __init__(self):
        self.typing = False
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        if not self.typing:
            self.typing = True
            threading.Timer(1, self.reset_typing).start()

    def reset_typing(self):
        self.typing = False
    def is_typing(self):
        return self.typing

def spam_keys(detector):
    while True:
        if not detector.is_typing():
            for win in gw.getAllWindows():
                # Exclude the GUI window and the error message box
                if win.title not in ["Anti-Spy Tool By Daniel", "Error"]: 
                    win.minimize()
        time.sleep(1)  # Wait for 1 second



detector = TypingDetector()
threading.Thread(target=spam_keys, args=(detector,)).start()

# Add a counter for incorrect password attempts
incorrect_attempts = 0

def check_password():
    global incorrect_attempts, stop_explorer_loop
    password = password_entry.get()
    if password != settings['password']:
        incorrect_attempts += 1
        if incorrect_attempts >= 3:
            subprocess.run(["nircmd", "exitwin", "reboot"])
        else:
            messagebox.showerror("Error", "Incorrect password. You have " + str(3 - incorrect_attempts) + " attempts left.")
    else:
        # Stop the explorer closing loop and restart explorer
        stop_explorer_loop = True
        os.system("start explorer.exe")
        subprocess.run(["nircmd.exe", "win", "show", "class", "Shell_TrayWnd"])
        subprocess.run(["nircmd.exe", "win", "show", "class", "Progman"])
        os._exit(0)  # Exit the script entirely

root = tk.Tk()
root.geometry("180x80")
root.title("Anti-Spy Tool By Daniel")  # Set the title of your GUI window
root.focus_force = True

# Make the window full screen
root.attributes('-fullscreen', True)

# Remove the title bar
root.overrideredirect(True)

# Create a custom submit button
submit_button = tk.Button(root, text="Submit", command=check_password, bg="Grey", fg="white", font=("Helvetica", 16))

# Position the button in the center of the screen
submit_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

password_entry = tk.Entry(root, show="*", font=("Helvetica", 16))
password_entry.pack()

# Position the entry in the center of the screen
password_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

root.mainloop()
