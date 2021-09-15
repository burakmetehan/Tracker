from temporary_files.Functions import update_json
from tkinter import ttk
import time

import Functions
from Globals import *


class TodayPomodoro(ttk.Labelframe):
    def __init__(self, container):
        
        #============Label Frame=========
        super().__init__(container, text="Today's Pomodoros")

        self.create_widgets()


    def create_widgets(self):
        self.category = ttk.Label(self, text="Category:")
        self.category.grid(row=0, column=0)

        self.subcategory = ttk.Label(self, text="Subcategory:")
        self.subcategory.grid(row=0, column=1)

        self.description = ttk.Label(self, text="Description:")
        self.description.grid(row=0, column=2)

        self.time = ttk.Label(self, text="Time:")
        self.time.grid(row=0, column=3)

        self.start_time = ttk.Label(self, text="Start Time:")
        self.start_time.grid(row=0, column=4)

        self.today_pomodoro_frame = ttk.Frame(self)
        self.today_pomodoro_frame.grid(row=1, column=0, columnspan=5)


        """ Checking date whether it is appropriate or not """
        today_activities = Functions.read_json(TODAY_ACTIVITY_FILE_PATH)

        date = time.localtime()
        today_date = f"{date.tm_mday} {date.tm_mon} {date.tm_year}"

        if not self.check_date(today_date, today_activities["metadata"]["date"]): # Different day
            today_activities.pop("ACTIVITY")
            today_activities["metadata"]["total_activity"] = 0
            today_activities["metadata"]["date"] = today_date
            today_activities["ACTIVITY"] = {}
            Functions.update_json(TODAY_ACTIVITY_FILE_PATH, today_activities)

        self.add_all_activity(today_activities)


    def add_one_row(self, cat:str, subcat:str, desp:str, spent_time:int, start_time:str, row_number):
        """ Adding One Row: Category, Subcategory, Description, Spent Time, Start Time """
        ttk.Label(self.today_pomodoro_frame, text=cat).grid(row=row_number, column=0)
        ttk.Label(self.today_pomodoro_frame, text=subcat).grid(row=row_number, column=1)
        ttk.Label(self.today_pomodoro_frame, text=desp).grid(row=row_number, column=2)
        ttk.Label(self.today_pomodoro_frame, text=spent_time).grid(row=row_number, column=3)
        ttk.Label(self.today_pomodoro_frame, text=start_time).grid(row=row_number, column=4)


    def add_all_activity(self, today_activities):
        """ Adding All Today's Activity from today_activity.json """
        # Destroying existing content
        for child in self.today_pomodoro_frame.winfo_children():
            child.destroy()

        # Creating the content
        today_total_activity = int(today_activities["metadata"]["total_activity"])

        for i in range(today_total_activity):
            activity = today_activities["ACTIVITY"][f"activity_{i}"]

            self.add_one_row(activity["category"], activity["subcategory"], activity["description"], activity["spent_time"], activity["start_time"], i)


    def check_date(self, today_date, today_activities_date):
        if today_date == today_activities_date: # Same day
            return True
        else: # Different Day
            return False


    def update_today_pomodoro(self, activities):
        """ Updating content function. Checking and adding activities from today_activity.json """
        date = time.localtime()
        today_date = f"{date.tm_mday} {date.tm_mon} {date.tm_year}"

        if not self.check_date(today_date, activities["metadata"]["date"]): # Different day
            activities["metadata"]["total_activity"] = 0
            activities.pop("ACTIVITY")            
            activities["metadata"]["date"] = today_date
            activities["ACTIVITY"] = {}
            Functions.update_json(TODAY_ACTIVITY_FILE_PATH, activities)

        self.add_all_activity(activities)