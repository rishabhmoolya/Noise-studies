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
import scipy as sp
import scipy.stats as stat
from scipy.stats import norm
sys.path.append('./Lib/')
node_name = 'HistOcc'

# =============================================================================
# import holoviews as hv
# from holoviews import opts
# hv.extension('bokeh', 'matplotlib')
# =============================================================================

#Creating a file with all the values:
fm = {'Voltages':[], '1st_NOC':[], 'Stuck': [], '2nd_NOC':[], 'Without_Stuck':[]}
fm = pd.DataFrame(fm)
fm.to_csv('Noisy_m595(13th April).csv')

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
T10 = np.array([])
T26 = np.array([])
T20 = np.array([])
Ts20 = np.array([])
Ts26 = np.array([])
stdn600_26 = np.array([])
stdn700_26 = np.array([])
stdn800_26 = np.array([])
stds600_20 = np.array([])
stds700_20 = np.array([])
stds800_20 = np.array([])
error_n600 = np.array([])
error_n700 = np.array([])
error_n800 = np.array([])
error_s600 = np.array([])
error_s700 = np.array([])
error_s800 = np.array([])


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
for j in range(26, 19, -6):
    for i in range(300, 900, 100):
        if i == 100 and j == 26:
            continue
        if i == 200 and j == 26:
            continue
        if i == 300 and j == 26:
            continue
        if i == 400 and j == 26:
            continue
        if i == 500 and j == 26:
            continue
        for k in range(1,4,1):
            # Running an analog scan:
            with tb.open_file(f"/media/rishabh/RISHABH/m595_2022_04_13/m595_({k}){i}V_Tb{j}C_analog_scan_interpreted.h5", 'r') as infile:
                data_a1 = infile.get_node('/' + node_name)[:].T
                maska1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
                maska2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
                
            # Running the 1st noise occupancy scan:
            with tb.open_file(f"/media/rishabh/RISHABH/m595_2022_04_13/m595_({k}){i}V_Tb{j}C_(1)noise_occupancy_scan_interpreted.h5", 'r') as infile:
               datan1 = infile.get_node('/' + node_name)[:].T
               maskn1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
               maskn2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T    
            
            #Running the stuck pixel scan:
            with tb.open_file(f"/media/rishabh/RISHABH/m595_2022_04_13/m595_({k}){i}V_Tb{j}C_stuck_pixel_scan_interpreted.h5", 'r') as infile:
                data_s1 = infile.get_node('/' + node_name)[:].T
                masks1 = infile.get_node('/configuration_in/chip/masks/enable')[:].T
                masks2 = infile.get_node('/configuration_out/chip/masks/enable')[:].T
            
            #Running the 2st noise occupancy scan:
            with tb.open_file(f"/media/rishabh/RISHABH/m595_2022_04_13/m595_({k}){i}V_Tb{j}C_(2)noise_occupancy_scan_interpreted.h5", 'r') as infile:
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
            print(f"Masked pixels after stuck pixels occupancy scan:{o_stuck}")
            O_stuck = np.append(O_stuck,o_stuck)
            
            
            # 2nd Noise occupancy:
            Data3 = np.array(datan2[0])
            d3 = 192*136-Enabled2[0].size
            print(f"Masked pixels after 2nd noise occupancy:{d3 - d2}")
            
            
            # Final matrix:
            Dataf = Data1 - Data2 + Data3
            Df = 192 * 136 - (Enabledn2[0].size - Enabled_s2[0].size + Enabled2[0].size)
            print(f"Masked pixels only after 1st and 2nd noise occupancy scan:{Df}" + "\n")
            Dfinal = np.append(Dfinal, Df)
            
            # Adding values to 'Tables':
            gm = {'Voltages':i, '1st_NOC':d1, 'Stuck': (d2 - d1), '2nd_NOC':(d3 - d2), 'Without_Stuck': Df, 'Temperature': -j}
            fm = fm.append(gm, ignore_index = True)
            fm.to_csv('Noisy_m595(13th April).csv')
            
            
            # Creating an array containing the No. of noisy pixels at a given Voltage
            if i == 600:
                v_np600 = np.append(v_np600, Df)
                v_s600 = np.append(v_s600,o_stuck)
            if i == 700:
                v_np700 = np.append(v_np700, Df)
                v_s700 = np.append(v_s700,o_stuck)
            if i == 800:
                v_np800 = np.append(v_np800, Df)
                v_s800 = np.append(v_s800,o_stuck)
            if j == 20:
                T20 = np.append(T20, Df)
                Ts20 = np.append(Ts20,o_stuck)
            elif j == 26: 
                T26 = np.append(T26, Df)
                Ts26 = np.append(Ts26,o_stuck)

            pn = percentage(Dfinal)
            ps = percentage(O_stuck)
            pv_np600 = percentage(v_np600)
            pv_np700 = percentage(v_np700)
            pv_np800 = percentage(v_np800)
            pv_s600 = percentage(v_s600)
            pv_s700 = percentage(v_s700)
            pv_s800 = percentage(v_s800)
            error_n600 = np.std(pv_np600)/np.sqrt(len(pv_np600))
            error_n700 = np.std(pv_np700)/np.sqrt(len(pv_np700))
            error_n800 = np.std(pv_np800)/np.sqrt(len(pv_np800))
            error_s600 = np.std(pv_s600)/np.sqrt(len(pv_s600))
            error_s700 = np.std(pv_s700)/np.sqrt(len(pv_s700))
            error_s800 = np.std(pv_s800)/np.sqrt(len(pv_s800))

            # Differentiating between types of pixels(with rows 0 and 191):
            sum = Maskn2 + M2 + Mask_2
            c1 = []
            c2 = []
            c3 = []    
            c_1 = []
            c_2 = []
            c_3 = []
            
            for l in range(0, 192):
                for m in range(128, 264):
                    if sum[l][m] == 0 :
                        x = {l, m}
                        c1.append(x) 
                    elif sum[l][m] == 1 :
                        y = {l, m}
                        c2.append(y)
                    elif sum[l][m] == 2 :
                        z = {l,  m}
                        c3.append(z)
                        
