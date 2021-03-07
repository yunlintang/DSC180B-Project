import numpy as np
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score



def data_cleaning(csv_file):
    trained = pd.read_csv('x.csv', encoding = "ISO-8859-1").drop('Unnamed: 0', axis = 1)
    trained.columns = ['sentiment', 'id', 'date', 'flag', 'user', 'text']
    trained = trained[['text', 'sentiment']]
    trained['sentiment'] = trained['sentiment'].replace(0, -1).replace(4, 1).replace(2, 0)
    trained['text'] = trained['text'].str.lower()
    labels = trained['sentiment']
    return trained
def remove_hashtags(text):
    text = re.sub(r"^#\S+|\s#\S+", '', text)
    return text
def remove_urls(text):
    text = re.sub(r'http\S+', '', text)
    return text
def remove_ats(text):
    text = re.sub(r"^@\S+|\s@\S+", '', text)
    return text
def text_cleaning(df):
    df['text'] = df['text'].apply(remove_hashtags)
    df['text'] = df['text'].apply(remove_urls)
    df['text'] = df['text'].apply(remove_ats)
    return df

def SVC_model(cleaned):
    X_train, X_vali, y_train, y_vali = train_test_split(cleaned['text'], cleaned['sentiment'], test_size = 0.25, random_state=0)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(X_train)
    dictionary = vectorizer.get_feature_names()
    X_validation = vectorizer.transform(X_vali)
    X_train_bag_of_words_rep = X.toarray()
    X_vali_bag_of_words_rep = X_validation.toarray()
    clf = SVC(C = 0.1, kernel = 'linear', gamma = "auto")
    clf.fit(X,y_train)
    result = clf.predict(X_validation)
    accuracy = accuracy_score(result, y_vali)
    return accuracy, result