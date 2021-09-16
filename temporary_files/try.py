from pathlib import Path
import tkinter as tk
from tkinter import ttk
from time import sleep
import json
import os, subprocess
import time
import sys

import Functions

new_d = Functions.read_json("./files/config.json")

print(new_d)

