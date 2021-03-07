from dotenv import load_dotenv, find_dotenv
import os

# get the keys for Kaggle api
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
KAGGLE_KEY = os.environ.get('KAGGLE_KEY')
KAGGLE_USERNAME = os.environ.get('KAGGLE_USERNAME')