# =============================================================================
#             for x in range(len(Dfinal)):
#                 if x <= 2:
#                     mean600_26 = np.mean(Dfinal[0:3])
#                 elif x <= 5:
#                     mean700_26 = np.mean(Dfinal[3:6])
#                 elif x <= 8:
#                     mean800_26 = np.mean(Dfinal[6:9])
# =============================================================================

print(f"The number of Different masked pixels:{len(c1)} pixels")              
print(f"The position of Different masked pixels:{list(c1)}" + "\n")
print(f"The number of Stuck masked pixels:{len(c2)} pixels") 
print(f"The position of Stuck masked pixels:{list(c2)}"+ "\n")
print(f"The number of Same masked pixels:{len(c3)} pixels") 
print(f"The position of Same masked pixels:{list(c3)}"+ "\n")

plt.figure(15)                        
_,data,_ = plt.hist(Dfinal, bins =20,density =1, alpha = 0.5)
mu, sigma = sp.stats.norm.fit(Dfinal)
best_fit_line = sp.stats.norm.pdf(data,mu,sigma)
plt.ylabel('# Noisy pixels')
plt.plot(data, best_fit_line)

# =============================================================================
# plt.figure(16)                        
# mu, sigma = sp.stats.distributions.norm.fit(Dfinal)
# fitted_line = sp.stats.distributions.norm.pdf(data,mu,sigma)
# _,data1,_ = plt.hist(Dfinal, bins =20,density =1, alpha = 0.5)
# plt.ylabel('# Noisy pixels')
# plt.plot(data, fitted_line)
# 
# plt.hist(Dfinal, density = True)
# 
# std600_26 = np.std(Dfinal[0:3])
# std700_26 = np.std(Dfinal[3:6])
# std800_26 = np.std(Dfinal[6:9])
# SE = stat.sem(data)
# =============================================================================


