import pandas as pd
import glob

data_paths = glob.glob('./datasets/first_concat_data/*')
print(data_paths)
df = pd.DataFrame()
for data_path in data_paths:
    df_temp = pd.read_csv(data_path)
    df = pd.concat([df, df_temp])
df.reset_index(inplace=True)
print(df.head())
print(df.tail())
df.info()
df.to_csv('./datasets/earthquake_all.csv', index=False)