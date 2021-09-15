import tkinter as tk
from tkinter import ttk
from time import sleep
import json
import os, subprocess

entry = {'activity_3': {'category': 'CENG 140', 'description': 'PTR'}}


filename = './files/test.json'

# 1. Read file contents
with open(filename, "r") as file:
    data = json.load(file)
# 2. Update json object
#data.append(entry)
data["ACTIVITY"].update(entry)
# 3. Write json file
with open(filename, "w") as file:
    json.dump(data, file)
    