import tkinter as tk
from tkinter import ttk
from time import sleep
import json


class CountDown():
    def __init__(self, caller, minute:int=25, config_path:str="./config.json"):
        self._minute = minute
        self._config_path = config_path
        
        try:
            config = self.read_json(config_path)
            self.load_json(config)
        except:
            pass


    def count_down(self, minute:int):
        total_secs = minute*60
        while(total_secs):
            print(f"{total_secs//60:02d} : {total_secs%60:02d}")

            sleep(1)
            total_secs-=1
    
    def read_json(self, config_path):
        with open(config_path, "r") as config:
            return json.load(config)
    
    def load_json(self, config:dict):
        # Loading minute 
        self._minute = int(config["APP"]["minute"])


""" Countdown """
import tkinter as tk
from tkinter import ttk
from time import sleep
import json

from tkinter import *

class Application(Frame):
    def __init__(self,master):
        super(Application,self).__init__(master)
        self.pack()
        self.createWidgets()
        self._alarm_id = None
        self._paused = False
        self._starttime = 25 * 60

    def createWidgets(self):
        self.someFrame = Frame(self)
        self.startButton = Button(self.someFrame, text="Start",command=self.startTime)
        self.startButton.pack(side=LEFT)

        self.stopButton = Button(self.someFrame, text="Stop", command=self.stopTime)
        self.stopButton.pack(side=LEFT)

        self.resetButton = Button(self.someFrame, text="Reset", command=self.resetTime)
        self.resetButton.pack(side=LEFT)
        self.someFrame.pack(side=TOP)

        self.labelvariable = StringVar()
        self.labelvariable.set("25:00")

        self.thelabel = Label(self,textvariable = self.labelvariable,font=('Helvetica',50))
        self.thelabel.pack(side=TOP)

        self.firstButton = Button(self,text="pomodoro",command=self.pomodoro)
        self.firstButton.pack(side=LEFT)

        self.secondButton = Button(self,text="short break",command=self.shortBreak)
        self.secondButton.pack(side=LEFT)

        self.thirdButton = Button(self,text="long break",command=self.longBreak)
        self.thirdButton.pack(side=LEFT)

    def pomodoro(self):
        if self._alarm_id is not None:
            self.master.after_cancel(self._alarm_id)
        self.countdown(1500)

    def shortBreak(self):
        if self._alarm_id is not None:
            self.master.after_cancel(self._alarm_id)
        self._paused = False
        self.countdown(300)

    def longBreak(self):
        if self._alarm_id is not None:
            self.master.after_cancel(self._alarm_id)
        self._paused = False
        self.countdown(600)

    def startTime(self):
        """ Resume """
        self._paused = False
        if self._alarm_id is None:
            self.countdown(self._starttime)

    def stopTime(self):
        """ Pause """
        if self._alarm_id is not None:
            self._paused = True

    def resetTime(self):
        """ Restore to last countdown value. """
        if self._alarm_id is not None:
            self.master.after_cancel(self._alarm_id)
            self._alarm_id = None
            self._paused = False
            self.countdown(self._starttime)
            self._paused = True

    def countdown(self, timeInSeconds, start=True):
        if start:
            self._starttime = timeInSeconds
        if self._paused:
            self._alarm_id = self.master.after(1000, self.countdown, timeInSeconds, False)
        else:
            mins, secs = divmod(timeInSeconds, 60)
            timeformat = "{0:02d}:{1:02d}".format(mins, secs)
            app.labelvariable.set(timeformat)
            self._alarm_id = self.master.after(1000, self.countdown, timeInSeconds-1, False)


if __name__ == '__main__':
    root = Tk()
    root.title("Timer")
    app = Application(root)
    root.mainloop()
""""""

