import json
from tkinter import messagebox

def read_json(json_path):
    try:
        with open(json_path, "r") as file:
            return json.load(file)
    except:
        messagebox.showerror(title="JSON File Error", message="JSON file is missing or corrupted in read")
        return False

def update_json(json_path, data):
        try:
            with open(json_path, "w") as file:
                json.dump(data, file)
        except:
            messagebox.showerror(title="JSON File Error", message="JSON file is missing or corrupted in update")
            return False
