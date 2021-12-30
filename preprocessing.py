import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import pickle

df = pd.read_csv('./datasets/earthquake_filter_use_data.csv')
df.info()

df['depth'].fillna(df['depth'].mean(), inplace=True)
df['gap'].fillna(500, inplace=True)
df['rms'].fillna(0, inplace=True)

print(df['latitude'].describe())
print(df['longitude'].describe())

df['time'] = pd.to_datetime(df['time'])
df.sort_values(by='time', ascending=True, inplace=True)
df.info()
df.set_index('time', inplace=True)

# fig = plt.figure(figsize=(7.44,4))
# ax = fig.add_axes([0,0,1,1])  # 전체 figure 전부 활용
# ax.plot(df['longitude'], df['latitude'], '.', markersize=0.7, alpha=0.3, color='#ff5555')
# plt.show()

scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df)
print(scaled_data[:5])
print(scaled_data.shape)
scaled_data = pd.DataFrame(scaled_data, columns = df.columns, index=df.index)
print(type(scaled_data))
print(scaled_data.head())

with open('./datasets/earthquake_minmaxscaler.pickle', 'wb') as f:
  pickle.dump(scaler, f)

scaled_data.to_csv('./datasets/earthquake_minmax_scaled_data.csv')
