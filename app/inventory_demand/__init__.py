import pandas as pd
from keras import optimizers
from keras.layers import Dense, Flatten
from keras.layers.convolutional import Conv1D, MaxPooling1D
from keras.models import Sequential
from numpy.random import seed
from sklearn.model_selection import train_test_split

seed(1)


def transform_data(training_data, months):
    training_data['date'] = pd.to_datetime(training_data['date'])
    window = (training_data['date'].max().date() - training_data['date'].min().date()).days
    lag_size = months*30
    print(f'{window} date difference')
    print('-------------')
    train_gp = training_data.sort_values('date').groupby(
        ['item', 'store', 'date'], as_index=False)
    train_gp = train_gp.agg({'sales': ['mean']})
    train_gp.columns = ['item', 'store', 'date', 'sales']
    lag = lag_size
    print(f'train_gp: {train_gp}')
    series = series_to_supervised(train_gp.drop(
        'date', axis=1), window=window, lag=lag)
    last_item = 'item(t-%d)' % window
    last_store = 'store(t-%d)' % window
    print(len(series))
    series = series[(series['store(t)'] == series[last_store])]
    series = series[(series['item(t)'] == series[last_item])]
    # aca borro columnas
    # columns_to_drop = [('%s(t+%d)' % (col, lag)) for col in []]
    # for i in range(window, 0, -1):
    #     columns_to_drop += [('%s(t-%d)' % (col, i))
    #                         for col in ['item', 'store']]
    # series.drop(columns_to_drop, axis=1, inplace=True)
    # series.drop(['item(t)', 'store(t)'], axis=1, inplace=True)
    labels_col = 'sales(t+%d)' % lag_size
    labels = series[labels_col]
    series = series.drop(labels_col, axis=1)
    print(len(series), len(labels.values), lag_size)

    X_train, X_valid, Y_train, Y_valid = train_test_split(
        series, labels.values, test_size=0.4, random_state=0)

    X_train_series = X_train.values.reshape(
        (X_train.shape[0], X_train.shape[1], 1))
    X_valid_series = X_valid.values.reshape(
        (X_valid.shape[0], X_valid.shape[1], 1))
    return {'X_train_series': X_train_series, 'Y_train': Y_train, 'X_valid_series': X_valid_series, 'Y_valid': Y_valid}


def series_to_supervised(data, window=1, lag=1, dropnan=True):
    cols, names = list(), list()
    # Input sequence (t-n, ... t-1)
    for i in range(window, 0, -1):
        cols.append(data.shift(i))
        names += [('%s(t-%d)' % (col, i)) for col in data.columns]
    # Current timestep (t=0)
    cols.append(data)
    names += [('%s(t)' % (col)) for col in data.columns]
    # Target timestep (t=lag)
    cols.append(data.shift(-lag))
    names += [('%s(t+%d)' % (col, lag)) for col in data.columns]
    # Put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # Drop rows with NaN values
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
