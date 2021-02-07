import pandas as pd
import numpy as np

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
import datetime



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

def cal_daily_vader_score(file_path,date_list,out_path):
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
    df = pd.DataFrame({'date': date_list, 'score':score_list})
    df.to_csv(out_path+"sentiment_scores.csv", index=False)
    print("result is saved at:", out_path+"sentiment_scores.csv")
    return score_list