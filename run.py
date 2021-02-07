import sys
import os
import json
import subprocess

sys.path.insert(0, 'src')

import env_setup
from analysis.data_analysis import *
from analysis.daily_sentiment import *
from data.clean_text import *
from data.extract_to_csv import *
from data.case_download import *



def main(targets):

    env_setup.make_datadir()
    test_targets = ['test-data', 'analysis']

    if 'test' in targets:
        targets = test_targets
    
    if 'data' in targets:
        with open('config/data-params.json') as fh:
            data_param = json.load(fh)

        all_dates = get_date_list(data_param["start_date"],data_param["end_date"])
        for i in all_dates:
            subprocess.call([data_param["script_type"], data_param["script_path"], i])
        convert_all_json(data_param['data_path'], data_param['data_path'])
        clean_all_csv(data_param['data_path'], data_param['out_path'])
        total_case(data_param['case_csv'], data_param['out_path'], data_param['start_date'], data_param['end_date'], data_param['url'])


    if 'analysis' in targets:
        with open('config/analysis-params.json') as fh:
            ana_param = json.load(fh)
        date_list = gen_date_list(ana_param['start_date'], ana_param['end_date'])
        cal_daily_vader_score(ana_param['data_path'],date_list, ana_param['out_path'])
        analyze_data(ana_param['data_path'], ana_param['out_path'], ana_param['freq_names'], ana_param['case_name'], ana_param['words_toplot'])


    if 'test-data' in targets:
        with open('config/data-params.json') as fh:
            data_cfg = json.load(fh)
        convert_all_json(data_cfg)


    if 'all' in targets:
        main('data')
        main('eda')
        main('analysis')


    return

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
