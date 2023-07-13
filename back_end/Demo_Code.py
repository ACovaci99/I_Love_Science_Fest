# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 10:19:16 2023

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
start_time = time.time()

current_directory = os.getcwd()

# Print the current directory
print(f"Current directory: {current_directory}")

subdirectory_name = "plots"

# Create the path to the subdirectory
subdirectory_path = os.path.join(current_directory, subdirectory_name)

# Example usage
image_path = os.path.join(subdirectory_path , "test_small.jpg")  # Replace with your PNG image path
matrix = functions.png_to_matrix(image_path)   
print(matrix)
cmap=functions.create_green_to_blue_cmap()
plt.figure()
functions.plot_heatmap(matrix, cmap, vmin=1, vmax=3)
plt.show()
fracs = functions.count_value_in_kernel2(matrix, 40)


#%%


rows = 100 
cols = 100

col_to_keep = ['ALT', 'WATER', 'GREEN', 'IMPERVIOUS', 'WATER_1000', 'GREEN_1000',
       'IMPERVIOUS_1000', 'SHORT_WAVE_FROM_SKY_1HOUR', 't2m_inca',
       'rel_humid_inca', 'wind_speed_inca', 'max_t2m_inca', 'min_t2m_inca']

df = pd.DataFrame(fracs)
df=df.rename(columns={0:'WATER_1000', 1:'GREEN_1000', 2:'IMPERVIOUS_1000', 3:'WATER', 4:'GREEN', 5:'IMPERVIOUS',})

df_reff=df.head(1)
df_reff.WATER_1000 = 0.0
df_reff.WATER = 0.0
df_reff.IMPERVIOUS_1000 = 0.0
df_reff.IMPERVIOUS = 0.0
df_reff.GREEN_1000 = 1.0
df_reff.GREEN = 1.0
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
arr= arr - T_reff
xd=np.reshape(arr,(rows,cols))
plt.figure()
functions.plot_heatmap(xd, 'cubehelix',vmin=0, vmax=6)
plt.title('Urban Heat Island Intensity Ghent at t= 01 h')
plt.savefig(os.path.join(subdirectory_path,'output.png'), format='png')
plt.show()

end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")