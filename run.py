import sys
import os
import json
import subprocess
from Analysis.Analysis_script import *

sys.path.insert(0, 'src')


def main(targets):



    if 'data' in targets:
        with open('config/data-params.json') as fh:
            data_param = json.load(fh)

        all_dates = get_date_list(data_param["start_date"],data_param["end_date"])
        for i in all_dates:
            subprocess.call([data_param["script_type"], data_param["script_path"], i])

    if 'test' in targets:
        with open('config/data-params.json') as fh:
            data_param = json.load(fh)

        subprocess.call(["sh", "src/test/test_collection_script/inject_data.sh"])
        main('eda')

        pdf = pd.DataFrame(data_param["test_pdf"])
        output = []
        for i in data_param["test_API_hash"]:
            output.append(calc_user_polarity(i,data_param["test_total_tweet"],pdf))
        print('The polarity of the user is')
        print(output)

        plot_hist(output, 'test_his')
        print()
        print('Histogram is saved to data/temp')

    if 'eda' in targets:
        with open('config/EDA-params.json') as fh:
            eda_param = json.load(fh)


        # display_top(cumulative_hashtags(eda_param["data_path"],eda_param["start_date"],eda_param["end_date"]),eda_param["default_tpu_cutoff"], eda_param["save_graph"])
        #
        # tags_plot(eda_param["science_list"],eda_param["data_path"],eda_param["start_date"],eda_param["end_date"], eda_param["save_graph"], eda_param["science_tag"])

        num_tweets = get_total_tweets(eda_param["data_path"],eda_param["start_date"],eda_param["end_date"])
        print()
        print('Total number of tweets is:')
        print(num_tweets)
        print()


        print('The top 200 Hashtags are:')
        freq_df = cumulative_hashtags(eda_param["data_path"],eda_param["start_date"],eda_param["end_date"])
        freq_df = display_top(freq_df,eda_param["default_tpu_cutoff"], eda_param["save_graph"])
        print()
        print('The Base Occurence Rate is')
        print(calc_base_rate(num_tweets, freq_df, True))
        print()
        restricted_hashtag = get_tweet_with_hashtag(eda_param["data_path"],eda_param["start_date"],eda_param["end_date"], ['FakeNews','TrumpVirus','WuhanVirus'])
        subset_size =  len(restricted_hashtag)
        print("Number of tweets with marker Hashtags is")
        print(subset_size)
        print()
        print('The Marker Occurence is')
        print(calc_marker_rate(subset_size, restricted_hashtag,freq_df, True))

        print()
        calc_polarity('data/temp/base_rate.csv','data/temp/marker_rate.csv',True)

        print('Science diagram Saved to data/temp')
        print()
        tags_plot(eda_param["science_list"],eda_param["data_path"],eda_param["start_date"],eda_param["end_date"], eda_param["save_graph"], eda_param["science_tag"])
        print('Misinformation diagram Saved to data/temp')
        print()

        tags_plot(eda_param["misinformation_list"],eda_param["data_path"],eda_param["start_date"],eda_param["end_date"], eda_param["save_graph"], eda_param["misinformation_tag"])

        plot_tweet_per_user(get_tweet_per_user(eda_param["data_path"],eda_param["start_date"],eda_param["end_date"]), eda_param["default_tpu_cutoff"], eda_param["save_graph"])


    if 'analysis' in targets:
        with open('config/analysis-params.json') as fh:
            ana_param = json.load(fh)



        pol_list = get_userpol_list_from_tweet(ana_param["sci_ID"])
        print(pol_list)
        plot_hist(pol_list, ana_param["sci_name"])


        pol_list_mis = get_userpol_list_from_tweet(ana_param["mis_ID"])
        print(pol_list_mis)
        plot_hist(pol_list_mis, ana_param["mis_name"])




    if 'all' in targets:
        main('data')
        main('eda')
        main('analysis')


    return

if __name__ == '__main__':
    targets = sys.argv[1:]

    main(targets)
