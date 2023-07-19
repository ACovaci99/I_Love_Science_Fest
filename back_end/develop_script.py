# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 13:49:56 2023

@author: andre
"""

import functions
import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np
import joblib
# Start the timer
import os

from PIL import Image
#%%
start_time = time.time()

current_directory = os.getcwd()


subdirectory_name = "plots"

# Create the path to the subdirectory
subdirectory_path = os.path.join(current_directory, subdirectory_name)

image_path = os.path.join(subdirectory_path , "cropped.jpeg")  # Replace with your PNG image path

image = Image.open(image_path)
width, height = image.size

rows = height 
cols = width

print(rows, cols)
matrix = functions.png_to_matrix(image_path) 
cmap=functions.create_green_to_blue_cmap()
plt.figure()
functions.plot_heatmap(matrix, cmap, vmin=1, vmax=3)
plt.show()


#fracs = functions.count_value_in_kernel2(matrix, 40)


end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")


#%%

from PIL import Image

def png_to_image(image):
    rgb_image = image.convert("RGB")
    width, height = rgb_image.size

    output_image = Image.new("RGB", (width, height))

    for y in range(height):
        for x in range(width):
            r, g, b = rgb_image.getpixel((x, y))
            
            diff_rg = abs(r - g)
            diff_gb = abs(g - b)

            # Categorize the pixel based on the differences
            if diff_rg > 20 and diff_gb > 15:
                if b > max(r, g):
                    color = (0, 0, 255)    # Blue
                else:
                    color = (0, 255, 0)    # Green
            else:
                color = (0, 0, 0)          # Black

            output_image.putpixel((x, y), color)

    return output_image


urrent_directory = os.getcwd()


subdirectory_name = "plots"

# Create the path to the subdirectory
subdirectory_path = os.path.join(current_directory, subdirectory_name)

image_path = os.path.join(subdirectory_path , "cropped.jpeg")  # Replace with your PNG image path

image = Image.open(image_path)

output_image = png_to_image(image)
output_image.show()  # Display the resulting image


#%%
from PIL import Image


def reduce_resolution(image, plate_width , plate_height):

    resized_image = image.resize((plate_width, plate_height))

    return resized_image


new_ = reduce_resolution(output_image, 16 , 16)
new_.show()

#%%

def png_to_image2(image):
    rgb_image = image.convert("RGB")
    width, height = rgb_image.size
    
    print(width, height)

    output_image = Image.new("RGB", (width, height))

    for y in range(height):
        for x in range(width):
            r, g, b = rgb_image.getpixel((x, y))
            #print(r, g, b)
            
            diff_rg = abs(r - g)
            diff_gb = abs(g - b)
            #print(diff_rg, diff_rg, r, g, b)

            # Categorize the pixel based on the differences
            if diff_gb > 30:
                if b > max(r, g):
                    color = (0, 0, 255)    # Blue
                else:
                    color = (0, 255, 0)    # Green
            else:
                color = (0, 0, 0)          # Black

            output_image.putpixel((x, y), color)

    return output_image

output_image2 = png_to_image2(new_)
output_image2.show() 

#%%



df_vlinder = pd.read_csv(os.path.join(subdirectory_path,'big_2020_09.csv' ))
df_vlinder=df_vlinder[df_vlinder['Vlinder']=='vlinder05']
df_vlinder=df_vlinder.reset_index(drop=True)
plt.figure()
df_vlinder.PRECIP_QUANTITY.plot()
plt.figure()
df_vlinder.t2m_inca.plot()
plt.figure()
df_vlinder.wind_speed_inca.plot()


#%%
import functions

current_directory = os.getcwd()
subdirectory_name = "plots"
# Create the path to the subdirectory
subdirectory_path = os.path.join(current_directory, subdirectory_name)

# Example usage
image_path = os.path.join(subdirectory_path , "cropped.jpeg")  # Replace with your PNG image path

image = Image.open(image_path)
plot = functions.main_func(image,10)
plot.show()
