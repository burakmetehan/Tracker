import tkinter as tk
from tkinter import ttk

import Functions
from Globals import ICON_PATH, ACTIVITY_FILE_PATH


class ActivityWindow():
    def __init__(self, master, title:str="All Activities"):

        self.popup = tk.Toplevel(master)
        self.popup.title(title)        
        self.popup.iconbitmap(ICON_PATH)
        self.popup.resizable(0,0)
        self.popup.geometry("+250+250")

        self.activities = Functions.read_json(ACTIVITY_FILE_PATH)
        self.total_activities = int(self.activities["metadata"]["total_activity"])

        

        self.create_widgets()


    def create_widgets(self):
        self.header = ttk.Label(self.popup, text="ACTIVITIES", font=("", 25)).pack()
        self.insert_seperator(0.4)
    
        self.activities_frame = ttk.Frame(self.popup)
        self.activities_frame.pack()
        self.main_label()
        self.add_all_activity(1)

        self.horizontal_seperators()
        self.vertical_seperatators()


    def main_label(self):
        self.category = ttk.Label(self.activities_frame, text="Category:")
        self.category.grid(row=0, column=0, sticky="w")
        

        self.subcategory = ttk.Label(self.activities_frame, text="Subcategory:")
        self.subcategory.grid(row=0, column=1, sticky="w")

        self.description = ttk.Label(self.activities_frame, text="Description:")
        self.description.grid(row=0, column=2, sticky="w")

        self.time = ttk.Label(self.activities_frame, text="Time:")
        self.time.grid(row=0, column=3)

        self.start_time = ttk.Label(self.activities_frame, text="Start Time:")
        self.start_time.grid(row=0, column=4)


    def add_all_activity(self, previous_row_number):
        for i in range(self.total_activities):
            activity = self.activities["ACTIVITY"][f"activity_{i}"]

            self.add_one_activity(activity["category"], activity["subcategory"], activity["description"], activity["spent_time"], activity["start_time"], i+previous_row_number)


    def  add_one_activity(self, cat:str, subcat:str, desp:str, spent_time:int, start_time:str, row_number):
        """ Adding One Row: Category, Subcategory, Description, Spent Time, Start Time """
        ttk.Label(self.activities_frame, text=cat, wraplength=150).grid(row=row_number, column=0, sticky="w")
        ttk.Label(self.activities_frame, text=subcat, wraplength=150).grid(row=row_number, column=1, sticky="w")
        ttk.Label(self.activities_frame, text=desp, wraplength=450).grid(row=row_number, column=2, sticky="w")
        ttk.Label(self.activities_frame, text=spent_time, wraplength=150).grid(row=row_number, column=3)
        ttk.Label(self.activities_frame, text=start_time, wraplength=150).grid(row=row_number, column=4, sticky="w")


    def insert_seperator(self, relWidth:float=1):
        seperator_frame = ttk.Frame(self.popup)
        ttk.Separator(seperator_frame, orient="horizontal").place(relwidth=relWidth, relx=(1-relWidth)/2)
        seperator_frame.pack(fill="x")
    

    def horizontal_seperators(self):
        for i in range(self.total_activities):
            ttk.Separator(self.activities_frame, orient="horizontal").grid(row=i, column=0, columnspan=5, sticky="ews")

    def vertical_seperatators(self):
        for i in range(4):
            ttk.Separator(self.activities_frame, orient="vertical").grid(row=1, column=i, rowspan=self.total_activities+1, sticky="nse")