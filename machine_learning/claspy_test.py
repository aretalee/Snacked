from claspy.segmentation import BinaryClaSPSegmentation
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


col = ['user', 'activity', 'timestamp', 'x-axis', 'y-axis', 'z-axis']
wisdm = pd.read_csv('WISDM_ar_v1.1_raw.txt', sep=',', on_bad_lines='skip', header = None, names = col)

wisdm = wisdm.dropna()
wisdm.shape

wisdm['z-axis'] = wisdm['z-axis'].str.replace(';', '')
wisdm['z-axis'] = wisdm['z-axis'].apply(lambda x:float(x))

df = wisdm[wisdm['timestamp'] != 0].sort_values(by = ['user', 'timestamp'], ignore_index=True)

testOne = df[df['user'] == 33].iloc[:8000]
testOne.to_csv('claspy_test1.txt', sep='\t', index=False)

x = testOne['x-axis'].values
y = testOne['y-axis'].values
z = testOne['z-axis'].values
data = np.column_stack((x, y, z))

claspOne = BinaryClaSPSegmentation()
dataOne = claspOne.fit_predict(data)

claspOne.plot(heading=f"Segmentation of activity routine:", ts_name="ACC", font_size=18, file_path="wisdm_example.png")
plt.show()


testTwo = df[df['user'] == 8]
testTwo.to_csv('claspy_test2.txt', sep='\t', index=False)

xs = testTwo['x-axis'].values
ys = testTwo['y-axis'].values
zs = testTwo['z-axis'].values
mv_data = np.column_stack((xs, ys, zs))


claspTwo = BinaryClaSPSegmentation()
dataTwo = claspTwo.fit_predict(mv_data)

claspTwo.plot(heading=f"Segmentation of activity routine:", ts_name="ACC", font_size=18, file_path="wisdm_example.png")
plt.show()

