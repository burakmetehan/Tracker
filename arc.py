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
