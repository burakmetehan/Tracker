import tkinter as tk
from tkinter import ttk, messagebox
import time

from Globals import *
from TimerPopUpWindow import *
from ToDoFrame import ToDoFrame
from TodayActivityFrame import TodayActivity
from ButtonFrame import ButtonFrame
import Functions


class TimerFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        self.timer_text = ttk.Label(self, text="Activity")
        self.timer_text.grid(row=0, column=0)

        # The text has "25 : 00" as default value
        self.timer = ttk.Label(self, text=" Time is not found in config ", font=("", 50))
        self.timer.grid(row=1, column=0)

        # Loading Config
        self.config = Functions.read_json(CONFIG_FILE_PATH)
        self.load_config(self.config)

        # Variables from config
        self.activity_time = self.config_activity_time * 60
        self.break_time = self.config_break_time * 60
        self.auto_break = self.config_auto_break

        self.function_start_time = self.activity_time # This variable will change between calls according to function
        
        # Updating Timer
        self.update_timer(self.function_start_time)


        """ Variables for countdown function """
        self.is_activity = True
        self.paused = False
        self.alarm_id = None

        # progressTime is only used if an activity is ended by clicking done button
        self.progressTime = self.activity_time


    def access_other_frames(self, root:tk.Tk, todo_frame:ToDoFrame, today_activity_frame:TodayActivity, button_frame: ButtonFrame):
        self.root = root
        self.todo_frame = todo_frame
        self.today_activity_frame = today_activity_frame
        self.button_frame = button_frame


    def count_down(self):
        """ This function is accessed from outside and it calls the main countdown function """

        if self.is_activity:
            self.__count_down_activity(self.root, self.function_start_time)
        else:
            self.__count_down_break(self.root, self.break_time)


    def __count_down_activity(self, root:tk.Tk, timeInSeconds):
        self.progressTime = timeInSeconds
        if self.paused: # when it is paused, timeInSeconds should be same
            self.alarm_id = root.after(1000, self.__count_down_activity, root, timeInSeconds)
        else:
            self.update_timer(timeInSeconds) # Updating Timer

            if timeInSeconds > 0: # Continue condition
                self.alarm_id = root.after(1000, self.__count_down_activity, root, timeInSeconds - 1)
            else: # Time is over.
                # Saving Activity. Activity time is completely used.
                self.save_activity(root, self.activity_time)

                # Reset timer
                self.reset_countdown_and_timer(new_time=self.break_time, next_event="brake")
                
                # Start break time                
                self.break_countdown_caller(root)
    

    def __count_down_break(self, root:tk.Tk, timeInSeconds:int):
        if self.paused: # when it is paused, timeInSeconds should be same
            self.alarm_id = root.after(1000, self.__count_down_break, root, timeInSeconds)
        else:
            self.update_timer(timeInSeconds) # Updating Timer

            if timeInSeconds > 0: # Continue condition
                self.alarm_id = root.after(1000, self.__count_down_break, root, timeInSeconds - 1)
            else: # Time is over.
                messagebox.showinfo(title="Break is done", message=BREAK_DONE_MESSAGE_BOX_TEXT)

                self.reset_countdown_and_timer(new_time=self.activity_time, next_event="activity")

    def break_countdown_caller(self, root:tk.Tk):
        if self.auto_break:
            # Changing buttons. Since root will be App, it will have following items
            root.button_frame.start_button.configure(text="Resume", state="disabled")
            root.button_frame.pause_button.configure(state="enabled")
            root.button_frame.done_button.configure(state="enabled")
            self.count_down()


    def reset_countdown_and_timer(self, new_time, next_event:str):
        """ Reset countdown variables and timer. new_time: time of the next event, next_event: "activity" or "brake" """
        # Reset countdown variable
        self.is_activity = next_event.lower() == "activity"
        self.paused = False
        self.alarm_id = None
        
        # Reset timer
        self.timer_text.configure(text=next_event.capitalize())
        self.function_start_time = new_time
        self.update_timer(self.function_start_time)
        
        # Reset buttons
        self.button_frame.start_button.configure(text="Start", state="enabled")
        self.button_frame.pause_button.configure(text="Pause", state="disabled")
        self.button_frame.reset_button.configure(text="Reset", state="enabled")
        self.button_frame.done_button.configure(text="Done", state="disabled")


    def load_config(self, config):
        if not config:
            return

        # Getting variable from config.json
        self.config_activity_time = int(config["APP"]["minute"])
        self.config_break_time = int(config["APP"]["break"])
        self.config_auto_break = bool(config["APP"]["auto_break"])


    def save_activity(self, root:tk.Tk, total_time:int):
        """ This function first check the todofrane_activity.json file. If there is activity it is deleted from todofrane_activity.json and added to activity.json and today_activity.json """

        activities = Functions.read_json(TODOFRAME_ACTIVITY_PATH)
        todo_total_activity = int(activities["metadata"]["total_activity"])
        
        if todo_total_activity: # If there is activity
            activity = activities["ACTIVITY"]["activity_0"]
            category = activity["category"]
            subcategory = activity["subcategory"]
            description = activity["description"]

            # Deleting activity from todoframe_activity.json
            activities["metadata"]["total_activity"] = todo_total_activity-1

            for i in range(1, todo_total_activity):
                activities["ACTIVITY"][f"activity_{i-1}"] = activities["ACTIVITY"][f"activity_{i}"]
            
            activities["ACTIVITY"].pop(f"activity_{todo_total_activity-1}")
            Functions.update_json(TODOFRAME_ACTIVITY_PATH, activities)
            #==============================================
            
            # Updating To Do List
            self.todo_frame.update_todo_frame()    
        else: # If there is not such activity
            yes_or_no = messagebox.askyesno(title="Warning", message=YES_OR_NO_MESSAGE_BOX_TEXT)

            if yes_or_no: # Need pop up for entry inserting
                pop_up_window = TimerPopUpWindow(self, title=POP_UP_WINDOW_TITLE, message=POP_UP_WINDOW_MESSAGE)

                root.wait_window(pop_up_window.top)

                category = pop_up_window.category
                subcategory = pop_up_window.subcategory
                description = pop_up_window.description
            else:
                category = ""
                subcategory = ""
                description = ""
                
        # Updating activity.json
        activities = Functions.read_json(ACTIVITY_FILE_PATH)
        self.save_activity_and_update_json(activities, category, subcategory, description, total_time, ACTIVITY_FILE_PATH)

        # Updating today_activity.json
        activities = Functions.read_json(TODAY_ACTIVITY_FILE_PATH)
        self.save_activity_and_update_json(activities, category, subcategory, description, total_time, TODAY_ACTIVITY_FILE_PATH)
        self.today_activity_frame.update_today_activity(activities)

        messagebox.showinfo(title="Congratulations", message=ACTIVITY_DONE_MESSAGE_BOX_TEXT)


    def save_activity_and_update_json(self, activities:dict, category:str, subcategory:str, description:str, total_time:int, json_path):
        """ Creating entry variable to save it to activity.json """
        total_activity = int(activities['metadata']['total_activity'])

        end_time = int(time.time())
        start_time = end_time - total_time*60
                
        entry = {f"activity_{total_activity}": {'category': category, 'subcategory': subcategory,'description': description, 'spent_time': total_time, 'start_time': time.ctime(start_time), 'end_time': time.ctime(end_time)}}

        # Saving activity
        activities['metadata']['total_activity'] = total_activity + 1
        activities["ACTIVITY"].update(entry)

        Functions.update_json(json_path, activities)


    def update_timer(self, timeInSeconds:int):
        """ Updating the "Timer" with given time that is in seconds. """
        self.timer.configure(text=f"{timeInSeconds//60:02d} : {timeInSeconds%60:02d}") # Updating Timer
    