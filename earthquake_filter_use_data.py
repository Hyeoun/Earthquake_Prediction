import pandas as pd

df = pd.read_csv('./datasets/earthquake_all.csv')
df.info()
df = df[['time', 'latitude', 'longitude', 'depth', 'mag', 'gap', 'rms']]

print('time, latitude, longitude, depth, mag,    gap,    rms')
print('   {},        {},         {},   {},   {}, {}, {}'.format(df['time'].isnull().sum(), df['latitude'].isnull().sum(), df['longitude'].isnull().sum(),
                                          df['depth'].isnull().sum(), df['mag'].isnull().sum(), df['gap'].isnull().sum(), df['rms'].isnull().sum()))  # 널값 확인
print(df.head())
df.info()
df.to_csv('./datasets/earthquake_filter_use_data.csv', index=False)