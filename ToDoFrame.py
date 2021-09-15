from tkinter import ttk, messagebox

from Globals import *
from PlaceHolderEntry import *
import Functions


class ToDoFrame(ttk.Labelframe):
    def __init__(self, container):        
        #============Label Frame=========
        super().__init__(container, text="To Do", style="MyFrame.TLabelframe")

        # Style of LabelFrame
        self.style = ttk.Style(self)
        self.style.configure("MyFrame.TLabelframe", borderwidth=5)
        #==================================
    
        self.create_widgets()
        self.update_todo_frame()


    def create_widgets(self):
        #====Entry Part======
        self.entry_frame = ttk.Frame(self)
        self.entry_frame.grid(row=0, columnspan=4)

        self.category = PlaceHolderEntry(self.entry_frame, "Category")
        self.category.grid(row=0, column=0)

        self.subcategory = PlaceHolderEntry(self.entry_frame, "Subcategory")
        self.subcategory.grid(row=0, column=1)

        self.description = PlaceHolderEntry(self.entry_frame, "Description")
        self.description.grid(row=0, column=2)

        self.add_button = ttk.Button(self.entry_frame, text="Add To Do", command=self.add_to_do)
        self.add_button.grid(row=0, column=3)
        #=====================

        #====To Do List Part======
        self.todo_list_frame = ttk.Frame(self)
        self.todo_list_frame.grid(row=1, columnspan=3)
        #=========================


    def add_to_do(self):
        """ Adding items to "To Do List" """
        is_convenience = self.check_convenience()
        Yes_Or_No_Message = "The catergory or/and subcategory or/and description is not inserted properly. Do you want to continue without insert?"

        if not is_convenience:
            yes_or_no = messagebox.askyesno(title="Warning", message=Yes_Or_No_Message)
            if yes_or_no: # Continue without insert
                category, subcategory, description = self.get_data()
            else:
                return
        else: # Save it to "To Do Frame"
            category, subcategory, description = self.get_data()

        todo_activities = Functions.read_json(TODOFRAME_ACTIVITY_PATH)
        
        self.save_activity(todo_activities, category, subcategory, description)
        self.update_todo_frame()


    def add_new_data_widget(self, category: str, subcategory:str, description:str, row_number:int):
        cate = ttk.Label(self.todo_list_frame, text=category)
        cate.grid(row=row_number, column=0, sticky="W")
        
        subcate = ttk.Label(self.todo_list_frame, text=subcategory)
        subcate.grid(row=row_number, column=1, sticky="W")

        desp = ttk.Label(self.todo_list_frame, text=description)
        desp.grid(row=row_number, column=2, sticky="W")


    def check_convenience(self):
        """ Checking Category, Subcategory and Description have user-inserted item """
        if self.category.get() == "Category" or self.subcategory.get() == "Subcategory" or self.description.get() == "Description":
            return False
        else:
            return True


    def get_data(self):
        """ Getting data from entry elements """
        category = "" if self.category.get() == "Category" else self.category.get()
        subcategory = "" if self.subcategory.get() == "Subcategory" else self.subcategory.get()
        description = "" if self.description.get() == "Description" else self.description.get()
        
        return category, subcategory, description


    def save_activity(self, activities:dict, category:str, subcategory:str, description:str):
        """ Saving activity to todoframe_activity.json """
        total_activity = int(activities['metadata']['total_activity'])
                
        entry = {f"activity_{total_activity}": {'category': category, 'subcategory': subcategory,'description': description, }}

        # Saving activity and telling everything is done
        activities['metadata']['total_activity'] = total_activity + 1
        activities["ACTIVITY"].update(entry)

        Functions.update_json(TODOFRAME_ACTIVITY_PATH, activities)


    def update_todo_frame(self):
        """ Updating the "To Do List" """
        for child in self.todo_list_frame.winfo_children():
            child.destroy()

        todo_activities = Functions.read_json(TODOFRAME_ACTIVITY_PATH)
        
        total_activity = int(todo_activities['metadata']['total_activity'])

        for i in range(total_activity):
            category = todo_activities["ACTIVITY"][f"activity_{i}"]["category"]
            subcategory = todo_activities["ACTIVITY"][f"activity_{i}"]["subcategory"]
            description = todo_activities["ACTIVITY"][f"activity_{i}"]["description"]
            self.add_new_data_widget(category, subcategory, description, i+1)
        
        # Reseting the entry elements
        self.category.reset_entry()
        self.subcategory.reset_entry()
        self.description.reset_entry()