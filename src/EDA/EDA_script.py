import pandas as pd
import numpy as np
import json
import datetime
import matplotlib.pyplot as plt
from collections import Counter

def convert_to_json (filepath):
    tweets_json = []
    with open(filepath) as f:
        for jsonObj in f:
            tweetDict = json.loads(jsonObj)
            tweets_json.append(tweetDict)
    return tweets_json

def get_hashtext(ht):
    output = []
    if ht != []:
        for i in ht:
            output.append(i['text'])
    return output

def get_all_hashtag(tweets_json):
    all_hashtags = []
    for i in tweets_json:
        all_hashtags.append(i['entities']['hashtags'])
    return all_hashtags

def get_hashtag_within_list(filepath, hashtag_list):
    tweets_json = convert_to_json(filepath)

    all_hashtags = []
    # print(tweets_json)
    for i in tweets_json:

        for j in hashtag_list:

            if j in get_hashtext(i['entities']['hashtags']):

                all_hashtags.append(get_hashtext(i['entities']['hashtags']))
                break
            else:
                continue
    return all_hashtags


def flatten_hashtag(all_hashtags):
    output = []
    for i in all_hashtags:
        output.append(get_hashtext(i))
    return [item for sublist in output for item in sublist]

def json_to_hashtags(filepath):
    tweets_json = convert_to_json(filepath)
    all_hashtags = get_all_hashtag(tweets_json)
    return flatten_hashtag(all_hashtags)

def get_date_list(start_date, end_date_exclusive):
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date_exclusive, "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    all_dates = [date_obj.strftime('%Y-%m-%d') for date_obj in date_generated]
    return all_dates

def get_total_tweets(json_loc,start_date, end_date_exclusive):
    all_dates = get_date_list(start_date, end_date_exclusive)
    counter = 0
    for i in all_dates:
        counter += len(convert_to_json(json_loc+i+'.json'))
    return counter

def cumulative_hashtags(json_loc,start_date, end_date_exclusive):
    all_dates = get_date_list(start_date, end_date_exclusive)
    output = []
    for i in all_dates:
        output.append(json_to_hashtags(json_loc+i+'.json'))
    output = [item for sublist in output for item in sublist]
    hashtag_dic = Counter(output)
    sorted_hashtag_dic = sorted(hashtag_dic.items(), key=lambda x: x[1], reverse=True)
    df = pd.DataFrame.from_dict(sorted_hashtag_dic).rename(columns={0: "Hashtag", 1: "Frequency"})
    return df


def get_tweet_with_hashtag(json_loc,start_date, end_date_exclusive,hashtag_list):
    all_dates = get_date_list(start_date, end_date_exclusive)
    output = []
    for i in all_dates:
        output.append(get_hashtag_within_list(json_loc+i+'.json', hashtag_list))
    output = [item for sublist in output for item in sublist]
    output = [item for sublist in output for item in sublist]
    hashtag_dic = Counter(output)
    sorted_hashtag_dic = sorted(hashtag_dic.items(), key=lambda x: x[1], reverse=True)
    df = pd.DataFrame.from_dict(sorted_hashtag_dic).rename(columns={0: "Hashtag", 1: "Frequency"})
    return output



def calc_base_rate(total_tweets, freq_df, save_csv):
    freq_df['Frequency'] = freq_df['Frequency']/total_tweets
    freq_df = freq_df.rename(columns={'Frequency':'Base Occurrence'})
    if save_csv:
        freq_df.to_csv("data/temp/base_rate.csv", index = False)
    return freq_df

def calc_marker_rate(total_tweets, restricted_hashtag,freq_df, save_csv):
    count_dic = pd.Series(restricted_hashtag).value_counts()
    output = {}
    for i in freq_df['Hashtag']:
        if i in count_dic:
            output[i] = count_dic[i]
        else:
            output[i] = 0
    marker_df = pd.DataFrame(output.items()).rename(columns={0: "Hashtag", 1: "Marker Occurence"})
    marker_df['Marker Occurence'] = marker_df['Marker Occurence']/total_tweets
    if save_csv:
        marker_df.to_csv("data/temp/marker_rate.csv", index = False)
    return marker_df

def display_top(hashtag_dict, n, save_csv):
    print(hashtag_dict[:n])
    top_df = pd.DataFrame(hashtag_dict[:n]).rename(columns={0: "Hashtag", 1: "Counts"})
    if save_csv:

        top_df.to_csv("data/temp/top_50_hashtags.csv", index = False)
    return top_df





def plot_numht_time(json_loc,start_date, end_date_exclusive, hashtag):
    all_dates = get_date_list(start_date, end_date_exclusive)
    counter = []
    for i in all_dates:
        date_hashtags = json_to_hashtags(json_loc+i+'.json')
        hashtag_dic = Counter(date_hashtags)
        counter.append(hashtag_dic[hashtag])
    return counter

def tags_plot(tag_list,json_loc,start_date, end_date_exclusive, save_to_folder, tag_type):
    fig, axs = plt.subplots(len(tag_list),figsize=(18,12))
    plt.setp(axs, xticks=np.arange(0, 1000, 15))
    all_dates = get_date_list(start_date,end_date_exclusive)
    for i in np.arange(len(tag_list)):

        x = plot_numht_time(json_loc,start_date,end_date_exclusive,tag_list[i])
        axs[i].plot(all_dates, x)
        axs[i].set_ylabel('Frequency')
        axs[i].set_title('#'+tag_list[i]+' Frequency')

    plt.xlabel("Date")
    if save_to_folder:
        fig.savefig('data/temp/'+tag_type+'.png')




def calc_polarity(base_csv, marker_csv, save_csv):
    base_rate = pd.read_csv(base_csv)
    marker_rate = pd.read_csv(marker_csv)
    marker_rate['Marker Occurence'] = (marker_rate['Marker Occurence']-base_rate['Base Occurrence'])/base_rate['Base Occurrence']
    output_df = marker_rate.rename(columns={'Marker Occurence': 'Polarity'})
    if save_csv:
        output_df.to_csv("data/temp/polarity_rate.csv", index = False)
    return output_df



def get_tweet_per_user(json_loc,start_date, end_date_exclusive):
    all_dates = get_date_list(start_date, end_date_exclusive)
    total_Counter = Counter()
    for i in all_dates:
        tweets_json = convert_to_json(json_loc+i+'.json')
        all_userid = []
        for i in tweets_json:
            all_userid.append(i['user']['id'])
        cur_counter = Counter(all_userid)
        total_Counter += cur_counter
    return total_Counter

def plot_tweet_per_user(count_dict, cutoff, save_to_folder):
    no_outlier_x = [i for i in count_dict.values() if i<cutoff]
    plt.figure(figsize=(13,8))
    plt.hist(no_outlier_x, bins = 100)
    plt.xticks(np.arange(1,51))
    plt.title('Distribution of Number of Posts per User')
    if save_to_folder:
        plt.savefig('data/temp/tweet_per_user.png')