################################## PLOTS ######################################

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

# =============================================================================
# plt.figure(7)
# plt.ylabel('Rows in LIN FE(0 to 191)', fontweight="bold")
# plt.title('Output of BDAQ scans[With row 0]', size = 14, fontweight="bold")
# plt.xlabel('Columns in LIN FE(128 to 264)', fontweight="bold")
# s = plt.imshow(sum[0:192,128:264]==0) 
# bar = plt.colorbar(s,ticks =[1.0,0.0])
# bar.set_label('Noisy pixels', rotation=270, fontweight="bold")
# bar.ax.set_yticklabels(['1.0(noisy/dead pixel)','0.0(good pixel)'])
# plt.show()
# 
# plt.figure(8)
# plt.ylabel('Rows in LIN FE(0 to 191)', fontweight="bold")
# plt.title('Output of BDAQ scans[With row 0]', size = 14, fontweight="bold")
# plt.xlabel('Columns in LIN FE(128 to 264)', fontweight="bold")
# s = plt.imshow(sum[0:192,128:264]==1) 
# bar = plt.colorbar(s,ticks =[1.0,0.0])
# bar.set_label('Stuck pixels', rotation=270, fontweight="bold")
# bar.ax.set_yticklabels(['1.0(stuck pixel)','0.0(good pixel)'])
# plt.show()
# 
# plt.figure(9)
# plt.ylabel('Rows in LIN FE(0 to 191)', fontweight="bold")
# plt.title('Output of BDAQ scans[With row 0]', size = 14, fontweight="bold")
# plt.xlabel('Columns in LIN FE(128 to 264)', fontweight="bold")
# s = plt.imshow(sum[0:192,128:264]==2) 
# bar = plt.colorbar(s,ticks =[1.0,0.0])
# bar.set_label('Noisy pixels', rotation=270, fontweight="bold")
# bar.ax.set_yticklabels(['1.0(same masked pixel)','0.0(good pixel)'])
# plt.show()
# =============================================================================

# =============================================================================
# plt.figure(7)
# plt.ylabel('Rows in LIN FE(1 to 191)', fontweight="bold")
# plt.title('Output of BDAQ scans', size = 14, fontweight="bold")
# plt.xlabel('Columns in LIN FE(128 to 264)', fontweight="bold")
# s = plt.imshow(sum[1:192,128:264]) 
# bar = plt.colorbar(s, ticks =[3.0,2.0,1.0,0.0])
# bar.set_label('Noisy pixels', rotation=270, fontweight="bold")
# bar.ax.set_yticklabels(['3.0(same masked pixel)','2.0(stuck pixel)','1.0(noisy/dead pixel)','0.0(good pixel)'])
# plt.show()
# 
# =============================================================================

# Noisy pixels Vs Voltage at constant Temperature:
plt.figure(10)
plt.ylabel('Noisy Pixels[%]', fontweight="bold")
plt.title('Noisy pixels vs Voltage @ T_bridge = -20℃ and I_b = 360uA(595, bitten, $0.862$e16 $n_{eq} . cm^{-2}$, Annealing 80.5days)', fontweight="bold")
plt.xlabel('Voltage(V)', fontweight="bold")
plt.axis([None, None, 0, 3])
plt.yticks(np.arange(0,3.5,0.5))
plt.rcParams["figure.figsize"] = [7.50,3.50]
plt.rcParams["figure.autolayout"] = True
plt.grid(color = 'black', linestyle = '--', linewidth = 0.5)
plt.axhline(y = 1, xmin=0, xmax=1, color='k', linestyle='--', linewidth=2)
plt.annotate('[261 pixels]',ha = 'center', va = 'bottom', xytext = (0.2, 1.1),xy = (0.2, 1),arrowprops = {'facecolor' : 'black'})
error300 = np.std(pn[9:12])/np.sqrt(len(pn[9:12]))

