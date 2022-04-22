import json, os, re, pprint
import pandas as pd
import getpass
import config_csv_rate as cg

# Take the chamber name and Hv scan path from config file.
chamber = cg.chamber 
hvscan_path = cg.hvscan_path 


# Function to sort the HV points in ascending order
def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)   

# Function that reads json file and insert its data on a csv file by using pandas
def output_csv(run_number):
    # Path to the json file. Each scan should have one json file.
    file_path =  f"{hvscan_path}/{run_number:06}/ANALYSIS/{chamber}"
    with open(file_path + '/output.json') as json_file:
        output = json.load(json_file)
        HV_points = natural_sort([i for i in output if i.startswith('HV')])

        data = []
        for idx, HV_point in enumerate(HV_points):
            if idx == 0:
                columns = [i for i in output[HV_point]]
            line = [output[HV_point][column] for column in columns]
            data.append(line)
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(f'data_{chamber}_{run_number:06}.csv', index=False)

if __name__ == "__main__":
    # Take the scan list and produce all csv files of interest,
    run_number_list = cg.run_number_list

    for run_number in run_number_list:
        output_csv(run_number)
