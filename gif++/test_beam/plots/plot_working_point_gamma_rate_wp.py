import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import mplhep as hep

plt.style.use(hep.style.CMS)


def linear(x, a, b):
    return (a*x+b)

def working_point_gamma_rate_WP(path, gas_list, fit=False):
    
    # Figure and axis
    fig, ax = plt.subplots()
    
    colors = np.array(['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                       '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                       '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                       '#c7c7c7', '#bcbd22',])
    
    for f, col in zip(gas_list.keys(), colors):
        
        if f == 'std_gas':
            leg = 'Standard gas'
        elif f == 'ecomix2':
            leg = 'Ecomix-2'
        elif f == 'ecomix3':
            leg = 'Ecomix-3'
        # List to pass the working point 
        working_point_list = []
        # List to pass the error of the working point
        working_point_error_list = []
        # List to pass the gamma rate
        gamma_rate_list = []
        for c in gas_list[f]:
            # Read the csv file as a panda dataframe
            df = pd.read_csv(path + f + '/' + c)

            # Takes the gamma cluster size    
            gamma_cs = df['gamma_CLS_WP_muon'][0]
            # Takes the hit rate
            gamma_hit_rate = df['noiseGammaRate_WP_muon'][0]
            # Compute the cluster rate
            cluster_rate = gamma_hit_rate / gamma_cs
            gamma_rate = cluster_rate/df['eff_WP_muon'][0]*100
            
            # Takes the working point      
            working_point = df['WP_muon'][0]
            
            #print(f'Mixture: {f} and WP: {working_point}')
            
            # Append the values
            working_point_list.append(working_point/1000)
            working_point_error_list.append(0)
            gamma_rate_list.append(gamma_rate)
            
        
        # Attributes xaxis and yaxis
        plt.errorbar(gamma_rate_list, working_point_list, yerr=working_point_error_list, marker='D', markersize=10,
                     linestyle='', label=leg, mfc=col, mec=col, ecolor=col)
            
       
        if fit:
            from scipy import optimize
            
            array_rate = np.array(gamma_rate_list)
            array_wp = np.array(working_point_list)
                    
            params, params_covariance = optimize.curve_fit(linear, array_rate, array_wp, p0=[1.2, 10])
            plt.plot(array_rate, linear(array_rate, params[0], params[1]), color=col,
                    label=f'Fit: a={params[0]:.4f} $(kVcm^2/Hz)$, b={params[1]:.2f} kV')
        
        print(working_point_list)
        #print(gamma_rate_list)
        del working_point_list
        del working_point_error_list
        del gamma_rate_list
    
    ax.legend(loc='best', fontsize=20)
        
    # Xlabel
    ax.xaxis.set_label_coords(0.5, -0.055)
    ax.set_xlabel(r'Gamma Rate $(Hz/cm^2)$', fontsize = 22)

    # Ylabel
    ax.yaxis.set_label_coords(-0.11, 0.86)
    ax.set_ylabel(r'Working point (kV)', fontsize = 22)
    #plt.ylim([9600, 12000])

    # CMS format
    hfont = {'fontname':'Helvetica'}        
    plt.text(0.12, 0.89, "Ecogas@GIF++:", fontdict=hfont,  fontweight='bold', fontsize=15, transform=plt.gcf().transFigure) # Value for on top: 0.17, 0.89, inside plot: 0.17, 0.80
    plt.text(0.31, 0.89, "(ALICE, ATLAS, CMS, EPDT, LHCb/SHiP)", fontdict=hfont, style='italic',fontsize = 15, transform=plt.gcf().transFigure) # Value for on top: 0.27, 0.89, inside plot: 0.27, 0.80

    ### If ones would like to move the scientific notation
    #t = ax.yaxis.get_offset_text()
    #t.set_x(0.008)

    plt.grid()

    return ax