##############################################################################
# Author: M.Antonello 
# Date: 26/11/2020
# Input: 1 interpreted.h5 file of a source scan (1 chip per time!)
# Output: 1 png plot with the occupancy map and the missing bumps number (in the title) + 1 png with the occupancy distribution
# Variables to change: Sensor, Thr, VMAX (only if hot pixels are present) 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
import numpy as np
import tables as tb
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
sys.path.append('./Lib/')
#import Open_Dialog as OD

# Select file
#app = OD.QApplication(sys.argv)
#Open = OD.App()
analyzed_data_file=open.fileName
# Set the nodes of .h5 file and the Thr value
node_name = 'HistOcc'
with tb.open_file(analyzed_data_file, 'r') as infile:
    data1 = infile.get_node('/' + node_name)[:].T
    mask1 = infile.get_node('/masks/disable')[:].T

# ANALYSIS:
Data=np.array(data1[0])

####### TO CHANGE: ##############
Sensor='3073_10_12 -- Chip: 0x2179'
Thr=10
VMAX=2500 #np.max(Data)
#################################

# Enabled pixels mask
Mask_before=np.zeros((192,400))
Enabled=np.where(mask1)
Disabled=(400*192)-Enabled[0].size
print('# of pixels masked before: %i' % Disabled)
Mask_before[Enabled[0],Enabled[1]]=1

# Matrix from Occupancy map
Mask=np.ones((192,400))+1
Cut=np.where(Data<Thr)
print('# of pixels < Thr: %i' % Cut[0].size)
Mask[Cut[0],Cut[1]]=0

# Find the missing bumps
Neglet_mat=Mask+Mask_before
Missing=np.where(Neglet_mat==1)
Missing_mat=np.zeros((192,400))
print('# of MISSING: %i' % Missing[0].size)
Missing_mat[Missing[0],Missing[1]]=1
Perc=float("{:.4f}".format(Missing[0].size/(400*192-Disabled)*100))

#Plot
fig , (ax1, ax2) = plt.subplots(1,2, figsize=(20, 6))
plt.rcParams.update({'font.size': 16})
fig.suptitle("Sensor "+Sensor+" -- Missing bumps: "+str(Missing[0].size)+" ("+str(Perc)+"%) -- Masked pixels: "+str(400*192-Enabled[0].size))
imgplot = ax1.imshow(Data, vmax=VMAX)
ax1.set_title("Occupancy Map (Z Lim: %s hits)" % str(VMAX))
bar1=plt.colorbar(imgplot, orientation='horizontal',ax=ax1, extend='max', label='Hits')
bar1.cmap.set_over('red')
cmap = mpl.colors.ListedColormap(['white', 'red', 'green'])
bounds = [0, 1, 1.9, 3]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
imgplot2 = ax2.imshow(Neglet_mat,cmap=cmap,norm=norm)
ax2.set_title("Missing Map (Cut: < %s hits)" % str(Thr))
bar2=plt.colorbar(imgplot2, ticks=bounds, orientation='horizontal', label='Masked                  Missing                     Good',  spacing='proportional')
bar2.set_ticks([])
fig.savefig(analyzed_data_file[0:-3]+'_Missing_Bumps_Thr_'+str(Thr)+'.png', format='png', dpi=300)

#Histogram
Data_F=Data[Enabled[0],Enabled[1]].flatten()
fig3 = plt.figure()
plt.rcParams.update({'font.size': 16})
ax = fig3.add_subplot(111)
ax.grid(b=False, which='major', color='#999999', linestyle='-', alpha=0.7)
ax.minorticks_on()
ax.grid(b=True, which='minor', color='#999999', linestyle=':', alpha=0.6)
h=plt.hist(Data_F,bins = range(0,VMAX))
ax.set_xlabel('Number of total Hits/pixel')
ax.set_ylabel('Entries')
fig3.savefig(analyzed_data_file[0:-3]+'_Hist_Thr_'+str(Thr)+'.png', format='png', dpi=300)
