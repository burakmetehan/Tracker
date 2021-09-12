import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path
import os

#============================GLOBALS====================
MAIN_PATH = Path(__file__).parent.absolute()
os.chdir(MAIN_PATH)
#=========================================================


class TimerFrame(ttk.Frame):
    def __init__(self, container, minute:int = 25):
        super().__init__(container)
        
        self._timer = ttk.Label(self, text=f"{minute:02d} : {00:02d}", font=("", 50)) # The text has "25 : 00" as default value
        self._timer.grid(row=0, column=0)
        
        self._minute = minute
        
        self._config = self.read_json("./files/config.json")
        self.load_json(self._config)

        #self._maintime = self._minute * 60
        self._maintime = self._minute * 2

        #
        self._start = True
        self._paused = False
        self._progressTime = self._maintime
        self._alarm_id = None


    def count_down(self, root:tk.Tk):
        self.__count_down(root, self._progressTime, self._start)

    def __count_down(self, root:tk.Tk, timeInSeconds, start=True):
        if start:
            self._progressTime = timeInSeconds

        if self._paused:
            self._alarm_id = root.after(1000, self.__count_down, root, timeInSeconds, False)

        else:
            self._timer.configure(text=f"{timeInSeconds//60:02d} : {timeInSeconds%60:02d}")
            if timeInSeconds > 0:
                self._alarm_id = root.after(1000, self.__count_down, root, timeInSeconds - 1, False)
            else: # When time is up
                messagebox.showinfo(title="Congratulations", message="Activity is done. The activity is saved in your activities.")
    

    def read_json(self, config_path):
        try:
            with open(config_path, "r") as config:
                return json.load(config)
        except:
            messagebox.showerror(title="Config File Error", message="Config file is missing or corrupted")
            return False
    

    def load_json(self, config):
        if not config:
            return
        # Updating Variable 
        self._minute = int(config["APP"]["minute"])
        self._total_secs = self._minute * 60

        # Updating Widget
        self._timer.configure(text=f"{self._minute:02d} : {00:02d}")


class ButtonFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.__create_widgets()
    
    def __create_widgets(self):
        self._start_button = ttk.Button(self, text="Start")
        self._start_button.grid(row=0, column=0)

        self._pause_button = ttk.Button(self, text="Pause", state="disabled")
        self._pause_button.grid(row=0, column=1)

        self._reset_button = ttk.Button(self, text="Reset")
        self._reset_button.grid(row=0, column=2)

        self._done_button = ttk.Button(self, text="Done", state="disabled")
        self._done_button.grid(row=0, column=3)

        
class ToDoFrame(ttk.Labelframe):
    def __init__(self, container):        
        #============Label Frame=========
        super().__init__(container, text="To Do", style="MyFrame.TLabelframe")

        # Style of LabelFrame
        self.style = ttk.Style(self)
        self.style.configure("MyFrame.TLabelframe", borderwidth=0)
        #==================================
        
        self.__create_widgets()

    def __create_widgets(self):
        category = PlaceHolderEntry(self, "Category")
        category.grid(row=0, column=0)

        description = PlaceHolderEntry(self, "Description")
        description.grid(row=0, column=1)


class TodayPomodoro(ttk.Labelframe):
    def __init__(self, container):
        
        #============Label Frame=========
        super().__init__(container, text="Today's Pomodoros", style="MyFrame.TLabelframe")

        # Style of LabelFrame
        self.style = ttk.Style(self)
        self.style.configure("MyFrame.TLabelframe", borderwidth=0)
        #==================================
        
        self.__create_widgets()

    def __create_widgets(self):
        category = PlaceHolderEntry(self, "Category")
        category.grid(row=0, column=0)

        description = PlaceHolderEntry(self, "Description")
        description.grid(row=0, column=1)


class PlaceHolderEntry(ttk.Entry):
    def __init__(self, container, placeholder):
        super().__init__(container)
        
        self.__placeholder = placeholder
        
        self.insert(0, self.__placeholder)
        self.bind("<FocusIn>", self.__clear_placeholder)
        self.bind("<FocusOut>", self.__add_placeholder)

        # Style Configuring
        self.style = ttk.Style(self)
        self.style.configure("placeholder.TEntry", foreground="#d5d5d5")

        PlaceHolderEntry.configure(self, style="placeholder.TEntry")


    def __clear_placeholder(self, event=None):
        self.delete(0, "end")


    def __add_placeholder(self, event=None):
        if not self.get():
            self.insert(0, self.__placeholder)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tracker")

        self.__create_widgets()

    
    def __create_widgets(self):
        self.timer_frame = TimerFrame(self)
        self.timer_frame.grid(column=0, row=0)
        #timer_frame.count_down(self)

        self.button_frame = ButtonFrame(self)
        self.button_frame.grid(column=0, row=1)
        self.button_frame._start_button.configure(command=self.__start_action)
        self.button_frame._pause_button.configure(command=self.__pause_action)
        self.button_frame._reset_button.configure(command=self.__reset_action)
        self.button_frame._done_button.configure(command=self.__done_action)

        self.todo_frame = ToDoFrame(self)
        self.todo_frame.grid(column=0, row=2)

        self.today_pomodoro = TodayPomodoro(self)
        self.today_pomodoro.grid(column=0, row=3)


    def __start_action(self):
        """ Start/Resume """
        self.timer_frame._paused = False
        
        """When it is started once the button will be seen as "Resume"
        When activy is done or reset it will be seen as "Start" """
        self.button_frame._start_button.configure(text="Resume")
        
        if self.timer_frame._alarm_id is None:
            self.timer_frame.count_down(self)

        self.button_frame._start_button.configure(state="disabled")
        self.button_frame._pause_button.configure(state="enabled")
    
    def __pause_action(self):
        """ Pause """
        if self.timer_frame._alarm_id is not None:
            self.timer_frame._paused = True
        
        self.button_frame._start_button.configure(state="enabled")
        self.button_frame._pause_button.configure(state="disabled")
    

    def __reset_action(self):
        """ Reset """
        if self.timer_frame._alarm_id is not None:
            self.after_cancel(self.timer_frame._alarm_id)

            """ Reset """
            self.button_frame._start_button.configure(text="Start")

            self.timer_frame._alarm_id = None
            self.timer_frame._paused = False
            self.timer_frame._progressTime = self.timer_frame._maintime

            self.timer_frame._timer.configure(text=f"{self.timer_frame._maintime//60:02d} : {self.timer_frame._maintime%60:02d}")

        self.button_frame._start_button.configure(state="enabled")
        self.button_frame._pause_button.configure(state="disabled")
    

    def __done_action(self):
        """ Save and Reset """
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()

