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
from pathlib import Path
import json

from hd_utility import HD_Utility
from hd_utility import HD_Camera
from hd_utility import VideoWindow
from datetime import datetime
import json
import cv2


class Paths_Controller:
    PDF_TEXT_JSON_PATH = '../pdf_texts.json'


class GUI_Main_Page:

    ROOT_WINDOW_DIM = "1300x700"
    IMAGE_CANVAS_DIM = (1000, 500)

    def __init__(self, google_drive_handler, pdf_texts_json, server_handler = None):

        self.default_img_path = 'G:\\005 - GitRepositories\\1 - Not Updated on Git\\ILSF\\GUI\\vub.png'
        self.google_drive_handler = google_drive_handler
        self.pdf_texts_json = pdf_texts_json
        self.server_handler = server_handler

        # Begin The Loop
        self.root = tk.Tk()

        #### Video Window
        self.__open_video_window__()
        self.new_created_windows = []


        # Set Page Title and Logo
        self.root.title("VUB ILSF")
        self.root.iconphoto(False, tk.PhotoImage(file=self.default_img_path))
        self.root.resizable(0, 0)
        self.root.geometry(GUI_Main_Page.ROOT_WINDOW_DIM)

        # Initialize The Image Canvas
        image = self.read_image()
        self.label = tk.Label(self.root, image=image)
        self.label.pack(pady=10)


        # initialize Buttons
        button_frame = tk.Frame(self.root , pady=30)
        self.btn_retake     = CustomButton(button_frame, text = "Retake", state =  self.__get_button_status__(False), command = self.action_retake)
        self.btn_capture    = CustomButton(button_frame, text = "Capture", state = self.__get_button_status__(True), command = self.action_capture)
        self.btn_submit     = CustomButton(button_frame, text = "Submit", state = self.__get_button_status__(False), command = self.action_submit)
        self.close_extra    = CustomButton(button_frame, text = "Close Extra", state = self.__get_button_status__(True), command = self.action_close_extra_pages)

        self.btn_capture.pack(side=tk.LEFT, padx=(10, 10))
        self.btn_retake.pack(side=tk.LEFT, padx=(0, 10))
        self.btn_submit.pack(side=tk.LEFT, padx=(0, 10))
        self.close_extra.pack(side=tk.LEFT, padx=(0, 10))
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
        resized_image = original_image.resize(GUI_Main_Page.IMAGE_CANVAS_DIM, Image.LANCZOS)
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
        if self.video_capture.current_frame is not None:
            new_image = self.video_capture.current_frame_tk

        # Update The Image
        self.label.configure(image=new_image)
        self.label.image = new_image

    def action_close_extra_pages(self):
        for window in self.new_created_windows:
            window.destroy()

    def action_submit(self):
        self.__change_buttons_status__(capturing = True)

        # Get Panel data
        scale = float(self.drop_down.get_selected_value())
        img_label = self.label.image
        img_label = ImageTk.getimage(img_label)
        img_label.save("img_label.png")

        #################### Image Processing ###################
        try:
            # Send the Image to Andrei's Model
            img_heatmap_processed = back_end_run(img_label, scale)
            img_heatmap_processed.save("Heatmap_processed.png")


            # Update The Image
            img_heatmap_processed = ImageTk.PhotoImage(img_heatmap_processed)
            self.label.configure(image=img_heatmap_processed)
            self.label.image = img_heatmap_processed
        except Exception as e:
            print("Exception: Andrei's Code Not Working in gui_utility.py")
            print(e)
            img_heatmap_processed = self.read_image()

        # Make a PDF File
        pdf_file_name = "Sample PDF.pdf"
        pdf_texts = (self.pdf_texts_json['french'], self.pdf_texts_json['english'])
        HD_Utility.create_pdf(("img_label.png", "1.jpg"), pdf_texts, pdf_file_name)

        #################### Server Uploading ###################

        # Create File
        file_name_in_drive = f'Analysis_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.jpg'
        HD_Utility.pdf2jpg(pdf_file_name, file_name_in_drive)

        # Upload The File To Google Drive
        # file_id = self.google_drive_handler.upload_image(file_name_in_drive, file_name_in_drive, self.google_drive_handler.folder_id)
        # url = self.google_drive_handler.get_file_url(file_id)

        # Upload the File To the Server
        url = self.server_handler.upload_new_document(path_to_file=file_name_in_drive)
        print(f"Uploaded File to: {url}")

        # Create The QR Code
        qr_code_img = HD_Utility.make_qr(data=url, file_name=f'qr.png')
        print("Created QR Code")



        #################### Creating Final Plots ###################
        # Initialize Images before setting:
        size = (400, 400)
        img1 = HD_Utility.load_and_resize_image("GUI/vub.png", size)
        img3 = HD_Utility.load_and_resize_image("GUI/vub.png", size)
        img2 = HD_Utility.load_and_resize_image("GUI/vub.png", size)


        try:
        # Cat three plots (img1, img2, qr)
            img1 = HD_Utility.load_and_resize_image("img_label.png", size)
            img3 = HD_Utility.load_and_resize_image('qr.png', (200,200))
            img2 = HD_Utility.load_and_resize_image("Heatmap_processed.png", size)

        except:
            print("Exception in gui_utility: QR or Heatmap not found.")

        # Merge Plots
        new_img = HD_Utility.create_concatenated_image(img1, img2, img3)
        final_plot = ImageTk.PhotoImage(new_img)

        # Create a new window and configure label
        new_window = tk.Toplevel(self.root)
        label = tk.Label(new_window, image=final_plot)
        label.image = final_plot  # keep a reference to the image
        label.pack()
        self.new_created_windows.append(new_window)

        # Update The Image
        final_plot = ImageTk.PhotoImage(new_img)
        self.label.configure(image=final_plot)
        self.label.image = final_plot


    def __open_video_window__(self):
        self.video_window = tk.Toplevel(self.root)
        self.video_capture = VideoWindow(self.video_window)


    def action_retake(self):
        self.__change_buttons_status__(capturing = True)

        # Change to Default Image
        new_image = self.read_image(self.default_img_path)
        self.label.configure(image=new_image)
        self.label.image = new_image
