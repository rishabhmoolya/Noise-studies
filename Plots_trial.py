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
from scipy.stats import norm
import statistics
sys.path.append('./Lib/')
node_name = 'HistOcc'

#Creating a file with all the values:
fm = {'Voltages':[], '1st_NOC':[], 'Stuck': [], '2nd_NOC':[], 'Without_Stuck':[]}
fm = pd.DataFrame(fm)
fm.to_csv('Noisy_m595(13th April).csv')

Dfinal = np.array([])
O_stuck = np.array([])
D_final = np.array([])
v_np600 = np.array([])
v_np700 = np.array([])
v_np800 = np.array([])
v600T26 = np.array([])
v700T26 = np.array([])
v800T26 = np.array([])
v600nT20 = np.array([])
v600sT20 = np.array([])
meannT20 = np.array([])
meansT20 = np.array([])
v700T20 = np.array([])
v800T20 = np.array([])
errorn = np.array([])
errors = np.array([])
stdnT20 = np.array([])
stdnsT20 = np.array([])

T10 = np.array([])
T26 = np.array([])
T20 = np.array([])
V = [ '300', '400', '500', '600', '700', '800' ]

def percentage(g):
    percent = (g * 100)/(192*136)
    return percent


#Running the threshold_gold scan:
with tb.open_file("/media/rishabh/RISHABH/m595_2022_04_13/20220413_161844_threshold_scan_interpreted.h5", 'r') as infile:
    data1 = infile.get_node('/' + node_name)[:].T
    maskt1 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
    maskt2 = infile.get_node('/configuration_in/chip/masks/enable')[:].T

# config_in file:
Maskt1 = np.zeros([192, 400])
Enabled = np.where(maskt1)
Maskt1[Enabled[0], Enabled[1]] = 1
# config_out file:
Maskt2 = np.zeros([192, 400])
Enabledt2 = np.where(maskt2)
Maskt2[Enabledt2[0], Enabledt2[1]] = 1

# Running a for loop to store all the values:
# Running an analog scan:
for i in range (1,9,1):
    with tb.open_file(f"/media/rishabh/RISHABH/m595_2022_04_13/m595_(r{i})600V_Tb20C_analog_scan_interpreted.h5", 'r') as infile:
                    data_a1 = infile.get_node('/' + node_name)[:].T
                    maska1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
                    maska2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
                    
    # Running the 1st noise occupancy scan:
    with tb.open_file(f"/media/rishabh/RISHABH/m595_2022_04_13/m595_(r{i})600V_Tb20C_(1)noise_occupancy_scan_interpreted.h5", 'r') as infile:
       datan1 = infile.get_node('/' + node_name)[:].T
       maskn1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
       maskn2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T   
                
    #Running the stuck pixel scan:
    with tb.open_file(f"/media/rishabh/RISHABH/m595_2022_04_13/m595_(r{i})600V_Tb20C_stuck_pixel_scan_interpreted.h5", 'r') as infile:
        data_s1 = infile.get_node('/' + node_name)[:].T
        masks1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
        masks2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
                
    #Running the 2st noise occupancy scan:
    with tb.open_file(f"/media/rishabh/RISHABH/m595_2022_04_13/m595_(r{i})600V_Tb20C_(2)noise_occupancy_scan_interpreted.h5", 'r') as infile:
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
    # 1st Noise occupancy:
    Data1 = np.array(datan1[0])
    d1 = 192*136 - Enabledn2[0].size
    print(f"Masked pixels after 1st noise occupancy scan: {d1}")

    # Stuck pixels:
    Data2 = np.array(data_s1[0])
    d2 = 192*136- Enabled_s2[0].size
    o_stuck = (d2-d1)
    print(f"Masked pixels after stuck pixels occupancy scan:{d2 - d1}")
    O_stuck = np.append(O_stuck,o_stuck)


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
    gm = {'Voltages':i, '1st_NOC':d1, 'Stuck': (d2 - d1), '2nd_NOC':(d3 - d2), 'Without_Stuck': Df, 'Temperature': -20}
    fm = fm.append(gm, ignore_index = True)
    fm.to_csv('Noisy_m595(13th April).csv')

    pn = percentage(Dfinal)
    ps = percentage(O_stuck)
    v600nT20 = np.append(v600nT20, Df)
    v600sT20 = np.append(v600sT20, O_stuck)
    stdnT20 = np.std(pn)
    stdsT20 = np.std(ps)
    errorn = stdnT20/np.sqrt(len(pn))
    errors = stdsT20/np.sqrt(len(ps))

    # Differentiating between a noisy and a stuck pixel:
    sum = Maskn2 + M2 + Mask_2
    c1 = []
    c2 = []
    c3 = []    
    for l in range(0, 192):
        for m in range(128, 264):
            if sum[l][m] == 0 :
                x = {'Row':l,'Column': m}
                c1.append(x) 
            elif sum[l][m] == 1 :
                y = {'Row':l,'Column': m}
                c2.append(y)
            elif sum[l][m] == 2 :
                z = {'Row':l, 'Column': m}
                c3.append(z)

                               
