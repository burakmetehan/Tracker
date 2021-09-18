import tkinter as tk
from tkinter import ttk
from pathlib import Path
import os
import json


#============================GLOBALS====================
MAIN_PATH = Path(__file__).parent.absolute()
os.chdir(MAIN_PATH)
#=========================================================


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.activity = self.read_activity()

        self.main_frame = tk.Frame(self)
        self.main_frame.pack()

        self.render_all_activity(self.main_frame, self.activity)


        self.style = ttk.Style(self)
        self.style.configure("Category.TLabel", background="#ADD8E6", width=-16, border=5, borderwidth=5, padding=(5, 5))
        self.style.configure("Description.TLabel", background="#1E5162", foreground="#e6bbad", width=-64, padding=(5,5))


    def read_activity(self):
        with open("./files/activity.json", "r") as activity:
            return json.load(activity)


    def render_all_activity(self, container:tk.Frame, all_activies:dict):
        total_activity = int(all_activies["metadata"]["total_activity"])
        for i in range(total_activity):
            self.render_one_activity(container, all_activies, i, f"activity_{i}")


    def render_one_activity(self, container:tk.Frame, all_activies:dict, row, activity_name:str="ERROR"):
        category_label = ttk.Label(container, style="Category.TLabel")
        description_label = ttk.Label(container, style="Description.TLabel")

        # Setting the values
        category_label.configure(text=all_activies["ACTIVITY"][activity_name]["category"])
        description_label.configure(text=all_activies["ACTIVITY"][activity_name]["description"])

        # Positioning
        category_label.grid(row=row, column=0)
        description_label.grid(row=row, column=1)


if __name__ == "__main__":
    app = App()
    app.mainloop()

