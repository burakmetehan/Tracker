import tkinter as tk
from tkinter import ttk
from time import sleep
import json
import os, subprocess
import time


def get_data():
    category = "Category"
    subcategory = "Subcategory"
    description = "Description"
        
    return category, subcategory, description

print(get_data())
a, b, c = get_data()
print(a)
print(b)
print(c)
