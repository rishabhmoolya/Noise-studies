##############################################################################
# Author: M.Antonello 
# Date: 26/11/2020
# Input: 1 interpreted.h5 file of a source scan (1 chip per time!)
# Output: 1 png plot with the occupancy map and the missing bumps number (in the title) + 1 png with the occupancy distribution
# Variables to change: Sensor, Thr, VMAX (only if hot pixels are present) 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
import sys
import numpy as np
import pandas as pd
import tables as tb
import matplotlib.pyplot as plt
import matplotlib as mpl
sys.path.append('./Lib/')

node_name = 'HistOcc'

#Running the threshold_gold scan:
#with tb.open_file("20211111_140024_threshold_scan_interpreted.h5", 'r') as infile:
#    data1 = infile.get_node('/' + node_name)[:].T
#    mask1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
#    mask2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T

#Running an analog scan:
#with tb.open_file("WW/m611_200V_WW_17C_analog_scan_interpreted.h5", 'r') as infile:
#    data1 = infile.get_node('/' + node_name)[:].T
#    mask1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
#    mask2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T


#Running the 1st noise occupancy scan(without the C in the file name):
with tb.open_file("WW/m611_200V_WW_17_noise_occupancy_scan_interpreted.h5", 'r') as infile:
   datan1 = infile.get_node('/' + node_name)[:].T
   maskn1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
   maskn2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T    

#Running the stuck pixel scan:
with tb.open_file("WW/m611_200V_WW_17C_stuck_pixel_scan_interpreted.h5", 'r') as infile:
    data_s1 = infile.get_node('/' + node_name)[:].T
    masks1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
    masks2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T

#Running the 2st noise occupancy scan:
with tb.open_file("WW/m611_100V_WW_17C_noise_occupancy_scan_interpreted.h5", 'r') as infile:
   datan2 = infile.get_node('/' + node_name)[:].T
   mask1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
   mask2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T


#1st Noise occupancy:
Maskn1=np.zeros([192,400]) ####change the number of rows and columns for Linear FE(128-264) but code uses 127.5 to 263.5##### 
Enabled=np.where(maskn1)
Maskn1[Enabled[0],Enabled[1]]=1

Maskn2=np.zeros([192,400])
Enabledn2=np.where(maskn2)
Maskn2[Enabledn2[0],Enabledn2[1]]=1

#Stuck pixels:
M1=np.zeros([192,400]) ####change the number of rows and columns for Linear FE(128-264) but code uses 127.5 to 263.5##### 
Enabled_s=np.where(masks1)
#print(Enabled)
M1[Enabled_s[0],Enabled_s[1]]=1

M2=np.zeros([192,400]) 
Enabled_s2=np.where(masks2)
#print(Enabled)
M2[Enabled_s2[0],Enabled_s2[1]]=1

#2nd Noise occupancy:
Mask_1=np.zeros([192,400]) ####change the number of rows and columns for Linear FE(128-264) but code uses 127.5 to 263.5##### 
Enabled=np.where(mask1)
#print(Enabled)
Mask_1[Enabled[0],Enabled[1]]=1

#if Mask_1[Enabled[0],Enabled[1]] == 1:
# print("Masked pixels: "+str(192*136-Enabled[0].size))

Mask_2=np.zeros([192,400])#[:,126:263]
#Mask2= Mask_2[:,127:264]
Enabled2=np.where(mask2)
Mask_2[Enabled2[0],Enabled2[1]]=1
#print(Enabled2)

#Mask_3=Mask_1-Mask_2

# ANALYSIS:
#1st Noise occupancy:
Data1=np.array(datan1[0])
d1= 192*136-Enabledn2[0].size
print(f"Masked pixels after 1st noise occupancy scan:{d1}")

#Stuck pixels:
Data2=np.array(data_s1[0])
d2=192*136-Enabled_s2[0].size
print(f"Masked pixels after stuck pixels occupancy scan:{d2}")

#2nd Noise occupancy:
Data3=np.array(datan2[0])
d3= 192*136-Enabled2[0].size
print(f"Masked pixels after 2nd noise occupancy:{d3}")

#Final matrix:
Dataf= Data1-Data2+Data3
Df=192*136-(Enabledn2[0].size-Enabled_s2[0].size+Enabled2[0].size)
print(f"Masked pixels only after 1st and 2nd noise occupancy scan:{Df}")

#Creating 'Tables':
fm= {'1st_NOC':[d1], 'Stuck': [d2], '2nd_NOC':[d3], 'Without_Stuck':[Df]}
fm=pd.DataFrame(fm)
fm.to_csv('Tables.csv')

#Adding values to 'Tables':
gm= {'1st_NOC':1, 'Stuck': 2, '2nd_NOC':3, 'Without_Stuck': 4}
fm= fm.append(gm, ignore_index=True)
fm.to_csv('Tables.csv')
#list=[1,2,3,4]
#fm=fm.append([list])
#fm.to_csv('Tables.csv')

#Stuck pixels:
#fig_1=plt.imshow(masks1)
#plt.colorbar()
#plt.show()

#fig_2=plt.imshow(masks2)
#plt.colorbar()
#plt.show()


#noise occupancy:
fig=plt.imshow(mask1)
plt.colorbar()
plt.show()

fig2=plt.imshow(mask2)
plt.colorbar()
plt.show()

#imgplot = plot(Data)
#ax1.set_title("Occupancy Map (Z Lim: %s hits)" % str(100))