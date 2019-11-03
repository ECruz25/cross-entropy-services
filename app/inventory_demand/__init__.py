import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

from keras import optimizers
from keras.utils import plot_model
from keras.models import Sequential, Model
from keras.layers.convolutional import Conv1D, MaxPooling1D
from keras.layers import Dense, LSTM, RepeatVector, TimeDistributed, Flatten

from numpy.random import seed
seed(1)

def train(training_data):
    lag_size = 90 # 3 months
    train_gp = training_data.sort_values('date').groupby(['item', 'store', 'date'], as_index=False)
    train_gp = train_gp.agg({'sales':['mean']})
    train_gp.columns = ['item', 'store', 'date', 'sales']
    window = 365 ## cuantos dias tengo en mi informacion, cambiarlo a adaptarse a cuanta informacion tenga el cliente
    lag = lag_size
    series = series_to_supervised(train_gp.drop('date', axis=1), window=window, lag=lag)
    last_item = 'item(t-%d)' % window
    last_store = 'store(t-%d)' % window
    series = series[(series['store(t)'] == series[last_store])]
    series = series[(series['item(t)'] == series[last_item])]
    columns_to_drop = [('%s(t+%d)' % (col, lag)) for col in ['item', 'store']]
    for i in range(window, 0, -1):
        columns_to_drop += [('%s(t-%d)' % (col, i)) for col in ['item', 'store']]
    series.drop(columns_to_drop, axis=1, inplace=True)
    series.drop(['item(t)', 'store(t)'], axis=1, inplace=True)
    labels_col = 'sales(t+%d)' % lag_size
    labels = series[labels_col]
    series = series.drop(labels_col, axis=1)

    X_train, X_valid, Y_train, Y_valid = train_test_split(series, labels.values, test_size=0.4, random_state=0)
    epochs = 40
    batch = 256
    lr = 0.0003
    adam = optimizers.Adam(lr)

    X_train_series = X_train.values.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_valid_series = X_valid.values.reshape((X_valid.shape[0], X_valid.shape[1], 1))

    model_cnn = Sequential()
    model_cnn.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(X_train_series.shape[1], X_train_series.shape[2])))
    model_cnn.add(MaxPooling1D(pool_size=2))
    model_cnn.add(Flatten())
    model_cnn.add(Dense(50, activation='relu'))
    model_cnn.add(Dense(1))
    model_cnn.compile(loss='mse', optimizer=adam)
    model_cnn.summary()

    cnn_history = model_cnn.fit(X_train_series, Y_train, validation_data=(X_valid_series, Y_valid), epochs=epochs, verbose=2)
    return "success"

def series_to_supervised(data, window=1, lag=1, dropnan=True):
    cols, names = list(), list()
    for i in range(window, 0, -1):
        cols.append(data.shift(i))
        names += [('%s(t-%d)' % (col, i)) for col in data.columns]
    cols.append(data)
    names += [('%s(t)' % (col)) for col in data.columns]
    cols.append(data.shift(-lag))
    names += [('%s(t+%d)' % (col, lag)) for col in data.columns]
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    if dropnan:
        agg.dropna(inplace=True)
    return agg