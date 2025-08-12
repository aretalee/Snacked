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

df = har_df[har_df['timestamp'] != 0].sort_values(by = ['user', 'timestamp'], ignore_index=True)

testOne = df[df['user'] == 8].iloc[:1500]
testOne.to_csv('test1.txt', sep='\t', index=False)
claspOne = BinaryClaSPSegmentation()
data = claspOne.fit_predict(np.array(testOne))

claspOne.plot(heading=f"Segmentation of activity routine:", ts_name="ACC", font_size=18, file_path="wisdm_example.png")
plt.show()



testTwo = df[df['user'] == 8]
testTwo.to_csv('test2.txt', sep='\t', index=False)

# xs = testTwo['x-axis'].values
# ys = testTwo['y-axis'].values
# zs = testTwo['z-axis'].values
# mv_data = np.column_stack((xs, ys, zs))


claspTwo = BinaryClaSPSegmentation()
data = claspTwo.fit_predict(testTwo)
# data = claspTwo.fit_predict(mv_data)

claspTwo.plot(heading=f"Segmentation of activity routine:", ts_name="ACC", font_size=18, file_path="wisdm_example.png")
plt.show()

