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

def create_image_jpg(citymap_img,heatmap_img,game,filename="grid.jpg"):
    ilsf_banner = "ideal_city/ILSF_banner_800.png"
    VUB_logo = "ideal_city/all_logo.png" # size: 473 × 130
    canvas_width=800
    image_width=400
    image_height=400
    subtitles =[]
    #array of images
    if game:
        images=["ideal_city/border_ideal_demo_city.png",
                 "ideal_city/ideal_city_heatmap.png",
                citymap_img,
                heatmap_img]
        canvas_height=1120
        title = "Koel je stad af - Rafraîchissez votre ville"
        subtitles=["Voorbeeldstad - Ville d'exemple","Mijn aanpassingen - Mes modifications"]

    else:
        images = [citymap_img,heatmap_img]
        canvas_height=680
        title = "Mijn droomstad - La ville de mes rêves"

    # Create a blank white canvas as base
    with Image(width=canvas_width, height=canvas_height, background=Color('white')) as base:
        # First add the title and the VUB logo next to it
        offset=100
        with Drawing() as draw:
            draw.font = 'fonts/Roboto-Regular.ttf'
            draw.font_size = 40
            draw.text_alignment = 'center'
            draw.text(400, 50, title)
            draw(base)
        # Then the first subtitle if there is one
        if len(subtitles) > 0:
            with Drawing() as draw:
                draw.font = 'fonts/Roboto-Regular.ttf'
                draw.font_size = 20
                draw.text_alignment = 'center'
                draw.text(400, 100, subtitles[0])
                draw(base)
            offset = 120
        # add the two images
        for i in range(2):
            with Image(filename=images[i]) as img:
                img.resize(image_width, image_height)
                base.composite(img, left=image_width * (i % 2), top=offset+image_height * (i // 2))

        # Then the second subtitle if there is one
        if len(subtitles) > 1:
            offset=offset + 430
            with Drawing() as draw:
                draw.font = 'fonts/Roboto-Regular.ttf'
                draw.font_size = 20
                draw.text_alignment = 'center'
                draw.text(400, offset, subtitles[1])
                draw(base)
            offset = offset + 20

            for i in range(2):
                with Image(filename=images[i+2]) as img:
                    img.resize(image_width, image_height)
                    base.composite(img, left=image_width * (i % 2), top=offset+image_height * (i // 2))
        # Then the ILSF banner
        with Image(filename=ilsf_banner) as img:
            img.resize(canvas_width, 130)
            base.composite(img, left=0, top=canvas_height-130)

        # Put the VUB logo at the bottom left corner on top of the banner
        with Image(filename=VUB_logo) as img:
            img.resize(236, 65)
            base.composite(img, left=0, top=canvas_height-130)

        base.save(filename=filename)

#Test the layout for the game scenario with 4 images: the demo city, the demo heat map, the new city and the new heatmap
create_image_jpg("result.jpg","Heatmap_processed.png",True,"grid_game.jpg")
create_image_jpg("result.jpg","Heatmap_processed.png",False,"grid.jpg")

