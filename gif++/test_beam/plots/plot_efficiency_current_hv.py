import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import mplhep as hep
plt.style.use(hep.style.CMS)


""" This function is used to plot the efficiency and current in function of HVeff 

The argument file is a list with csv files for each ABS (rates) with the following columns: 

For each csv file one should include a legend for the rates/abs.

Example - how you call the function:
path_all = 'data_all/'
file_off =["std_gas/data_RE1_1_B_004795.csv", "ecomix2/data_RE1_1_B_004680.csv", "ecomix3/data_RE1_1_B_004848.csv"]
legend = ['Std. Gas', 'Ecomix2', 'Ecomix3'] 
chamber = 'RE1_1_001'
gaps = {'BOT': 3150, 'TW': 1840,  'TN': 990}
src = 'off'
ax = pechv.plot_eff_current_hv(path_all, file_off, legend, chamber, gaps, plot='ecogas', source=src, typ=None, fit=True, p0=[0.96,0.7,10])

"""

def sigmoid(x, a, b, c):
    return a/(1 + np.exp(-b*(x-c)))

def plot_eff_current_hv(path, file, legend, chamber, gaps, plot, source, p0=[96.6, 0.007, 12.0], fit=False, typ=None):
    
    # List to pass the efficiency for each csv
    eff_list = []
    # List to pass the efficiency error for each csv
    eff_error_list = []
    # List to pass the voltage for each csv
    hv_list = []
    # List to pass the desity current for each csv
    density_current_list = []
    density_current_err_list = []
    for f in file:
        # Read the csv file as a panda dataframe
        df = pd.read_csv(path + f)
        # Takes the effective voltage
        try:
            eff_volt = df['hveff_' + chamber + '-' + list(gaps.keys())[0]]
        except:
            eff_volt = df['hveff_' + chamber + '-' + list(gaps.keys())[1]]
        hv_list.append(eff_volt/1000) #voltage in kV   
        #print(hv_list)
    
        # Takes the efficiency     
        efficiency = df['efficiencyMuon_corrected']
        efficiency_error = df['efficiencyMuon_corrected_err']
        # Insert the desired values on the lists
        eff_list.append(efficiency/100) #efficiency 0 - 1
        eff_error_list.append(efficiency_error/100)        

        # Takes the current
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
        
        #print('\t', file, K_total, K_total_err)
        
        if source == 'off':
            K_total = K_total*1000
            K_total_err = K_total_err*1000
            
        elif source == '100':
            K_total = K_total*100
            K_total_err = K_total_err*100

        else: #source == '22' or source == '10' or source == '6.9':
            K_total = K_total*10
            K_total_err = K_total_err*10

        density_current_list.append(K_total) #density_current in mA/m2
        density_current_err_list.append(K_total_err)
        
        #print('\t\t',f,' \n', K_total, K_total_err)
                
    # Figure and axis
    fig, ax = plt.subplots()
    # Add twinx function to use two different y axis
    ax2 = ax.twinx()
    y_max = 1.0
    ax2.set_ylim(0, y_max)

    # Attributes xaxis and yaxis
    
    colors = np.array(['#228b22', '#1f77b4', '#ff7f0e'])
    markers = np.array(["v", "<", "^"])
        
    #print(f'Current: {density_current_list}', f'  -  Efficiency: {eff_list}')

    # Loop used for plot the data for each csv file
    for (ef, er, vo, de, derr, leg, col, ma) in zip(eff_list, eff_error_list, hv_list, density_current_list, density_current_err_list, legend, colors, markers):
        if typ == None:
            ax2.errorbar(x=vo, xerr=None, y=de, yerr=derr, marker=ma, markersize=10, linestyle='', label=leg, mfc='None', mec=col, ecolor=col), #marker='.', linestyle=None, linewidth=0)
            ax.errorbar(x=vo, xerr=None, y=ef, yerr=er, marker=ma, markersize=10, linestyle='', label=leg, mfc=col, mec=col, ecolor=col), #marker='.', linestyle=None, linewidth=0)
        
        if fit:
            from scipy import optimize
           
            params, params_covariance = optimize.curve_fit(sigmoid, vo, ef, p0=p0)
            v_min = vo.iloc[0]
            v_max = vo.iloc[-1]
            c = (v_max + v_min)/2
            x = np.linspace(v_min, v_max, 100)
            plt.plot(x, sigmoid(x, params[0], params[1], params[2]), color=col)
            print('---- source ', source, ' ---- gas mixture ', leg) 
            print('fit -- params 0, 1, 2 = ', params[0], ', ', params[1], ', ', params[2], '\t - sigma = ', np.sqrt(np.diag(params_covariance)))
            #print('fit -- params_covariante matriz = \n', params_covariance)
            erro = np.sqrt(np.diag(params_covariance))
            #print('\t (eff max (%))', params[0]*0.95*100, '+- ', erro[0]*0.95*100, #considering efficiency at WP
            print('\t (eff max (%))', params[0]*100, '+- ', erro[0]*100,
                  '\n\t\t (slope)', params[1], '+- ', erro[1], '\n')
                        

 
    #ax.legend(loc='upper left') 
    #ax.legend(bbox_to_anchor=(-0.1, 1.02), loc="lower left")
    ax.legend()
    
    # Xlabel
    ax.xaxis.set_label_coords(0.1, -0.055)
    ax.set_xlabel(r'$HV_{eff} (kV)$', fontsize = 22)

    # Ylabel
    ax.yaxis.set_label_coords(-0.09, 0.86)
    ax.set_ylabel(r'Efficiency', fontsize = 22)
    ax.set_ylim(0, y_max)

    ax.yaxis.set_label_coords(-0.09, 0.86)
    ax2.set_ylabel(r'Current density $[\mu A/m^2]$', fontsize = 22)
    if source == 'off':
        ax2.set_ylabel(r'Current density $[\mu A/m^2] \times 10^{3}$', fontsize = 22)
    elif source == '100':    
        ax2.set_ylabel(r'Current density $[\mu A/m^2] \times 10^{2}$', fontsize = 22)
    elif source == '22' or source == '10' or source == '6.9':    
        ax2.set_ylabel(r'Current density $[\mu A/m^2] \times 10^{1} $', fontsize = 22)
    ax2.set_ylim(0, y_max)
    
    # CMS format
    if plot == 'rpc':
        hfont = {'fontname':'Helvetica'}
        plt.text(0.13, 0.89, "CMS MUON", fontdict=hfont,  fontweight='bold', transform=plt.gcf().transFigure) # Value for on top: 0.17, 0.89, inside plot: 0.17, 0.80
        plt.text(0.37, 0.89, "Preliminary", fontdict=hfont, style='italic',fontsize = 23, transform=plt.gcf().transFigure) # Value for on top: 0.27, 0.89, inside plot: 0.27, 0.80
        plt.text(0.77, 0.89, "GIF++", fontdict=hfont,  fontweight='bold', transform=plt.gcf().transFigure) # Value for on top: 0.17, 0.89, inside plot: 0.17, 0.80
    elif plot == 'ecogas':
        hfont = {'fontname':'Helvetica'}    
        plt.text(0.13, 0.89, "Ecogas@GIF++:", fontdict=hfont,  fontweight='bold', fontsize=15, transform=plt.gcf().transFigure) # Value for on top: 0.17, 0.89, inside plot: 0.17, 0.80
        plt.text(0.32, 0.89, "(ALICE, ATLAS, CMS, EPDT, LHCb/SHiP) - Source "+source, fontdict=hfont, style='italic',fontsize = 15, transform=plt.gcf().transFigure) # Value for on top: 0.27, 0.89, inside plot: 0.27, 0.80
        
        plt.axhline(y=100, color='black', linestyle='dotted')
    
   

    ### If ones would like to move the scientific notation
    #t = ax.yaxis.get_offset_text()
    #t.set_x(0.008)

    plt.grid()

    return ax
