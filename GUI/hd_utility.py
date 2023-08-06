
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
            elements.append(PlatypusImage(img, width=2*width/3, height=height/3))  # Adjust the width and height as needed
            elements.append(Spacer(width, height/10))

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
        ret, frame = self.vid.read()
        return frame

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
            self.current_frame = frame
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)

            self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
            self.canvas.image = image
            self.current_frame_tk = image

        self.root.after(10, self.update_frame)  # refresh frame every 10 ms
