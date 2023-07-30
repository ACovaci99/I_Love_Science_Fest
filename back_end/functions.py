# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 10:19:16 2023

@author: andre
"""
import math
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import random

import functions
import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np
import joblib
# Start the timer
import os

from PIL import Image


def count_value_in_kernel2(matrix, radius):
    # radius = 1000 m
    # start by padding the matrix with NaN values such that the kernel sweeping
    # doesn't have problems with corners and edges
    matrix = pad_matrix(matrix, radius) 
    rows = len(matrix)
    cols = len(matrix[0])
    fracs=[]

    # make a kernel for the r=1000 m 
    kernel = generate_circle_kernel(radius)
    kernel_start = radius
    kernel_end_row = rows-radius
    kernel_end_col = cols-radius
    kernel_area = (1+radius*2)*(1+radius*2)

    # make a kernel for the r=250 m
    sub_rad = int(radius / 4) #250 m
    sub_kernel = generate_circle_kernel(sub_rad)
    kernel_sub_area = (1+sub_rad*2)*(1+sub_rad*2)
    
    # loop over the entire matrix between the points that are not NaN
    for r in range(kernel_start, kernel_end_row):
        for c in range(kernel_start, kernel_end_col):
            
          # big kernel
          rows_needed = get_integers_within_distance(r, radius)
          cols_needed = get_integers_within_distance(c, radius)
          
          # make a subset of the matrix with the size of the big kernel
          
          matrix_needed = extract_matrix_subset(matrix, rows_needed, cols_needed)
          
          # multiplying element wise the subsetted matrix with the big kernel
          new_mat = elementwise_multiply(matrix_needed, kernel)
          num_nan = count_element_in_matrix(new_mat, np.nan)
          num_0 = count_element_in_matrix(new_mat, 0)
          
          #counting the number of values in the matrix that are 0 & NaN and substracting
          val_in_kernel = kernel_area - num_nan - num_0

          # calculating the fractions for r = 1000 m 
          blue_frac=count_element_in_matrix(new_mat, 1)/val_in_kernel
          green_frac=count_element_in_matrix(new_mat, 2)/val_in_kernel
          black_frac=count_element_in_matrix(new_mat, 3)/val_in_kernel


          #use the matrix obtained after the pointwise multiplication for aplying the 
          # medium kernel on the center to get the fractions at r =250 m
          rows_needed = get_integers_within_distance(radius, sub_rad)
          cols_needed = get_integers_within_distance(radius, sub_rad)
          matrix_sub = extract_matrix_subset(new_mat, rows_needed, cols_needed)
          new_sub_mat = elementwise_multiply(matrix_sub, sub_kernel)

          num_nan = count_element_in_matrix(new_sub_mat, np.nan)
          num_0 = count_element_in_matrix(new_sub_mat, 0)
          val_in_kernel = kernel_sub_area - num_nan - num_0

          blue_frac_sub=count_element_in_matrix(new_sub_mat, 1)/val_in_kernel
          green_frac_sub=count_element_in_matrix(new_sub_mat, 2)/val_in_kernel
          black_frac_sub=count_element_in_matrix(new_sub_mat, 3)/val_in_kernel


          fracs.append([blue_frac, green_frac, black_frac, blue_frac_sub, green_frac_sub, black_frac_sub])

    return fracs


def elementwise_multiply(matrix1, matrix2):
    result = np.multiply(matrix1, matrix2)
    return result

def extract_matrix_subset(matrix, rows, cols): 
    # get a subset of a bigger matrix at the rows and cols values
    subset = []

    for row in rows:
        row_subset = []
        for col in cols:
            row_subset.append(matrix[row][col])
        subset.append(row_subset)

    return subset

def generate_circle_kernel(radius):
    #generates a kernele of size 2 * radius + 1 with all the ellements with 
    # the radius from the center equal to 1 and the rest equal to 0
    size = 2 * radius + 1
    kernel = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            distance = np.sqrt((i - radius)**2 + (j - radius)**2)
            if distance <= radius:
                kernel[i][j] = 1

    return kernel


def get_integers_within_distance(target, distance):
    #gets all integers within a distance from a value
    # used to calculate the rows and cols for extract_matrix_subset
    integers = []

    for i in range(target - distance, target + distance + 1):
        integers.append(i)

    return integers



# =============================================================================
# def generate_random_matrix(rows, cols, fractions):
#     matrix = []
# 
#     for i in range(rows):
#         row = []
#         for j in range(cols):
#             value = random.choices(range(1, len(fractions) + 1), weights=fractions)[0]
#             row.append(value)
#         matrix.append(row)
# 
#     return matrix
# =============================================================================


def count_element_in_matrix(matrix, element):
    # couts the amount of times an element appears in a matrix 
    count = 0

    if np.isnan(element):
      count = np.sum(np.isnan(matrix))
    else:
      count = np.count_nonzero(matrix == element)

    return count



def pad_matrix(matrix, r):
    # pads out the matrix with a buffer of size r of NaN values
    m = len(matrix)
    n = len(matrix[0])
    padded_matrix = [[np.nan] * (n + 2 * r) for _ in range(m + 2 * r)]
    for i in range(m):
        for j in range(n):
            padded_matrix[i + r][j + r] = matrix[i][j]
    return padded_matrix



def plot_heatmap(matrix, color, intp, vmin=None, vmax=None):
    # makes a heatmap with a specific output 
    heatmap = plt.imshow(matrix, cmap=color, interpolation=intp, vmin=vmin, vmax=vmax)
    colorbar = plt.colorbar(heatmap)
    plt.show()
    

def create_green_to_blue_cmap():
    colors = ['blue', 'green', 'black']
    cmap = mcolors.LinearSegmentedColormap.from_list('green_to_blue', colors)
    #used to make the blue, green, black landcover heatmaps
    return cmap


from PIL import Image
import numpy as np


def png_to_matrix(image, bool_= False):
    #function that turns an image file into an Blue, green & black matrix 
    rgb_image = image.convert("RGB")
    width, height = rgb_image.size

    matrix = np.zeros((height, width), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            r, g, b = rgb_image.getpixel((x, y))
            
            
            diff_rg = abs(r - g)
            diff_gb = abs(g - b)
            
            if bool_:
                # Categorize the pixel based on the differences
                if diff_rg > 30 and diff_gb > 30:
                    if b > max(r, g):
                        matrix[y, x] = 1  # Blue
                    if g > max(r, b):
                        matrix[y, x] = 2  # Green
                else:
                    matrix[y, x] = 3    # Black
            else:
                
                if b > g and b > r:
                    matrix[y, x] = 1  # Blue
                elif g > r and g > b:
                    matrix[y, x] = 2  # Green
                else:
                    matrix[y, x] = 3    # Black
                
                
    return matrix

def png_to_image(image):
    #turns an image into a blue, green and black variant image 
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

def reduce_resolution(image, plate_width , plate_height):
    #reduce the resolution of an image object to a desired height x width
    resized_image = image.resize((plate_width, plate_height), resample=Image.NEAREST)    
    return resized_image


def png_to_image2(image):
    #function that turns an image file into an Blue, green & black matrix 
    rgb_image = image.convert("RGB")
    width, height = rgb_image.size
    
    

    matrix = np.zeros((height, width), dtype=np.uint8)

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
                    matrix[y, x] = 1    # Blue
                else:
                    matrix[y, x] = 2    # Green
            else:
                matrix[y, x] = 3          # Black

    return matrix

def median_filter_custom(image, kernel_size):
    #sweeps a kernel over an image and calcutes the median for the kernel and sets 
    # that pixel to that value. this is done to smooth out the plot and filter out 
    # small errors  (e.g., shadows)
    
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

def run_module(image,scale):
    # takes in a PIL image and a scale (needs to be a an integer)
    
    
    
    # part 1: turning the image into a landcover map
    scale = int(scale)
    start_time = time.time()
    color_high_res = png_to_image(image)
    #turn picture into a square of lower resolution to do a first cleanup
    low_res = reduce_resolution(color_high_res, 320 , 320)
    #apply median filtering to smooth out the picture a bit
    new_=median_filter_custom(low_res, 6)
    #reduce it to the 16 x 16 resolution of the baseplate
    low_res = reduce_resolution(new_, 16 , 16)
    # turn this image into a matrix 
    low_res_matrix = png_to_image2(low_res)
    
    
    #optional turn this into 
    cmap=functions.create_green_to_blue_cmap()
    plt.figure()
    functions.plot_heatmap(low_res_matrix, cmap, 'nearest',vmin=1, vmax=3)
    plt.show()
    
    


    #cale = int(scale * 20)
    fracs = functions.count_value_in_kernel2(low_res_matrix, scale)

    rows = 16
    cols = 16
    
    
    current_directory = os.getcwd()
    subdirectory_name = "back_end/plots"
    # Create the path to the subdirectory
    subdirectory_path = os.path.join(current_directory, subdirectory_name)
    col_to_keep = ['ALT', 'WATER', 'GREEN', 'IMPERVIOUS', 'WATER_1000', 'GREEN_1000',
           'IMPERVIOUS_1000', 'SHORT_WAVE_FROM_SKY_1HOUR', 't2m_inca',
           'rel_humid_inca', 'wind_speed_inca', 'max_t2m_inca', 'min_t2m_inca']

    df = pd.DataFrame(fracs)
    df=df.rename(columns={0:'WATER_1000', 1:'GREEN_1000', 2:'IMPERVIOUS_1000', 3:'WATER', 4:'GREEN', 5:'IMPERVIOUS',})

    df_reff=df.head(1).copy()
    df_reff.loc[0,'WATER_1000'] = 0.0
    df_reff.loc[0,'WATER'] = 0.0
    df_reff.loc[0,'IMPERVIOUS_1000'] = 0.0
    df_reff.loc[0,'IMPERVIOUS'] = 0.0
    df_reff.loc[0,'GREEN_1000'] = 1.0
    df_reff.loc[0,'GREEN'] = 1.0
    df_reff['Station']= 'vlinder05'

    time_='2020-09-15 01:00:00'
    df_vlinder = pd.read_csv(os.path.join(subdirectory_path,'big_2020_09.csv' ))
    df_vlinder=df_vlinder.rename(columns={"short_wave_from_sky_1hour":"SHORT_WAVE_FROM_SKY_1HOUR","net_radiation_1hour":"NET_RADIATION_1HOUR"})
    df_vlinder=df_vlinder[df_vlinder['Vlinder']=='vlinder05']
    df_vlinder=df_vlinder[df_vlinder['datetime']==time_]
    df_vlinder=df_vlinder[['ALT','SHORT_WAVE_FROM_SKY_1HOUR', 't2m_inca',
           'rel_humid_inca', 'wind_speed_inca', 'max_t2m_inca', 'min_t2m_inca','Vlinder']]
    df['Station']= 'vlinder05'
    df=df.merge(df_vlinder,how='left',left_on='Station',  right_on='Vlinder')
    df_reff=df_reff.merge(df_vlinder,how='left',left_on='Station',  right_on='Vlinder')
    df=df[col_to_keep]
    df_reff=df_reff[col_to_keep]



    model = joblib.load(os.path.join(subdirectory_path, "random_forest.joblib"))
    temp=model.predict(df)

    T_reff=model.predict(df_reff)
    arr = np.array(temp)
    arr_= arr - T_reff
    xd=np.reshape(arr_,(rows,cols))
    xd=np.reshape(arr,(rows,cols))
    fig = plt.figure()
    functions.plot_heatmap(xd, 'plasma', 'bilinear')
    #functions.plot_heatmap(xd, 'plasma', 'bilinear',vmin=0, vmax=6)
    plt.title('Case 1: UHI at night during a heatwave (summer)')
    #plt.savefig(os.path.join(subdirectory_path,'output.png'), format='png')
    final_plot = plt_to_image(fig)
    plt.close()

    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    
    return final_plot


import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PIL import Image

def plt_to_image(fig):
    #turns a plt.fig format into an image format.
    canvas = FigureCanvas(fig)

    # Render the plot onto the FigureCanvas
    canvas.draw()

    # Get the RGB pixel buffer from the FigureCanvas
    buffer = canvas.buffer_rgba()

    image = Image.frombuffer("RGBA", canvas.get_width_height(), buffer, "raw", "RGBA", 0, 1)

    # Convert the image to RGB mode if needed
    image_rgb = image.convert("RGB")
    
    return image_rgb


