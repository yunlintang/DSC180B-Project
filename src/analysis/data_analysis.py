import pandas as pd
import numpy as np
import json
import datetime
import matplotlib.pyplot as plt
from collections import Counter

def get_date_list(start_date, end_date_exclusive):
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date_exclusive, "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    all_dates = [date_obj.strftime('%Y-%m-%d') for date_obj in date_generated]
    return all_dates
