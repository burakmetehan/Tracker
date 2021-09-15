from tkinter import ttk
from PlaceHolderEntry import *

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
