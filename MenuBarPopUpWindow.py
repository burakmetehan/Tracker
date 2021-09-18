from Functions import read_json
import tkinter as tk
from tkinter import ttk

from PlaceHolderEntry import *
import Functions
from Globals import *


class ConfigPopUpWindow():
    def __init__(self, master, title:str):

        self.popup = tk.Toplevel(master)
        self.popup.title(title)
        self.popup.iconbitmap(ICON_PATH)
        self.popup.geometry("250x250")


        self.config_file = Functions.read_json(CONFIG_FILE_PATH)
        
        """ Activity Time """
        self.activity_time_frame = ttk.Frame(self.popup)
        self.activity_time_frame.pack()

        self.activity_time_text = ttk.Label(self.activity_time_frame, text="Activity Time")
        self.activity_time_text.pack()

        self.activity_time_entry = PlaceHolderEntry(self.activity_time_frame, self.config_file["APP"]["minute"])
        self.activity_time_entry.pack()


        """ Break Time """
        self.break_time_frame = ttk.Frame(self.popup)
        self.break_time_frame.pack()

        self.break_time_text = ttk.Label(self.break_time_frame, text="Break Time")
        self.break_time_text.pack()

        self.break_time_entry = PlaceHolderEntry(self.break_time_frame, self.config_file["APP"]["break"])
        self.break_time_entry.pack()


        """ Auto Break """
        self.auto_break_frame = ttk.Frame(self.popup)
        self.auto_break_frame.pack()

        self.auto_break_text = ttk.Label(self.auto_break_frame, text="Auto Break")
        self.auto_break_text.pack()

        self.auto_break_combobox = ttk.Combobox(self.auto_break_frame, values=(True, False), state="readonly")
        self.auto_break_combobox.current(0 if self.config_file["APP"]["auto_break"] else 1)
        self.auto_break_combobox.pack()


        """ Button Part """
        self.apply_button = ttk.Button(self.popup, text="Apply", command=self.config_update)
        self.apply_button.pack()

        self.button = ttk.Button(self.popup, text="Close", command=self.close)
        self.button.pack()


    def config_update(self):
        self.config_file["APP"]["minute"] = self.activity_time_entry.get()
        self.config_file["APP"]["break"] = self.break_time_entry.get()
        self.config_file["APP"]["auto_break"] = "True" == self.auto_break_combobox.get()
        Functions.update_json(CONFIG_FILE_PATH, self.config_file)


    def close(self):
        self.popup.destroy()
