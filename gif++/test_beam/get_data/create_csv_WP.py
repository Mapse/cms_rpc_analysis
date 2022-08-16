import json, os, re, pprint
import pandas as pd
import getpass

import config

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)    

def output_csv(run_number, chamber):
    hvscan_path = config.hvscan_path
    file_path = hvscan_path + '/' + run_number + '/ANALYSIS/' + chamber
    #file_path = f"{chamber}"
    user = getpass.getuser()
    save_path = f'/var/webdcs/ANALYSIS/{user}' + config.path_chamb
    
    with open(file_path + '/output.json') as json_file:
        output = json.load(json_file)
        columns = [i for i in output if i.find('WP') > -1]
        data = []
        data.append([output[column] for column in columns])
        df = pd.DataFrame(data, columns=columns)
        print(df.keys())
        df.to_csv(f'{save_path}/data_{chamber}_{run_number}_WP.csv', index=False)

if __name__ == "__main__":

    runs = config.runs
    chamber = config.chamber
    for i in runs:
    
        output_csv(i, chamber)
