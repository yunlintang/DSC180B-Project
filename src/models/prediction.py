from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):

	n_vars = 1 if type(data) is list else data.shape[1]
	df = pd.DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = pd.concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg


def get_data(score_list,detrended):
    x_data = np.array(score_list).reshape(-1, 1)
    y_data = np.array(detrended).reshape(-1, 1)
    train_data = series_to_supervised(y_data, n_in = 1, n_out = 15)
    total = train_data.assign(sentiment = x_data[:-15])
    total = total.iloc[:170]
    train = total.iloc[:120]
    test= total.iloc[120:170]
    train_x = train.iloc[:,:15]
    train_x = train_x.assign(sentiment = train['sentiment'])
    train_y = train.iloc[:,-2]
    test_x = test.iloc[:,:15]
    test_x = test_x.assign(sentiment = test['sentiment'])
    test_y = test.iloc[:,-2]
    return train_x, train_y, test_x, test_y


def knn_predict(train_x, train_y, test_x, test_y):
    neigh = KNeighborsRegressor(n_neighbors=3)
    neigh.fit(train_x, train_y)
    predicted = neigh.predict(test_x)
    return mean_squared_error(predicted, test_y)**0.5


def detrend_data(daily_cases):
    daily_cases = pd.read_csv(daily_cases)
    daily_cases.date = pd.to_datetime(daily_cases.date)
    daily_cases = daily_cases.set_index('date')
    result_mul = seasonal_decompose(daily_cases['new_cases'], model='multiplicative', extrapolate_trend='freq')
    detrended = daily_cases.new_cases - result_mul.trend
    return detrended


def make_prediction(**kwargs):
	detrended = detrend_data(kwargs['data_path']+kwargs['case_csv'])
	score_list = list(pd.read_csv(kwargs['score_path']+kwargs['score_csv'])['score'])
	train_x, train_y, test_x, test_y = get_data(score_list, detrended)
	print(test_x)
	knn_predict(train_x, train_y, test_x, test_y)

	return