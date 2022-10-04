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

        # Loads jon file with data
        output = json.load(json_file)

        ## To get values at WP
        columns_wp = [i for i in output if i.find('WP') > -1]

        data_wp = []
        data_wp.append([output[column] for column in columns_wp])
        df_wp = pd.DataFrame(data_wp, columns=columns_wp)
        #print(df_wp.keys())
        df_wp.to_csv(f'{save_path}/data_{chamber}_{run_number}_WP.csv', index=False)

        # To get values in all voltages
        HV_points = natural_sort([i for i in output if i.startswith('HV')])
        data_all = []
        for idx, HV_point in enumerate(HV_points):
            if idx == 0:
                '''hveff = [i for i in output[HV_point] if i.startswith('hveff')]
                imons = [i for i in output[HV_point] if (i.startswith('imon') and not i.startswith('$
                eff = [i for i in output[HV_point] if i.startswith('efficiencyMuon')]
                columns = hveff + imons + eff'''
                columns_all = [i for i in output[HV_point]]
            line = [output[HV_point][column] for column in columns_all]
            data_all.append(line)
        df_all = pd.DataFrame(data_all, columns=columns_all)
        df_all.to_csv(f'{save_path}/data_{chamber}_{run_number}.csv', index=False)

if __name__ == "__main__":

    runs = config.runs
    chamber = config.chamber
    for i in runs:

        output_csv(i, chamber)


