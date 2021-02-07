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
    test_targets = ['test-data','analysis']

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


    if 'test-data' in targets:
        with open('config/data-params.json') as fh:
            data_cfg = json.load(fh)
        clean_all_csv(data_cfg['path_test'], data_cfg['path_test'])


    if 'analysis' in targets:
        with open('config/analysis-params.json') as fh:
            ana_cfg = json.load(fh)
        if "test-data" in targets:
            ana_cfg['test'] = True
        else:
            ana_cfg['test'] = False
        ana_cfg['date_list'] = gen_date_list(**ana_cfg)
        cal_daily_vader_score(**ana_cfg)
        analyze_data(**ana_cfg)


    if 'all' in targets:
        main('data')
        main('eda')
        main('analysis')


    return

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
