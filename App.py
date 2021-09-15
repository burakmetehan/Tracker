import tkinter as tk

from Globals import *
from TimerFrame import *
from ButtonFrame import *
from ToDoFrame import *
from TodayPomodoro import *


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
            self.timer_frame.count_down(self)

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
        """ self.pause_action()
        self.timer_frame.save_activity(self, self.todo_frame.category.get(), self.todo_frame.description.get())
        self.reset_action() """
        pass
