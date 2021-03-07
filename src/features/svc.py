import numpy as np
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score


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
    return accuracy

def build_svc(**kwargs):
    path,cleanpath,filename = kwargs['data_path'],kwargs['cleaned_csv'],kwargs['sentiment_label_data']
    df = pd.read_csv(path+cleanpath)
    acc = SVC_model(df)
    print('accuracy of svc model on the labeled dataset:', acc)
    return