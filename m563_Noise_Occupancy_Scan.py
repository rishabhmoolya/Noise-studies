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
# with tb.open_file("/home/moolyari/DATA/m563_2022_03_08/20220309_111007_threshold_scan_interpreted.h5", 'r') as infile:
#     data1 = infile.get_node('/' + node_name)[:].T
#     mask1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
#     mask2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
# 
# =============================================================================

#Creating a file with all the values:
fm = {'Voltages':[], '1st_NOC':[], 'Stuck': [], '2nd_NOC':[], 'Without_Stuck':[], 'Temperature': []}
fm = pd.DataFrame(fm)
fm.to_csv('Noisy_m563.csv')

Dfinal = np.array([])
O_stuck = np.array([])
noisy = []
stuck = []
same = []
without_noisy = []
without_stuck = []
without_same = []
v_np600 = np.array([])
v_np700 = np.array([])
v_np800 = np.array([])
v_s600 = np.array([])
v_s700 = np.array([])
v_s800 = np.array([])
T15 = np.array([])
T18 = np.array([])
T21 = np.array([])
T_15 = np.array([])
T_18 = np.array([])
T_20 = np.array([])
V = ['100', '200', '300', '400', '500', '600', '700', '800' ]

def percentage(g):
    percent = (g * 100)/(192*136)
    return percent 

# Running a for loop to store all the values:
######################### With Wires ########################################
#for j in range(10, 21, 5):
for i in range(100, 900, 100):
    # Running an analog scan:
    with tb.open_file(f"/home/moolyari/DATA/m563_2022_03_08/m563_{i}V_Tb20C_analog_scan_interpreted.h5", 'r') as infile:
        data_a1 = infile.get_node('/' + node_name)[:].T
        maska1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
        maska2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
    # Running the 1st noise occupancy scan(without the C in the file name):
    with tb.open_file(f"/home/moolyari/DATA/m563_2022_03_08/m563_{i}V_Tb20C_(1)noise_occupancy_scan_interpreted.h5", 'r') as infile:
       datan1 = infile.get_node('/' + node_name)[:].T
       maskn1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
       maskn2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T    
    
    #Running the stuck pixel scan:
    with tb.open_file(f"/home/moolyari/DATA/m563_2022_03_08/m563_{i}V_Tb20C_stuck_pixel_scan_interpreted.h5", 'r') as infile:
        data_s1 = infile.get_node('/' + node_name)[:].T
        masks1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
        masks2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
    
    #Running the 2st noise occupancy scan:
    with tb.open_file(f"/home/moolyari/DATA/m563_2022_03_08/m563_{i}V_Tb20C_(2)noise_occupancy_scan_interpreted.h5", 'r') as infile:
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
    
    Mask_2 = np.zeros([192, 400])
    Enabled2 = np.where(mask2)
    Mask_2[Enabled2[0], Enabled2[1]] = 1
    
    # ANALYSIS:
    # 1st Noise occupancy:
    Data1 = np.array(datan1[0])
    d1 = 192*136 - Enabledn2[0].size
    print(f"Masked pixels after 1st noise occupancy scan: {d1}")
    
    # Stuck pixels:
    Data2 = np.array(data_s1[0])
    d2 = 192*136 - Enabled_s2[0].size
    print(f"Masked pixels after stuck pixels occupancy scan: {d2}")
    
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
    gm = {'Voltages':i, '1st_NOC':d1, 'Stuck':(d2 - d1), '2nd_NOC':(d3 - d2), 'Without_Stuck': abs(Df), 'Temperature': -20}
    fm = fm.append(gm, ignore_index = True)
    fm.to_csv('Noisy_m563.csv')
    
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
#     elif j == 20:
#         T20 = np.append(T20, Df)
# =============================================================================
        pn = percentage(Dfinal)
        ps = percentage(O_stuck)
        pv_np600 = percentage(v_np600)
        pv_np700 = percentage(v_np700)
        pv_np800 = percentage(v_np800)
        pv_s600 = percentage(v_s600)
        pv_s700 = percentage(v_s700)
        pv_s800 = percentage(v_s800)
        
        sum = Maskn2 + M2 +Mask_2 
        c1 = []
        c2 = []
        c3 = []
        for k in range(0, 192):
            for l in range(128, 264):
                if sum[k][l] == 0 :
                    x = {'Row':k,'Column': l}
                    c1.append(x) 
                elif sum[k][l] == 1 :
                    y = {'Row': k, 'Column': l}
                    c2.append(y)
                elif sum[k][l] == 2 :
                    z = {'Row':k,'Column': l}
                    c3.append(z)

print(f"The number of Different masked pixels:{len(c1)} pixels")              
print(f"The position of Different masked pixels:{list(c1)}" + "\n")
print(f"The number of Stuck masked pixels:{len(c2)} pixels") 
print(f"The position of Stuck masked pixels:{list(c2)}"+ "\n")
print(f"The number of Same masked pixels:{len(c3)} pixels") 
print(f"The position of Same masked pixels:{list(c3)}"+ "\n")


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
# plt.imshow(maskn1[:,128:264])
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

