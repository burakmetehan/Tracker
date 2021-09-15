from pathlib import Path
import os

#============================GLOBALS====================
MAIN_PATH = Path(__file__).parent.absolute()
os.chdir(MAIN_PATH)

CONFIG_FILE_PATH = "./files/config.json"
ACTIVITY_FILE_PATH = "./files/activity.json"
TODAY_ACTIVITY_FILE_PATH = "./files/today_activity.json"
TODOFRAME_ACTIVITY_PATH = "./files/todoframe_activity.json"
#=========================================================