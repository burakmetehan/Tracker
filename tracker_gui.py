import tkinter as tk
from tkinter import ttk


class TimerFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.__create_widgets()
    
    def __create_widgets(self):
        minutes = ttk.Label(self, text="25", font=("",50))
        minutes.grid(column=0, row=0)

        colon = ttk.Label(self, text=" : ", font=("",50))
        colon.grid(column=1, row=0)

        seconds = ttk.Label(self, text="00", font=("",50))
        seconds.grid(column=2, row=0)


class ButtonFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.__create_widgets()
    
    def __create_widgets(self):
        start_button = ttk.Button(self, text="Start")
        start_button.grid(row=0, column=0)

        stop_button = ttk.Button(self, text="Stop")
        stop_button.grid(row=0, column=1)


class ToDoFrame(ttk.Labelframe):
    def __init__(self, container):
        super().__init__(container, text="To Do")

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
        timer_frame = TimerFrame(self)
        timer_frame.grid(column=0, row=0)

        button_frame = ButtonFrame(self)
        button_frame.grid(column=0, row=1)

        todo_frame = ToDoFrame(self)
        todo_frame.grid(column=0, row=2)




if __name__ == "__main__":
    app = App()
    app.mainloop()