line1 = plt.plot(V[0], pn[9], 'ro', lw=2,  label= 'T = -20℃(noisy)')
line2 = plt.plot(V[0], pn[10], 'ro', lw=1.5)
line3 = plt.plot(V[0], pn[11], 'ro', lw=1.5)

#plt.errorbar(V[0], pn[10], yerr = error300)

errors300 = np.std(ps[9:12])/np.sqrt(len(ps[9:12]))
line01 = plt.plot(V[0], ps[9], 'bv', lw=2, label= 'T = -20℃(stuck)')
line02 = plt.plot(V[0], ps[10], 'bv', lw=1.5)
line03 = plt.plot(V[0], ps[11], 'bv', lw=1.5)
#plt.errorbar(V[0], ps[10], yerr = errors300)


line4 = plt.plot(V[1], pn[12], 'ro', lw=2)
line5 = plt.plot(V[1], pn[13], 'ro', lw=1.5)
line6 = plt.plot(V[1], pn[14], 'ro', lw=1.5)

line04 = plt.plot(V[1], ps[12], 'bv', lw=2)
line05 = plt.plot(V[1], ps[13], 'bv', lw=1.5)
line06 = plt.plot(V[1], ps[14], 'bv', lw=1.5)

line7 = plt.plot(V[2], pn[15], 'ro', lw=2)
line8 = plt.plot(V[2], pn[16], 'ro', lw=1.5)
line9 = plt.plot(V[2], pn[17], 'ro', lw=1.5)

line07 = plt.plot(V[2], ps[15], 'bv', lw=2)
line08 = plt.plot(V[2], ps[16], 'bv', lw=1.5)
line09 = plt.plot(V[2], ps[17], 'bv', lw=1.5)

line10 = plt.plot(V[3], pn[18], 'ro', lw=2)
line11= plt.plot(V[3], pn[19], 'ro', lw=1.5)
line12= plt.plot(V[3], pn[20], 'ro', lw=1.5)

line010 = plt.plot(V[3], ps[18], 'bv', lw=2)
line011= plt.plot(V[3], ps[19], 'bv', lw=1.5)
line012= plt.plot(V[3], ps[20], 'bv', lw=1.5)

line13 = plt.plot(V[4], pn[21], 'ro', lw=2)
line14 = plt.plot(V[4], pn[22], 'ro', lw=1.5)
line15= plt.plot(V[4], pn[23], 'ro', lw=1.5)

line013 = plt.plot(V[4], ps[21], 'bv', lw=2)
line014 = plt.plot(V[4], ps[22], 'bv', lw=1.5)
line015= plt.plot(V[4], ps[23], 'bv', lw=1.5)

line16 = plt.plot(V[5], pn[24], 'ro', lw=2)
line17 = plt.plot(V[5], pn[25], 'ro', lw=1.5)
line18 = plt.plot(V[5], pn[26], 'ro', lw=1.5)

line016 = plt.plot(V[5], ps[24], 'bv', lw=2)
line017 = plt.plot(V[5], ps[25], 'bv', lw=1.5)
line018 = plt.plot(V[5], ps[26], 'bv', lw=1.5)

plt.legend()
plt.show()

# Noisy pixels Vs Voltage at constant Temperature:
plt.figure(11)
plt.ylabel('Noisy Pixels[%]', fontweight="bold")
plt.title('Noisy pixels vs Voltage @ T_bridge = -26℃ and I_b = 360uA(595, bitten, $0.862$e16 $n_{eq} . cm^{-2}$, Annealing 80.5days)', fontweight="bold")
plt.xlabel('Voltage(V)', fontweight="bold")
plt.axis([None, None, 0, 3])
plt.yticks(np.arange(0,3.5,0.5))
plt.rcParams["figure.figsize"] = [7.50,3.50]
plt.rcParams["figure.autolayout"] = True
plt.grid(color = 'black', linestyle = '--', linewidth = 0.5)
plt.axhline(y = 1, xmin=0, xmax=1, color='k', linestyle='--', linewidth=2)
plt.annotate('[261 pixels]',ha = 'center', va = 'bottom', xytext = (0.2, 1.1),xy = (0.2, 1),arrowprops = {'facecolor' : 'black'})
line19 = plt.plot(V[3], pn[0], 'ks', lw=2, label= 'T = -26℃(noisy)')
line20 = plt.plot(V[3], pn[1], 'ks', lw=1.5)
line21 = plt.plot(V[3], pn[2], 'ks', lw=1.5)
#plt.errorbar(V[3], pn[0], yerr = std600_26)

