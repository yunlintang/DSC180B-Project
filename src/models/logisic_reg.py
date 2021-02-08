import numpy as np
import pandas as pd
import re
import torch
import transformers
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from scipy import sparse


def data_cleaning(csv_file):
    trained = pd.read_csv(csv_file, encoding = "ISO-8859-1", header = None)
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
def tokenize(text):
    tokenizer_class, pretrained_weights = (transformers.BertTokenizer, 'bert-base-uncased')
    tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
    encode_text = tokenizer.encode(text, add_special_tokens = True)
    return encode_text
def tokenization(df):
    tokenized_text = df['text'].apply(tokenize)
    return tokenized_text
def padding(tokenized_text):
    max_length = 0
    for i in range(len(tokenized_text)):
        length = len(tokenized_text[i])
        if length > max_length:
            max_length = length
    for i in range(len(tokenized_text)):
        tokenized_text[i] = tokenized_text[i] + (max_length - len(tokenized_text[i]))*[0]
    lis = [tokenized_text[0]]
    for i in range(1, len(tokenized_text)):
        lis = lis + [tokenized_text[i]]
    trained_matrix = sparse.csr_matrix(lis)
    return trained_matrix
def model_trained(trained_matrix, df):
    labels = df['sentiment']
    X_train, X_test, y_train, y_test = train_test_split(trained_matrix, labels, test_size=0.25, random_state=42)
    model = LogisticRegression(max_iter=500)
    model.fit(X_train, y_train)
    value = model.predict(X_test)
    accuracy = accuracy_score(value, y_test)
    return accuracy


x = data_cleaning("trained.csv")
cleaned = text_cleaning(x)
tokenized_text = tokenization(cleaned)
trained_matrix = padding(tokenized_text)
model_trained(trained_matrix, cleaned)