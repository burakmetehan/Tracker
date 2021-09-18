import tkinter as tk


class PlaceHolderEntry(tk.Entry):
    def __init__(self, container, placeholder, width:int=None):
        super().__init__(container)

        self.configure(width=width)

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
    
    def reset_entry(self):
        self.delete(0, "end")
        self.put_placeholder()