line019 = plt.plot(V[3], ps[0], 'g*', lw=2, label= 'T = -26℃(stuck)')
line020 = plt.plot(V[3], ps[1], 'g*', lw=1.5)
line021 = plt.plot(V[3], ps[2], 'g*', lw=1.5)

line22 = plt.plot(V[4], pn[3], 'ks', lw=2)
line23 = plt.plot(V[4], pn[4], 'ks', lw=1.5)
line24 = plt.plot(V[4], pn[5], 'ks', lw=1.5)

line022 = plt.plot(V[4], ps[3], 'g*', lw=2)
line023 = plt.plot(V[4], ps[4], 'g*', lw=1.5)
line024 = plt.plot(V[4], ps[5], 'g*', lw=1.5)

line25 = plt.plot(V[5], pn[6], 'ks', lw=2)
line26 = plt.plot(V[5], pn[7], 'ks', lw=1.5)
line27 = plt.plot(V[5], pn[8], 'ks', lw=1.5)

line025 = plt.plot(V[5], ps[6], 'g*', lw=2)
line026 = plt.plot(V[5], ps[7], 'g*', lw=1.5)
line027 = plt.plot(V[5], ps[8], 'g*', lw=1.5)

plt.legend()
plt.show()

# Noisy pixels Vs Temperature at constant Voltage:
plt.figure(12)
tp = [-26,-20]
plt.ylabel('Noisy Pixels[%]', fontweight="bold")
plt.title('Noisy pixels vs Temperature[Only Noisy, I_b = 360uA](595, bitten, $0.862$e16 $n_{eq} . cm^{-2}$, Annealing 80.5days)', fontweight="bold")
plt.xlabel('Temperature(℃)', fontweight="bold")
plt.axis([None, None, 0, 2.5])
plt.yticks(np.arange(0,2.5,0.5))
plt.rcParams["figure.figsize"] = [7.50,3.50]
plt.rcParams["figure.autolayout"] = True
plt.annotate('[261 pixels]',ha = 'center', va = 'bottom', xytext = (-25.5, 1.1),xy = (-25.5, 1),arrowprops = {'facecolor' : 'black'})
line1 = plt.plot(tp[0], pv_np600[0], 'r--o', lw=1.5, label= '600 V @ T = -26°C')
line2 = plt.plot(tp[0], pv_np600[1], 'r--o', lw=1.5)
line3 = plt.plot(tp[0], pv_np600[2], 'r--o', lw=1.5)
#plt.errorbar(tp[0], pv_np600[0], yerr = error_n600)

line4 = plt.plot(tp[1], pv_np600[3], 'r--v', lw=1.5, label= '600 V @ T = -20°C')
line5 = plt.plot(tp[1], pv_np600[4], 'r--v', lw=1.5)
line6 = plt.plot(tp[1], pv_np600[5], 'r--v', lw=1.5)

line7 = plt.plot(tp[0], pv_np700[0], 'b--o', lw=1.5, label= '700 V @ T = -26°C')
line8 = plt.plot(tp[0], pv_np700[1], 'b--o', lw=1.5)
line9 = plt.plot(tp[0], pv_np700[2], 'b--o', lw=1.5)

line10 = plt.plot(tp[1], pv_np700[3], 'b--v', lw=1.5, label= '700 V @ T = -20°C')
line11 = plt.plot(tp[1], pv_np700[4], 'b--v')
line12= plt.plot(tp[1], pv_np700[5], 'b--v')

