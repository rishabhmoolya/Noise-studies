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
#fm.to_csv('Noisy_WW_pc.csv')
fm.to_csv('Noisy_Without_pc.csv')
f_m = {'Voltages':[], '1st_NOC':[], 'Stuck': [], '2nd_NOC':[], 'Without_Stuck':[]}
f_m = pd.DataFrame(f_m)
#fm.to_csv('Noisy_WW_pc.csv')
f_m.to_csv('Noisy_Without_pc.csv')
Dfinal = np.array([])
D_final = np.array([])
v_np600 = np.array([])
v_np700 = np.array([])
v_np800 = np.array([])
v_npwo600 = np.array([])
v_npwo700 = np.array([])
v_npwo800 = np.array([])
T15 = np.array([])
T18 = np.array([])
T21 = np.array([])
T_15 = np.array([])
T_18 = np.array([])
T_21 = np.array([])
V = ['100', '200', '300', '400', '500', '600', '700', '800' ]

# With jumper cables:
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
        
        # Creating an array containing the No. of noisy pixels at a given Voltage
        if i == 600:
            v_np600 = np.append(v_np600, Df)
        if i == 700:
            v_np700 = np.append(v_np700, Df)
        if i == 800:
            v_np800 = np.append(v_np800, Df)
        if j == 15:
            T15 = np.append(T15, Df)
        elif j == 18: 
            T18 = np.append(T18, Df)
        elif j == 21:
            T21 = np.append(T21, Df)
        
        ##################### Without Wires ###############################
        if j == 18:                  # Running the 1st noise occupancy scan(without the C in the file name)  
            with tb.open_file(f"/home/moolyari/Documents/Code/DATA/m611_labtest/T_bridge=18C/Without/m611_{i}V_18_noise_occupancy_scan_interpreted.h5", 'r') as infile:
               datan_1 = infile.get_node('/' + node_name)[:].T
               maskn_1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
               maskn_2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T    
            
            #Running the stuck pixel scan:
            with tb.open_file(f"/home/moolyari/Documents/Code/DATA/m611_labtest/T_bridge=18C/Without/m611_{i}V_18C_stuck_pixel_scan_interpreted.h5", 'r') as infile:
                data_s_1 = infile.get_node('/' + node_name)[:].T
                masks_1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
                masks_2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
            
            #Running the 2st noise occupancy scan:
            with tb.open_file(f"/home/moolyari/Documents/Code/DATA/m611_labtest/T_bridge=18C/Without/m611_{i}V_18C_noise_occupancy_scan_interpreted.h5", 'r') as infile:
               datan_2 = infile.get_node('/' + node_name)[:].T
               mask_1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
               mask_2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T   
               
            # 1st Noise occupancy:
            # config_in file:
            Maskn_1 = np.zeros([192, 400])
            Enabled_w = np.where(maskn_1)
            Maskn_1[Enabled_w[0], Enabled_w[1]] = 1
            # config_out file:
            Maskn_2 = np.zeros([192, 400])
            Enabledn_2 = np.where(maskn_2)
            Maskn_2[Enabledn_2[0], Enabledn_2[1]] = 1

            # Stuck pixels:
            # config_in file:
            M01 = np.zeros([192, 400]) ####change the number of rows and columns for Linear FE(128-264) but code uses 127.5 to 263.5##### 
            Enabled_ws = np.where(masks_1)
            # print(Enabled)
            M01[Enabled_ws[0], Enabled_ws[1]] = 1
            # config_out file:
            M02 = np.zeros([192, 400])
            Enabled_ws2 = np.where(masks_2)
            # print(Enabled)
            M02[Enabled_ws2[0], Enabled_ws2[1]] = 1
            
            # 2nd Noise occupancy:
            Mask_01 = np.zeros([192, 400]) ####change the number of rows and columns for Linear FE(128-264) but code uses 127.5 to 263.5##### 
            Enabled_s = np.where(mask_1)
            # print(Enabled)
            Mask_01[Enabled_s[0], Enabled_s[1]] = 1
            
            Mask_02 = np.zeros([192, 400])    # [:, 126: 263]
            # Mask2 = Mask_2[:, 127: 264]
            Enabled_2 = np.where(mask_2)
            Mask_02[Enabled_2[0], Enabled_2[1]] = 1
            # print(Enabled2)
            
            # ANALYSIS:
            # 1st Noise occupancy:
            Data_1 = np.array(datan_1[0])
            d_1 = 192*136 - Enabledn_2[0].size
            print(f"Masked pixels after 1st noise occupancy scan: {d_1}")
            
            # Stuck pixels:
            Data_2 = np.array(data_s_1[0])
            d_2 = 192*136- Enabled_ws2[0].size
            print(f"Masked pixels after stuck pixels occupancy scan:{d_2}")
            
            # 2nd Noise occupancy:
            Data_3 = np.array(datan_2[0])
            d_3 = 192*136-Enabled_2[0].size
            print(f"Masked pixels after 2nd noise occupancy:{d_3}")
            
            # Final matrix:
            Data_f = Data_1 - Data_2 + Data_3
            D_f = 192 * 136 - (Enabledn_2[0].size - Enabled_ws2[0].size + Enabled_2[0].size)
            print(f"Masked pixels only after 1st and 2nd noise occupancy scan:{D_f}")
            D_final = np.append(D_final, D_f)
            
            # Adding values to 'Tables':
            g_m = {'Voltages':i, '1st_NOC':d_1, 'Stuck': d_2 - d_1, '2nd_NOC':d_3 - d_2, 'Without_Stuck': D_f, 'Temperature': -18}
            f_m = fm.append(g_m, ignore_index = True)
            f_m.to_csv('Noisy_Without_pc.csv')
            
            if i == 600:
                v_npwo600 = np.append(v_npwo600, D_f)
            if i == 700:
                v_npwo700 = np.append(v_npwo700, D_f)
            if i == 800:
                v_npwo800 = np.append(v_npwo800, D_f)
            if j == 15:
                T_15 = np.append(T_15, D_f)
            elif j == 18: 
                T_18 = np.append(T_18, D_f)
            elif j == 21:
                T_21 = np.append(T_21, D_f)
