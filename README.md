# DSC180B-Project

## Table of Contents

- [Introduction](#introduction)
- [Requirement](#requirement)
- [Steps for Building](#building)
- [Data](#data)
- [EDA](#EDA)
- [Model](#model)
- [Contributors](#contributors)

## Introduction
-----------
Covid-19 changed everyone, from the way we interact, to how we work, and our methods of communication, especially through social media. Under this pandemic period, social media becomes a huge and important part of people’s daily lives. It provides mobile users a convenient way to connect to each other around the world and acquire the updated and trending information about the topic of covid-19. Beside these, people can also express their thoughts and feelings toward certain topics by posting on social media. Throughout the studying of this quarter, we noticed that there are numbers of posts in our Twitter dataset that are related to the topic of covid-19 having some strong emotions and sentiments. In the meantime, a previous study has shown that more people are experiencing negative emotions such as anxiety and panic under this pandemic period. Therefore, we are interested in analyzing the posts that are related to the topic of covid-19 on social media and investigating the underlying causes of the negative emotions implied in these posts.


## Requirement
-----------
- python 3
- install the used modules included in the requirements.txt:
```
cd references
pip install -r requirements.txt
```
- In order to rehydrate the twitter data, you need to create a Twitter Developer Api account and get the API(costumer) key, API secret key, Access Token, and Access Token Secret. 
- Save these keys into `.env` file in the project root directory.


## Building
-----------
We are still in progess to build targets; for now, there are four targets that are available to use: 
- data
* run **`python run.py data`** for downloading and making datasets (three in total).
* data will be saved in the paths `data/raw` and `data/inteirm`.
- analysis
* run **`python run.py analysis`** for cleaning and analyzing the collected data
* results (plots and tables) will be saved in the paths `data/analysis`.
* you can directly view the EDA report in `notebooks/analysis.ipynb`.
- model
* run **`python run.py model`** for building different models.
* still in progress.
- test
* run **`python run.py test`** for building steps on our made-up test data.
* this target is equivalent to **`python run.py test-data analysis`**.


## Data

#### Importation of Data
We use data from [thepanacealab](https://github.com/thepanacealab) which gathers COVID-19 twitter data daily. Our data generation script enables us to input a certain date and automatically download the corresponding tweets on that date from the Panacea Lab, unzip the tab-delimited file (tsv), generate a list full of tweets IDs and rehydrate them using twarc, a command line tool and Python library that archives Twitter data.
```
.
├──src
│  ├── data              
│      ├── bashscript  # changing directory, unzipping file, curl and twarc
│      ├── get_IDs.py   # table processing function that extracts the tweetID and output txt
└── ...
```

Navigate to the directory and use the `python run.py data` to run the data collection script.

The script will download all of the tweetsIDs and hydrate them using `twarc`. The data will be saved under the `data/raw` folder with date being the subfolder name. Note that the `data/raw` folder is not being version controlled to avoid data corruption. The script will create the raw folder if it does not already exist.


## EDA

Use the command `python run.py eda` to generate statistics and graphs of the twitter data. The script counts all the hashtags and outputs the top 50 to `.csv` format. It then plots the frequency of 6 hashtags against date by users choice. The script then composes a dictionary with each user's post count and plot a histogram of the distribution of average post per user.

The files will be generated in the `data/temp` folder. The `notebooks/data_EDA.ipynb` displays a report alongside those statistics.

** Requirements for the data collection script
- python3
- numpy
- pandas
- curl
- twarc (user needs to configure twarc before running the script)
- tweepy

## Analysis

We begin our analysis by characterizing the most popular hashtags by their polarity. Our three marker hashtags for conspiracy misinformation, #FakeNews, #TrumpVirus, and #WuhanVirus, all have a benchmark polarity of 242.8. This absolute value measures the extent to which tweets containing these hashtags are spreading unverified content that contain misinformation.
Given the hashtag polarities, we will take our analysis to the next step by studying two popular tweets, one of which spread misinformation and the other one containing scientific content. We plot the user polarity of people who retweeted these two tweets.



## Test
Our test data contains no personal information as all of the details have been replaced. Only one tweet in the test set has a hashtag of COVID19 which ensures it to run efficiently.



```
### Responsibilities

* Jiawei Zheng developed
* Yunlin Tang developed
* Zhou Li developed
```
