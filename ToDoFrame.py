from tkinter import ttk, messagebox
from PlaceHolderEntry import *
from TimerFrame import *

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
        self.category = PlaceHolderEntry(self, "Category")
        self.category.grid(row=0, column=0)

        self.subcategory = PlaceHolderEntry(self, "Subcategory")
        self.subcategory.grid(row=0, column=1)

        self.description = PlaceHolderEntry(self, "Description")
        self.description.grid(row=0, column=2)

        self.space_label = ttk.Label(self, text="    ")
        self.space_label.grid(row=0, column=3)

        self.add_button = ttk.Button(self, text="Add To Do", command=self.add_to_do)
        self.add_button.grid(row=0, column=4)
    

    def add_to_do(self):
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

        todo_activities = TimerFrame.read_json(None, TODOFRAME_ACTIVITY_PATH)
        
        self.save_activity(todo_activities, category, subcategory, description)
        self.update_todo_frame()

    
    def add_new_data_widget(self, category: str, subcategory:str, description:str, row_number:int): 
        new_frame = ttk.Frame(self)
        new_frame.grid(row=row_number, column=0, columnspan=3)       
        
        cate = ttk.Label(new_frame, text=category)
        cate.grid(row=row_number, column=0)
        
        subcate = ttk.Label(new_frame, text=subcategory)
        subcate.grid(row=row_number, column=1)

        desp = ttk.Label(new_frame, text=description)
        desp.grid(row=row_number, column=2)


    def check_convenience(self):
        """ Checking Category, Subcategory and Description have user inserted item """
        if self.category.get() == "Category" or self.subcategory.get() == "Subcategory" or self.description.get() == "Description":
            return False
        else:
            return True


    def get_data(self):
        category = "" if self.category.get() == "Category" else self.category.get()
        subcategory = "" if self.subcategory.get() == "Subcategory" else self.subcategory.get()
        description = "" if self.description.get() == "Description" else self.description.get()
        
        return category, subcategory, description


    def update_todo_frame(self):
        todo_activities = TimerFrame.read_json(None, TODOFRAME_ACTIVITY_PATH)
        
        total_activity = int(todo_activities['metadata']['total_activity'])

        for i in range(total_activity):
            category = todo_activities["ACTIVITY"][f"activity_{i}"]["category"]
            subcategory = todo_activities["ACTIVITY"][f"activity_{i}"]["subcategory"]
            description = todo_activities["ACTIVITY"][f"activity_{i}"]["description"]
            self.add_new_data_widget(category, subcategory, description, i+1)
        
        self.category.reset_entry()
        self.subcategory.reset_entry()
        self.description.reset_entry()


    def save_activity(self, activities:dict, category:str, subcategory:str, description:str):
        """ Creating entry variable to save it to todoframe_activity.json """
        total_activity = int(activities['metadata']['total_activity'])
                
        entry = {f"activity_{total_activity}": {'category': category, 'subcategory': subcategory,'description': description, }}

        # Saving activity and telling everything is done
        activities['metadata']['total_activity'] = total_activity + 1
        activities["ACTIVITY"].update(entry)

        TimerFrame.update_json(None, TODOFRAME_ACTIVITY_PATH, activities)

