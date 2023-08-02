import tkinter as tk
from PIL import ImageTk, Image
from Button import CustomButton
from DropDownBar import DropDownBar
from IPython.display import display

import sys
import os
sys.path.insert(0, '../ILSF/back_end')  # Replace with the actual path to the other repository
sys.path.insert(0, '../ILSF/front_end')  # Replace with the actual path to the other repository


from functions import run_module as back_end_run
from camera_capture import capture_img
from pathlib import Path
import json

from hd_utility import HD_Utility
from datetime import datetime
import json




class GUI_Main_Page:



    def __init__(self, google_drive_handler):

        self.default_img_path = 'G:\\005 - GitRepositories\\1 - Not Updated on Git\\ILSF\\GUI\\vub.png'
        self.google_drive_handler = google_drive_handler

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


        # Dropdown Frame:
        dropdown_frame = tk.Frame(self.root)
        dropdown_frame.pack(pady=10)

        # Create Label Field
        self.label_field = tk.Label(dropdown_frame, text="Choose Scale: ")
        self.label_field.pack(side=tk.LEFT)

        # Intialize Drop Down Bar
        json_path = "G:\\005 - GitRepositories\\1 - Not Updated on Git\\ILSF\\GUI\\Scales.json"
        json_data = HD_Utility.read_json_file(json_path)
        self.drop_down = DropDownBar(dropdown_frame, json_data)
        self.drop_down.create_dropdown()


        # End of Loop
        self.root.mainloop()


    def read_image(self, image_path = 'G:\\005 - GitRepositories\\1 - Not Updated on Git\\ILSF\\GUI\\vub.png'):
        # Load the image
        original_image = Image.open(image_path)

        # Resize the image to fit the canvas
        resized_image = original_image.resize((500, 500), Image.LANCZOS)
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
        new_image = capture_img('image_1.png')

        # Update The Image
        self.label.configure(image=new_image)
        self.label.image = new_image

    def action_submit(self):
        self.__change_buttons_status__(capturing = True)

        # Get Panel data
        scale = float(self.drop_down.get_selected_value())
        image = self.label.image
        image = ImageTk.getimage(image)

        # Send the Image to Andrei's Model
        final_plot = back_end_run(image, scale)
        ### Todo: Save final plot image locally

        # Update The Image
        final_plot = ImageTk.PhotoImage(final_plot)
        self.label.configure(image=final_plot)
        self.label.image = final_plot

        # Make a PDF File

        # Upload The File To Google Drive
        image_name = '1.png'
        file_name_in_drive = f'Analysis - {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'
        file_id = self.google_drive_handler.upload_image(image_name, file_name_in_drive, self.google_drive_handler.folder_id)

        # Create The QR Code
        url = my_drive.get_file_url(file_id)
        qr_code_img = HD_Utility.make_qr(data=url, file_name=f'{url}.png')

        # Update The Image
        final_plot = ImageTk.PhotoImage(qr_code_img)
        self.label.configure(image=final_plot)
        self.label.image = final_plot




    def action_retake(self):
        self.__change_buttons_status__(capturing = True)

        # Change to Default Image
        new_image = self.read_image(self.default_img_path)
        self.label.configure(image=new_image)
        self.label.image = new_image

        # Get New Image From Camera
        image = capture_img('image_1.png')
