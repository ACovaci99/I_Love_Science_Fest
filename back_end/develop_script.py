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

image_path = os.path.join(subdirectory_path , "knipsel2.PNG")  # Replace with your PNG image path

image = Image.open(image_path)
width, height = image.size

print(width, height)

output_image = png_to_image(image)
output_image.show()  # Display the resulting image


#%%
from PIL import Image


def reduce_resolution(image, plate_width , plate_height):

    resized_image = image.resize((plate_width, plate_height), resample=Image.NEAREST)

    return resized_image

import numpy as np
from PIL import Image
from scipy.ndimage import median_filter

def median_filter_pil(image, kernel_size):
    # Convert the PIL image to a NumPy array
    image_array = np.array(image)

    # Apply median filtering to the image array
    filtered_array = median_filter(image_array, size=kernel_size)
    
    # Convert the filtered array back to uint8 data type
    filtered_array = filtered_array.astype(np.uint8)

    # Convert the filtered array back to a PIL image
    filtered_image = Image.fromarray(filtered_array)

    return filtered_image

def median_filter_custom(image, kernel_size):
    # Create a copy of the original image
    filtered_image = image.copy()

    # Get the dimensions of the image
    width, height = image.size

    # Calculate the padding size for the kernel
    padding = kernel_size // 2

    # Iterate over each pixel in the image
    for y in range(padding, height - padding):
        for x in range(padding, width - padding):
            # Extract the neighborhood around the current pixel
            neighborhood = image.crop((x - padding, y - padding, x + padding + 1, y + padding + 1))

            # Get the pixel values within the neighborhood
            pixels = list(neighborhood.getdata())

            # Calculate the median value within the neighborhood
            median = sorted(pixels)[len(pixels) // 2]

            # Set the pixel value in the filtered image to the median
            filtered_image.putpixel((x, y), median)

    return filtered_image

new_ = reduce_resolution(output_image, 320 , 320)
new_.show()
new_=median_filter_custom(new_, 6)
new_.show()
new_ = reduce_resolution(new_, 16 , 16)
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
image_path = os.path.join(subdirectory_path , "knipsel2.PNG")  # Replace with your PNG image path

image = Image.open(image_path)
plot = functions.run_module(image, 4)
plot.show()





#%%%

current_directory = os.getcwd()
subdirectory_name = "plots"
# Create the path to the subdirectory
subdirectory_path = os.path.join(current_directory, subdirectory_name)

# Example usage
image_path = os.path.join(subdirectory_path , "new_firas4.png") 

image = Image.open(image_path)
image.show()
from PIL import Image
from skimage.feature import canny
from skimage.color import rgb2gray

def edge_detection(image):
    # Convert the image to grayscale
    gray_image = image.convert('L')

    # Convert PIL image to NumPy array
    image_array = np.array(gray_image)

    # Convert grayscale image to RGB by duplicating the single channel
    image_rgb = np.stack((image_array,) * 3, axis=-1)

    # Perform Canny edge detection
    edges = canny(rgb2gray(image_rgb))

    # Convert the edges array back to PIL image
    edges_image = Image.fromarray(edges.astype('uint8') * 255)

    return edges_image


ed = edge_detection(image)
ed.show()


from PIL import Image, ImageOps, ImageDraw

def remove_region_within_edges(image, edges):
    # Convert the edges image to grayscale
    edges_gray = edges.convert('L')

    # Create a blank mask image with the same size as the edges
    mask = Image.new('L', edges_gray.size, 0)

    # Draw the region within the edges on the mask
    draw = ImageDraw.Draw(mask)
    draw.polygon(edges_gray.getbbox(), fill=255)

    # Apply the mask to the original image
    result = Image.composite(image, Image.new('RGB', image.size), mask)

    return result


remove_object_with_edges(image, ed).show()


#%%
current_directory = os.getcwd()
subdirectory_name = "plots"
# Create the path to the subdirectory
subdirectory_path = os.path.join(current_directory, subdirectory_name)

# Example usage
image_path = os.path.join(subdirectory_path , "new_firas2.png") 

import cv2
import numpy as np

def extract_object(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image from BGR to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the object color in HSV
    lower_color = np.array([0, 50, 50])  # Adjust these values based on the object color
    upper_color = np.array([360, 255, 255])  # Adjust these values based on the object color

    # Create a mask for the object using color segmentation
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Apply the mask to the original image
    extracted_object = cv2.bitwise_and(image, image, mask=mask)

    return extracted_object

# Example usage
extracted_image = extract_object(image_path)
cv2.imshow('Extracted Object', extracted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#%%



import cv2
import numpy as np

def remove_white_object(image, threshold):
    # Convert PIL image to OpenCV format
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Convert image to grayscale
    gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    # Create a binary mask of white pixels
    _, mask = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)

    # Perform inpainting
    result = cv2.inpaint(image_cv, mask, 3, cv2.INPAINT_TELEA)

    # Convert back to PIL image format
    result_pil = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))

    return result_pil

current_directory = os.getcwd()
subdirectory_name = "plots"
# Create the path to the subdirectory
subdirectory_path = os.path.join(current_directory, subdirectory_name)

# Example usage
image_path = os.path.join(subdirectory_path , "new_firas.png") 

image = Image.open(image_path)
image.show()

remove_white_object(image, 150).show()



#%%%



import cv2
import numpy as np

def warp_colored_region(image):
    # Convert image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define lower and upper color thresholds for color-based segmentation
    lower_color = np.array([0, 50, 50])  # Adjust these values based on the color range of the region
    upper_color = np.array([30, 255, 255])  # Adjust these values based on the color range of the region

    # Create a mask of the colored region using color segmentation
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour (assuming it represents the colored region)
    largest_contour = max(contours, key=cv2.contourArea)

    # Find the four corners of the largest contour
    epsilon = 0.1 * cv2.arcLength(largest_contour, True)
    corners = cv2.approxPolyDP(largest_contour, epsilon, True)
    print(corners)
    if len(corners) >= 4:
        # Create a target square shape for warping
        target_size = 500  # Adjust the size as desired
        target_shape = np.float32([[0, 0], [target_size, 0], [target_size, target_size], [0, target_size]])

        # Find the perspective transformation matrix using homography
        transform_matrix, _ = cv2.findHomography(corners, target_shape)

        # Warp the image into the square format
        warped_image = cv2.warpPerspective(image, transform_matrix, (target_size, target_size))

        return warped_image
    else:
        print("Insufficient corners detected. Unable to warp the image.")
        return None

# Example usage
current_directory = os.getcwd()
subdirectory_name = "plots"
# Create the path to the subdirectory
subdirectory_path = os.path.join(current_directory, subdirectory_name)

# Example usage
image_path = os.path.join(subdirectory_path , "new_firas3.png") 
image = cv2.imread(image_path)
warped_image = warp_colored_region(image)
if warped_image is not None:
    cv2.imshow('Warped Image', warped_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()






#%%




