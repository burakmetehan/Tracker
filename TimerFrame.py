import tkinter as tk
import tkinter as tk
from tkinter import ttk, messagebox
import time

from Globals import *
from PopUpWindow import *
from ToDoFrame import *
import Functions


class TimerFrame(ttk.Frame):
    def __init__(self, container, minute:int = 25):
        super().__init__(container)
        
        # The text has "25 : 00" as default value
        self.timer = ttk.Label(self, text=f"{minute:02d} : {00:02d}", font=("", 50))
        self.timer.grid(row=0, column=0)

        self.minute = minute
        
        self.config = Functions.read_json(CONFIG_FILE_PATH)
        self.load_timer_config(self.config)

        #self.maintime = self.minute * 60
        self.maintime = self.minute * 2

        """ Variables for countdown function """
        self.paused = False
        self.progressTime = self.maintime
        self.alarm_id = None


    def count_down(self, root:tk.Tk, todo_frame:ToDoFrame):
        """ This function is accessed from outside and it calls the main countdown function """

        # This variable will be used to update To Do Frame
        self.todo_frame = todo_frame


        self.__count_down(root, self.progressTime)


    def __count_down(self, root:tk.Tk, timeInSeconds, start=True):
        if start:
            self.progressTime = timeInSeconds

        if self.paused: # when it is paused, timeInSeconds should be same
            self.alarm_id = root.after(1000, self.__count_down, root, timeInSeconds, False)

        else:
            self.timer.configure(text=f"{timeInSeconds//60:02d} : {timeInSeconds%60:02d}") # Updating Timer

            if timeInSeconds > 0: # Continue condition
                self.alarm_id = root.after(1000, self.__count_down, root, timeInSeconds - 1, False)
            else: # Time is over.
                self.save_activity(root, self.minute)
       

    def load_timer_config(self, config):
        if not config:
            return
        # Updating Variable 
        self.minute = int(config["APP"]["minute"])

        # Updating Widget
        self.timer.configure(text=f"{self.minute:02d} : {00:02d}")


    def save_activity(self, root:tk.Tk, total_time:int):
        """ This function first check the todofrane_activity.json file. If there is activity it is deleted from todofrane_activity.json and added to activity.json and today_activity.json """

        todo_activities = Functions.read_json(TODOFRAME_ACTIVITY_PATH)
        todo_total_activity = int(todo_activities["metadata"]["total_activity"])
        
        if todo_total_activity: # If there is activity
            activity = todo_activities["ACTIVITY"]["activity_0"]
            category = activity["category"]
            subcategory = activity["subcategory"]
            description = activity["description"]

            # Deleting activity from todofrane_activity.json
            todo_activities["metadata"]["total_activity"] = todo_total_activity-1

            for i in range(1, todo_total_activity):
                todo_activities["ACTIVITY"][f"activity_{i-1}"] = todo_activities["ACTIVITY"][f"activity_{i}"]
            
            todo_activities["ACTIVITY"].pop(f"activity_{todo_total_activity-1}")

            Functions.update_json(TODOFRAME_ACTIVITY_PATH, todo_activities)
            
            # Creating ToDoFrame instance to update the Frame
            self.todo_frame.update_todo_frame()
            

        else: # If there is not such activity
            yes_or_no = messagebox.askyesno(title="Warning", message=Message_Box_Text)

            if yes_or_no: # Need pop up for entry inserting
                pop_up_window = PopUpWindow(self, title=Pop_Up_Window_Title, message=Pop_Up_Window_Message)

                root.wait_window(pop_up_window.top)

                category = pop_up_window.category
                subcategory = pop_up_window.subcategory
                description = pop_up_window.description
            else:
                category = ""
                subcategory = ""
                description = ""
                

        activities = Functions.read_json(ACTIVITY_FILE_PATH)
        """ Creating entry variable to save it to activity.json """
        self.save_and_update_json(activities, category, subcategory, description, total_time)

        messagebox.showinfo(title="Congratulations", message="Activity is done. The activity is saved in your activities.")


    def save_and_update_json(self, activities:dict, category:str, subcategory:str, description:str, total_time:int):
        """ Creating entry variable to save it to activity.json """
        total_activity = int(activities['metadata']['total_activity'])

        end_time = time.time()
        start_time = end_time - total_time*60
                
        entry = {f"activity_{total_activity}": {'category': category, 'subcategory': subcategory,'description': description, 'time': total_time, 'start_time': time.ctime(start_time), 'end_time': time.ctime(end_time)}}

        # Saving activity and telling everything is done
        activities['metadata']['total_activity'] = total_activity + 1
        activities["ACTIVITY"].update(entry)

        Functions.update_json(ACTIVITY_FILE_PATH, activities)  
