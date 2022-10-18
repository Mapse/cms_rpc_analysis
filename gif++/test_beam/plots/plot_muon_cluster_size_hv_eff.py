
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import mplhep as hep

plt.style.use(hep.style.CMS)

def plot_muon_cluster_size_hv_eff(path ,file, legend, chamber, gaps, plot, typ=None):
    
    # List to pass the muon cluster size for each csv
    muon_cs_list = []
    muon_cs_error_list = []
    # List to pass the cluster size for each csv
    hv_list = []
        
    for f in file:
        # Read the csv file as a panda dataframe
        df = pd.read_csv(path + f)       
            
        # Takes the current for each gap     
        muon_cs = df['muonCLS']
        # Takes the cs error
        muon_cs_error = df['muonCLS_err']/np.sqrt(muon_cs.size)
        
        # Takes the eff voltage
        try:
            eff_volt = df['hveff_' + chamber + '-' + list(gaps.keys())[0]]
        except:
            eff_volt = df['hveff_' + chamber + '-' + list(gaps.keys())[1]]
       
        # Insert the desired values on the lists
        muon_cs_list.append(muon_cs)
        muon_cs_error_list.append(muon_cs_error)
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
    for (ef, er, vo, leg, col, ma) in zip(muon_cs_list, muon_cs_error_list, hv_list, legend, colors, markers):
        #ax.plot(vo, ef, marker='s', linestyle=None, linewidth=0)
        if typ == None:
            plt.errorbar(vo, ef, yerr=er, marker='8', markersize=10, linestyle='', label=leg, mfc=col, mec=col, ecolor=col), #marker='.', linestyle=None, linewidth=0)
        elif typ == 'comp':
            plt.errorbar(vo, ef, yerr=er, marker=ma, markersize=10, linestyle='', label=leg, mfc=col, mec=col, ecolor=col), #marker='.', linestyle=None, linewidth=0)
        ax.legend(loc='best', fontsize=16,)# bbox_to_anchor=(0.2, 0.2),)

    # Xlabel
    ax.xaxis.set_label_coords(0.5, -0.055)
    ax.set_xlabel(r'$HV_{eff} (kV)$', fontsize = 22)

    # Ylabel
    ax.yaxis.set_label_coords(-0.09, 0.86)
    ax.set_ylabel(r'Muon Cluster Size', fontsize = 22)
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

    plt.grid()
    
    return ax