line13 = plt.plot(tp[0], pv_np800[0], 'g--o', lw=1.5, label= '800 V @ T = -26°C')
line14 = plt.plot(tp[0], pv_np800[1], 'g--o', lw=1.5)
line15= plt.plot(tp[0], pv_np800[2], 'g--o', lw=1.5)

line16 = plt.plot(tp[1], pv_np800[3], 'g--v', lw=1.5, label= '800 V @ T = -20°C')
line17 = plt.plot(tp[1], pv_np800[4], 'g--v', lw=1.5)
line18= plt.plot(tp[1], pv_np800[5], 'g--v', lw=1.5)


plt.legend()
plt.grid(color = 'black', linestyle = '--', linewidth = 0.5)
plt.axhline(y=1, xmin=0, xmax=1, color='k', linestyle='--', linewidth=2)
plt.show()

# Noisy pixels Vs Temperature at constant Voltage:
plt.figure(13)
tp = [-26,-20]
plt.ylabel('Noisy Pixels[%]', fontweight="bold")
plt.title('Noisy pixels vs Temperature[Only Stuck, I_b = 360uA](595, bitten, $0.862$e16 $n_{eq} . cm^{-2}$, Annealing 80.5days)', fontweight="bold")
plt.xlabel('Temperature(℃)', fontweight="bold")
plt.axis([None, None, 0, 1.5])
plt.yticks(np.arange(0,1.5,0.5))
plt.rcParams["figure.figsize"] = [7.50,3.50]
plt.rcParams["figure.autolayout"] = True
plt.annotate('[261 pixels]',ha = 'center', va = 'bottom', xytext = (-25.5, 1.1),xy = (-25.5, 1),arrowprops = {'facecolor' : 'black'})

line01 = plt.plot(tp[0], pv_s600[0], 'r--o', lw=1.5, label= '600 V @ T = -26°C')
line02 = plt.plot(tp[0], pv_s600[1], 'r--o', lw=1.5)
line03 = plt.plot(tp[0], pv_s600[2], 'r--o', lw=1.5)

line04 = plt.plot(tp[1], pv_s600[3], 'r--v', lw=1.5, label= '600 V @ T = -20°C')
line05 = plt.plot(tp[1], pv_s600[4], 'r--v', lw=1.5)
line06 = plt.plot(tp[1], pv_s600[5], 'r--v', lw=1.5)

line07 = plt.plot(tp[0], pv_s700[0], 'b--o', lw=1.5, label= '700 V @ T = -26°C')
line08 = plt.plot(tp[0], pv_s700[1], 'b--o', lw=1.5)
line09 = plt.plot(tp[0], pv_s700[2], 'b--o', lw=1.5)

line010 = plt.plot(tp[1], pv_s700[3], 'b--v', lw=1.5, label= '700 V @ T = -20°C')
line011 = plt.plot(tp[1], pv_s700[4], 'b--v')
line012= plt.plot(tp[1], pv_s700[5], 'b--v')

line013 = plt.plot(tp[0], pv_s800[0], 'g--o', lw=1.5, label= '800 V @ T = -26°C')
line014 = plt.plot(tp[0], pv_s800[1], 'g--o', lw=1.5)
line015= plt.plot(tp[0], pv_s800[2], 'g--o', lw=1.5)

line016 = plt.plot(tp[1], pv_s800[3], 'g--v', lw=1.5, label= '800 V @ T = -20°C')
line017 = plt.plot(tp[1], pv_s800[4], 'g--v', lw=1.5)
line018= plt.plot(tp[1], pv_s800[5], 'g--v', lw=1.5)

plt.legend()
plt.grid(color = 'black', linestyle = '--', linewidth = 0.5)
plt.axhline(y=1, xmin=0, xmax=1, color='k', linestyle='--', linewidth=2)
plt.show()
