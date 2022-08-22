import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import mplhep as hep

plt.style.use(hep.style.CMS)

def current_density_cluster_rate_WP(path, gas_list):
    
    surface_bot_gap = 0.315*1e4 #cm²
    surface_top_wide_gap = 0.184*1e4 #cm²
    surface_partiton_b = 0.0837*1e4 #cm²
    
    # Figure and axis
    fig, ax = plt.subplots()
    
    for f in gas_list.keys():
        if f == 'std_gas':
            leg = 'Standard gas'
        elif f == 'ecomix2':
            leg = 'Ecomix-2'
        elif f == 'ecomix3':
            leg = 'Ecomix-3'
        # List to pass the density current 
        density_current_list = []
        # List to pass the error of density current
        density_current_error_list = []
        # List to pass the cluster rate
        cluster_rate_list = []
        for c in gas_list[f]:
            # Read the csv file as a panda dataframe
            df = pd.read_csv(path + f + '/' + c)

            # Takes the gamma cluster size    
            gamma_cs = df['gamma_CLS_WP_muon'][0]
            # Takes the hit rate
            gamma_hit_rate = df['noiseGammaRate_WP_muon'][0]
            # Compute the cluster rate
            cluster_rate = gamma_hit_rate / gamma_cs
            #print(df.columns)
            
            # Takes the current
            ibot = df['imon_RE1_1_001-BOT_WP_muon'][0]
            #ibot_err = df['imon_err_RE1_1_001-BOT_WP_muon']/np.sqrt(ibot.size)

            #itn = df['imon_RE1_1_001-TN_WP_muon'][0]
            #itn_err = df['imon_err_RE1_1_001-TN_WP_muon']/np.sqrt(itn.size)

            itw = df['imon_RE1_1_001-TW_WP_muon'][0]
            #itw_err = df['imon_err_RE1_1_001-TW_WP_muon']/np.sqrt(itw.size)
            
            #current_partiton_b = surface_partiton_b * (ibot/surface_bot_gap + itw/surface_top_wide_gap )
            #current_partiton_b_err = surface_partiton_b * (ibot_err/surface_partiton_b + itw_err/surface_partiton_b )
            Kbot = ibot/surface_bot_gap
            Ktw = itw/surface_top_wide_gap

            # Takes the density current at partition b
            density_current_partition_b = (Kbot * surface_bot_gap + Ktw * surface_top_wide_gap)/(surface_bot_gap + surface_top_wide_gap)
            #density_current_partition_b = current_partiton_b/surface_partiton_b            
            density_current_list.append(density_current_partition_b)
            density_current_error_list.append(0)
            cluster_rate_list.append(cluster_rate)
        
        # Attributes xaxis and yaxis
        plt.errorbar(cluster_rate_list, density_current_list, yerr=density_current_error_list, marker='D', markersize=10,
                     linestyle='', label=leg)
        ax.legend(loc='best', fontsize=20)
        
        del density_current_list
        del density_current_error_list
        del cluster_rate_list

    # Xlabel
    ax.xaxis.set_label_coords(0.5, -0.055)
    ax.set_xlabel(r'Cluster Rate $(Hz/cm^2)$', fontsize = 22)

    # Ylabel
    ax.yaxis.set_label_coords(-0.11, 0.86)
    ax.set_ylabel(r'Current Density $(\mu A/cm^2)$', fontsize = 22)
    #plt.ylim([80, 100])

    # CMS format
    hfont = {'fontname':'Helvetica'}    
    plt.text(0.13, 0.89, "Ecogas@GIF++:", fontdict=hfont,  fontweight='bold', fontsize=15, transform=plt.gcf().transFigure) # Value for on top: 0.17, 0.89, inside plot: 0.17, 0.80
    plt.text(0.32, 0.89, "(ALICE, ATLAS, CMS, EPDT, LHCb/SHiP)", fontdict=hfont, style='italic',fontsize = 15, transform=plt.gcf().transFigure) # Value for on top: 0.27, 0.89, inside plot: 0.27, 0.80

    ### If ones would like to move the scientific notation
    #t = ax.yaxis.get_offset_text()
    #t.set_x(0.008)

    plt.grid()  

    return ax