print(f"The number of Different masked pixels:{len(c1)}")              
print(f"The position of Different masked pixels:{list(c1)}" + "\n")
print(f"The number of Stuck masked pixels:{len(c2)}") 
print(f"The position of Stuck masked pixels:{list(c2)}"+ "\n")
print(f"The number of Same masked pixels:{len(c3)}") 
print(f"The position of Same masked pixels:{list(c3)}"+ "\n")



################################## PLOTS ######################################
# =============================================================================
# plt.figure(7)
# plt.ylabel('Rows in LIN FE(0 to 191)', fontweight="bold")
# plt.title('Output of BDAQ scans', size = 14, fontweight="bold")
# plt.xlabel('Columns in LIN FE(128 to 264)', fontweight="bold")
# s = plt.imshow(sum[0:192,128:264]) 
# bar = plt.colorbar(s, ticks =[3.0,2.0,1.0,0.0])
# bar.set_label('Noisy pixels', rotation=270, fontweight="bold")
# bar.ax.set_yticklabels(['3.0(same masked pixel)','2.0(stuck pixel)','1.0(noisy/dead pixel)','0.0(good pixel)'])
# plt.show()
# =============================================================================

plt.figure(7)
plt.ylabel('Rows in LIN FE(0 to 191)', fontweight="bold")
plt.title('Output of BDAQ scans', size = 14, fontweight="bold")
plt.xlabel('Columns in LIN FE(128 to 264)', fontweight="bold")
s = plt.imshow(sum[0:192,128:264]==0) 
bar = plt.colorbar(s,ticks =[1.0,0.0])
bar.set_label('Noisy pixels', rotation=270, fontweight="bold")
bar.ax.set_yticklabels(['1.0(noisy/dead pixel)','0.0(good pixel)'])
plt.show()

plt.figure(8)
plt.ylabel('Rows in LIN FE(0 to 191)', fontweight="bold")
plt.title('Output of BDAQ scans', size = 14, fontweight="bold")
plt.xlabel('Columns in LIN FE(128 to 264)', fontweight="bold")
s = plt.imshow(sum[0:192,128:264]==1) 
bar = plt.colorbar(s,ticks =[1.0,0.0])
bar.set_label('Stuck pixels', rotation=270, fontweight="bold")
bar.ax.set_yticklabels(['1.0(stuck pixel)','0.0(good pixel)'])
plt.show()

plt.figure(9)
plt.ylabel('Rows in LIN FE(0 to 191)', fontweight="bold")
plt.title('Output of BDAQ scans', size = 14, fontweight="bold")
plt.xlabel('Columns in LIN FE(128 to 264)', fontweight="bold")
s = plt.imshow(sum[0:192,128:264]==2) 
bar = plt.colorbar(s,ticks =[1.0,0.0])
bar.set_label('Noisy pixels', rotation=270, fontweight="bold")
bar.ax.set_yticklabels(['1.0(same masked pixel)','0.0(good pixel)'])
plt.show()