plt.figure(7)
plt.ylabel('Rows in LIN FE(0 to 191)', fontweight="bold")
plt.title('Output of BDAQ scans[Without row 0]', size = 14, fontweight="bold")
plt.xlabel('Columns in LIN FE(128 to 264)', fontweight="bold")
s = plt.imshow(sum[1:192,128:264]==0) 
bar = plt.colorbar(s,ticks =[1.0,0.0])
# bar.set_label('Noisy pixels', rotation=270, fontweight="bold")
bar.ax.set_yticklabels(['1.0(noisy/dead pixel)','0.0(good pixel)'])
plt.show()

plt.figure(8)
plt.ylabel('Rows in LIN FE(0 to 191)', fontweight="bold")
plt.title('Output of BDAQ scans[Without row 0]', size = 14, fontweight="bold")
plt.xlabel('Columns in LIN FE(128 to 264)', fontweight="bold")
s = plt.imshow(sum[1:192,128:264]==1) 
bar = plt.colorbar(s,ticks =[1.0,0.0])
bar.set_label('Stuck pixels', rotation=270, fontweight="bold")
# bar.ax.set_yticklabels(['1.0(stuck pixel)','0.0(noisy/dead pixel)'])
plt.show()

plt.figure(9)
plt.ylabel('Rows in LIN FE(0 to 191)', fontweight="bold")
plt.title('Output of BDAQ scans[Without row 0]', size = 14, fontweight="bold")
plt.xlabel('Columns in LIN FE(128 to 264)', fontweight="bold")
s = plt.imshow(sum[1:192,128:264]==2) 
bar = plt.colorbar(s,ticks =[1.0,0.0])
# bar.set_label('Noisy pixels', rotation=270, fontweight="bold")
bar.ax.set_yticklabels(['1.0(same masked pixel)','0.0(noisy/dead pixel)'])
plt.show()

# =============================================================================
# # Noisy pixels Vs Voltage at constant Temperature:
# plt.figure(10)
# tp = np.linspace(-14.10,-21,3)
# tp1 = np.linspace(-13.2,-21,3)
# tp2 = np.linspace(-13.3,-21.5,3)
# plt.ylabel('No. of Noisy Pixels')
# plt.title('Noisy pixels vs Voltage')
# plt.xlabel('Voltage(V)')
# plt.axis([None, None, 0, 140])
# plt.rcParams["figure.figsize"] = [7.50,3.50]
# plt.rcParams["figure.autolayout"] = True
# line1 = plt.plot(V, T15, 'ro', lw=1, label= 'T = -15???')
# line2 = plt.plot(V, T18, 'go', lw=1, label= 'T = -18???')
# line3 = plt.plot(V, T21, 'bo', lw=1, label= 'T = -21???')
# line4 = plt.plot(V, D_final, 'ko', lw=1, label= 'T = -18???(without wires')
# plt.legend()
# plt.show()
# =============================================================================
 
# Noisy pixels Vs Voltage at constant Temperature:
plt.figure(11)
tp = np.linspace(-14.10,-21,3)
tp1 = np.linspace(-13.2,-21,3)
tp2 = np.linspace(-13.3,-21.5,3)
plt.ylabel('No. of Noisy Pixels')
plt.title('Noisy pixels vs Voltage')
plt.xlabel('Voltage(V)')
plt.axis([None, None, 0, 140])
plt.rcParams["figure.figsize"] = [7.50,3.50]
plt.rcParams["figure.autolayout"] = True
line_2 = plt.plot(V, T18, 'ro', lw=1, label= 'T = -18???')
line_4 = plt.plot(V, D_final, 'bo', lw=1, label= 'T = -18???(without wires')
plt.legend()
plt.show()
 
# Noisy pixels Vs Temperature  at constant Voltage:
plt.figure(12)
tp = np.linspace(-14.10,-21,3)
tp1 = np.linspace(-13.2,-21,3)
tp2 = np.linspace(-13.3,-21.5,3)
plt.ylabel('No. of Noisy Pixels')
plt.title('Noisy pixels vs Temperature with wires')
plt.xlabel('Temperature(???)')
plt.axis([None, None, 0, 140])
plt.rcParams["figure.figsize"] = [7.50,3.50]
plt.rcParams["figure.autolayout"] = True
line1 = plt.plot(tp, v_np600, 'ro', lw=1, label= '600 V')
line2 = plt.plot(tp, v_np700, 'go', lw=1, label= '700 V')
line3 = plt.plot(tp, v_np800, 'bo', lw=1, label= '800 V')
line4 = plt.plot(-18.35, v_npwo600, 'mo', lw=1, label= '600 V (w/o wires)')
line5 = plt.plot(-18.49, v_npwo700, 'co', lw=1, label= '700 V (w/o wires)')
line6 = plt.plot(-18.39, v_npwo800, 'ko', lw=1, label= '800 V (w/o wires)')
plt.legend()
plt.show()
 
