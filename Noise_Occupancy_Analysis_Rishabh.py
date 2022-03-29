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
# with tb.open_file("/media/rishabh/AMALA/Rishabh/m595_2022_03_10/20220310_135709_threshold_scan_interpreted.h5", 'r') as infile:
#     data1 = infile.get_node('/' + node_name)[:].T
#     mask1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
#     mask2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
# 
# =============================================================================

#Creating a file with all the values:
fm = {'Voltages':[], '1st_NOC':[], 'Stuck': [], '2nd_NOC':[], 'Without_Stuck':[]}
fm = pd.DataFrame(fm)
fm.to_csv('Noisy_m595.csv')

Dfinal = np.array([])
pos = {}
pos = pd.DataFrame(pos)
pos1 = {}
pos1 = pd.DataFrame(pos1)
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

# Running a for loop to store all the values:
######################### With Wires ########################################
for j in range(20, 5, -5):
    for i in range(100, 900, 100):
        if j == 15 and i in range(100, 600):
            continue
        if j == 10 and i in range(100,600):
            continue
        if j == 10 and i in range(700,900):
            continue
        if j == 12 and i in range(100, 600):
            continue
    # Running an analog scan:
    with tb.open_file(f"/media/rishabh/AMALA/Rishabh/m595_2022_03_10/m595_{i}V_Tb20C_analog_scan_interpreted.h5", 'r') as infile:
        data_a1 = infile.get_node('/' + node_name)[:].T
        maska1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
        maska2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
    # Running the 1st noise occupancy scan(without the C in the file name):
    with tb.open_file(f"/media/rishabh/AMALA/Rishabh/m595_2022_03_10/m595_{i}V_Tb20C_(1)noise_occupancy_scan_interpreted.h5", 'r') as infile:
       datan1 = infile.get_node('/' + node_name)[:].T
       maskn1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
       maskn2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T    
    
    #Running the stuck pixel scan:
    with tb.open_file(f"/media/rishabh/AMALA/Rishabh/m595_2022_03_10/m595_{i}V_Tb20C_stuck_pixel_scan_interpreted.h5", 'r') as infile:
        data_s1 = infile.get_node('/' + node_name)[:].T
        masks1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
        masks2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
    
    #Running the 2st noise occupancy scan:
    with tb.open_file(f"/media/rishabh/AMALA/Rishabh/m595_2022_03_10/m595_{i}V_Tb20C_(2)noise_occupancy_scan_interpreted.h5", 'r') as infile:
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
    # 1st Noise occupancy:
    Data1 = np.array(datan1[0])
    d1 = 192*136 - Enabledn2[0].size
    print(f"Masked pixels after 1st noise occupancy scan: {d1}")
    
    # Stuck pixels:
    Data2 = np.array(data_s1[0])
    d2 = 192*136- Enabled_s2[0].size
    print(f"Masked pixels after stuck pixels occupancy scan:{abs(d2 - d1)}")
    
    # 2nd Noise occupancy:
    Data3 = np.array(datan2[0])
    d3 = 192*136-Enabled2[0].size
    print(f"Masked pixels after 2nd noise occupancy:{abs(d3 - d2)}")
    
    # Final matrix:
    Dataf = Data1 - Data2 + Data3
    Df = 192 * 136 - (Enabledn2[0].size - Enabled_s2[0].size + Enabled2[0].size)
    print(f"Masked pixels only after 1st and 2nd noise occupancy scan:{abs(Df)}" + "\n")
    Dfinal = np.append(Dfinal, Df)
    
    # Adding values to 'Tables':
    gm = {'Voltages':i, '1st_NOC':d1, 'Stuck': abs(d2 - d1), '2nd_NOC':abs(d3 - d2), 'Without_Stuck': abs(Df)}
    fm = fm.append(gm, ignore_index = True)
    fm.to_csv('Noisy_m595.csv')
    
    # Creating an array containing the No. of noisy pixels at a given Voltage
    if i == 600:
        v_np600 = np.append(v_np600, Df)
    if i == 700:
        v_np700 = np.append(v_np700, Df)
    if i == 800:
        v_np800 = np.append(v_np800, Df)
# =============================================================================
#     if j == 15:
#         T15 = np.append(T15, Df)
#     elif j == 18: 
#         T18 = np.append(T18, Df)
#     elif j == 21:
#         T21 = np.append(T21, Df)
# =============================================================================
    
        sum = Maskn2 + Mask_2
        c1 = []
        c2 = []
        for k in range(0, 191):
            for l in range(128, 264):
                if sum[k][l] == 0 :
                    x = {'Row':k,'Column': l}
                    c1.append(x) 
                elif sum[k][l] == 1 :
                    y = {'Row':k,'Column': l}
                    c2.append(y)


