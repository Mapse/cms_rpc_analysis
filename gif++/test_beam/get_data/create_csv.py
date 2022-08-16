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
    user = getpass.getuser()
    save_path = f'/var/webdcs/ANALYSIS/{user}' + config.path_chamb
    
    with open(file_path + '/output.json') as json_file:
        output = json.load(json_file)
        HV_points = natural_sort([i for i in output if i.startswith('HV')])
        data = []
        for idx, HV_point in enumerate(HV_points):
            if idx == 0:
                '''hveff = [i for i in output[HV_point] if i.startswith('hveff')]
                imons = [i for i in output[HV_point] if (i.startswith('imon') and not i.startswith('imon_err'))]
                eff = [i for i in output[HV_point] if i.startswith('efficiencyMuon')]
                columns = hveff + imons + eff'''
                columns = [i for i in output[HV_point]]
            line = [output[HV_point][column] for column in columns]
            data.append(line)
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(f'{save_path}/data_{chamber}_{run_number}.csv', index=False)

if __name__ == "__main__":

    runs = config.runs
    chamber = config.chamber
    for i in runs:
    
        output_csv(i, chamber)
