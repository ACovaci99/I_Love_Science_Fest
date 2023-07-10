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


def count_value_in_kernel2(matrix, radius):
    radius = 20 #my choice 1000 m
    matrix = pad_matrix(matrix, radius)
    rows = len(matrix)
    cols = len(matrix[0])
    fracs=[]

    # Calculate the kernel's starting and ending indices
    kernel = generate_circle_kernel(radius)
    kernel_start = radius
    kernel_end_row = rows-radius
    kernel_end_col = cols-radius
    kernel_area = (1+radius*2)*(1+radius*2)


    sub_rad = int(radius / 5) #250 m
    sub_kernel = generate_circle_kernel(sub_rad)
    kernel_sub_area = (1+sub_rad*2)*(1+sub_rad*2)
    counter=0

    for r in range(kernel_start, kernel_end_row):
        print(counter)
        counter=counter+1
        for c in range(kernel_start, kernel_end_col):
          # big kernel
          rows_needed = get_integers_within_distance(r, radius)
          cols_needed = get_integers_within_distance(c, radius)
          matrix_needed = extract_matrix_subset(matrix, rows_needed, cols_needed)
          new_mat = elementwise_multiply(matrix_needed, kernel)
          num_nan = count_element_in_matrix(new_mat, np.nan)
          num_0 = count_element_in_matrix(new_mat, 0)
          val_in_kernel = kernel_area - num_nan - num_0

          blue_frac=count_element_in_matrix(new_mat, 1)/val_in_kernel
          green_frac=count_element_in_matrix(new_mat, 2)/val_in_kernel
          black_frac=count_element_in_matrix(new_mat, 3)/val_in_kernel


          #sub kernel
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
    subset = []

    for row in rows:
        row_subset = []
        for col in cols:
            row_subset.append(matrix[row][col])
        subset.append(row_subset)

    return subset

def generate_circle_kernel(radius):
    size = 2 * radius + 1
    kernel = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            distance = np.sqrt((i - radius)**2 + (j - radius)**2)
            if distance <= radius:
                kernel[i][j] = 1

    return kernel


def get_integers_within_distance(target, distance):
    integers = []

    for i in range(target - distance, target + distance + 1):
        integers.append(i)

    return integers



def generate_random_matrix(rows, cols, fractions):
    matrix = []

    for i in range(rows):
        row = []
        for j in range(cols):
            value = random.choices(range(1, len(fractions) + 1), weights=fractions)[0]
            row.append(value)
        matrix.append(row)

    return matrix


def count_element_in_matrix(matrix, element):
    count = 0

    if np.isnan(element):
      count = np.sum(np.isnan(matrix))
    else:
      count = np.count_nonzero(matrix == element)

    return count



def pad_matrix(matrix, r):
    m = len(matrix)
    n = len(matrix[0])
    padded_matrix = [[np.nan] * (n + 2 * r) for _ in range(m + 2 * r)]
    for i in range(m):
        for j in range(n):
            padded_matrix[i + r][j + r] = matrix[i][j]
    return padded_matrix



def plot_heatmap(matrix, color, vmin=None, vmax=None):
    heatmap = plt.imshow(matrix, cmap=color, interpolation='nearest', vmin=vmin, vmax=vmax)
    colorbar = plt.colorbar(heatmap)
    plt.show()
    

def create_green_to_blue_cmap():
    colors = ['blue', 'green', 'black']
    cmap = mcolors.LinearSegmentedColormap.from_list('green_to_blue', colors)
    return cmap
cmap = create_green_to_blue_cmap()


from PIL import Image
import numpy as np

def png_to_matrix(image_path):
    image = Image.open(image_path)
    rgb_image = image.convert("RGB")
    width, height = rgb_image.size

    matrix = np.zeros((height, width), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            r, g, b = rgb_image.getpixel((x, y))
            if b > g and b > r:
                matrix[y, x] = 1  # Blue
            elif g > r and g > b:
                matrix[y, x] = 2  # Green
            else:
                matrix[y, x] = 3    # Black
    return matrix


# Example usage
image_path = "/content/gent_small.png"  # Replace with your PNG image path
matrix = png_to_matrix(image_path)
print(matrix)