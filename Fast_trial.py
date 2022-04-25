##############################################################################
# Author: R. Moolya
# Date: 26/11/2021
# Input: 1 interpreted.h5 file each of a threshold_gold, analog,noise occupancy and stuck pixels scan 
##############################################################################
import sys
import numpy as np
import pandas as pd
import tables as tb
import matplotlib.pyplot as plt
import matplotlib as mpl
sys.path.append('./Lib/')
node_name = 'HistOcc'

#Creating a file with all the values:
fm = {'Voltages':[], '1st_NOC':[], 'Stuck': [], '2nd_NOC':[], 'Without_Stuck':[], 'Temperature':[]}
fm = pd.DataFrame(fm)
fm.to_csv('Noisy_m596.csv')

Dfinal = np.array([])
pos = {}
pos = pd.DataFrame(pos)
pos1 = {}
pos1 = pd.DataFrame(pos1)
D_final = np.array([])
v_np600 = np.array([])
v_np700 = np.array([])
v_np800 = np.array([])
T15 = np.array([])
T18 = np.array([])
T21 = np.array([])
T_15 = np.array([])
T_18 = np.array([])
T_21 = np.array([])
V = ['100', '200', '300', '400', '500', '600', '700', '800' ]

#Running the threshold_gold scan:
with tb.open_file("/media/rishabh/RISHABH/m596_2022_04_05/20220406_152128_threshold_scan_interpreted.h5", 'r') as infile:
    data1 = infile.get_node('/' + node_name)[:].T
    maskt1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
    maskt2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T

#Threshold scan:
# config_in file:
Maskt1 = np.zeros([192, 400])
Enabled = np.where(maskt1)
Maskt1[Enabled[0], Enabled[1]] = 1
# config_out file:
Maskt2 = np.zeros([192, 400])
Enabledt2 = np.where(maskt2)
Maskt2[Enabledt2[0], Enabledt2[1]] = 1

# Running an analog scan:
with tb.open_file(f"/media/rishabh/RISHABH/m596_2022_04_05/20220406_163025_analog_scan_interpreted.h5", 'r') as infile:
    data_a1 = infile.get_node('/' + node_name)[:].T
    maska1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
    maska2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
    
# Running the 1st noise occupancy scan:
with tb.open_file(f"/media/rishabh/RISHABH/m596_2022_04_05/20220406_163044_noise_occupancy_scan_interpreted.h5", 'r') as infile:
   datan1 = infile.get_node('/' + node_name)[:].T
   maskn1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
   maskn2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T    

#Running the stuck pixel scan:
with tb.open_file(f"/media/rishabh/RISHABH/m596_2022_04_05/20220406_163135_stuck_pixel_scan_interpreted.h5", 'r') as infile:
    data_s1 = infile.get_node('/' + node_name)[:].T
    masks1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
    masks2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T

#Running the 2st noise occupancy scan:
with tb.open_file(f"/media/rishabh/RISHABH/m596_2022_04_05/20220406_163156_noise_occupancy_scan_interpreted.h5", 'r') as infile:
   datan2 = infile.get_node('/' + node_name)[:].T
   mask1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
   mask2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T

# Analog scan:
# config_in file:
Maska1 = np.zeros([192, 400])
Enableda = np.where(maska1)
Maska1[Enableda[0], Enableda[1]] = 1
# config_out file:
Maska2 = np.zeros([192, 400])
Enableda2 = np.where(maska2)
Maska2[Enableda2[0], Enableda2[1]] = 1

# 1st Noise occupancy:
# config_in file:
Maskn1 = np.zeros([192, 400])
Enabledn1 = np.where(maskn1)
Maskn1[Enabledn1[0], Enabledn1[1]] = 1
# config_out file:
Maskn2 = np.zeros([192, 400])
Enabledn2 = np.where(maskn2)
Maskn2[Enabledn2[0], Enabledn2[1]] = 1


# Stuck pixels:
# config_in file:
M1 = np.zeros([192, 400])  
Enabled_s = np.where(masks1)
M1[Enabled_s[0], Enabled_s[1]] = 1
# config_out file:
M2 = np.zeros([192, 400])
Enabled_s2 = np.where(masks2)
M2[Enabled_s2[0], Enabled_s2[1]] = 1

# 2nd Noise occupancy:
Mask_1 = np.zeros([192, 400]) 
Enabled = np.where(mask1)
Mask_1[Enabled[0], Enabled[1]] = 1

Mask_2 = np.zeros([192, 400])    # [:, 126: 263]
Enabled2 = np.where(mask2)
Mask_2[Enabled2[0], Enabled2[1]] = 1

# ANALYSIS:
# Analog scan:
Data0 = np.array(data_a1[0])
d0 = 192*136 - Enableda2[0].size
print(f"Masked pixels after analog scan:{d0}")

# 1st Noise occupancy:
Data1 = np.array(datan1[0])
d1 = 192*136 - Enabledn2[0].size
print(f"Masked pixels after 1st noise occupancy scan: {d1}")

# Stuck pixels:
Data2 = np.array(data_s1[0])
d2 = 192*136- Enabled_s2[0].size
print(f"Masked pixels after stuck pixels occupancy scan:{d2 - d1}")

# 2nd Noise occupancy:
Data3 = np.array(datan2[0])
d3 = 192*136-Enabled2[0].size
print(f"Masked pixels after 2nd noise occupancy:{d3 - d2}")

# Final matrix:
Dataf = Data1 - Data2 + Data3
Df = 192 * 136 - (Enabledn2[0].size - Enabled_s2[0].size + Enabled2[0].size)
print(f"Masked pixels only after 1st and 2nd noise occupancy scan:{abs(Df)}" + "\n")
Dfinal = np.append(Dfinal, Df)

# Adding values to 'Tables':
gm = {'Voltages':100, '1st_NOC':d1, 'Stuck': (d2 - d1), '2nd_NOC':(d3 - d2), 'Without_Stuck': Df, 'Temperature': -20}
fm = fm.append(gm, ignore_index = True)
fm.to_csv('Noisy_m596.csv')

# Differentiating between a noisy and a stuck pixel:
sum = Maskn2 + Mask_2
c1 = []
c2 = []
# c3 = []
for k in range(0, 191):
    for l in range(128, 264):
        if sum[k][l] == 0 :
            x = {'Row':k,'Column': l}
            c1.append(x) 
        elif sum[k][l] == 1 :
            y = {'Row':k,'Column': l}
            c2.append(y) 
                
d1 = Maskt2 - Maska2 #Diff b/w Gold file and analog output
plt.figure(1)
plt.imshow(d1[:,128:264])  
plt.colorbar()
plt.show()

d1 = Maskt2 - Maskn1 #Diff b/w Gold file output and 1st Noise input 
plt.figure(2)
plt.imshow(d1[:,128:264])  
plt.colorbar()
plt.show()

d11 = Maska2 - Maskn1 #Diff b/w analog output and 1st Noise input
plt.figure(3)
plt.imshow(d11[:,128:264])  
plt.colorbar()
plt.show()

d2 = Maskn2 - M1 #Diff b/w 1st Noise output and Stuck input
plt.figure(4)
plt.imshow(d2[:,128:264])  
plt.colorbar()
plt.show()

d3 = M2 - Mask_1 #Diff b/w Stuck output and 2nd Noise input
plt.figure(5)
plt.imshow(d3[:,128:264])
plt.colorbar()
plt.show()
