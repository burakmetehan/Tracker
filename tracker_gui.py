import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path
import os


#============================GLOBALS====================
MAIN_PATH = Path(__file__).parent.absolute()
os.chdir(MAIN_PATH)

CONFIG_FILE_PATH = "./files/config.json"
ACTIVITY_FILE_PATH = "./files/activity.json"
TODAY_ACTIVITY_FILE_PATH = "./files/today_activity.json"
#=========================================================


class PopUpWindow():
    def __init__(self, master, title:str, message:str):
        
        self.top = tk.Toplevel(master)
        self.top.title(title)
        self.top.geometry("300x150")

        self.category = ""
        self.description = ""

        """ Message Part """
        self.mes_label = ttk.Label(self.top, text=message)
        self.mes_label.pack()

        """ Category Part """        
        self.cate_text = ttk.Label(self.top, text="Category: ")
        self.cate_text.pack()

        self.cate_entry = ttk.Entry(self.top)
        self.cate_entry.pack()

        """ Description Part """
        self.desc_text = ttk.Label(self.top, text="Description: ")
        self.desc_text.pack()

        self.desc_entry = ttk.Entry(self.top)
        self.desc_entry.pack()

        """ Button Part """
        self.button = ttk.Button(self.top, text="Close", command=self.close)
        self.button.pack()
    

    def close(self):
        self.category = self.cate_entry.get()
        self.description = self.desc_entry.get()
        self.top.destroy()


class TimerFrame(ttk.Frame):
    def __init__(self, container, minute:int = 25):
        super().__init__(container)
        
        self.timer = ttk.Label(self, text=f"{minute:02d} : {00:02d}", font=("", 50)) # The text has "25 : 00" as default value
        self.timer.grid(row=0, column=0)

        self.minute = minute
        
        self.config = self.read_json(CONFIG_FILE_PATH)
        self.load_timer_config(self.config)

        self.maintime = self.minute * 60
        #self.maintime = self.minute * 2

        """ Variables for countdown function """
        self.paused = False
        self.progressTime = self.maintime
        self.alarm_id = None


    def count_down(self, root:tk.Tk, category: str, description: str):
        """ This function is accessed from outside and it calls the main countdown function """
        
        # This variables will be used while saving
        self.category = category
        self.description = description

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
                self.save_activity(root, self.category, self.description)


    def read_json(self, json_path):
        try:
            with open(json_path, "r") as file:
                return json.load(file)
        except:
            messagebox.showerror(title="JSON File Error", message="JSON file is missing or corrupted in read")
            return False
    

    def update_json(self, json_path, data):
        try:
            with open(json_path, "w") as file:
                json.dump(data, file)
        except:
            print("Problem here")
            messagebox.showerror(title="JSON File Error", message="JSON file is missing or corrupted in update")
            return False


    def load_timer_config(self, config):
        if not config:
            return
        # Updating Variable 
        self.minute = int(config["APP"]["minute"])

        # Updating Widget
        self.timer.configure(text=f"{self.minute:02d} : {00:02d}")


    def save_activity(self, root:tk.Tk, category:str, description:str):
        activities = self.read_json(ACTIVITY_FILE_PATH)

        #=================Texts=================
        Message_Box_Text = "The catergory or/and description is not specified. Do you want to specify? Yes: Specify category and description No: Save with empty information."
        Yes_Or_No_Title = "Insert Information"
        Yes_Or_No_Message = "Enter a category and description"
        #=======================================

        # Arranging category and description for update saved file
        if category == "Category" or description == "Description": # Default contents
            yes_or_no = messagebox.askyesno(title="Warning", message=Message_Box_Text)
            
            if yes_or_no: # Need pop up for entry inserting
                pop_up_window = PopUpWindow(self, Yes_Or_No_Title, Yes_Or_No_Message)
                
                # Waiting to destroy the pop up
                root.wait_window(pop_up_window.top)

                category = pop_up_window.category
                description = pop_up_window.description
            else:
                category = ""
                description = ""


        """ Creating entry variable to save it to activity.json """
        total_activity = int(activities['metadata']['total_activity'])

        
        entry = {f"activity_{total_activity}": {'category': category, 'description': description}}

        # Saving activity and telling everything is done
        activities['metadata']['total_activity'] = total_activity + 1
        activities["ACTIVITY"].update(entry)

        self.update_json(ACTIVITY_FILE_PATH, activities)

        messagebox.showinfo(title="Congratulations", message="Activity is done. The activity is saved in your activities.")


class ButtonFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.create_widgets()


    def create_widgets(self):
        self.start_button = ttk.Button(self, text="Start")
        self.start_button.grid(row=0, column=0)

        self.pause_button = ttk.Button(self, text="Pause", state="disabled")
        self.pause_button.grid(row=0, column=1)

        self.reset_button = ttk.Button(self, text="Reset")
        self.reset_button.grid(row=0, column=2)

        self.done_button = ttk.Button(self, text="Done", state="disabled")
        self.done_button.grid(row=0, column=3)

        
class ToDoFrame(ttk.Labelframe):
    def __init__(self, container):        
        #============Label Frame=========
        super().__init__(container, text="To Do", style="MyFrame.TLabelframe")

        # Style of LabelFrame
        self.style = ttk.Style(self)
        self.style.configure("MyFrame.TLabelframe", borderwidth=0)
        #==================================
        
        self.create_widgets()


    def create_widgets(self):
        self.category = PlaceHolderEntry(self, "Category")
        self.category.grid(row=0, column=0)

        self.description = PlaceHolderEntry(self, "Description")
        self.description.grid(row=0, column=1)


class TodayPomodoro(ttk.Labelframe):
    def __init__(self, container):
        
        #============Label Frame=========
        super().__init__(container, text="Today's Pomodoros", style="MyFrame.TLabelframe")

        # Style of LabelFrame
        self.style = ttk.Style(self)
        self.style.configure("MyFrame.TLabelframe", borderwidth=0)
        #==================================

        self.create_widgets()


    def create_widgets(self):
        self.category = PlaceHolderEntry(self, "Category")
        self.category.grid(row=0, column=0)

        self.description = PlaceHolderEntry(self, "Description")
        self.description.grid(row=0, column=1)


class PlaceHolderEntry(tk.Entry):
    def __init__(self, container, placeholder):
        super().__init__(container)
        
        self.placeholder = placeholder
        self.placeholder_color = "#d5d5d5"
                
        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)

        self.put_placeholder()


    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self.configure(foreground=self.placeholder_color)
 
    def focus_in(self, event="None"):
        if self["foreground"] == self.placeholder_color:
            self.delete(0, "end")
            self.configure(foreground="#000000")
    
    def focus_out(self, event=None):
        if not self.get():
            self.put_placeholder()


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tracker")

        self.create_widgets()

    
    def create_widgets(self):
        self.timer_frame = TimerFrame(self)
        self.timer_frame.grid(column=0, row=0)


        self.button_frame = ButtonFrame(self)
        self.button_frame.grid(column=0, row=1)
        self.button_frame.start_button.configure(command=self.start_action)
        self.button_frame.pause_button.configure(command=self.pause_action)
        self.button_frame.reset_button.configure(command=self.reset_action)
        self.button_frame.done_button.configure(command=self.done_action)

        self.todo_frame = ToDoFrame(self)
        self.todo_frame.grid(column=0, row=2)

        self.today_pomodoro = TodayPomodoro(self)
        self.today_pomodoro.grid(column=0, row=3)


    def start_action(self):
        """ Start/Resume """
        self.timer_frame.paused = False
        
        """When it is started once the button will be seen as "Resume"
        When activy is done or reset it will be seen as "Start" """
        self.button_frame.start_button.configure(text="Resume")
        
        if self.timer_frame.alarm_id is None:
            self.timer_frame.count_down(self, self.todo_frame.category.get(), self.todo_frame.description.get())

        self.button_frame.start_button.configure(state="disabled")
        self.button_frame.pause_button.configure(state="enabled")
        self.button_frame.done_button.configure(state="enabled")


    def pause_action(self):
        """ Pause """
        if self.timer_frame.alarm_id is not None:
            self.timer_frame.paused = True
        
        self.button_frame.start_button.configure(state="enabled")
        self.button_frame.pause_button.configure(state="disabled")


    def reset_action(self):
        """ Reset """
        if self.timer_frame.alarm_id is not None:
            self.after_cancel(self.timer_frame.alarm_id)

            """ Reset """
            self.button_frame.start_button.configure(text="Start")

            self.timer_frame.alarm_id = None
            self.timer_frame.paused = False
            self.timer_frame.progressTime = self.timer_frame.maintime

            self.timer_frame.timer.configure(text=f"{self.timer_frame.maintime//60:02d} : {self.timer_frame.maintime%60:02d}")

        self.button_frame.start_button.configure(state="enabled")
        self.button_frame.pause_button.configure(state="disabled")


    def done_action(self):
        """ Pause, Save and Reset """
        self.pause_action()
        self.timer_frame.save_activity(self, self.todo_frame.category.get(), self.todo_frame.description.get())
        self.reset_action()


if __name__ == "__main__":
    app = App()
    app.mainloop()

