
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import mplhep as hep

plt.style.use(hep.style.CMS)

def plot_cluster_charge_hv_eff(path ,file, legend, gaps, gas=None):
    
    # List to pass the cluster charge
    cluster_charge_list = []
    cluster_charge_error_list = []
    # List to pass the hv effective
    hv_list = []
        
    for f in file:
        # Read the csv file as a panda dataframe
        df = pd.read_csv(path + f)
        
        ### To TEST ####
        """imon_total = 0
        for i in gap.keys():
            imon_total = imon_total + df['imon_' + i ]"""
        
        # Takes the hit rate for each gap     
        hit_rate = df['noiseGammaRate']
        # Takes the hit rate error
        hit_rate_error = df['noiseGammaRate_err']
        # Takes the gamma cluster size
        gamma_cluster_size = df['gammaCLS']
        # Takes the gamma cluster size error
        gamma_cluster_size_error = df['gammaCLS_err']
        
        # Takes the eff voltage
        eff_volt = df['hveff_' + list(gaps.keys())[0]]
        
        # Calculates the cluster rate
        cluster_rate = hit_rate/gamma_cluster_size
        # Calculates the cluster charge
        
        # Calculates the chluster charge
        cluster_charge = 0
        for i in gaps:
            cluster_charge = cluster_charge + df['imon_' + i]/cluster_rate/gaps[i]
            
        #### To TEST ####
        #cluster_charge = imon_total/cluster_rate/7000
       
        # Insert the desired values on the lists
        cluster_charge_list.append(cluster_charge*1e6)
        cluster_charge_error_list.append(0)
        hv_list.append(eff_volt/1000)
        
    # Figure and axis
    fig, ax = plt.subplots()
    # Attributes xaxis and yaxis
    
    colors = np.array(['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                       '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                       '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                       '#c7c7c7', '#bcbd22',])
    markers = np.array(["1", "8", "s", "p", "*", "+", "X", "d", "P", ">", "x", "D", "H"])
    
    # Loop used for plot the data for each csv file
    for (ef, er, vo, leg, col, ma) in zip(cluster_charge_list, cluster_charge_error_list, hv_list, legend, colors, markers):
        #ax.plot(vo, ef, marker='s', linestyle=None, linewidth=0)
        plt.errorbar(vo, ef, yerr=er, marker='8', markersize=10, linestyle='', label=leg, mfc=col), #marker='.', linestyle=None, linewidth=0)
        ax.legend(loc='best', fontsize='17')

    # Xlabel
    ax.xaxis.set_label_coords(0.5, -0.055)
    ax.set_xlabel(r'$HV_{eff} (kV)$', fontsize = 22)

    # Ylabel
    ax.yaxis.set_label_coords(-0.09, 0.86)
    ax.set_ylabel(r'Cluster charge $(pC)$', fontsize = 22)
    #plt.legend('labels')

    # CMS format
    hfont = {'fontname':'Helvetica'}    
    plt.text(0.13, 0.89, "Ecogas@GIF++:", fontdict=hfont,  fontweight='bold', fontsize=15, transform=plt.gcf().transFigure) # Value for on top: 0.17, 0.89, inside plot: 0.17, 0.80
    plt.text(0.32, 0.89, "(ALICE, ATLAS, CMS, EPDT, LHCb/SHiP)", fontdict=hfont, style='italic',fontsize = 15, transform=plt.gcf().transFigure) # Value for on top: 0.27, 0.89, inside plot: 0.27, 0.80

    # Gas type
    plt.text(0.16, 0.55, f"{gas}", fontdict=hfont, style='italic',fontsize = 14, transform=plt.gcf().transFigure) # Value for on top: 0.27, 0.89, inside plot: 0.27, 0.80

    ### If ones would like to move the scientific notation
    #t = ax.yaxis.get_offset_text()
    #t.set_x(0.008)

    plt.grid()
    
    return ax