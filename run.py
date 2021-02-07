import sys
import os
import json
import subprocess

# sys.path.insert(0, 'src/analysis')

from src.data import clean_text
from src.data import extract_to_csv 
from src.data import case_download 


from src.analysis import data_analysis
from src.analysis import daily_sentiment
from src.analysis import time_series

modulename = 'pandas'
if modulename not in sys.modules:
    print ('You have not imported the {} module'.format(modulename))

def main(targets):
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
        date_list = daily_sentiment.gen_date_list("2020-03-22", "2020-12-01")
        daily_compound = daily_sentiment.cal_daily_vader_score(ana_param['csv_path'],date_list)
    
    if 'timeseries' in targets:
        data_loc = 'data/cases/new_cases.csv'
        # time_series.plot_daily_cases(data_loc)




    if 'test' in targets:
        with open('config/data-params.json') as fh:
            data_param = json.load(fh)


    if 'all' in targets:
        main('data')
        main('eda')
        main('analysis')


    return

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
