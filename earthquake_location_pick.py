import pandas as pd
import numpy as np
import time
import datetime
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import pickle

scaled_df = pd.read_csv('./datasets/earthquake_minmax_scaled_data.csv')
scaled_df['time'] = pd.to_datetime(scaled_df['time'])
scaled_df.sort_values(by='time', ascending=True, inplace=True)
scaled_df.info()
scaled_df.set_index('time', inplace=True)

with open('./datasets/earthquake_minmaxscaler.pickle', 'rb') as f:
  scaler = pickle.load(f)

# N = +, S = -, W = -, E = +
up, down, left, right = 43, 32, 136, 148
left_down = scaler.transform([[down, left, 1, 1, 1, 1]])  # 좌, 하 좌표
right_up = scaler.transform([[up, right, 1, 1, 1, 1]])  # 우, 상 좌표

left_down = list(left_down[0])
right_up = list(right_up[0])

df_location = scaled_df[(left_down[1] <= scaled_df['longitude']) & (scaled_df['longitude'] <= right_up[1]) & (left_down[0] <= scaled_df['latitude']) & (scaled_df['latitude'] <= right_up[0])]
data_location = df_location.to_numpy()
print(data_location[:5])
print(data_location.shape)

sequence_X = []
sequence_Y = []
term = 300
for i in range(len(data_location) - term):
    x = data_location[i:i+term]
    y = data_location[i+term]
    sequence_X.append(x)
    sequence_Y.append(y)
    if i is 0:
        print(x, '->', y)

sequence_X = np.array(sequence_X)
sequence_Y = np.array(sequence_Y)

X_train, X_test, Y_train, Y_test = train_test_split(sequence_X, sequence_Y, test_size=0.2)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)
xy = X_train, X_test, Y_train, Y_test
np.save('./datasets/earthquake_preprocessed_(X_{}~{},Y_{}~{},T_{}).npy'.format(left, right, down, up, term), xy)