import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import mplhep as hep

plt.style.use(hep.style.CMS)

def efficiency_gamma_rate_WP(path, gas_list):
    
    # Figure and axis
    fig, ax = plt.subplots()
    for f in gas_list.keys():
        if f == 'std_gas':
            leg = 'Standard gas'
        elif f == 'ecomix2':
            leg = 'Ecomix-2'
        elif f == 'ecomix3':
            leg = 'Ecomix-3'
        
        # List to pass the efficiency for each csv
        eff_list = []
        # List to pass the efficiency error for each csv
        eff_error_list = []
        gamma_rate_list = []
        for c in gas_list[f]:
            # Read the csv file as a panda dataframe
            df = pd.read_csv(path + f + '/' + c)

            # Takes the gamma cluster size    
            gamma_cs = df['gamma_CLS_WP_muon_corr'][0]
            # Takes the hit rate
            gamma_hit_rate = df['noiseGammaRate_WP_muon_corr'][0]
            # Compute the cluster rate
            cluster_rate = gamma_hit_rate / gamma_cs
            gamma_rate = cluster_rate / df['eff_WP_muon_corr'][0] * 100

            # Takes the efficiency     
            efficiency = df['eff_WP_muon'][0]
            #efficiency_error = df['efficiencyMuon_err']
            # Insert the desired values on the lists
            eff_list.append(efficiency)
            eff_error_list.append(0)
            gamma_rate_list.append(gamma_rate)
        
        # Attributes xaxis and yaxis
        plt.errorbar(gamma_rate_list, eff_list, yerr=eff_error_list, marker='D', markersize='10',
                     linestyle='', label=leg)
        ax.legend(loc='best', fontsize=20)
        
        del eff_list
        del eff_error_list
        del gamma_rate_list
        
    # Xlabel
    ax.xaxis.set_label_coords(0.5, -0.055)
    ax.set_xlabel(r'Gamma Rate $(Hz/cm^2)$', fontsize = 22)

    # Ylabel
    ax.yaxis.set_label_coords(-0.09, 0.86)
    ax.set_ylabel(r'Efficiency (%)', fontsize = 22)
    plt.ylim([80, 100])

    # CMS format
    hfont = {'fontname':'Helvetica'}    
    plt.text(0.13, 0.89, "Ecogas@GIF++:", fontdict=hfont,  fontweight='bold', fontsize=15, transform=plt.gcf().transFigure) # Value for on top: 0.17, 0.89, inside plot: 0.17, 0.80
    plt.text(0.32, 0.89, "(ALICE, ATLAS, CMS, EPDT, LHCb/SHiP)", fontdict=hfont, style='italic',fontsize = 15, transform=plt.gcf().transFigure) # Value for on top: 0.27, 0.89, inside plot: 0.27, 0.80

    ### If one would like to move the scientific notation
    #t = ax.yaxis.get_offset_text()
    #t.set_x(0.008)

    plt.grid()
    #plt.savefig("Efficiency_VS_Gamma_Rate_WP.png")