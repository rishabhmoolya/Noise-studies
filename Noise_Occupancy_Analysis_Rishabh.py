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

# =============================================================================
# Running the threshold_gold scan:
# with tb.open_file("20211111_140024_threshold_scan_interpreted.h5", 'r') as infile:
#     data1 = infile.get_node('/' + node_name)[:].T
#     mask1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
#     mask2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
# 
# Running an analog scan:
# with tb.open_file("WW/m611_200V_WW_17C_analog_scan_interpreted.h5", 'r') as infile:
#     data1 = infile.get_node('/' + node_name)[:].T
#     mask1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
#     mask2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
# =============================================================================

#Creating a file with all the values:
fm = {'Voltages':[], '1st_NOC':[], 'Stuck': [], '2nd_NOC':[], 'Without_Stuck':[]}
fm = pd.DataFrame(fm)
fm.to_csv('Noisy_WW_pc.csv')

Dfinal = np.array([])
V = ['100', '200', '300', '400', '500', '600', '700', '800' ]


# Number of Noisy Pixels Vs Voltage:
# Running a for loop to store all the values:
for j in range(15, 24, 3):
    for i in range(100, 900, 100):
        # Running the 1st noise occupancy scan(without the C in the file name):
        with tb.open_file(f"/home/moolyari/Documents/Code/DATA/m611_labtest/T_bridge={j}C/m611_{i}V_WW_{j}_noise_occupancy_scan_interpreted.h5", 'r') as infile:
           datan1 = infile.get_node('/' + node_name)[:].T
           maskn1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
           maskn2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T    
        
        #Running the stuck pixel scan:
        with tb.open_file(f"/home/moolyari/Documents/Code/DATA/m611_labtest/T_bridge={j}C/m611_{i}V_WW_{j}C_stuck_pixel_scan_interpreted.h5", 'r') as infile:
            data_s1 = infile.get_node('/' + node_name)[:].T
            masks1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
            masks2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
        
        #Running the 2st noise occupancy scan:
        with tb.open_file(f"/home/moolyari/Documents/Code/DATA/m611_labtest/T_bridge={j}C/m611_{i}V_WW_{j}C_noise_occupancy_scan_interpreted.h5", 'r') as infile:
           datan2 = infile.get_node('/' + node_name)[:].T
           mask1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
           mask2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
           
# =============================================================================
#          with tb.open_file(f"/home/moolyari/Documents/Code/DATA/m611_labtest/T_bridge={j}C/Without/m611_{i}V_WW_17_noise_occupancy_scan_interpreted.h5", 'r') as infile:
#             datan1 = infile.get_node('/' + node_name)[:].T
#             maskn1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
#             maskn2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T    
#          
#          #Running the stuck pixel scan:
#          with tb.open_file(f"/home/moolyari/Documents/Code/DATA/m611_labtest/T_bridge={j}C/Without/m611_{i}V_WW_17C_stuck_pixel_scan_interpreted.h5", 'r') as infile:
#              data_s1 = infile.get_node('/' + node_name)[:].T
#              masks1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
#              masks2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
#          
#          #Running the 2st noise occupancy scan:
#          with tb.open_file(f"/home/moolyari/Documents/Code/DATA/m611_labtest/T_bridge={j}C/Without/m611_{i}V_WW_17C_noise_occupancy_scan_interpreted.h5", 'r') as infile:
#             datan2 = infile.get_node('/' + node_name)[:].T
#             mask1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
#             mask2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T   
# =============================================================================
           
        # 1st Noise occupancy:
        # config_in file:
        Maskn1 = np.zeros([192, 400])
        Enabled = np.where(maskn1)
        Maskn1[Enabled[0], Enabled[1]] = 1
        # config_out file:
        Maskn2 = np.zeros([192, 400])
        Enabledn2 = np.where(maskn2)
        Maskn2[Enabledn2[0], Enabledn2[1]] = 1

        # Stuck pixels:
        # config_in file:
        M1 = np.zeros([192, 400]) ####change the number of rows and columns for Linear FE(128-264) but code uses 127.5 to 263.5##### 
        Enabled_s = np.where(masks1)
        # print(Enabled)
        M1[Enabled_s[0], Enabled_s[1]] = 1
        # config_out file:
        M2 = np.zeros([192, 400])
        Enabled_s2 = np.where(masks2)
        # print(Enabled)
        M2[Enabled_s2[0], Enabled_s2[1]] = 1
        
        # 2nd Noise occupancy:
        Mask_1 = np.zeros([192, 400]) ####change the number of rows and columns for Linear FE(128-264) but code uses 127.5 to 263.5##### 
        Enabled = np.where(mask1)
        # print(Enabled)
        Mask_1[Enabled[0], Enabled[1]] = 1
        
        Mask_2 = np.zeros([192, 400])    # [:, 126: 263]
        # Mask2 = Mask_2[:, 127: 264]
        Enabled2 = np.where(mask2)
        Mask_2[Enabled2[0], Enabled2[1]] = 1
        # print(Enabled2)
        
        # ANALYSIS:
        # 1st Noise occupancy:
        Data1 = np.array(datan1[0])
        d1 = 192*136 - Enabledn2[0].size
        print(f"Masked pixels after 1st noise occupancy scan: {d1}")
        
        # Stuck pixels:
        Data2 = np.array(data_s1[0])
        d2 = 192*136- Enabled_s2[0].size
        print(f"Masked pixels after stuck pixels occupancy scan:{d2}")
        
        # 2nd Noise occupancy:
        Data3 = np.array(datan2[0])
        d3 = 192*136-Enabled2[0].size
        print(f"Masked pixels after 2nd noise occupancy:{d3}")
        
        # Final matrix:
        Dataf = Data1 - Data2 + Data3
        Df = 192 * 136 - (Enabledn2[0].size - Enabled_s2[0].size + Enabled2[0].size)
        print(f"Masked pixels only after 1st and 2nd noise occupancy scan:{Df}")
        Dfinal = np.append(Dfinal, Df)
        
        # Adding values to 'Tables':
        gm = {'Voltages':i, '1st_NOC':d1, 'Stuck': d2 - d1, '2nd_NOC':d3 - d2, 'Without_Stuck': Df, 'Temperature': -j}
        fm = fm.append(gm, ignore_index = True)
        fm.to_csv('Noisy_WW_pc.csv')
        

