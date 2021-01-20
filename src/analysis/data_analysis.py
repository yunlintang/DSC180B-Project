import pandas as pd
import numpy as np
import json
import datetime
import matplotlib.pyplot as plt
from collections import Counter
import matplotlib.dates as mdates
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud

def get_date_list(start_date, end_date_exclusive):
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date_exclusive, "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    all_dates = [date_obj.strftime('%Y-%m-%d') for date_obj in date_generated]
    return all_dates

def draw_wordcloud(freq, topath, tofilename):
    wc = WordCloud(width=1600, height=800, background_color='white').generate_from_frequencies(freq)
    fig = plt.figure(figsize=(20,10))
    plt.imshow(wc)
    plt.axis('off')
    fig.savefig(topath+tofilename)
    return

def compute_freq(df, vectorizer, topath, tofilename):
    vec = vectorizer.set_params(**{'max_features':100})
    doc_vec = vec.fit_transform(df['text'].values.astype('U'))
    df_dtm = pd.DataFrame(doc_vec.toarray(), columns=vec.get_feature_names())
    df_freq = df_dtm.sum().sort_values(ascending=False)
    df_freq.to_csv(topath+tofilename, header=False)
    return

def plot_freq(df, df_case_cnt, word, topath,tofilename):
    # process the counts of word
    df_word = df[df['text'].apply(lambda x: word in x)]
    df_word = df_word.groupby('date').count().reset_index()
    df_word['date'] = pd.to_datetime(df_word['date'])
    df_word_cnt = (df_word['text'] - df_word['text'].min()) / (df_word['text'].max() - df_word['text'].min())

    # plot
    fig, ax = plt.subplots(figsize=(15,8))
    ax.plot(df_word['date'], df_word_cnt, label="'{}' counts per day".format(word))
    ax.plot(df_word['date'], df_case_cnt, label='new cases per day')
    ax.xaxis.set_major_locator(mdates.WeekdayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.legend()
    plt.xlabel('date')
    plt.xticks(rotation=45)
    fig.savefig(topath+tofilename)
    return


def analyze_data(datapath):
    # read data
    df = pd.DataFrame({'date':[], 'text':[]})
    for fn in os.listdir(datapath):
        if 'clean' in fn:
            df_temp = pd.read_csv(datapath+fn,lineterminator='\n')
            text = list(df_temp['clean_text'].to_numpy())
            date = [fn[:10]] * len(text)
            df_temp = pd.DataFrame({'date':date, 'text':text})
            df = df.append(df_temp, ignore_index=True)
    # drop nan
    df = df.dropna(subset=['text'])
    df = df.reset_index(drop=True)
