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


#Creating a file with all the values:
fm= {'Voltages':[], '1st_NOC':[], 'Stuck': [], '2nd_NOC':[], 'Without_Stuck':[]}
fm=pd.DataFrame(fm)
fm.to_csv('T_bridge=-21C_WW_pc.csv')

Dfinal=np.array([])

# Running a for loop to store all the values:
for i in range(100,900,100):
    #Running the 1st noise occupancy scan(without the C in the file name):
    with tb.open_file(f"/home/moolyari/Documents/Code/DATA/m611_labtest/T_bridge=-21C/m611_{i}V_23_noise_occupancy_scan_interpreted.h5", 'r') as infile:
       datan1 = infile.get_node('/' + node_name)[:].T
       maskn1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
       maskn2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T    
    
    #Running the stuck pixel scan:
    with tb.open_file(f"/home/moolyari/Documents/Code/DATA/m611_labtest/T_bridge=-21C/m611_{i}V_23C_stuck_pixel_scan_interpreted.h5", 'r') as infile:
        data_s1 = infile.get_node('/' + node_name)[:].T
        masks1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
        masks2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
    
    #Running the 2st noise occupancy scan:
    with tb.open_file(f"/home/moolyari/Documents/Code/DATA/m611_labtest/T_bridge=-21C/m611_{i}V_23C_noise_occupancy_scan_interpreted.h5", 'r') as infile:
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
    
    Mask_2=np.zeros([192,400])#[:,126:263]
    #Mask2= Mask_2[:,127:264]
    Enabled2=np.where(mask2)
    Mask_2[Enabled2[0],Enabled2[1]]=1
    #print(Enabled2)
    
    #Mask_3=Mask_1-Mask_2

    # ANALYSIS:
    #1st Noise occupancy:
    Data1=np.array(datan1[0])
    d1=192*136-Enabledn2[0].size
    print(f"Masked pixels after 1st noise occupancy scan:{d1}")
    
    #Stuck pixels:
    Data2=np.array(data_s1[0])
    d2=192*136-Enabled_s2[0].size
    print(f"Masked pixels after stuck pixels occupancy scan:{d2}")
    
    #2nd Noise occupancy:
    Data3=np.array(datan2[0])
    d3=192*136-Enabled2[0].size
    print(f"Masked pixels after 2nd noise occupancy:{d3}")
    
    #Final matrix:
    Dataf= Data1-Data2+Data3
    Df=192*136-(Enabledn2[0].size-Enabled_s2[0].size+Enabled2[0].size)
    print(f"Masked pixels only after 1st and 2nd noise occupancy scan:{Df}")
    Dfinal=np.append(Dfinal,Df)
    
    #Adding values to 'Tables':
    gm={'Voltages':i, '1st_NOC':d1, 'Stuck': d2, '2nd_NOC':d3, 'Without_Stuck': Df}
    fm= fm.append(gm, ignore_index=True)
    fm.to_csv('T_bridge=-21C_WW_pc.csv')

#print(Dfinal)

# #Finding the position of the Noisy pixels:
# print(Enabledn2)




#1st noise occupancy:
fig=plt.imshow(maskn1)
plt.colorbar()
plt.show()

fig2=plt.imshow(maskn2)
plt.colorbar()
plt.show()

#Stuck pixels:
# fig_1=plt.imshow(masks1)
# plt.colorbar()
# plt.show()

# fig_2=plt.imshow(masks2)
# plt.colorbar()
# plt.show()

#2nd noise occupancy:
fig=plt.imshow(mask1)
plt.colorbar()
plt.show()

fig2=plt.imshow(mask2)
plt.colorbar()
plt.show()

# imgplot = plot(Data)
# ax1.set_title("Occupancy Map (Z Lim: %s hits)" % str(100))

#Noisy pixels Vs Temperature:
fig3 = plt.figure()
plt.ylabel('No. of Noisy Pixels')
plt.title('Noisy pixels vs Temperature')
plt.xlabel('Temperature(°C)')
tp=np.linspace(-21.8,-20.20,8)  #[T_bridge=-21C_WW_pc:(-21.8,-20.20,8);T_bridge=18_17C_pc:(-20,18,8); T_bridge=18_17C_WW_pc:(-18.3,-17,8); T_bridge=15_14C_WW_pc:(-14.3,-13.2,8)]
plt.plot(tp,Dfinal)
plt.show()