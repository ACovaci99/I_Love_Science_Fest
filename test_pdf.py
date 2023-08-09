import fitz  # PyMuPDF

# Replace 'input_file.pdf' with the path to your PDF file
pdf_file = 'D:/github/I_Love_Science_Fest/Sample PDF.pdf'

# Convert the first page of the PDF to an image
pdf_document = fitz.open(pdf_file)
first_page = pdf_document.load_page(0)
pix = first_page.get_pixmap()
pix.save('output_image.jpg')
pdf_document.close()