print(fm)
# 1st noise occupancy:
fig = plt.imshow(maskn1)
plt.colorbar()
plt.show()

fig2 = plt.imshow(maskn2)
plt.colorbar()
plt.show()

# Stuck pixels:
# fig_1 = plt.imshow(masks1)
# plt.colorbar()
# plt.show()

# fig_2 = plt.imshow(masks2)
# plt.colorbar()
# plt.show()

# 2nd noise occupancy:
fig = plt.imshow(mask1)
plt.colorbar()
plt.show()

fig2 = plt.imshow(mask2)
plt.colorbar()
plt.show()

# Noisy pixels Vs Voltage:
fig3 = plt.figure()
plt.ylabel('No. of Noisy Pixels')
plt.title('Noisy pixels vs Voltage')
plt.xlabel('Voltage(V)')
plt.plot(V, Dfinal)
plt.show()


# =============================================================================
# # Noisy pixels Vs Temperature:
#     
# #Creating a file with all the values:
# fm0 = {'Voltages':[], '1st_NOC':[], 'Stuck': [], '2nd_NOC':[], 'Without_Stuck':[]}
# fm0 = pd.DataFrame(fm0)
# fm0.to_csv('T_bridge=-21C_WW_T.csv')
# 
# D0final = np.array([])
# V0 = [ '600', '700', '800' ]    
#     
# # Running a for loop to store all the values:
# for i in range(600, 900, 100):
#     # Running the 1st noise occupancy scan(without the C in the file name):
#     with tb.open_file(f"/home/moolyari/Documents/Code/DATA/m611_labtest/T_bridge=-21C/m611_{i}V_23_noise_occupancy_scan_interpreted.h5", 'r') as infile:
#        datan01 = infile.get_node('/' + node_name)[:].T
#        maskn01 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
#        maskn02 = infile.get_node('/configuration_out/chip/masks/enable')[:].T    
#     
#     #Running the stuck pixel scan:
#     with tb.open_file(f"/home/moolyari/Documents/Code/DATA/m611_labtest/T_bridge=-21C/m611_{i}V_23C_stuck_pixel_scan_interpreted.h5", 'r') as infile:
#         data_s01 = infile.get_node('/' + node_name)[:].T
#         masks01 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
#         masks02 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
#     
#     #Running the 2st noise occupancy scan:
#     with tb.open_file(f"/home/moolyari/Documents/Code/DATA/m611_labtest/T_bridge=-21C/m611_{i}V_23C_noise_occupancy_scan_interpreted.h5", 'r') as infile:
#        datan02 = infile.get_node('/' + node_name)[:].T
#        mask01 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
#        mask02 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
#        
#     # 1st Noise occupancy:
#     # config_in file:
#     maskn1 = np.zeros([192, 400])
#     enabled = np.where(maskn01)
#     maskn1[enabled[0], enabled[1]] = 1
#     # config_out file:
#     maskn2 = np.zeros([192, 400])
#     enabledn2 = np.where(maskn02)
#     maskn2[enabledn2[0], enabledn2[1]] = 1
# 
#     # Stuck pixels:
#     # config_in file:
#     m1 = np.zeros([192, 400]) ####change the number of rows and columns for Linear FE(128-264) but code uses 127.5 to 263.5##### 
#     enabled_s = np.where(masks01)
#     m1[enabled_s[0], enabled_s[1]] = 1
#     # config_out file:
#     m2 = np.zeros([192, 400])
#     enabled_s2 = np.where(masks02)
#     m2[enabled_s2[0], enabled_s2[1]] = 1
#     
#     # 2nd Noise occupancy:
#     mask_1 = np.zeros([192, 400]) ####change the number of rows and columns for Linear FE(128-264) but code uses 127.5 to 263.5##### 
#     enabled = np.where(mask01)
#     mask_1[enabled[0], enabled[1]] = 1
#     
#     mask_2 = np.zeros([192, 400])    # [:, 126: 263]
#     # Mask2 = Mask_2[:, 127: 264]
#     enabled2 = np.where(mask02)
#     mask_2[enabled2[0], enabled2[1]] = 1
# 
#     
#     # ANALYSIS:
#     # 1st Noise occupancy:
#     Data01 = np.array(datan01[0])
#     d01 = 192*136 - enabledn2[0].size
#     print(f"Masked pixels after 1st noise occupancy scan: {d01}")
#     
#     # Stuck pixels:
#     Data02 = np.array(data_s01[0])
#     d02 = 192*136- enabled_s2[0].size
#     print(f"Masked pixels after stuck pixels occupancy scan:{d02}")
#     
#     # 2nd Noise occupancy:
#     Data03 = np.array(datan02[0])
#     d03 = 192*136-enabled2[0].size
#     print(f"Masked pixels after 2nd noise occupancy:{d03}")
#     
#     # Final matrix:
#     Data0f = Data01 - Data02 + Data03
#     D0f = 192 * 136 - (enabledn2[0].size - enabled_s2[0].size + enabled2[0].size)
#     print(f"Masked pixels only after 1st and 2nd noise occupancy scan:{D0f}")
#     D0final = np.append(D0final, D0f)
#     
#     # Adding values to 'Tables':
#     gm0 = {'Voltages':i, '1st_NOC':d01, 'Stuck': d02, '2nd_NOC':d03, 'Without_Stuck': D0f}
#     fm0 = fm0.append(gm0, ignore_index = True)
#     fm0.to_csv('T_bridge=-21C_WW_T.csv')
#     
#     
#         
# 
# # 1st noise occupancy:
# fig = plt.imshow(maskn01)
# plt.colorbar()
# plt.show()
#  
# fig2 = plt.imshow(maskn02)
# plt.colorbar()
# plt.show()
#  
# # =============================================================================
# # Stuck pixels:
# # fig_1 = plt.imshow(masks01)
# # plt.colorbar()
# # plt.show()
# #  
# # fig_2 = plt.imshow(masks02)
# # plt.colorbar()
# # plt.show()
# # =============================================================================
#  
# # 2nd noise occupancy:
# fig = plt.imshow(mask01)
# plt.colorbar()
# plt.show()
# 
# fig2 = plt.imshow(mask02)
# plt.colorbar()
# plt.show()
# =============================================================================


# =============================================================================
# fig3 = plt.figure()
# plt.ylabel('No. of Noisy Pixels')
# plt.title('Noisy pixels vs Temperature')
# plt.xlabel('Voltage(V)')
# tp = np.linspace(-21.8,-20.20,8)  #[T_bridge=-21C_WW_pc:(-21.8,-20.20,8);T_bridge=18_17C_pc:(-20,18,8); T_bridge=18_17C_WW_pc:(-18.3,-17,8); T_bridge=15_14C_WW_pc:(-14.3,-13.2,8)]
# plt.plot(V, Dfinal)
# plt.show()
# =============================================================================


















# Trial and Error:
# =============================================================================
# Mask_3 = Mask_1 - Mask_2
# print (Dfinal)
# print (Enabledn2)
# print (V)
# =============================================================================

#Finding the position of the Noisy pixels:
# =============================================================================
# pos = 0
# for i in range(len(Maskn2)):
#   if Maskn2[i]==1: 
#       print(f"The position of the noisy pixel is:{Enabledn2[i]}")
# =============================================================================
 
# for i in  range(len(Maskn2)):    
#    print (Maskn2[i]==1)


# imgplot = plot(Data)
# ax1.set_title("Occupancy Map (Z Lim: %s hits)" % str(100))






