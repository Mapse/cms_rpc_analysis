
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from uncertainties import ufloat
from uncertainties.umath import *

import mplhep as hep

plt.style.use(hep.style.CMS)

def plot_cluster_rate_hv_eff(path ,file, legend, chamber, gaps, plot, typ=None):
    
    # List to pass the cluster charge
    cluster_rate_list = []
    cluster_rate_error_list = []
    # List to pass the hv effective
    hv_list = []
        
    for f in file:
        # Read the csv file as a panda dataframe
        df = pd.read_csv(path + f)
        
        ### To TEST ####
        """imon_total = 0
        for i in gap.keys():
            imon_total = imon_total + df['imon_' + i ]"""
        
        # Takes the hit rate and hit hat error.     
        hit_rate_val = df['noiseGammaRate'] 
        hit_rate_err = df['noiseGammaRate_err']/np.sqrt(hit_rate_val.size)
        
        # Takes the gamma cluster size and gamma cluster size error
        gamma_cluster_size_val = df['gammaCLS'] 
        gamma_cluster_size_err = df['gammaCLS_err']/np.sqrt(gamma_cluster_size_val.size)

        # Calculates the cluster rate
        cluster_rate_val = hit_rate_val/gamma_cluster_size_val
        cluster_rate_err = cluster_rate_val * np.sqrt((hit_rate_err/hit_rate_val)**2 + (gamma_cluster_size_err/gamma_cluster_size_val)**2)
        
        # Takes the eff voltage
        try:
            eff_volt = df['hveff_' + chamber + '-' + list(gaps.keys())[0]]
        except:
            eff_volt = df['hveff_' + chamber + '-' + list(gaps.keys())[1]]
        
        # Insert the desired values on the lists
        cluster_rate_list.append(cluster_rate_val)
        cluster_rate_error_list.append(cluster_rate_err)
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
    for (ef, er, vo, leg, col, ma) in zip(cluster_rate_list, cluster_rate_error_list, hv_list, legend, colors, markers):
        
        if typ == None:
            plt.errorbar(vo, ef, yerr=er, marker='8', markersize=10, linestyle='', label=leg, mfc=col, mec=col, ecolor=col), #marker='.', linestyle=None, linewidth=0)
        elif typ == 'comp':
            plt.errorbar(vo, ef, yerr=er, marker=ma, markersize=10, linestyle='', label=leg, mfc=col, mec=col, ecolor=col), #marker='.', linestyle=None, linewidth=0)
        ax.legend(loc='best', fontsize='17')

    # Xlabel
    ax.xaxis.set_label_coords(0.5, -0.055)
    ax.set_xlabel(r'$HV_{eff} (kV)$', fontsize = 22)

    # Ylabel
    ax.yaxis.set_label_coords(-0.09, 0.86)
    ax.set_ylabel(r'Cluster rate $(Hz/cm^2)$', fontsize = 22)
    #plt.legend('labels')

    # CMS format
    if plot == 'rpc':
        hfont = {'fontname':'Helvetica'}
        plt.text(0.13, 0.89, "CMS MUON", fontdict=hfont,  fontweight='bold', transform=plt.gcf().transFigure) # Value for on top: 0.17, 0.89, inside plot: 0.17, 0.80
        plt.text(0.37, 0.89, "Preliminary", fontdict=hfont, style='italic',fontsize = 23, transform=plt.gcf().transFigure) # Value for on top: 0.27, 0.89, inside plot: 0.27, 0.80
        plt.text(0.77, 0.89, "GIF++", fontdict=hfont,  fontweight='bold', transform=plt.gcf().transFigure) # Value for on top: 0.17, 0.89, inside plot: 0.17, 0.80
    elif plot == 'ecogas':
        hfont = {'fontname':'Helvetica'}    
        plt.text(0.13, 0.89, "Ecogas@GIF++:", fontdict=hfont,  fontweight='bold', fontsize=15, transform=plt.gcf().transFigure) # Value for on top: 0.17, 0.89, inside plot: 0.17, 0.80
        plt.text(0.32, 0.89, "(ALICE, ATLAS, CMS, EPDT, LHCb/SHiP)", fontdict=hfont, style='italic',fontsize = 15, transform=plt.gcf().transFigure) # Value for on top: 0.27, 0.89, inside plot: 0.27, 0.80


    ### If ones would like to move the scientific notation
    #t = ax.yaxis.get_offset_text()
    #t.set_x(0.008)

    plt.grid()
    
    return ax
