import pandas as pd
import numpy as np
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import signal
from statsmodels.tsa.seasonal import seasonal_decompose


def gen_date_list(start_str, end_str):
    """Generate the date list in string format of 
    2020-01-01
    used to read in all the csv documents
    """
    start = datetime.datetime.strptime(start_str, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_str, "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    date_list = []
    for date in date_generated:
        date_list.append(date.strftime("%Y-%m-%d"))
    return date_list

def cal_daily_vader_score(file_path, date_list):
    """Calculate the daily sensiment score in a folder path
    within selected dates
    The function always print the current processing date
    """
    sid = SentimentIntensityAnalyzer()
    pol = sid.polarity_scores
    score_list = []
    for i in date_list:
        print(i)
        test_df = pd.read_csv(file_path + i + '-clean.csv',lineterminator='\n')
        score = test_df['clean_text'].apply(lambda x: pol(str(x))).apply(lambda x:x['compound']).mean()
        score_list.append(score)
    return score_list


def plot_daily_cases(file_path, topath, filename):
    df = pd.read_csv(file_path)
    fig = plt.figure(figsize=(16,6))
    cases_plot = sns.lineplot(data = df.new_cases)
    fig.savefig(topath+filename)
    print("daily case plot is saved at:", topath+filename)
    return cases_plot

def detrend_data(daily_cases):
    daily_cases = pd.read_csv(daily_cases)
    daily_cases.date = pd.to_datetime(daily_cases.date)
    daily_cases = daily_cases.set_index('date')
    result_mul = seasonal_decompose(daily_cases['new_cases'], model='multiplicative', extrapolate_trend='freq')
    detrended = daily_cases.new_cases - result_mul.trend
    return detrended

def plot_detrend_score(score_list, date_list, detrended, topath, filename):
    sns.set_style("darkgrid")
    fig = plt.figure(figsize=(16, 6))
    ax = sns.lineplot(y = score_list, x = date_list, label = 'Sentiment Score')
    ax2 = sns.lineplot(y = detrended/2500000+np.mean(score_list), x = date_list, label = 'Detrended Daily Cases')
    plt.xticks(rotation=30)
    for ind, label in enumerate(ax.get_xticklabels()):
        if ind % 10 == 0: 
            label.set_visible(True)
        else:
            label.set_visible(False)
    ax.legend()
    fig.savefig(topath+filename)
    print("plot of detrended score is saved at:", topath+filename)
    return

def plot_daily_sentiment(**kwargs):
    start_date, end_date = kwargs['start_date'], kwargs['end_date']
    data_path, data_case, out_path, plot_name = kwargs['data_path'], kwargs['case_name'], kwargs['out_path'], kwargs['detrend_name']

    if kwargs['test']:
        start_date, end_date, data_path = kwargs['test_sd'], kwargs['test_ed'], kwargs['test_path']

    plot_daily_cases(data_path+data_case, out_path, kwargs['daily_name'])
    date_list = gen_date_list(start_date, end_date)
    daily_compound = cal_daily_vader_score(data_path, date_list)
    detrended = detrend_data(data_path+data_case)
    plot_detrend_score(daily_compound, date_list, detrended, out_path, plot_name)
    return daily_compound, detrended