###########################################################################################################################################################


############################ PLOTS #########################
#################### Without Wires #######################
# =============================================================================
# # 1st noise occupancy:
# fig_1 = plt.imshow(maskn_1)
# plt.colorbar()
# plt.show()
# 
# fig_2 = plt.imshow(maskn_2)
# plt.colorbar()
# plt.show()
# 
# # Stuck pixels:
# # fig_01 = plt.imshow(masks_1)
# # plt.colorbar()
# # plt.show()
# 
# # fig_02 = plt.imshow(masks_2)
# # plt.colorbar()
# # plt.show()
# 
# # 2nd noise occupancy:
# figs1 = plt.imshow(mask_1)
# plt.colorbar()
# plt.show()
# 
# figs1 = plt.imshow(mask_2)
# plt.colorbar()
# plt.show()
# ###############################################################
# 
# 
# ####################### With Wires ############################
# # 1st noise occupancy:
# fig = plt.imshow(maskn1)
# plt.colorbar()
# plt.show()
# 
# fig2 = plt.imshow(maskn2)
# plt.colorbar()
# plt.show()
# 
# # Stuck pixels:
# # fig_1 = plt.imshow(masks1)
# # plt.colorbar()
# # plt.show()
# 
# # fig_2 = plt.imshow(masks2)
# # plt.colorbar()
# # plt.show()
# 
# # 2nd noise occupancy:
# fig = plt.imshow(mask1)
# plt.colorbar()
# plt.show()
# 
# fig2 = plt.imshow(mask2)
# plt.colorbar()
# plt.show()
# 
# =============================================================================
# Noisy pixels Vs Voltage at constant Temperature:
fig3 = plt.figure()
tp = np.linspace(-14.10,-21,3)
tp1 = np.linspace(-13.2,-21,3)
tp2 = np.linspace(-13.3,-21.5,3)
plt.ylabel('No. of Noisy Pixels')
plt.title('Noisy pixels vs Voltage')
plt.xlabel('Voltage(V)')
plt.axis([None, None, 0, 140])
plt.rcParams["figure.figsize"] = [7.50,3.50]
plt.rcParams["figure.autolayout"] = True
line1 = plt.plot(V, T15, 'r--o', lw=1, label= 'T = -15℃')
line2 = plt.plot(V, T18, 'g:o', lw=1, label= 'T = -18℃')
line3 = plt.plot(V, T21, 'b--o', lw=1, label= 'T = -21℃')
line4 = plt.plot(V, D_final, 'k--o', lw=1, label= 'T = -18℃(without wires')
plt.legend()
plt.show()

# Noisy pixels Vs Voltage at constant Temperature:
fig3 = plt.figure()
tp = np.linspace(-14.10,-21,3)
tp1 = np.linspace(-13.2,-21,3)
tp2 = np.linspace(-13.3,-21.5,3)
plt.ylabel('No. of Noisy Pixels')
plt.title('Noisy pixels vs Voltage')
plt.xlabel('Voltage(V)')
plt.axis([None, None, 0, 140])
plt.rcParams["figure.figsize"] = [7.50,3.50]
plt.rcParams["figure.autolayout"] = True
line_2 = plt.plot(V, T18, 'r:o', lw=1, label= 'T = -18℃')
line_4 = plt.plot(V, D_final, 'b--o', lw=1, label= 'T = -18℃(without wires')
plt.legend()
plt.show()

# Noisy pixels Vs Temperature  at constant Voltage:
fig4 = plt.figure()
tp = np.linspace(-14.10,-21,3)
tp1 = np.linspace(-13.2,-21,3)
tp2 = np.linspace(-13.3,-21.5,3)
plt.ylabel('No. of Noisy Pixels')
plt.title('Noisy pixels vs Temperature with wires')
plt.xlabel('Temperature(℃)')
plt.axis([None, None, 0, 140])
plt.rcParams["figure.figsize"] = [7.50,3.50]
plt.rcParams["figure.autolayout"] = True
line1 = plt.plot(tp, v_np600, 'r--o', lw=1, label= '600 V')
line2 = plt.plot(tp, v_np700, 'g--o', lw=1, label= '700 V')
line3 = plt.plot(tp, v_np800, 'b--o', lw=1, label= '800 V')
line4 = plt.plot(-18.35, v_npwo600, 'm:o', lw=1, label= '600 V (w/o wires)')
line5 = plt.plot(-18.49, v_npwo700, 'c:o', lw=1, label= '700 V (w/o wires)')
line6 = plt.plot(-18.39, v_npwo800, 'k:o', lw=1, label= '800 V (w/o wires)')
plt.legend()
plt.show()


# [T_bridge=-21C_WW_pc:(-21.8,-20.20,8);T_bridge=18_17C_pc:(-20,18,8); T_bridge=18_17C_WW_pc:(-18.3,-17,8); T_bridge=15_14C_WW_pc:(-14.3,-13.2,8)]


       

















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






