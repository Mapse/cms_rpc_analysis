
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import mplhep as hep

plt.style.use(hep.style.CMS)

def plot_current_hv_eff(path ,file, legend, chamber, gaps, gas=None):
    
    # List to pass the current for each csv
    density_current_list = []
    density_current_err_list = []
    # List to pass the cluster size for each csv
    hv_list = []
        
    for f in file:
        # Read the csv file as a panda dataframe
        df = pd.read_csv(path + f)  
        
        try:
            eff_volt = df['hveff_' + chamber + '-' + list(gaps.keys())[0]]
        except:
            eff_volt = df['hveff_' + chamber + '-' + list(gaps.keys())[1]]
            
        K_total = 0
        K_total_err = 0
        S_total = 0
        for i in gaps:

            current = df['imon_' + chamber + '-' + i]
            current_err = df['imon_err_' + chamber + '-' + i]/np.size(current)
            surface = gaps[i]

            #I_chamber.append(current) 
            #I_chamber_err.append(current_err/np.sqrt(current.size))

            #K_chamber.append(current/area)
            #K_chamber_err.append(current_err/area)

            K_total = K_total + (current/surface) * surface
            K_total_err = K_total_err + (current_err/surface) * surface

            S_total = S_total + gaps[i]
       
        K_total = K_total/S_total
        K_total_err = K_total_err/S_total
        
        density_current_list.append(K_total)
        density_current_err_list.append(K_total_err)
        hv_list.append(eff_volt/1000)
             
    # Figure and axis
    fig, ax = plt.subplots()
    # Attributes xaxis and yaxis
    
    colors = np.array(['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                       '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                       '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                       '#c7c7c7', '#bcbd22',])
    markers = np.array(["X", "8", "D", "p", "*", "H", "1", "d", "P", ">", "x", "s", "+"])
    
    # Loop used for plot the data for each csv file
    for (ef, er, vo, leg, col, ma) in zip(density_current_list, density_current_err_list, hv_list, legend, colors, markers):
        #ax.plot(vo, ef, marker='s', linestyle=None, linewidth=0)
        plt.errorbar(vo, ef, yerr=er, marker=ma, markersize=14, linestyle='', label=leg, mfc=col, mec=col, ecolor=col), #marker='.', linestyle=None, linewidth=0)
        ax.legend(loc='best', fontsize=18)

    # Xlabel
    ax.xaxis.set_label_coords(0.5, -0.055)
    ax.set_xlabel(r'$HV_{eff} (kV)$', fontsize = 22)
    
    '''## Remove WP
    ax.xaxis.set_label_coords(0.5, -0.055)
    ax.set_xlabel(r'$HV_{eff}-HV_{w.p.} (V)$', fontsize = 22)'''

    # Ylabel
    ax.yaxis.set_label_coords(-0.10, 0.86)
    ax.set_ylabel(r'Current Density$(\mu A/cm^2)$', fontsize = 22)
    #plt.legend('labels')

    # CMS format
    hfont = {'fontname':'Helvetica'}    
    plt.text(0.13, 0.89, "Ecogas@GIF++:", fontdict=hfont,  fontweight='bold', fontsize=15, transform=plt.gcf().transFigure) # Value for on top: 0.17, 0.89, inside plot: 0.17, 0.80
    plt.text(0.32, 0.89, "(ALICE, ATLAS, CMS, EPDT, LHCb/SHiP)", fontdict=hfont, style='italic',fontsize = 15, transform=plt.gcf().transFigure) # Value for on top: 0.27, 0.89, inside plot: 0.27, 0.80
    
    # Gas type
    #plt.text(0.16, 0.55, f"{gas}", fontdict=hfont, style='italic',fontsize = 14, transform=plt.gcf().transFigure) # Value for on top: 0.27, 0.89, inside plot: 0.27, 0.80


    ### If ones would like to move the scientific notation
    #t = ax.yaxis.get_offset_text()
    #t.set_x(0.008)

    plt.grid()

    return ax 
    
