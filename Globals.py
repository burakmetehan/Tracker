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

#=====================TimerFrame Texts====================
Message_Box_Text = "There is not active activity in todo list. Do you want to insert information?\nIf you choose \"No\" the item will be saved without information."
Pop_Up_Window_Title = "Insert Information"
Pop_Up_Window_Message = "Enter a category, subcategory and description"
#=========================================================