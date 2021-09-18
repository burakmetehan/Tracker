from tkinter import font, ttk, messagebox

from Globals import *
from PlaceHolderEntry import *
import Functions


CATE_WIDTH = 15
DESP_WIDTH = 75

class ToDoFrame(ttk.Frame):
    def __init__(self, container):        
        #============Label Frame=========
        super().__init__(container)
    
        self.create_widgets()
        self.update_todo_frame()


    def create_widgets(self):
        #====Entry Part======
        self.entry_frame = ttk.Frame(self)
        self.entry_frame.pack(fill="both")

        self.category = PlaceHolderEntry(self.entry_frame, "Category", width=CATE_WIDTH)
        self.category.pack(side="left")

        self.subcategory = PlaceHolderEntry(self.entry_frame, "Subcategory", width=CATE_WIDTH)
        self.subcategory.pack(side="left")

        self.description = PlaceHolderEntry(self.entry_frame, "Description", width=DESP_WIDTH)
        self.description.pack(side="left")


        self.add_button = ttk.Button(self.entry_frame, text="Add To Do", style="my.TButton", command=self.add_to_do)
        self.add_button.pack()

        #=====================
        

        #====To Do List Part======
        self.todo_list_frame = ttk.Frame(self)
        self.todo_list_frame.pack(fill="both")       
        #=========================


    def add_to_do(self):
        """ Adding items to "To Do List" """
        is_convenience = self.check_convenience()

        if not is_convenience:
            yes_or_no = messagebox.askyesno(title="Warning", message=TODO_YES_OR_NO_MESSAGE_BOX_TEXT)
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
        cate = ttk.Label(self.todo_list_frame, text=category, width=CATE_WIDTH)
        cate.grid(row=row_number, column=0, sticky="W")
        
        subcate = ttk.Label(self.todo_list_frame, text=subcategory, width=CATE_WIDTH)
        subcate.grid(row=row_number, column=1, sticky="W")

        desp = ttk.Label(self.todo_list_frame, text=description, width=DESP_WIDTH, anchor="w")
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
