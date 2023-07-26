import qrcode # Install using: pip install qrcode[pil]

def make_qr(data: str, file_name: str) -> None:
    """
    Generate a QR code image and save it to a file.

    Parameters:
    data (str): The information to be encoded into the QR code.
    file_name (str): The name of the file where the QR code will be saved.

    Returns:
    None
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


make_qr("https://www.openai.com", "openai_qr.png")
