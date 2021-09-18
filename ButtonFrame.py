import tkinter as tk
from tkinter import ttk


class ButtonFrame(ttk.Frame):
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
