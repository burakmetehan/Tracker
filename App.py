import tkinter as tk

from Globals import *
from TimerFrame import *
from ButtonFrame import *
from ToDoFrame import *
from TodayPomodoro import *
from MenuBar import *


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tracker")
        self.resizable(0, 0)

        self.create_widgets()
        self.timer_frame.access_other_frames(self, self.todo_frame, self.today_pomodoro, self.button_frame)


        # Centering the window
        self.update_idletasks()
        app_width = self.winfo_width()
        app_height = self.winfo_height()        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight() 
        self.geometry(f"{app_width}x{app_height}+{screen_width//2 - app_width//2}+{screen_height//2 - app_height//2}")


    def create_widgets(self):
        self.menu = MenuBar(self)

        self.timer_frame = TimerFrame(self)
        self.timer_frame.pack()

        self.button_frame = ButtonFrame(self)
        self.button_frame.pack()
        self.button_frame.start_button.configure(command=self.start_action)
        self.button_frame.pause_button.configure(command=self.pause_action)
        self.button_frame.reset_button.configure(command=self.reset_action)
        self.button_frame.done_button.configure(command=self.done_action)

        self.todo_frame = ToDoFrame(self)
        self.todo_frame.pack(expand=True, pady=10)

        self.today_pomodoro = TodayPomodoro(self)
        self.today_pomodoro.pack(expand=True, pady=10)


    def start_action(self):
        """ Start/Resume """
        self.timer_frame.paused = False
        
        """When it is started once the button will be seen as "Resume"
        When activy is done or reset it will be seen as "Start" """
        self.button_frame.start_button.configure(text="Resume")
        
        if self.timer_frame.alarm_id is None: # First start
            self.timer_frame.count_down()

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

            # Reset button
            self.button_frame.start_button.configure(text="Start")

            # Reset timer_frame variables
            self.timer_frame.alarm_id = None
            self.timer_frame.paused = False

            # Reset
            self.timer_frame.progressTime = self.timer_frame.function_start_time

            self.timer_frame.update_timer(self.timer_frame.function_start_time)

        self.button_frame.start_button.configure(state="enabled")
        self.button_frame.pause_button.configure(state="disabled")


    def done_action(self):
        """ Pause, Save and Reset """
        # Timer needs to be paused until done_action is finished
        self.timer_frame.paused = True

        if self.timer_frame.alarm_id is None: # no ongoing timer
            return
        
        if self.timer_frame.is_activity: # Activity is ended by clicking "Done"
            # Stop Timer Loop
            self.after_cancel(self.timer_frame.alarm_id)

            # Saving activity
            spent_time = self.timer_frame.activity_time-self.timer_frame.progressTime
            self.timer_frame.save_activity(self, spent_time)

            # Reset "Timer" and Start "Break"
            self.timer_frame.reset_countdown_and_timer(new_time=self.timer_frame.break_time, next_event="brake")
            
            self.timer_frame.break_countdown_caller(self)
        else: # Break is ended by clicking "Done"
            # Stop Timer Loop
            self.after_cancel(self.timer_frame.alarm_id)

            # Reset "Timer" and Start "Break"
            self.timer_frame.reset_countdown_and_timer(new_time=self.timer_frame.activity_time, next_event="activity")

            # Display message
            messagebox.showinfo(title="Break is done", message=BREAK_DONE_MESSAGE_BOX_TEXT)
