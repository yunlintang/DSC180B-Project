import pandas as pd
import numpy as np
from scipy import signal

import matplotlib.pyplot as plt
import seaborn as sns

# data_loc = 'data/cases/new_cases.csv'
# df = pd.read_csv(data_loc)

def plot_daily_cases(file_path):
    df = pd.read_csv(file_path)
    plt.figure(figsize=(16,6))
    cases_plot = sns.lineplot(data = df.new_cases)
    plt.show()
    return cases_plot

# def calc_poly_fir(df, poly_degree):
#     return 
