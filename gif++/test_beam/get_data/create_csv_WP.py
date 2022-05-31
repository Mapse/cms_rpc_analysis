import json, os, re, pprint
import pandas as pd
import getpass

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)    

def output_csv(run_number, chamber):
    hvscan_path = "/var/webdcs/HVSCAN"
    file_path = f"{hvscan_path}/{run_number:06}/ANALYSIS/{chamber}" 
    #file_path = f"{chamber}"
    user = getpass.getuser()
    save_path = f'/var/webdcs/ANALYSIS/{user}/test_beam_october_2021/RE1_1'
    
    with open(file_path + '/output.json') as json_file:
        output = json.load(json_file)
        columns = [i for i in output if i.find('WP') > -1]
        data = []
        data.append([output[column] for column in columns])
        df = pd.DataFrame(data, columns=columns)
        print(df.keys())
        df.to_csv(f'{save_path}/data_{chamber}_{run_number:06}.csv', index=False)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Output csv data')
    parser.add_argument('run_number', metavar='run_number', type=int, nargs=1, help='run number')
    parser.add_argument('chamber', metavar='chamber', type=str, nargs=1, help='chamber name')

    args = parser.parse_args()
    run_number = args.run_number[0]
    chamber = args.chamber[0]
    
    output_csv(run_number, chamber)
