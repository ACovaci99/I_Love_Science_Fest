from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

def pdf_func(im1,im2,im3,im4,game):
    # Paths to your image files
    image_paths = [im1,im2,im3,im4]
    if game == 'a':
        image_texts = ['Demo city', 'Demo Heat Map', 'Your city', 'Your Heat Map']
    else:
        image_texts = ['Your city', 'Your Heat Map', ' ', ' ']
    
    
    
    # Create a blank white canvas as base
    width, height = 800, 1000
    with Image(width=width, height=height, background=Color('white')) as base:
    
        x_offset = 80
        y_offset = 40
        image_size = 300
        grid_thickness = 10
        cell_width = (width - 3 * x_offset) / 2
        cell_height = (height - 3 * y_offset) / 2
    
        # Loop to place each image in 2x2 structure
        for idx, path in enumerate(image_paths):
            with Image(filename=path) as img:
                img.resize(image_size, image_size)
                
                base.composite(img, left=int(x_offset + (cell_width - img.width) // 2), 
                               top=int(y_offset + (cell_height - img.height - 30) // 2))  # 30 is an approx space for the text
    
                # Add text below each image
                with Drawing() as draw:
                    draw.font_size = 20
                    text_width = draw.get_font_metrics(base, image_texts[idx]).text_width
                    draw.text(int(x_offset + (cell_width - text_width) // 2), 
                              int(y_offset + (cell_height + img.height) // 2 + 5), 
                              image_texts[idx])
                    draw(base)
    
                # Adjust offsets for next image
                if idx % 2 == 0:
                    x_offset += cell_width + 80
                else:
                    x_offset = 80
                    y_offset += cell_height + 40
    
        # Draw the 2x2 grid
        with Drawing() as draw:
            draw.stroke_color = Color('black')
            draw.stroke_width = grid_thickness
            draw.fill_color = Color('transparent')
            
            # Vertical line, adjusted to stay within the bounding box
            draw.line((width/2, 40-grid_thickness), (width/2, height-80+grid_thickness))
            
            # Horizontal line, adjusted to stay within the bounding box
            draw.line((40-grid_thickness, height/2-20), (width-40+grid_thickness, height/2-20))
            
            # Outer border
            draw.rectangle(left=40-grid_thickness, top=40-grid_thickness, 
                           right=width-40+grid_thickness, bottom=height-80+grid_thickness)
            draw(base)
    
        # Add text at the bottom
        with Drawing() as draw:
            draw.font_size = 20
            bottom_text = " "
            text_width = draw.get_font_metrics(base, bottom_text).text_width
            draw.text(int((width - text_width) // 2), height - 10, bottom_text)
            draw(base)
    
        # Save as PDF
        base.format = 'pdf'
        base.save(filename='output3.pdf')
