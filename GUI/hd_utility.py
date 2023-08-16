
import qrcode # Install using: pip install qrcode[pil]
from PIL import ImageTk, Image
import json
from reportlab.pdfgen import canvas # pip install reportlab pillow

from reportlab.lib.pagesizes import A4  # Import A4 constant
from PIL import Image

from reportlab.platypus import PageBreak
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Image as PlatypusImage, PageBreak, Spacer
import cv2
import tkinter as tk
import fitz
import numpy as np
import time


class HD_Utility:
    # =================================================================== #
    def make_qr(data: str, file_name: str) -> None:
        """
        Generate a QR code image and save it to a file.

        Parameters:
        data (str): The information to be encoded into the QR code.
        file_name (str): The name of the file where the QR code will be saved.

        Returns:
        None

        Example Usage:
        make_qr("https://www.openai.com", "openai_qr.png")

        Requirement:
        import qrcode # Install using: pip install qrcode[pil]
        """

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        img.save(file_name)
        return img


    # =================================================================== #
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


    # =================================================================== #
    # from PIL import ImageTk, Image
    def convert_to_pil(label):
        # Get the PhotoImage object from the label
        photo_image = label.cget("image")

        # Convert the PhotoImage to a PIL Image object
        pil_image = ImageTk.getimage(photo_image)

        return pil_image

    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4  # Import A4 constant
    from PIL import Image

    def create_pdf_deprecated(images, texts, output_filename):
        # Install: pip install reportlab pillow

        # Open a New PDF File
        c = canvas.Canvas(output_filename, pagesize=A4)  # Use A4 size
        page_width, page_height = A4

        # Get Image(s) Size
        image_height= images[0].height
        image_width= images[0].width

        # Set Initial Coordinates
        x_coord = page_width/2 - image_width/2
        constant_decrease = 50
        y_coord = page_height - image_height - constant_decrease

        # Add images
        for image in images:
            c.drawInlineImage(image, x_coord, y_coord)  # You may need to adjust coordinates
            y_coord -= (constant_decrease + image_height)

        # Next Page
        c.showPage()

        # Set Text Coordinate
        y_coord = page_height - constant_decrease

        # Add descriptions
        for text in texts:
            c.drawString(x_coord, y_coord, text)
            y_coord -= constant_decrease*2

        # Close the PDF
        c.save()

    def create_pdf(images_paths, texts, output_filename):

        '''
        Example:
        txts = ("This is a description hgasdfhAGFH,DGSFHDSagf hkHJLDHASFG HJaglfkghdfhGJ KHJasdgfhkDGALSFdsfgazdgsdfgasgasfgasfgsgasgasfdgsdfgasdfgasdfgasHGdsf HJKDFGHkadgfhdklsfgjhfg 1",
        "This is a description hgasdfhAGFH,DGSFHDSagf hkHJLDHASFG HJaglfkghdfhGJ KHJasdgfhkDGALSFHGdsf HJKDFGHkadgfhdklsfgjhfg 2")
        output_filename = "output.pdf"
        hd_utility.HD_Utility.create_pdf(images_paths = ('1.jpg', 'image_1.png'), texts = txts, output_filename= output_filename)
        '''

        # Create a SimpleDocTemplate, which represents a PDF document
        doc = SimpleDocTemplate(output_filename, pagesize=A4)

        # Create a list to hold the elements to be added to the document
        elements = []

        # Get the width and height of the A4 size
        width, height = A4

        # Add image1 at the top of the page
        for img in images_paths:
            elements.append(PlatypusImage(img, width=2*width/3, height=height/5))  # Adjust the width and height as needed
            elements.append(Spacer(width, height/20))

        # First, get a style to use for the Paragraph
        styles = getSampleStyleSheet()
        style = styles["BodyText"]

        # Create the Paragraph with the text and style, and add it to the elements
        for text in texts:
            p = Paragraph(text, style)
            elements.append(p)

        # Build the PDF
        doc.build(elements)

    def load_and_resize_image(path, size):
        img = Image.open(path)
        img = img.resize(size, Image.ANTIALIAS)
        return img

    def create_concatenated_image(img1, img2, img3):
        widths, heights = zip(*(i.size for i in [img1, img2, img3]))
        total_width = sum(widths)
        max_height = max(heights)

        new_img = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for img in [img1, img2, img3]:
            new_img.paste(img, (x_offset, 0))
            x_offset += img.width

        return new_img

    def pdf2jpg(pdf_path, output_filename):
        # import fitz
        pdf_file = fitz.open(pdf_path)
        first_page = pdf_file.load_page(0)
        first_page_pix = first_page.get_pixmap()
        first_page_pix.save(output_filename)
        pdf_file.close()
        return first_page_pix




