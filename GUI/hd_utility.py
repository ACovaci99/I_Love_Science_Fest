
# =================================================================== #
import qrcode # Install using: pip install qrcode[pil]
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
from PIL import ImageTk, Image
def convert_to_pil(label):
    # Get the PhotoImage object from the label
    photo_image = label.cget("image")

    # Convert the PhotoImage to a PIL Image object
    pil_image = ImageTk.getimage(photo_image)

    return pil_image