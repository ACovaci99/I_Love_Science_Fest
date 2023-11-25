import tkinter as tk
from PIL import ImageTk, Image
from Button import CustomButton
from DropDownBar import DropDownBar
from IPython.display import display
from screeninfo import get_monitors

import sys
import os
sys.path.insert(0, '../I_Love_Science_Fest/back_end')  # Replace with the actual path to the other repository
sys.path.insert(0, '../I_Love_Science_Fest/front_end')  # Replace with the actual path to the other repository



from functions import run_module as back_end_run
from pathlib import Path
import json

from hd_utility import HD_Utility
from pdf_maker import create_image_jpg
# from hd_utility import HD_Camera
from hd_utility import VideoWindow
from datetime import datetime
import json
import cv2

class Paths_Controller:
    PDF_TEXT_JSON_PATH = '../pdf_texts.json'


class GUI_Main_Page:
    resolution = "1300x700"
    monitors = get_monitors()
    if len(monitors) > 1:
        second_monitor = monitors[1]  # Index 1 because 0 is the first monitor
        resolution = str(second_monitor.width)+"x"+str(second_monitor.height)
    else:
        print("Second monitor not found.")
    ROOT_WINDOW_DIM = resolution
    IMAGE_CANVAS_DIM = (1400, 700)

    def __init__(self, pdf_texts_json, server_handler = None):

        self.default_img_path = 'GUI/vub.png'
        #self.google_drive_handler = google_drive_handler
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
        #self.btn_submit     = CustomButton(button_frame, text = "Submit", state = self.__get_button_status__(False), command = self.action_submit)
        self.close_extra    = CustomButton(button_frame, text = "Close Extra", state = self.__get_button_status__(True), command = self.action_close_extra_pages)
        self.btn_send_picture = CustomButton(
        button_frame, 
        text="Calculate", 
        state=self.__get_button_status__(False), 
        command=self.send_picture_to_server
        )
        
        self.btn_process_display = CustomButton(
        button_frame, 
        text="Save", 
        state=self.__get_button_status__(False), 
        command=self.process_and_display_image
        )

        self.btn_capture.pack(side=tk.LEFT, padx=(10, 10))
        self.btn_retake.pack(side=tk.LEFT, padx=(0, 10))
        #self.btn_submit.pack(side=tk.LEFT, padx=(0, 10))        
        self.btn_send_picture.pack(side=tk.LEFT, padx=(0, 10))
        self.btn_process_display.pack(side=tk.LEFT, padx=(0, 10))
        self.close_extra.pack(side=tk.LEFT, padx=(0, 10))
        button_frame.pack()


        # Dropdown Frame 2:
        dropdown_frame2 = tk.Frame(self.root)
        dropdown_frame2.pack(pady=10, padx=(200, 0), side=tk.LEFT)
        
        # Create Label Field for Dropdown 2
        self.label_field2 = tk.Label(dropdown_frame2, text="Mode: ")
        self.label_field2.pack(side=tk.LEFT)
        
        # Initialize Drop Down Bar for Dropdown 2
        json_path2 = "GUI/Modes.json"  # Change this path if you're pulling from a different file
        json_data2 = HD_Utility.read_json_file(json_path2)
        self.drop_down2 = DropDownBar(dropdown_frame2, json_data2)
        self.drop_down2.create_dropdown()
        
        
        # Dropdown Frame 3:
        dropdown_frame3 = tk.Frame(self.root)
        dropdown_frame3.pack(pady=10, padx=(200, 0), side=tk.LEFT)
        
        # Create Label Field for Dropdown 1
        self.label_field3 = tk.Label(dropdown_frame3, text="Choose Scenario: ")
        self.label_field3.pack(side=tk.LEFT)
        
        # Initialize Drop Down Bar for Dropdown 1
        json_path3 = "GUI/Scenario.json"
        json_data3 = HD_Utility.read_json_file(json_path3)
        self.drop_down3 = DropDownBar(dropdown_frame3, json_data3)
        self.drop_down3.create_dropdown()
        
        # Dropdown Frame 1:
        dropdown_frame1 = tk.Frame(self.root)
        dropdown_frame1.pack(pady=10, padx=(200, 0), side=tk.LEFT)
        
        # Create Label Field for Dropdown 1
        self.label_field1 = tk.Label(dropdown_frame1, text="Choose Scale: ")
        self.label_field1.pack(side=tk.LEFT)
        
        # Initialize Drop Down Bar for Dropdown 1
        json_path1 = "GUI/Scales.json"
        json_data1 = HD_Utility.read_json_file(json_path1)
        self.drop_down1 = DropDownBar(dropdown_frame1, json_data1)
        self.drop_down1.create_dropdown()

        # End of Loop
        self.root.mainloop()

    def read_image(self, image_path = 'GUI/vub.png'):
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
        #self.btn_submit.config(state = self.__get_button_status__(not capturing))
        self.btn_send_picture.config(state = self.__get_button_status__(not capturing))
        self.btn_process_display.config(state = self.__get_button_status__(capturing))

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


    def __open_video_window__(self):
        self.video_window = tk.Toplevel(self.root)
        self.video_capture = VideoWindow(self.video_window)


    def action_retake(self):
        self.__change_buttons_status__(capturing = True)

        # Change to Default Image
        new_image = self.read_image(self.default_img_path)
        self.label.configure(image=new_image)
        self.label.image = new_image
        
        
        
        
        
        
    def send_picture_to_server(self):
        """Function to send the image to the server and receive a heatmap in response."""
        self.__change_buttons_status__(capturing=True)
        game = str(self.drop_down2.get_selected_value())
        if game == 'a': # this is the regular game 
            scale = 4 
            weather = 'a'
            other_arg = 'a'
        elif game == 'b': #map of brussels 16x16
            scale = 16 
            weather = str(self.drop_down3.get_selected_value())
            other_arg = 'b'
        elif game == 'c': #map of brussels 32 x 32
            scale = 2 
            weather = str(self.drop_down3.get_selected_value())
            other_arg = 'c'
        elif game == 'd': #map of brussels 32 x 32
            scale = float(self.drop_down1.get_selected_value())
            weather = str(self.drop_down3.get_selected_value())
            other_arg = 'd'
        # Get Panel data
        #value1, value2 = drop_down2.get_selected_value()
        img_label = self.label.image
        #img_label = ImageTk.getimage(self.read_image("ideal_city/border_ideal_demo_city.png"))
        img_label = ImageTk.getimage(img_label)
        img_label.save("img_label.png")
    
        try:
            # Send the Image to Andrei's Model
            img_heatmap_processed = back_end_run(img_label, scale,weather, other_arg)
            img_heatmap_processed.save("Heatmap_processed.png")
            #new_size = (300, 300)  # or (new_width, new_height)

            # Resize the image
            #img_heatmap_processed = img_heatmap_processed.resize(new_size)
            # Update The Image
            img_heatmap_processed = ImageTk.PhotoImage(img_heatmap_processed)
            self.label.configure(image=img_heatmap_processed)
            self.label.image = img_heatmap_processed
        except Exception as e:
            print("Exception: Andrei's Code Not Working in gui_utility.py")
            print(e)
            img_heatmap_processed = self.read_image()
    
        return img_heatmap_processed

    def process_and_display_image(self):
        img_heatmap_processed = Image.open("Heatmap_processed.png")
        img_heatmap_processed = ImageTk.PhotoImage(img_heatmap_processed)
        
        """Function to process and display the heatmap, create QR code, and display final plots."""
        
        # Make a PDF File
        
        
        game = str(self.drop_down2.get_selected_value())
        print(game)
        file_name_in_drive = f'Analysis_{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.jpg'
        create_image_jpg("result.jpg","Heatmap_processed.png",game=='a',file_name_in_drive)

        url = self.server_handler.upload_new_document(path_to_file=file_name_in_drive)
        url2 = url[:-4]
        print(f"Uploaded File to: {url2}")
        
        # Create The QR Code
        qr_code_img = HD_Utility.make_qr(data=url2, file_name=f'qr.png')
        print("Created QR Code")
        
        #size = (300, 300)
        size = (700, 700)
        img1 = HD_Utility.load_and_resize_image("GUI/vub.png", size)
        img3 = HD_Utility.load_and_resize_image("GUI/vub.png", size)
        img2 = HD_Utility.load_and_resize_image("GUI/vub.png", size)
        
        try:
        # Cat three plots (img1, img2, qr)
            img1 = HD_Utility.load_and_resize_image("img_label.png", size)
            img3 = HD_Utility.load_and_resize_image('qr.png', (400,400))
            img2 = HD_Utility.load_and_resize_image("Heatmap_processed.png", size)

        except:
            print("Exception in gui_utility: QR or Heatmap not found.")
        
        
        game = str(self.drop_down2.get_selected_value())
        if game == 'a': # this is the regular game 
            img1 = HD_Utility.load_and_resize_image("ideal_city/ideal_city_heatmap.png", size)
            img3 = HD_Utility.load_and_resize_image('qr.png', (400,400))
            img2 = HD_Utility.load_and_resize_image("Heatmap_processed.png", size)
        else:
            img1 = HD_Utility.load_and_resize_image("img_label.png", size)
            img3 = HD_Utility.load_and_resize_image('qr.png', (200,200))
            img2 = HD_Utility.load_and_resize_image("Heatmap_processed.png", size)




        # Merge Plots
        def create_concatenated_image_with_bg(images, bg_color=(255, 255, 255)):
        
            # Get total width and the maximum height of all images to be concatenated
            total_width = sum(image.width for image in images)
            max_height = max(image.height for image in images)
        
            # Create a new image with white background
            new_image = Image.new('RGB', (total_width, max_height), bg_color)
        
            # Paste each image next to each other
            x_offset = 0
            for image in images:
                y_offset = (max_height - image.height) // 2  # Center vertically
                new_image.paste(image, (x_offset, y_offset), mask=image if image.mode == 'RGBA' else None)
                x_offset += image.width
        
            return new_image

        # Example usage:
        images = [img1, img2, img3]
        concatenated_image = create_concatenated_image_with_bg(images)
        
        
        #new_img = HD_Utility.create_concatenated_image(img1, img2, img3)
        new_img = concatenated_image
        final_plot = ImageTk.PhotoImage(new_img)
        
        new_window = tk.Toplevel(self.root)
        label = tk.Label(new_window, image=final_plot)
        label.image = final_plot  # keep a reference to the image
        label.pack()
        self.new_created_windows.append(new_window)

        # Update The Image
        final_plot = ImageTk.PhotoImage(new_img)
        self.label.configure(image=final_plot)
        self.label.image = final_plot
        
    
    # Example of how to use the functions:
    # img_heatmap_processed = self.send_picture_to_server()
    # self.process_and_display_image(img_heatmap_processed)

