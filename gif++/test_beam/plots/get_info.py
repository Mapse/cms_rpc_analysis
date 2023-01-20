import pandas as pd

#call function example
#path_wp = 'data_wp/'
#file_off =["std_gas/data_RE1_1_B_004795.csv", "ecomix2/data_RE1_1_B_004680.csv", "ecomix3/data_RE1_1_B_004848.csv"]
#legend = ['Std. Gas', 'Ecomix2', 'Ecomix3'] 
#wp2table = wpi.get_WPinfo(path_wp, file_off, legend)

def get_WPinfo(path, file, legend):
    
    # List info from each csv to ECOGAS table
    info = []
    for f, l in zip(file, legend):
        # Read the csv file as a panda dataframe
        df = pd.read_csv(path + f)       
            
        #wp (Volts)  
        wp_muon_corr = df['WP_muon_corr'][0]
        wp_err_muon_corr = df['WP_err_muon_corr'][0]
                
        # Compute current
        current = df['imon_RE1_1_001-BOT_WP_muon_corr'][0] + df['imon_RE1_1_001-TN_WP_muon_corr'][0] + df['imon_RE1_1_001-TW_WP_muon_corr'][0]
        current_notCorr = df['imon_RE1_1_001-BOT_WP_muon'][0] + df['imon_RE1_1_001-TN_WP_muon'][0] + df['imon_RE1_1_001-TW_WP_muon'][0]
        
        gaps = {'BOT': 3150, 'TW': 1840,  'TN': 990}
        
        ktotal1 = df['imon_RE1_1_001-BOT_WP_muon'][0]/gaps['BOT'] + df['imon_RE1_1_001-TN_WP_muon'][0]/gaps['TN'] + df['imon_RE1_1_001-TW_WP_muon'][0]/gaps['TW']
        ktotal2 = (df['imon_RE1_1_001-BOT_WP_muon'][0]/gaps['BOT']) * gaps['BOT'] + (df['imon_RE1_1_001-TN_WP_muon'][0]/gaps['TN'])*gaps['TN'] + (df['imon_RE1_1_001-TW_WP_muon'][0]/gaps['TW'])*gaps['TW']   
        stotal = gaps['BOT'] + gaps['TN'] + gaps['TW']
        ktotal = ktotal1/stotal
        #(current/surface) * surface
        # rate@WP
        rate = df['noiseGammaRate_WP_muon_corr'][0]
        rate_err = df['gamma_CLS_WP_muon_corr'][0]
               
        print(l, ' wp_muon_corr: %.3f' % wp_muon_corr, '+- %.3f' % wp_err_muon_corr, 
              ' current: %.3f' % current,
              ' current not corr: %.3f' % current_notCorr,
              ' rate: %.3f' % rate, ' +- %.3f' % rate_err)
        print('\t', l, ' current: %.3f' % current,
              ' current not corr: %.3f' % current_notCorr,
              ' K1: %.3f' % ktotal1, ' K2 %.3f' % ktotal2, ' Ktotal/stotal %.9f' % ktotal)

        
        
        #print(df)       
        info.append(f'WP: {wp_muon_corr:.3f} +- {wp_err_muon_corr:.3f} V  current: {float(current):.3f} "(uA/cm^2)" rate: {float(rate):.3f} +- {rate_err:.3f} $Hz/cm^2$')
        
    return info

def get_data(path, file, legend):
    
    # List info from each csv to ECOGAS table
    info = []
    eff_list = []
    eff_error_list = []
    voltage_list = []

    for f, l in zip(file, legend):
        # Read the csv file as a panda dataframe
        df = pd.read_csv(path + f)       
            
        #wp (Volts)  
        #wp_muon_corr = df['WP_muon_corr'][0]
        #wp_err_muon_corr = df['WP_err_muon_corr'][0]
                
        # Compute current
        #current = df['imon_RE1_1_001-BOT_WP_muon_corr'][0] + df['imon_RE1_1_001-TN_WP_muon_corr'][0] + df['imon_RE1_1_001-TW_WP_muon_corr'][0]
        # rate@WP
        #rate = df['noiseGammaRate_WP_muon_corr'][0]
        #rate_err = df['gamma_CLS_WP_muon_corr'][0]
               
        #takes the efficiency
        # Insert the desired values on the lists
        #eff_list.append(efficiency)
        #eff_error_list.append(efficiency_error)
        #voltage_list.append(eff_volt/1000)
        
        print(' - ', l, ' - ')
        print('Eff +- error_eff \t current +- error current \t rate +- error rate')
        for i in range(len(df)):
            eff = df.loc[i,'efficiencyMuon_corrected']
            eff_err = df.loc[i,'efficiencyMuon_corrected_err']
            current = df.loc[i,'imon_RE1_1_001-BOT'] + df.loc[i,'imon_RE1_1_001-TN'] + df.loc[i,'imon_RE1_1_001-TW']
            current_err = df.loc[i,'imon_RE1_1_001-BOT'] + df.loc[i,'imon_err_RE1_1_001-TN'] + df.loc[i,'imon_RE1_1_001-TW']
            rate = df.loc[i,'noiseGammaRate']
            rate_err = df.loc[i,'noiseGammaRate_err']
            volt = df.loc[i,'hveff_RE1_1_001-TW']
            #voltage - need only one gap from TW, TN and BOT
            #print(' %.0f' % volt, '\t %.3f' % eff, '+- %.3f' % eff_err, ' \t %.3f' % current, '+- %.3f' % current_err, ' \t %.3f' % rate, '+- %.3f' % rate_err)
            print(' %.0f' % volt, ' %.3f' % eff, ' %.3f' % eff_err, ' %.3f' % current, ' %.3f' % current_err, ' %.3f' % rate, ' %.3f' % rate_err)
        #print(df)       
    
    return info

        #current = df['imon_RE1_1_001-BOT'] + df['imon_RE1_1_001-TN'] + df['imon_RE1_1_001-TW']
        #current_error = df['imon_RE1_1_001-BOT'] + df['imon_err_RE1_1_001-TN'] + df['imon_RE1_1_001-TW']
        #rate = df['noiseGammaRate']
        #rate_error = df['noiseGammaRate_err']
