import pandas as pd

def compute_cluster_rate_WP(path, file):
    
    # List to pass the gamma cluster size for each csv
    gamma_cs_list = []
        
    for f in file:
        # Read the csv file as a panda dataframe
        df = pd.read_csv(path + f)       
            
        # Takes the gamma cluster size    
        gamma_cs = df['gamma_CLS_WP_muon'][0]
        # Takes the hit rate
        gamma_hit_rate = df['noiseGammaRate_WP_muon'][0]
        # Compute the cluster rate
        cluster_rate = gamma_hit_rate / gamma_cs
        #gamma_cs_list.append(f'Clus. Rat.:{round(2, cluster_rate)}')
        gamma_cs_list.append(f'Clus. Rate: {round(float(cluster_rate), 2)} $Hz/cm^2$')
                
    return gamma_cs_list