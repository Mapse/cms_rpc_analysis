
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import mplhep as hep

plt.style.use(hep.style.CMS)

def plot_current_hv_eff(path ,file, legend, gas=None):
    
    # List to pass the current for each csv
    density_current_list = []
    density_current_err_list = []
    # List to pass the cluster size for each csv
    hv_list = []
        
    for f in file:
        # Read the csv file as a panda dataframe
        df = pd.read_csv(path + f)       
            
        eff_volt = df['hveff_' + 'RE1_1_001-BOT']
        # Takes the current
        ibot = df['imon_RE1_1_001-BOT']
        ibot_err = df['imon_err_RE1_1_001-BOT']/np.sqrt(ibot.size)
        
        itn = df['imon_RE1_1_001-TN']
        itn_err = df['imon_err_RE1_1_001-TN']/np.sqrt(itn.size)
        
        itw = df['imon_RE1_1_001-TW']
        itw_err = df['imon_err_RE1_1_001-TW']/np.sqrt(itw.size)
        
        # Surfaces
        sbot = 3150 # cm^2
        stn = 990 # cm^2
        stw = 1840 # m^2
        
        # Surface currents
        Kbot = ibot/sbot
        Ktn = itn/stn
        Ktw = itw/stw
        # Errors
        Kbot_err = ibot_err/sbot
        Ktn_err = itn_err/stn
        Ktw_err = itw_err/stw
        
        Ktotal = (Kbot * sbot + Ktn * stn + Ktw * stw)/(sbot + stn + stw)
        Ktotal_err = (Kbot_err * sbot + Ktn_err * stn + Ktw_err * stw)/(sbot + stn + stw)
        
        #print(ibot + itn + itw)
        
        #print(eff_volt)
        
        density_current_list.append(Ktotal)
        density_current_err_list.append(Ktotal_err)
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
        plt.errorbar(vo, ef, yerr=er, marker='8', markersize=10, linestyle='', label=leg, mfc=col, mec=col, ecolor=col), #marker='.', linestyle=None, linewidth=0)
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
    plt.text(0.16, 0.55, f"{gas}", fontdict=hfont, style='italic',fontsize = 14, transform=plt.gcf().transFigure) # Value for on top: 0.27, 0.89, inside plot: 0.27, 0.80


    ### If ones would like to move the scientific notation
    #t = ax.yaxis.get_offset_text()
    #t.set_x(0.008)

    plt.grid()

    return ax 
    