# =============================================================================
# # Reproducibilty:
# plt.figure(8)
# plt.ylabel('Noisy Pixels[%]', fontweight="bold")
# plt.title('Noisy pixels vs Time @ 600V(595, bitten, $0.862$e16 $n_{eq} . cm^{-2}$, Annealing 80.5days)', fontweight="bold")
# plt.xlabel('Time(minutes)', fontweight="bold")
# plt.axis([None, None, 0, 3])
# plt.yticks(np.arange(0,3.5,0.5))
# plt.rcParams["figure.figsize"] = [7.50,3.50]
# plt.rcParams["figure.autolayout"] = True
# t = np.linspace(10, 90, 8)
# plt.grid(color = 'black', linestyle = '--', linewidth = 0.8)
# line1 = plt.plot(t, pn, 'g--v', lw=2, label = 'Noisy pixels')
# plt.errorbar(t,pn, yerr = errorn, ecolor = 'red', elinewidth = 3, label = 'Error')
# line2 = plt.plot(t, ps, 'b:s', lw=2, label = 'Stuck pixels')
# plt.axhline(y = 1, xmin=0, xmax=1, color='k', linestyle='--', linewidth=2.5)
# plt.errorbar(t,ps, yerr = errors, ecolor = 'red', elinewidth = 3)
# plt.annotate('[261 pixels]',ha = 'center', va = 'bottom', xytext = (10.2, 1.2),xy = (10.2, 1),arrowprops = {'facecolor' : 'black'})
# plt.legend()
# plt.show()
# 
# # Reproducibilty(Zoomed in):
# plt.figure(9)
# plt.ylabel('Noisy Pixels[%]', fontweight="bold")
# plt.title('Noisy pixels vs Time @ 600V(595, bitten, $0.862$e16 $n_{eq} . cm^{-2}$, Annealing 80.5days)', fontweight="bold")
# plt.xlabel('Time(minutes)', fontweight="bold")
# plt.axis([None, None, 0, 1])
# plt.yticks(np.arange(0,1.2,0.1))
# plt.rcParams["figure.figsize"] = [7.50,3.50]
# plt.rcParams["figure.autolayout"] = True
# t = np.linspace(10, 90, 8)
# plt.grid(color = 'black', linestyle = '--', linewidth = 0.8)
# line1 = plt.plot(t, pn, 'g--v', lw=1, label = 'Noisy pixels')
# plt.errorbar(t,pn, yerr = errorn, ecolor = 'red', elinewidth = 5, label = 'Error')
# line2 = plt.plot(t, ps, 'b:s', lw=1, label = 'Stuck pixels')
# plt.axhline(y = 1, xmin=0, xmax=1, color='k', linestyle='--', linewidth=2.5)
# plt.errorbar(t,ps, yerr = errors, ecolor = 'red', elinewidth = 5)
# plt.annotate('[261 pixels]',ha = 'center', va = 'bottom', xytext = (10.2, 1.05),xy = (10.2, 1),arrowprops = {'facecolor' : 'black'})
# plt.legend()
# plt.show()
# =============================================================================

# =============================================================================
# plt.figure(10)
# plt.ylabel('No. of Pixels')
# plt.title('Noisy pixels vs Leakage Current @ 600V(Module 595)')
# plt.xlabel('Ib(\u03BCA)')
# plt.axis([None, None, 0, 10])
# plt.yticks(np.arange(0,120,10))
# plt.rcParams["figure.figsize"] = [7.50,3.50]
# plt.rcParams["figure.autolayout"] = True
# Ib = np.linspace(90, 105, 8)
# plt.grid(color = 'black', linestyle = '--', linewidth = 0.5)
# line1 = plt.plot(Ib, v600nT20, 'g--o', lw=1, label = 'Noisy pixels')
# line2 = plt.plot(Ib, v600sT20, 'b--o', lw=1, label = 'Stuck pixels')
# plt.legend()
# plt.show()
# =============================================================================

