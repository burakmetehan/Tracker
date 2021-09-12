import tkinter as tk
from tkinter import ttk
from time import sleep
import json
import os, subprocess


def read_activity():
    with open("./files/today_activity.json", "r") as activity:
        return json.load(activity)

win = tk.Tk()

frame = ttk.Frame(win)


activity = read_activity()
print(activity)
print(type(activity))

ttk.Label(win, padding=(5, 5))

zero = 0




frame.pack()
win.mainloop()

