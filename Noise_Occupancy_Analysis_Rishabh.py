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
Dfinal = np.array([])
v_np600 = np.array([])
v_np700 = np.array([])
v_np800 = np.array([])
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


# Position of the noisy pixels:
c = 0
if Df = 0:
    c = c + 1
    print(f"Pixels masked after the 1st Noise Occupancy Scan:{c}")
    

############################ PLOTS #########################
# =============================================================================
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
# # Noisy pixels Vs Voltage:
# fig3 = plt.figure()
# plt.ylabel('No. of Noisy Pixels')
# plt.title('Noisy pixels vs Voltage')
# plt.xlabel('Voltage(V)')
# plt.plot(V, Dfinal)
# plt.show()
# =============================================================================

# [T_bridge=-21C_WW_pc:(-21.8,-20.20,8);T_bridge=18_17C_pc:(-20,18,8); T_bridge=18_17C_WW_pc:(-18.3,-17,8); T_bridge=15_14C_WW_pc:(-14.3,-13.2,8)]

v600 = fm[fm['Voltages'] == 600]
v700 = fm[fm['Voltages'] == 700]
v800 = fm[fm['Voltages'] == 800]

print(v600)
print(v700)
print(v800)

fig4 = plt.figure()
tp = np.linspace(-14.10,-21,3)
tp1 = np.linspace(-13.2,-21,3)
tp2 = np.linspace(-13.3,-21.5,3)
plt.ylabel('No. of Noisy Pixels')
plt.title('Noisy pixels vs Temperature')
plt.xlabel('Temperature(℃)')
plt.axis([None, None, 0, 140])
plt.rcParams["figure.figsize"] = [7.50,3.50]
plt.rcParams["figure.autolayout"] = True
line1 = plt.plot(tp, v_np600, 'r--o', lw=1, label= '600 V')
line2 = plt.plot(tp, v_np700, 'g:o', lw=1, label= '700 V')
line3 = plt.plot(tp, v_np800, 'b--o', lw=1, label= '800 V')
plt.legend()
plt.show()

# =============================================================================
# fig , (ax1, ax2) = plt.subplots(1,2, figsize=(20, 6))
# plt.rcParams.update({'font.size': 16})
# fig.suptitle("Sensor "+Sensor+" -- Missing bumps: "+str(Missing[0].size)+" ("+str(Perc)+"%) -- Masked pixels: "+str(400*192-Enabled[0].size))
# imgplot = ax1.imshow(Data, vmax=VMAX)
# ax1.set_title("Occupancy Map (Z Lim: %s hits)" % str(VMAX))
# bar1=plt.colorbar(imgplot, orientation='horizontal',ax=ax1, extend='max', label='Hits')
# bar1.cmap.set_over('red')
# cmap = mpl.colors.ListedColormap(['white', 'red', 'green'])
# bounds = [0, 1, 1.9, 3]
# norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
# imgplot2 = ax2.imshow(Neglet_mat,cmap=cmap,norm=norm)
# ax2.set_title("Missing Map (Cut: < %s hits)" % str(Thr))
# bar2=plt.colorbar(imgplot2, ticks=bounds, orientation='horizontal', label='Masked                  Missing                     Good',  spacing='proportional')
# bar2.set_ticks([])
# fig.savefig(analyzed_data_file[0:-3]+'_Missing_Bumps_Thr_'+str(Thr)+'.png', format='png', dpi=300)
# =============================================================================


