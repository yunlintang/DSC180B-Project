import sys
import os
import json
import subprocess

sys.path.insert(0, 'src')

from analysis.data_analysis import *
from data.clean_text import *
from data.extract_to_csv import *



def main(targets):

    if 'data' in targets:
        with open('config/data-params.json') as fh:
            data_param = json.load(fh)

        all_dates = get_date_list(data_param["start_date"],data_param["end_date"])
        for i in all_dates:
            subprocess.call([data_param["script_type"], data_param["script_path"], i])
        convert_all_json(data_param['data_path'], data_param['data_path'])
        clean_all_csv(data_param['data_path'], data_param['out_path'])

    if 'test' in targets:
        with open('config/data-params.json') as fh:
            data_param = json.load(fh)


    if 'eda' in targets:
        with open('config/EDA-params.json') as fh:
            eda_param = json.load(fh)


    if 'analysis' in targets:
        with open('config/analysis-params.json') as fh:
            ana_param = json.load(fh)


    if 'all' in targets:
        main('data')
        main('eda')
        main('analysis')


    return

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