print(f"The number of Different masked pixels:{len(c1)}")              
print(f"The position of Different masked pixels:{list(c1)}" + "\n")
print(f"The number of Same masked pixels:{len(c2)}") 
print(f"The position of Same masked pixels:{list(c2)}"+ "\n")


# =============================================================================
# pos = pos.append(c1, ignore_index = True)  
# pos1 = pos1.append(c2, ignore_index = True)
# print(f"The position of Different masked pixels:{pos}")
# print(f"The position of Same masked pixels:{pos1}")
# =============================================================================

############################ PLOTS #########################

# =============================================================================
# # 1st noise occupancy:
# plt.figure(1)
# plt.imshow(maskn1)
# plt.colorbar()
# plt.show()
# 
# plt.figure(2) 
# plt.imshow(maskn2[:,128:264])
# plt.colorbar()
# plt.show()
# 
# # Stuck pixels:
# plt.figure(3)
# plt.imshow(masks1[:,128:264])
# plt.colorbar()
# plt.show()
# 
# plt.figure(4)
# plt.imshow(masks2[:,128:264])
# plt.colorbar()
# plt.show()
#  
# # 2nd noise occupancy:
# plt.figure(5)
# plt.imshow(mask1[:,128:264])
# plt.colorbar()
# plt.show()
# 
# plt.figure(6) 
# plt.imshow(mask2[:,128:264])
# plt.colorbar()
# plt.show()
# =============================================================================

# Noisy pixels Vs Voltage at constant Temperature:
plt.figure(7)
plt.ylabel('No. of Noisy Pixels')
plt.title('Noisy pixels vs Voltage')
plt.xlabel('Voltage(V)')
plt.axis([None, None, 0, 200])
plt.yticks(np.arange(min(T20)-2,max(T20),5))
plt.rcParams["figure.figsize"] = [7.50,3.50]
plt.rcParams["figure.autolayout"] = True
line3 = plt.plot(V, T20, 'bo', lw=1, label= 'T = -20℃')
plt.legend()
plt.show()


# =============================================================================
# # Noisy pixels Vs Voltage(600V, 700V, 800V) at constant Temperature:
# plt.figure(8)
# plt.ylabel('No. of Noisy Pixels')
# plt.title('Noisy pixels vs Voltage')
# plt.xlabel('Voltage(V)')
# plt.axis([None, None, 0, 200])
# plt.yticks(np.arange(0,max(T20),5))
# plt.rcParams["figure.figsize"] = [7.50,3.50]
# plt.rcParams["figure.autolayout"] = True
# line1 = plt.plot(V, T10, 'ro', lw=1, label= 'T = -10℃')
# line2 = plt.plot(V, T15, 'go', lw=1, label= 'T = -15℃')
# line3 = plt.plot(V, T20, 'b--o', lw=1, label= 'T = -20℃')
# plt.legend()
# plt.show() 
# =============================================================================
 
# Noisy pixels Vs Temperature  at constant Voltage:
plt.figure(9)
tp = np.linspace(-20,-10,3)
plt.ylabel('No. of Noisy Pixels')
plt.title('Noisy pixels vs Temperature')
plt.xlabel('Temperature(℃)')
plt.axis([None, None, 0, 345])
plt.yticks(np.arange(min(v_np600)-4,max(v_np800),5))
plt.rcParams["figure.figsize"] = [11.50,5.50]
plt.rcParams["figure.autolayout"] = True
#plt.xticks(ticks = tickvalues ,labels = labellist, rotation = 'vertical')
line1 = plt.plot(tp, v_np600, 'ro', lw=1, label= '600 V')
# =============================================================================
# line2 = plt.plot(tp, v_np700, 'go', lw=1, label= '700 V')
# line3 = plt.plot(tp, v_np800, 'bo', lw=1, label= '800 V')
# =============================================================================
plt.legend()
plt.show()

plt.figure(10)
plt.imshow(sum[:,128:264])
plt.colorbar()
plt.show()

# Stuck output and 2nd Noise input:
plt.figure(11)
plt.imshow(M2 - Mask_1)
plt.colorbar()
plt.show()

# Stuck output and 2nd Noise output:
plt.figure(12)
plt.imshow(M2 - Mask_2)
plt.colorbar()
plt.show()

# 1st Noise output and 2nd Noise input:
plt.figure(13)
plt.imshow(Maskn2 - Mask_2)
plt.colorbar()
plt.show()
 
