from claspy.segmentation import BinaryClaSPSegmentation
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import warnings
warnings.filterwarnings('ignore')



col = ['user', 'activity', 'timestamp', 'x-axis', 'y-axis', 'z-axis']
har_df = pd.read_csv('WISDM_ar_v1.1_raw.txt', sep=',', on_bad_lines='skip', header = None, names = col)

har_df = har_df.dropna()
har_df.shape

har_df['z-axis'] = har_df['z-axis'].str.replace(';', '')
har_df['z-axis'] = har_df['z-axis'].apply(lambda x:float(x))

df = har_df[har_df['timestamp'] != 0]
#.sort_values(by = ['user', 'timestamp'], ignore_index=True)


testing = df[df['user'] == 8]
testing.to_csv('testing.txt', sep='\t', index=False)

xs = testing['x-axis'].values
ys = testing['y-axis'].values
zs = testing['z-axis'].values
mv_data = np.column_stack((xs, ys, zs))


tclasp = BinaryClaSPSegmentation()
data = tclasp.fit_predict(mv_data)

tclasp.plot(heading=f"Segmentation of activity routine:", ts_name="ACC", font_size=18, file_path="wisdm_example.png")
plt.show()

