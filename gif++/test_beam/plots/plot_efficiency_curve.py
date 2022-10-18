import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



""" This function is used to plot the efficiency in function of HVeff 

The argument file is a list with csv files for each ABS (rates) with the following columns: 

For each csv file one should include a legend for the rates/abs.

How you call the function:

file = ['data_RE1_1_004662.csv']  -> List with the csv files containing the data
legend = [r'$xx Hz/cm^2$']        -> Legend for each csv file
chamber_hv = 'hveff_RE1_1_001-TN' -> Name of the column containing the voltages (inside the csv file). Normally the name is hveff_ + chamber + gap

plot_eff(file, legend)

"""

def sigmoid(x, a, b, c):
    return a/(1 + np.exp(-b*(x-c)))

def plot_eff(path, file, legend, chamber, gaps, plot, gas=None, fit=False, typ=None, p0=[96.6, 0.007, 12.0]):
    
    # List to pass the efficiency for each csv
    eff_list = []
    # List to pass the efficiency error for each csv
    eff_error_list = []
    voltage_list = []
    
    for f in file:
        # Read the csv file as a panda dataframe
        df = pd.read_csv(path + f)
        # Takes the effective voltage
        try:
            eff_volt = df['hveff_' + chamber + '-' + list(gaps.keys())[0]]
        except:
            eff_volt = df['hveff_' + chamber + '-' + list(gaps.keys())[1]]
            
        # Takes the efficiency     
        efficiency = df['efficiencyMuon_corrected']
        efficiency_error = df['efficiencyMuon_corrected_err']
        # Insert the desired values on the lists
        eff_list.append(efficiency)
        eff_error_list.append(efficiency_error)
        voltage_list.append(eff_volt/1000)
        
    # Figure and axis
    fig, ax = plt.subplots()
    # Attributes xaxis and yaxis
    #print(eff_error_list)
    
    colors = np.array(['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                       '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                       '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                       '#c7c7c7', '#bcbd22',])
    markers = np.array(["X", "8", "s", "p", "*", "+", "1", "d", "P", ">", "x", "D", "H"])
    
    # Loop used for plot the data for each csv file
    for (ef, er, vo, leg, col, ma) in zip(eff_list, eff_error_list, voltage_list, legend, colors, markers):
        #ax.plot(vo, ef, marker='s', linestyle=None, linewidth=0)
        if typ == None:
            plt.errorbar(vo, ef, yerr=er, marker='8', markersize=10, linestyle='', label=leg, mfc=col, mec=col, ecolor=col), #marker='.', linestyle=None, linewidth=0)
        elif typ == 'comp':
            plt.errorbar(vo, ef, yerr=er, marker=ma, markersize=10, linestyle='', label=leg, mfc=col, mec=col, ecolor=col), #marker='.', linestyle=None, linewidth=0)
        ax.legend(loc='best', fontsize=14)
        
        if fit:
            from scipy import optimize
        
            params, params_covariance = optimize.curve_fit(sigmoid, vo, ef, p0=p0)
            v_min = vo.iloc[0]
            v_max = vo.iloc[-1]
            x = np.linspace(v_min, v_max, 200)
            plt.plot(x, sigmoid(x, params[0], params[1], params[2]), color=col)

    # Xlabel
    ax.xaxis.set_label_coords(0.5, -0.055)
    ax.set_xlabel(r'$HV_{eff} (kV)$', fontsize = 22)
    #ax.set_xlim(None, 13000)

    # Ylabel
    ax.yaxis.set_label_coords(-0.09, 0.86)
    ax.set_ylabel(r'Efficiency (%)', fontsize = 22)
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
        
        plt.axhline(y=100, color='black', linestyle='dotted')
    
   

    ### If ones would like to move the scientific notation
    #t = ax.yaxis.get_offset_text()
    #t.set_x(0.008)

    plt.grid()

    return ax
