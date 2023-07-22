import tkinter as tk
from PIL import ImageTk, Image
from Button import CustomButton
from DropDownBar import DropDownBar
from IPython.display import display
# from ILSF.back_end.functions import
from pathlib import Path
import json


def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON data in file: {file_path}")
        return {}



class GUI_Main_Page:



    def __init__(self):

        self.default_img_path = 'G:\\005 - GitRepositories\\1 - Not Updated on Git\\ILSF\\GUI\\vub.png'

        # Begin The Loop
        self.root = tk.Tk()

        # Set Page Title and Logo
        self.root.title("VUB ILSF")
        self.root.iconphoto(False, tk.PhotoImage(file=self.default_img_path))
        self.root.resizable(0, 0)
        self.root.geometry("800x800")

        # Initialize The Image Canvas
        image = self.read_image()
        self.label = tk.Label(self.root, image=image)
        self.label.pack(pady=10)




        # initialize Buttons
        button_frame = tk.Frame(self.root , pady=30)
        self.btn_retake     = CustomButton(button_frame, text = "Retake", state =  self.__get_button_status__(False), command = self.action_retake)
        self.btn_capture    = CustomButton(button_frame, text = "Capture", state = self.__get_button_status__(True), command = self.action_capture)
        self.btn_submit     = CustomButton(button_frame, text = "Submit", state = self.__get_button_status__(False), command = self.action_submit)

        self.btn_capture.pack(side=tk.LEFT, padx=(10, 10))
        self.btn_retake.pack(side=tk.LEFT, padx=(0, 10))
        self.btn_submit.pack(side=tk.LEFT, padx=(0, 10))
        button_frame.pack()

        # TODO: Intialize Drop Down Bar
        # TODO: Read DropDownData from the JSON File given by Andrei
        json_path = "G:\\005 - GitRepositories\\1 - Not Updated on Git\\ILSF\\GUI\\Scales.json"

        json_data = read_json_file(json_path)
        self.drop_down = DropDownBar(self.root, json_data)
        self.drop_down.create_dropdown()


        # End of Loop
        self.root.mainloop()


    def read_image(self, image_path = 'G:\\005 - GitRepositories\\1 - Not Updated on Git\\ILSF\\GUI\\vub.png'):
        # Load the image
        original_image = Image.open(image_path)

        # Resize the image to fit the canvas
        resized_image = original_image.resize((500, 500), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized_image)
        return photo

    def __get_button_status__(self, status):
        if(status == True):
            return tk.NORMAL
        else:
            return tk.DISABLED

    def __change_buttons_status__(self, capturing):
        self.btn_capture.config(state = self.__get_button_status__(capturing))
        self.btn_retake.config(state = self.__get_button_status__(not capturing))
        self.btn_submit.config(state = self.__get_button_status__(not capturing))

    def action_capture(self):
        self.__change_buttons_status__(capturing = False)

        # Get New Image From Camera
        path = 'G:\\005 - GitRepositories\\1 - Not Updated on Git\\ILSF\\GUI\\1.png'
        new_image = self.read_image(path)

        # Update The Image
        self.label.configure(image=new_image)
        self.label.image = new_image



    def action_submit(self):
        self.__change_buttons_status__(capturing = True)
        selected_value = float(self.drop_down.get_selected_value())
        print(f"Submit - {selected_value}")
        # TODO:Send the Image to Andrei's Model


    def action_retake(self):
        self.__change_buttons_status__(capturing = True)

        # Change to Default Image
        new_image = self.read_image(self.default_img_path)
        self.label.configure(image=new_image)
        self.label.image = new_image

        # Open Camera To Take A Picture







GUI_Main_Page()