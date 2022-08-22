import pandas as pd

def compute_cluster_rate_WP(path, file):
    
    # List to pass the gamma cluster size for each csv
    gamma_cs_wp_list = []
        
    for f in file:
        # Read the csv file as a panda dataframe
        df = pd.read_csv(path + f)       
            
        # Takes the gamma cluster size    
        gamma_cs = df['gamma_CLS_WP_muon'][0]
        # Takes the hit rate
        gamma_hit_rate = df['noiseGammaRate_WP_muon'][0]
        # Compute the cluster rate
        cluster_rate = gamma_hit_rate / gamma_cs
        wp_muon_corr = df['WP_muon_corr'][0]/1000
        
        #gamma_cs_wp_list.append(f'{round(float(cluster_rate), 2)} $Hz/cm^2$, {wp_muon_corr} V')
        gamma_cs_wp_list.append(f'CLR: {float(cluster_rate):.2f} $Hz/cm^2$ | WP: {wp_muon_corr:.2f} kV')
                
    return gamma_cs_wp_list
