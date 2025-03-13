import pyautogui
import time
import threading
import tkinter as tk
from tkinter import messagebox
import keyboard

#Default settings, default interval in sec (should be able to be changed later), default hotkey
clicking = False
click_interval = 0.1 
hotkey = "f6"  

def clicker():
    """Function for auto-clicking."""
    global clicking
    while True:
        if clicking:
            #Click then wait a given interval
            pyautogui.click()
            time.sleep(click_interval)
        else:
            #Wait short intervals to not fry the CPU
            time.sleep(0.1)  

def toggle_clicking():
    """Start/Stop clicking when hotkey is pressed."""
    global clicking
    clicking = not clicking
    status_label.config(text=f"Status: {'ON' if clicking else 'OFF'}")

def set_interval():
    """Set the click interval."""
    global click_interval
    try:
        click_interval = float(interval_entry.get())  #Convert input to float 
        messagebox.showinfo("Success", f"Click interval set to {click_interval} seconds!")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number!")

def set_hotkey():
    """Set the custom hotkey."""
    global hotkey
    new_hotkey = hotkey_entry.get().strip().lower()

    if new_hotkey:
        keyboard.remove_hotkey(hotkey)  
        hotkey = new_hotkey
        keyboard.add_hotkey(hotkey, toggle_clicking)
        messagebox.showinfo("Success", f"Hotkey set to '{hotkey}'")
    else:
        messagebox.showerror("Error", "Please enter a valid hotkey!")

#Start the clicking thread
click_thread = threading.Thread(target=clicker, daemon=True)
click_thread.start()

#Create the GUI window
root = tk.Tk()
root.title("AutoClicker")
root.geometry("350x250")

#Click interval input
tk.Label(root, text="Click Interval (seconds):").pack()
interval_entry = tk.Entry(root)
interval_entry.pack()
interval_entry.insert(0, "0.1")

#Set interval button
set_btn = tk.Button(root, text="Set Interval", command=set_interval)
set_btn.pack()

#Hotkey input
tk.Label(root, text="Set Hotkey:").pack()
hotkey_entry = tk.Entry(root)
hotkey_entry.pack()
hotkey_entry.insert(0, hotkey)  # Display default hotkey

#Set hotkey button
hotkey_btn = tk.Button(root, text="Set Hotkey", command=set_hotkey)
hotkey_btn.pack()

#Start/Stop button
toggle_btn = tk.Button(root, text="Start / Stop", command=toggle_clicking)
toggle_btn.pack()

#Status label
status_label = tk.Label(root, text="Status: OFF", fg="red")
status_label.pack()

#Exit button
exit_btn = tk.Button(root, text="Exit", command=root.quit)
exit_btn.pack()

#Bind default hotkey
keyboard.add_hotkey(hotkey, toggle_clicking)

#Run the GUI
root.mainloop()