class HD_Camera:
    # import cv2
    def __init__(self):
        self.vid = cv2.VideoCapture(0)

    def camera_read(self):
        start_time=time.time()
        ret, image = self.vid.read()
        # Save the image to the specified file path
        name_path ='test.jpg'
        cv2.imwrite(name_path, image)

        if not ret:
            print("Error: Failed to capture an image from the webcam.")
            return None

        # Convert the image to grayscale to get rid of colors and their confusion
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Threshold the image to create a mask based on the grayscale interval [120, 255]
        _, mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour (the Lego square) based on its area
        largest_contour = max(contours, key=cv2.contourArea)

        # Create a mask for the largest contour
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, [largest_contour], -1, (255), thickness=cv2.FILLED)

        # Bitwise-and the mask with the original image to remove the background
        result = cv2.bitwise_and(image, image, mask=mask)

        # Find the bounding box coordinates of the contour
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Crop the image to the region of interest
        cropped_image = result[y:y + h, x:x + w]

        # Save the cropped image
        cv2.imwrite("result.jpg", cropped_image)
        
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time} seconds")
        
        dummy = Image.open('result.jpg')
        cropped_image = ImageTk.PhotoImage(dummy)

        return cropped_image

    def camera_release(self):
        self.vid.release()

class VideoWindow:
    def __init__(self, root):
        self.root = root
        self.root.resizable(False, False)
        self.root.overrideredirect(True)
        self.capture = cv2.VideoCapture(0)
        self.current_frame = None
        self.current_frame_tk = None
        self.canvas = tk.Canvas(root, width=600, height=600)
        self.canvas.pack()
        self.update_frame()

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            image = frame
            # Save the image to the specified file path
            name_path ='test.jpg'
            cv2.imwrite(name_path, image)

            if not ret:
                print("Error: Failed to capture an image from the webcam.")
                return None

            # Convert the image to grayscale to get rid of colors and their confusion
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Threshold the image to create a mask based on the grayscale interval [120, 255]
            _, mask = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)

            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if len(contours) == 0:
                dummy = Image.open('vub.png')
                frame = ImageTk.PhotoImage(dummy)
                self.current_frame = frame
                #image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #image = Image.fromarray(image)
                #image = ImageTk.PhotoImage(frame)

                self.canvas.create_image(0, 0, anchor=tk.NW, image=frame)
                self.canvas.image = frame
                self.current_frame_tk = frame
            else:
                    
                # Find the largest contour (the Lego square) based on its area
                largest_contour = max(contours, key=cv2.contourArea)
                #TO DO: check contours
    
                # Create a mask for the largest contour
                mask = np.zeros(image.shape[:2], dtype=np.uint8)
                cv2.drawContours(mask, [largest_contour], -1, (255), thickness=cv2.FILLED)
    
                # Bitwise-and the mask with the original image to remove the background
                result = cv2.bitwise_and(image, image, mask=mask)
    
                # Find the bounding box coordinates of the contour
                x, y, w, h = cv2.boundingRect(largest_contour)
    
                # Crop the image to the region of interest
                cropped_image = result[y:y + h, x:x + w]
    
                # Save the cropped image
                cv2.imwrite("result.jpg", cropped_image)
                
    
                # Calculate the elapsed time
    
                
                dummy = Image.open('result.jpg')
                frame = ImageTk.PhotoImage(dummy)
                self.current_frame = frame
                #image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #image = Image.fromarray(image)
                #image = ImageTk.PhotoImage(frame)
    
                self.canvas.create_image(0, 0, anchor=tk.NW, image=frame)
                self.canvas.image = frame
                self.current_frame_tk = frame

        self.root.after(10, self.update_frame)  # refresh frame every 10 ms
