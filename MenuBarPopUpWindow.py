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
        self.popup.geometry("300x150")


        self.config_file = Functions.read_json(CONFIG_FILE_PATH)
        
        """ Activity Time """
        self.activity_time_frame = ttk.Frame(self.popup)
        self.activity_time_frame.pack()

        self.activity_time_text = ttk.Label(self.activity_time_frame, text="Activity Time")
        self.activity_time_text.pack()

        self.activity_time_entry = PlaceHolderEntry(self.activity_time_frame, self.config_file["APP"]["minute"])
        self.activity_time_entry.pack()

        self.activity_time_button = ttk.Button(self.activity_time_frame, text="Apply", command=self.activity_time_update)
        self.activity_time_button.pack()


        """ Button Part """
        self.button = ttk.Button(self.popup, text="Close", command=self.close)
        self.button.pack()


    def activity_time_update(self):
        self.config_file["APP"]["minute"] = self.activity_time_entry.get()
        Functions.update_json(CONFIG_FILE_PATH, self.config_file)
    
    def close(self):
        self.popup.destroy()