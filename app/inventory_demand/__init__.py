import pandas as pd
from keras import optimizers
from keras.layers import Dense, Flatten
from keras.layers.convolutional import Conv1D, MaxPooling1D
from keras.models import Sequential
from numpy.random import seed
from sklearn.model_selection import train_test_split

seed(1)


def transform_data(training_data, months):
    lag_size = 1
    training_data['date'] = pd.to_datetime(training_data['date'])
    train_gp = training_data.sort_values('date').groupby(
        ['item', 'store', 'date'], as_index=False)
    train_gp = train_gp.agg({'sales': ['mean']})
    train_gp.columns = ['item', 'store', 'date', 'sales']
    window = (training_data['date'].max().date() - training_data['date'].min().date()).days
    lag = months * 30
    series = series_to_supervised(train_gp.drop(
        'date', axis=1), window=window, lag=lag)
    last_item = 'item(t-%d)' % window
    last_store = 'store(t-%d)' % window
    series = series[(series['store(t)'] == series[last_store])]
    series = series[(series['item(t)'] == series[last_item])]
    columns_to_drop = [('%s(t+%d)' % (col, lag)) for col in ['item', 'store']]
    for i in range(window, 0, -1):
        columns_to_drop += [('%s(t-%d)' % (col, i))
                            for col in ['item', 'store']]
    series.drop(columns_to_drop, axis=1, inplace=True)
    series.drop(['item(t)', 'store(t)'], axis=1, inplace=True)
    labels_col = 'sales(t+%d)' % lag_size
    labels = series[labels_col]
    series = series.drop(labels_col, axis=1)

    x_train, x_valid, y_train, y_valid = train_test_split(
        series, labels.values, test_size=0.4, random_state=0)

    X_train_series = x_train.values.reshape(
        (x_train.shape[0], x_train.shape[1], 1))
    X_valid_series = x_valid.values.reshape(
        (x_valid.shape[0], x_valid.shape[1], 1))
    return {'X_train_series': X_train_series, 'Y_train': y_train, 'X_valid_series': X_valid_series, 'Y_valid': y_valid}


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


def train_model(x_train_series, x_valid_series, y_train, y_valid):
    epochs = 1
    lr = 0.0003
    adam = optimizers.Adam(lr)
    model_cnn = Sequential()
    model_cnn.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(
        x_train_series.shape[1], x_train_series.shape[2])))
    model_cnn.add(MaxPooling1D(pool_size=2))
    model_cnn.add(Flatten())
    model_cnn.add(Dense(50, activation='relu'))
    model_cnn.add(Dense(1))
    model_cnn.compile(loss='mse', optimizer=adam)
    model_cnn.summary()

    model_cnn.fit(x_train_series, y_train, validation_data=(
        x_valid_series, y_valid), epochs=epochs, verbose=2)
    return model_cnn


def load_sample_data():
    import os
    re = pd.read_csv(f'{os.path.dirname(os.path.realpath(__file__))}/go.csv')
    items = []
    for row in re.iterrows():
        items.append({
            'item': int(row[1]['Item']),
            'store': int(row[1]['Store']),
            'amount': int(row[1]['Amount'])
        })
    return items
