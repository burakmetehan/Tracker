from pathlib import Path
import tkinter as tk
from tkinter import ttk
from time import sleep
import json
import os, subprocess
import time
import sys

import Functions
CONFIG_FILE_PATH = "./files/config.json"


today_activities = Functions.read_json(CONFIG_FILE_PATH)

print(today_activities)





