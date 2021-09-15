from pathlib import Path
import tkinter as tk
from tkinter import ttk
from time import sleep
import json
import os, subprocess
import time
import sys

import Functions
TODAY_ACTIVITY_FILE_PATH = "./files/today_activity.json"


today_activities = Functions.read_json(TODAY_ACTIVITY_FILE_PATH)

print(today_activities)

today_activities.pop("ACTIVITY")
today_activities["ACTIVITY"] = {}

print(today_activities)




