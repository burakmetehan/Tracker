import tkinter as tk
from tkinter import ttk


win = tk.Tk()

description_str = tk.StringVar()
description_str.set("Selam")
description = ttk.Entry(win, textvariable=description_str)
description.grid(row=0, column=1)

win.mainloop()