# =============================================================================
# # Without jumper cables: 
# for i in range(100, 900, 100):
#     
# # Running the 1st noise occupancy scan(without the C in the file name)
#     with tb.open_file(f"/home/moolyari/Documents/Code/DATA/m611_labtest/T_bridge=18C/Without/m611_{i}V_18_noise_occupancy_scan_interpreted.h5", 'r') as infile:
#        datan1 = infile.get_node('/' + node_name)[:].T
#        maskn1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
#        maskn2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T    
#     
#     #Running the stuck pixel scan:
#     with tb.open_file(f"/home/moolyari/Documents/Code/DATA/m611_labtest/T_bridge=18C/Without/m611_{i}V_18C_stuck_pixel_scan_interpreted.h5", 'r') as infile:
#         data_s1 = infile.get_node('/' + node_name)[:].T
#         masks1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
#         masks2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
#     
#     #Running the 2st noise occupancy scan:
#     with tb.open_file(f"/home/moolyari/Documents/Code/DATA/m611_labtest/T_bridge=18C/Without/m611_{i}V_18C_noise_occupancy_scan_interpreted.h5", 'r') as infile:
#        datan2 = infile.get_node('/' + node_name)[:].T
#        mask1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
#        mask2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T   
#        
#     # 1st Noise occupancy:
#     # config_in file:
#     Maskn1 = np.zeros([192, 400])
#     Enabled = np.where(maskn1)
#     Maskn1[Enabled[0], Enabled[1]] = 1
#     # config_out file:
#     Maskn2 = np.zeros([192, 400])
#     Enabledn2 = np.where(maskn2)
#     Maskn2[Enabledn2[0], Enabledn2[1]] = 1
# 
#     # Stuck pixels:
#     # config_in file:
#     M1 = np.zeros([192, 400]) ####change the number of rows and columns for Linear FE(128-264) but code uses 127.5 to 263.5##### 
#     Enabled_s = np.where(masks1)
#     # print(Enabled)
#     M1[Enabled_s[0], Enabled_s[1]] = 1
#     # config_out file:
#     M2 = np.zeros([192, 400])
#     Enabled_s2 = np.where(masks2)
#     # print(Enabled)
#     M2[Enabled_s2[0], Enabled_s2[1]] = 1
#     
#     # 2nd Noise occupancy:
#     Mask_1 = np.zeros([192, 400]) ####change the number of rows and columns for Linear FE(128-264) but code uses 127.5 to 263.5##### 
#     Enabled = np.where(mask1)
#     # print(Enabled)
#     Mask_1[Enabled[0], Enabled[1]] = 1
#     
#     Mask_2 = np.zeros([192, 400])    # [:, 126: 263]
#     # Mask2 = Mask_2[:, 127: 264]
#     Enabled2 = np.where(mask2)
#     Mask_2[Enabled2[0], Enabled2[1]] = 1
#     # print(Enabled2)
#     
#     # ANALYSIS:
#     # 1st Noise occupancy:
#     Data1 = np.array(datan1[0])
#     d1 = 192*136 - Enabledn2[0].size
#     print(f"Masked pixels after 1st noise occupancy scan: {d1}")
#     
#     # Stuck pixels:
#     Data2 = np.array(data_s1[0])
#     d2 = 192*136- Enabled_s2[0].size
#     print(f"Masked pixels after stuck pixels occupancy scan:{d2}")
#     
#     # 2nd Noise occupancy:
#     Data3 = np.array(datan2[0])
#     d3 = 192*136-Enabled2[0].size
#     print(f"Masked pixels after 2nd noise occupancy:{d3}")
#     
#     # Final matrix:
#     Dataf = Data1 - Data2 + Data3
#     Df = 192 * 136 - (Enabledn2[0].size - Enabled_s2[0].size + Enabled2[0].size)
#     print(f"Masked pixels only after 1st and 2nd noise occupancy scan:{Df}")
#     Dfinal = np.append(Dfinal, Df)
#     
#     # Adding values to 'Tables':
#     gm = {'Voltages':i, '1st_NOC':d1, 'Stuck': d2 - d1, '2nd_NOC':d3 - d2, 'Without_Stuck': Df, 'Temperature': -18}
#     fm = fm.append(gm, ignore_index = True)
#     fm.to_csv('Noisy_Without_pc.csv')
#     
# # =============================================================================
# #     # Creating an array containing the No. of noisy pixels at a given Voltage
# #     if i == 600:
# #         v_np600 = np.append(v_np600, Df)
# #     if i == 700:
# #         v_np700 = np.append(v_np700, Df)
# #     if i == 800:
# #         v_np800 = np.append(v_np800, Df)
# # =============================================================================
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
# # =============================================================================
# # # Noisy pixels Vs Voltage:
# # fig3 = plt.figure()
# # plt.ylabel('No. of Noisy Pixels')
# # plt.title('Noisy pixels vs Voltage')
# # plt.xlabel('Voltage(V)')
# # plt.plot(V, Dfinal)
# # plt.show()
# # =============================================================================
# 
# # Noisy pixels Vs Temperature:
# fig3 = plt.figure()
# plt.ylabel('No. of Noisy Pixels')
# plt.title('Noisy pixels vs Temperature without wires')
# plt.xlabel('Temperature(C)')
# tp = np.linspace(-18,-20,3)
# plt.plot(tp, Dfinal)
# plt.show()
# 
# # [T_bridge=-21C_WW_pc:(-21.8,-20.20,8);T_bridge=18_17C_pc:(-20,18,8); T_bridge=18_17C_WW_pc:(-18.3,-17,8); T_bridge=15_14C_WW_pc:(-14.3,-13.2,8)]
# print(fm)
# # =============================================================================
# # fig4 = plt.figure()
# # plt.ylabel('No. of Noisy Pixels')
# # plt.title('Noisy pixels vs Temperature @ 600V')
# # plt.xlabel('Temperature(C)')
# # tp = np.linspace(-14.10,-21,3)
# # plt.plot(tp, v_np600)
# # plt.show()
# # 
# # fig5 = plt.figure()
# # plt.ylabel('No. of Noisy Pixels')
# # plt.title('Noisy pixels vs Temperature @ 700V')
# # plt.xlabel('Temperature(C)')
# # tp1 = np.linspace(-13.2,-21,3)
# # plt.plot(tp, v_np700 )
# # plt.show()
# # 
# # fig6 = plt.figure()
# # plt.ylabel('No. of Noisy Pixels')
# # plt.title('Noisy pixels vs Temperature @ 800V')
# # plt.xlabel('Temperature(C)')
# # tp2 = np.linspace(-13.3,-21.5,3)
# # plt.plot(tp, v_np800)
# # plt.show()
# # 
# # v600 = fm[fm['Voltages'] == 600]
# # v700 = fm[fm['Voltages'] == 700]
# # v800 = fm[fm['Voltages'] == 800]
# # 
# # print(v600)
# # print(v700)
# # print(v800)
# # =============================================================================
#        
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






