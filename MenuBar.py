import tkinter as tk
from tkinter import Menu

from MenuBarPopUpWindow import *
from ActivityWindow import *

class MenuBar(Menu):
    def __init__(self, master:tk.Tk):
        self.master = master
        
        # Creating menu bar
        self.menu_bar = Menu(self.master)
        master.config(menu=self.menu_bar)

        
        self.create_file_menu()
        self.create_setting_menu()

        # Adding new menus to menu bar
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Setting", menu=self.setting_menu)
    
    def create_file_menu(self):
        """ Creating "File" Menu"""
        self.file_menu = Menu(self.menu_bar, tearoff=0)

        # Adding new "Activity" item to "File" menu
        self.file_menu.add_command(label="Activity", command=self.__activity)

        # Adding new "Exit" item to "File" menu
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.__exit)

    

    def create_setting_menu(self):
        self.setting_menu = Menu(self.menu_bar, tearoff=0)

        # Adding new "Config" item to "Setting" menu
        self.setting_menu.add_command(label="Config", command=self.__config)


    def __activity(self):
        pop_up_activity = ActivityWindow(self.master)
        self.master.wait_window(pop_up_activity.popup)


    def __exit(self):
        self.master.quit()
        self.master.destroy()
        exit()

    def __config(self):
        pop_up_window = ConfigPopUpWindow(self.master, "Config")
        self.master.wait_window(pop_up_window.popup)

