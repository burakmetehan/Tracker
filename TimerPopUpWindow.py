import tkinter as tk
from tkinter import ttk

class TimerPopUpWindow():
    def __init__(self, master, title:str, message:str):
        
        self.top = tk.Toplevel(master)
        self.top.title(title)
        self.top.iconbitmap(ICON_PATH)
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

        """ Subcategory Part """        
        self.subcate_text = ttk.Label(self.top, text="Subcategory: ")
        self.subcate_text.pack()

        self.subcate_entry = ttk.Entry(self.top)
        self.subcate_entry.pack()

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
        self.subcategory = self.subcate_entry.get()
        self.description = self.desc_entry.get()
        self.top.destroy()
