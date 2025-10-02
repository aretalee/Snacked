import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.signal import find_peaks
import warnings
warnings.filterwarnings('ignore')

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score



col = ['user', 'activity', 'timestamp', 'x-axis', 'y-axis', 'z-axis']
wisdm = pd.read_csv('WISDM_ar_v1.1_raw.txt', sep=',', on_bad_lines='skip', header = None, names = col)


wisdm = wisdm.dropna()
wisdm.shape

wisdm['z-axis'] = wisdm['z-axis'].str.replace(';', '')
wisdm['z-axis'] = wisdm['z-axis'].apply(lambda x:float(x))


user_one = wisdm[wisdm['user'] == 33]

training, testing = [], []

for label, group in user_one.groupby('activity'): 
  group = group.sort_values(by='timestamp')
  split = int(len(group) * 0.8)
  train = group.iloc[:split]
  test = group.iloc[split:]

  training.append(train)
  testing.append(test)

train_df= pd.concat(training) 
test_df= pd.concat(testing) 


train_df = train_df.sort_values(by = ['timestamp'], ignore_index=True)
test_df = test_df.sort_values(by = ['timestamp'], ignore_index=True)

x_items = []
y_items = []
z_items = []
train_labels = []

window = 100
step = 50


for i in range(0, train_df.shape[0] - window, step):
  xs = train_df['x-axis'].values[i: i + 100]
  ys = train_df['y-axis'].values[i: i + 100]
  zs = train_df['z-axis'].values[i: i + 100]
  label = train_df['activity'][i: i + 100].mode()[0]
  
  x_items.append(xs)
  y_items.append(ys)
  z_items.append(zs)
  train_labels.append(label)


X_training = pd.DataFrame()
  
# mean
X_training['x_mean'] = pd.Series(x_items).apply(lambda x: x.mean())
X_training['y_mean'] = pd.Series(y_items).apply(lambda x: x.mean())
X_training['z_mean'] = pd.Series(z_items).apply(lambda x: x.mean())

# std dev
X_training['x_std'] = pd.Series(x_items).apply(lambda x: x.std())
X_training['y_std'] = pd.Series(y_items).apply(lambda x: x.std())
X_training['z_std'] = pd.Series(z_items).apply(lambda x: x.std())

# avg absolute diff
X_training['x_aad'] = pd.Series(x_items).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_training['y_aad'] = pd.Series(y_items).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_training['z_aad'] = pd.Series(z_items).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

# min
X_training['x_min'] = pd.Series(x_items).apply(lambda x: x.min())
X_training['y_min'] = pd.Series(y_items).apply(lambda x: x.min())
X_training['z_min'] = pd.Series(z_items).apply(lambda x: x.min())

# max
X_training['x_max'] = pd.Series(x_items).apply(lambda x: x.max())
X_training['y_max'] = pd.Series(y_items).apply(lambda x: x.max())
X_training['z_max'] = pd.Series(z_items).apply(lambda x: x.max())

# max-min diff
X_training['x_maxmin_diff'] = X_training['x_max'] - X_training['x_min']
X_training['y_maxmin_diff'] = X_training['y_max'] - X_training['y_min']
X_training['z_maxmin_diff'] = X_training['z_max'] - X_training['z_min']

# median
X_training['x_median'] = pd.Series(x_items).apply(lambda x: np.median(x))
X_training['y_median'] = pd.Series(y_items).apply(lambda x: np.median(x))
X_training['z_median'] = pd.Series(z_items).apply(lambda x: np.median(x))

# median abs dev 
X_training['x_mad'] = pd.Series(x_items).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_training['y_mad'] = pd.Series(y_items).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_training['z_mad'] = pd.Series(z_items).apply(lambda x: np.median(np.absolute(x - np.median(x))))

# interquartile range
X_training['x_IQR'] = pd.Series(x_items).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_training['y_IQR'] = pd.Series(y_items).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_training['z_IQR'] = pd.Series(z_items).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

# negtive count
X_training['x_neg_count'] = pd.Series(x_items).apply(lambda x: np.sum(x < 0))
X_training['y_neg_count'] = pd.Series(y_items).apply(lambda x: np.sum(x < 0))
X_training['z_neg_count'] = pd.Series(z_items).apply(lambda x: np.sum(x < 0))

# positive count
X_training['x_pos_count'] = pd.Series(x_items).apply(lambda x: np.sum(x > 0))
X_training['y_pos_count'] = pd.Series(y_items).apply(lambda x: np.sum(x > 0))
X_training['z_pos_count'] = pd.Series(z_items).apply(lambda x: np.sum(x > 0))

# values above mean
X_training['x_above_mean'] = pd.Series(x_items).apply(lambda x: np.sum(x > x.mean()))
X_training['y_above_mean'] = pd.Series(y_items).apply(lambda x: np.sum(x > x.mean()))
X_training['z_above_mean'] = pd.Series(z_items).apply(lambda x: np.sum(x > x.mean()))

# number of peaks
X_training['x_peak_count'] = pd.Series(x_items).apply(lambda x: len(find_peaks(x)[0]))
X_training['y_peak_count'] = pd.Series(y_items).apply(lambda x: len(find_peaks(x)[0]))
X_training['z_peak_count'] = pd.Series(z_items).apply(lambda x: len(find_peaks(x)[0]))

# skewness
X_training['x_skewness'] = pd.Series(x_items).apply(lambda x: stats.skew(x))
X_training['y_skewness'] = pd.Series(y_items).apply(lambda x: stats.skew(x))
X_training['z_skewness'] = pd.Series(z_items).apply(lambda x: stats.skew(x))

# kurtosis
X_training['x_kurtosis'] = pd.Series(x_items).apply(lambda x: stats.kurtosis(x))
X_training['y_kurtosis'] = pd.Series(y_items).apply(lambda x: stats.kurtosis(x))
X_training['z_kurtosis'] = pd.Series(z_items).apply(lambda x: stats.kurtosis(x))

# energy
X_training['x_energy'] = pd.Series(x_items).apply(lambda x: np.sum(x**2)/100)
X_training['y_energy'] = pd.Series(y_items).apply(lambda x: np.sum(x**2)/100)
X_training['z_energy'] = pd.Series(z_items).apply(lambda x: np.sum(x**2/100))

# avg resultant
X_training['avg_result_accl'] = [i.mean() for i in ((pd.Series(x_items)**2 + pd.Series(y_items)**2 + pd.Series(z_items)**2)**0.5)]

# signal magnitude area
X_training['sma'] =    pd.Series(x_items).apply(lambda x: np.sum(abs(x)/100)) + pd.Series(y_items).apply(lambda x: np.sum(abs(x)/100)) \
                  + pd.Series(z_items).apply(lambda x: np.sum(abs(x)/100))



# fft: chaning time domain signals to frequency domain
x_fft = pd.Series(x_items).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
y_fft = pd.Series(y_items).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
z_fft = pd.Series(z_items).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))

# Statistical Features on raw x, y and z in frequency domain
# FFT mean
X_training['x_mean_fft'] = pd.Series(x_fft).apply(lambda x: x.mean())
X_training['y_mean_fft'] = pd.Series(y_fft).apply(lambda x: x.mean())
X_training['z_mean_fft'] = pd.Series(z_fft).apply(lambda x: x.mean())

# FFT std dev
X_training['x_std_fft'] = pd.Series(x_fft).apply(lambda x: x.std())
X_training['y_std_fft'] = pd.Series(y_fft).apply(lambda x: x.std())
X_training['z_std_fft'] = pd.Series(z_fft).apply(lambda x: x.std())

# FFT avg absolute diff
X_training['x_aad_fft'] = pd.Series(x_fft).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_training['y_aad_fft'] = pd.Series(y_fft).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_training['z_aad_fft'] = pd.Series(z_fft).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

# FFT min
X_training['x_min_fft'] = pd.Series(x_fft).apply(lambda x: x.min())
X_training['y_min_fft'] = pd.Series(y_fft).apply(lambda x: x.min())
X_training['z_min_fft'] = pd.Series(z_fft).apply(lambda x: x.min())

# FFT max
X_training['x_max_fft'] = pd.Series(x_fft).apply(lambda x: x.max())
X_training['y_max_fft'] = pd.Series(y_fft).apply(lambda x: x.max())
X_training['z_max_fft'] = pd.Series(z_fft).apply(lambda x: x.max())

# FFT max-min diff
X_training['x_maxmin_diff_fft'] = X_training['x_max_fft'] - X_training['x_min_fft']
X_training['y_maxmin_diff_fft'] = X_training['y_max_fft'] - X_training['y_min_fft']
X_training['z_maxmin_diff_fft'] = X_training['z_max_fft'] - X_training['z_min_fft']

# FFT median
X_training['x_median_fft'] = pd.Series(x_fft).apply(lambda x: np.median(x))
X_training['y_median_fft'] = pd.Series(y_fft).apply(lambda x: np.median(x))
X_training['z_median_fft'] = pd.Series(z_fft).apply(lambda x: np.median(x))

# FFT median abs dev 
X_training['x_mad_fft'] = pd.Series(x_fft).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_training['y_mad_fft'] = pd.Series(y_fft).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_training['z_mad_fft'] = pd.Series(z_fft).apply(lambda x: np.median(np.absolute(x - np.median(x))))

# FFT Interquartile range
X_training['x_IQR_fft'] = pd.Series(x_fft).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_training['y_IQR_fft'] = pd.Series(y_fft).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_training['z_IQR_fft'] = pd.Series(z_fft).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

# FFT values above mean
X_training['x_above_mean_fft'] = pd.Series(x_fft).apply(lambda x: np.sum(x > x.mean()))
X_training['y_above_mean_fft'] = pd.Series(y_fft).apply(lambda x: np.sum(x > x.mean()))
X_training['z_above_mean_fft'] = pd.Series(z_fft).apply(lambda x: np.sum(x > x.mean()))

# FFT number of peaks
X_training['x_peak_count_fft'] = pd.Series(x_fft).apply(lambda x: len(find_peaks(x)[0]))
X_training['y_peak_count_fft'] = pd.Series(y_fft).apply(lambda x: len(find_peaks(x)[0]))
X_training['z_peak_count_fft'] = pd.Series(z_fft).apply(lambda x: len(find_peaks(x)[0]))

# FFT skewness
X_training['x_skewness_fft'] = pd.Series(x_fft).apply(lambda x: stats.skew(x))
X_training['y_skewness_fft'] = pd.Series(y_fft).apply(lambda x: stats.skew(x))
X_training['z_skewness_fft'] = pd.Series(z_fft).apply(lambda x: stats.skew(x))

# FFT kurtosis
X_training['x_kurtosis_fft'] = pd.Series(x_fft).apply(lambda x: stats.kurtosis(x))
X_training['y_kurtosis_fft'] = pd.Series(y_fft).apply(lambda x: stats.kurtosis(x))
X_training['z_kurtosis_fft'] = pd.Series(z_fft).apply(lambda x: stats.kurtosis(x))

# FFT energy
X_training['x_energy_fft'] = pd.Series(x_fft).apply(lambda x: np.sum(x**2)/50)
X_training['y_energy_fft'] = pd.Series(y_fft).apply(lambda x: np.sum(x**2)/50)
X_training['z_energy_fft'] = pd.Series(z_fft).apply(lambda x: np.sum(x**2/50))

# FFT avg resultant
X_training['avg_result_accl_fft'] = [i.mean() for i in ((pd.Series(x_fft)**2 + pd.Series(y_fft)**2 + pd.Series(z_fft)**2)**0.5)]

# FFT Signal magnitude area
X_training['sma_fft'] = pd.Series(x_fft).apply(lambda x: np.sum(abs(x)/50)) + pd.Series(y_fft).apply(lambda x: np.sum(abs(x)/50)) \
                     + pd.Series(z_fft).apply(lambda x: np.sum(abs(x)/50))


# calculating max & min indices

# index of max value in time domain
X_training['x_argmax'] = pd.Series(x_items).apply(lambda x: np.argmax(x))
X_training['y_argmax'] = pd.Series(y_items).apply(lambda x: np.argmax(x))
X_training['z_argmax'] = pd.Series(z_items).apply(lambda x: np.argmax(x))

# index of min value in time domain
X_training['x_argmin'] = pd.Series(x_items).apply(lambda x: np.argmin(x))
X_training['y_argmin'] = pd.Series(y_items).apply(lambda x: np.argmin(x))
X_training['z_argmin'] = pd.Series(z_items).apply(lambda x: np.argmin(x))

# absolute difference between above indices
X_training['x_arg_diff'] = abs(X_training['x_argmax'] - X_training['x_argmin'])
X_training['y_arg_diff'] = abs(X_training['y_argmax'] - X_training['y_argmin'])
X_training['z_arg_diff'] = abs(X_training['z_argmax'] - X_training['z_argmin'])

# index of max value in frequency domain
X_training['x_argmax_fft'] = pd.Series(x_fft).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
X_training['y_argmax_fft'] = pd.Series(y_fft).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
X_training['z_argmax_fft'] = pd.Series(z_fft).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))

# index of min value in frequency domain
X_training['x_argmin_fft'] = pd.Series(x_fft).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
X_training['y_argmin_fft'] = pd.Series(y_fft).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
X_training['z_argmin_fft'] = pd.Series(z_fft).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))

# absolute difference between above indices
X_training['x_arg_diff_fft'] = abs(X_training['x_argmax_fft'] - X_training['x_argmin_fft'])
X_training['y_arg_diff_fft'] = abs(X_training['y_argmax_fft'] - X_training['y_argmin_fft'])
X_training['z_arg_diff_fft'] = abs(X_training['z_argmax_fft'] - X_training['z_argmin_fft'])


# do the same for test data

x_items_test = []
y_items_test = []
z_items_test = []
test_labels = []

window = 100
step = 50


for i in range(0, test_df.shape[0] - window, step):
  xs_test = test_df['x-axis'].values[i: i + 100]
  ys_test = test_df['y-axis'].values[i: i + 100]
  zs_test = test_df['z-axis'].values[i: i + 100]
  test_label = test_df['activity'][i: i + 100].mode()[0]
  
  x_items_test.append(xs_test)
  y_items_test.append(ys_test)
  z_items_test.append(zs_test)
  test_labels.append(test_label)

X_testing = pd.DataFrame()
  
# mean
X_testing['x_mean'] = pd.Series(x_items_test).apply(lambda x: x.mean())
X_testing['y_mean'] = pd.Series(y_items_test).apply(lambda x: x.mean())
X_testing['z_mean'] = pd.Series(z_items_test).apply(lambda x: x.mean())

# std dev
X_testing['x_std'] = pd.Series(x_items_test).apply(lambda x: x.std())
X_testing['y_std'] = pd.Series(y_items_test).apply(lambda x: x.std())
X_testing['z_std'] = pd.Series(z_items_test).apply(lambda x: x.std())

# avg absolute diff
X_testing['x_aad'] = pd.Series(x_items_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_testing['y_aad'] = pd.Series(y_items_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_testing['z_aad'] = pd.Series(z_items_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

# min
X_testing['x_min'] = pd.Series(x_items_test).apply(lambda x: x.min())
X_testing['y_min'] = pd.Series(y_items_test).apply(lambda x: x.min())
X_testing['z_min'] = pd.Series(z_items_test).apply(lambda x: x.min())

# max
X_testing['x_max'] = pd.Series(x_items_test).apply(lambda x: x.max())
X_testing['y_max'] = pd.Series(y_items_test).apply(lambda x: x.max())
X_testing['z_max'] = pd.Series(z_items_test).apply(lambda x: x.max())

# max-min diff
X_testing['x_maxmin_diff'] = X_testing['x_max'] - X_testing['x_min']
X_testing['y_maxmin_diff'] = X_testing['y_max'] - X_testing['y_min']
X_testing['z_maxmin_diff'] = X_testing['z_max'] - X_testing['z_min']

# median
X_testing['x_median'] = pd.Series(x_items_test).apply(lambda x: np.median(x))
X_testing['y_median'] = pd.Series(y_items_test).apply(lambda x: np.median(x))
X_testing['z_median'] = pd.Series(z_items_test).apply(lambda x: np.median(x))

# median abs dev 
X_testing['x_mad'] = pd.Series(x_items_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_testing['y_mad'] = pd.Series(y_items_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_testing['z_mad'] = pd.Series(z_items_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))

# interquartile range
X_testing['x_IQR'] = pd.Series(x_items_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_testing['y_IQR'] = pd.Series(y_items_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_testing['z_IQR'] = pd.Series(z_items_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

# negtive count
X_testing['x_neg_count'] = pd.Series(x_items_test).apply(lambda x: np.sum(x < 0))
X_testing['y_neg_count'] = pd.Series(y_items_test).apply(lambda x: np.sum(x < 0))
X_testing['z_neg_count'] = pd.Series(z_items_test).apply(lambda x: np.sum(x < 0))

# positive count
X_testing['x_pos_count'] = pd.Series(x_items_test).apply(lambda x: np.sum(x > 0))
X_testing['y_pos_count'] = pd.Series(y_items_test).apply(lambda x: np.sum(x > 0))
X_testing['z_pos_count'] = pd.Series(z_items_test).apply(lambda x: np.sum(x > 0))

# values above mean
X_testing['x_above_mean'] = pd.Series(x_items_test).apply(lambda x: np.sum(x > x.mean()))
X_testing['y_above_mean'] = pd.Series(y_items_test).apply(lambda x: np.sum(x > x.mean()))
X_testing['z_above_mean'] = pd.Series(z_items_test).apply(lambda x: np.sum(x > x.mean()))

# number of peaks
X_testing['x_peak_count'] = pd.Series(x_items_test).apply(lambda x: len(find_peaks(x)[0]))
X_testing['y_peak_count'] = pd.Series(y_items_test).apply(lambda x: len(find_peaks(x)[0]))
X_testing['z_peak_count'] = pd.Series(z_items_test).apply(lambda x: len(find_peaks(x)[0]))

# skewness
X_testing['x_skewness'] = pd.Series(x_items_test).apply(lambda x: stats.skew(x))
X_testing['y_skewness'] = pd.Series(y_items_test).apply(lambda x: stats.skew(x))
X_testing['z_skewness'] = pd.Series(z_items_test).apply(lambda x: stats.skew(x))

# kurtosis
X_testing['x_kurtosis'] = pd.Series(x_items_test).apply(lambda x: stats.kurtosis(x))
X_testing['y_kurtosis'] = pd.Series(y_items_test).apply(lambda x: stats.kurtosis(x))
X_testing['z_kurtosis'] = pd.Series(z_items_test).apply(lambda x: stats.kurtosis(x))

# energy
X_testing['x_energy'] = pd.Series(x_items_test).apply(lambda x: np.sum(x**2)/100)
X_testing['y_energy'] = pd.Series(y_items_test).apply(lambda x: np.sum(x**2)/100)
X_testing['z_energy'] = pd.Series(z_items_test).apply(lambda x: np.sum(x**2/100))

# avg resultant
X_testing['avg_result_accl'] = [i.mean() for i in ((pd.Series(x_items_test)**2 + pd.Series(y_items_test)**2 + pd.Series(z_items_test)**2)**0.5)]

# signal magnitude area
X_testing['sma'] =    pd.Series(x_items_test).apply(lambda x: np.sum(abs(x)/100)) + pd.Series(y_items_test).apply(lambda x: np.sum(abs(x)/100)) \
                  + pd.Series(z_items_test).apply(lambda x: np.sum(abs(x)/100))




# fft: chaning time domain signals to frequency domain
x_fft_test = pd.Series(x_items_test).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
y_fft_test = pd.Series(y_items_test).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
z_fft_test = pd.Series(z_items_test).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))

# Statistical Features on raw x, y and z in frequency domain
# FFT mean
X_testing['x_mean_fft'] = pd.Series(x_fft_test).apply(lambda x: x.mean())
X_testing['y_mean_fft'] = pd.Series(y_fft_test).apply(lambda x: x.mean())
X_testing['z_mean_fft'] = pd.Series(z_fft_test).apply(lambda x: x.mean())

# FFT std dev
X_testing['x_std_fft'] = pd.Series(x_fft_test).apply(lambda x: x.std())
X_testing['y_std_fft'] = pd.Series(y_fft_test).apply(lambda x: x.std())
X_testing['z_std_fft'] = pd.Series(z_fft_test).apply(lambda x: x.std())

# FFT avg absolute diff
X_testing['x_aad_fft'] = pd.Series(x_fft_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_testing['y_aad_fft'] = pd.Series(y_fft_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_testing['z_aad_fft'] = pd.Series(z_fft_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

# FFT min
X_testing['x_min_fft'] = pd.Series(x_fft_test).apply(lambda x: x.min())
X_testing['y_min_fft'] = pd.Series(y_fft_test).apply(lambda x: x.min())
X_testing['z_min_fft'] = pd.Series(z_fft_test).apply(lambda x: x.min())

# FFT max
X_testing['x_max_fft'] = pd.Series(x_fft_test).apply(lambda x: x.max())
X_testing['y_max_fft'] = pd.Series(y_fft_test).apply(lambda x: x.max())
X_testing['z_max_fft'] = pd.Series(z_fft_test).apply(lambda x: x.max())

# FFT max-min diff
X_testing['x_maxmin_diff_fft'] = X_testing['x_max_fft'] - X_testing['x_min_fft']
X_testing['y_maxmin_diff_fft'] = X_testing['y_max_fft'] - X_testing['y_min_fft']
X_testing['z_maxmin_diff_fft'] = X_testing['z_max_fft'] - X_testing['z_min_fft']

# FFT median
X_testing['x_median_fft'] = pd.Series(x_fft_test).apply(lambda x: np.median(x))
X_testing['y_median_fft'] = pd.Series(y_fft_test).apply(lambda x: np.median(x))
X_testing['z_median_fft'] = pd.Series(z_fft_test).apply(lambda x: np.median(x))

# FFT median abs dev 
X_testing['x_mad_fft'] = pd.Series(x_fft_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_testing['y_mad_fft'] = pd.Series(y_fft_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_testing['z_mad_fft'] = pd.Series(z_fft_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))

# FFT Interquartile range
X_testing['x_IQR_fft'] = pd.Series(x_fft_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_testing['y_IQR_fft'] = pd.Series(y_fft_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_testing['z_IQR_fft'] = pd.Series(z_fft_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

# FFT values above mean
X_testing['x_above_mean_fft'] = pd.Series(x_fft_test).apply(lambda x: np.sum(x > x.mean()))
X_testing['y_above_mean_fft'] = pd.Series(y_fft_test).apply(lambda x: np.sum(x > x.mean()))
X_testing['z_above_mean_fft'] = pd.Series(z_fft_test).apply(lambda x: np.sum(x > x.mean()))

# FFT number of peaks
X_testing['x_peak_count_fft'] = pd.Series(x_fft_test).apply(lambda x: len(find_peaks(x)[0]))
X_testing['y_peak_count_fft'] = pd.Series(y_fft_test).apply(lambda x: len(find_peaks(x)[0]))
X_testing['z_peak_count_fft'] = pd.Series(z_fft_test).apply(lambda x: len(find_peaks(x)[0]))

# FFT skewness
X_testing['x_skewness_fft'] = pd.Series(x_fft_test).apply(lambda x: stats.skew(x))
X_testing['y_skewness_fft'] = pd.Series(y_fft_test).apply(lambda x: stats.skew(x))
X_testing['z_skewness_fft'] = pd.Series(z_fft_test).apply(lambda x: stats.skew(x))

# FFT kurtosis
X_testing['x_kurtosis_fft'] = pd.Series(x_fft_test).apply(lambda x: stats.kurtosis(x))
X_testing['y_kurtosis_fft'] = pd.Series(y_fft_test).apply(lambda x: stats.kurtosis(x))
X_testing['z_kurtosis_fft'] = pd.Series(z_fft_test).apply(lambda x: stats.kurtosis(x))

# FFT energy
X_testing['x_energy_fft'] = pd.Series(x_fft_test).apply(lambda x: np.sum(x**2)/50)
X_testing['y_energy_fft'] = pd.Series(y_fft_test).apply(lambda x: np.sum(x**2)/50)
X_testing['z_energy_fft'] = pd.Series(z_fft_test).apply(lambda x: np.sum(x**2/50))

# FFT avg resultant
X_testing['avg_result_accl_fft'] = [i.mean() for i in ((pd.Series(x_fft_test)**2 + pd.Series(y_fft_test)**2 + pd.Series(z_fft_test)**2)**0.5)]

# FFT Signal magnitude area
X_testing['sma_fft'] = pd.Series(x_fft_test).apply(lambda x: np.sum(abs(x)/50)) + pd.Series(y_fft_test).apply(lambda x: np.sum(abs(x)/50)) \
                     + pd.Series(z_fft_test).apply(lambda x: np.sum(abs(x)/50))


# calculating max & min indices

# index of max value in time domain
X_testing['x_argmax'] = pd.Series(x_items_test).apply(lambda x: np.argmax(x))
X_testing['y_argmax'] = pd.Series(y_items_test).apply(lambda x: np.argmax(x))
X_testing['z_argmax'] = pd.Series(z_items_test).apply(lambda x: np.argmax(x))

# index of min value in time domain
X_testing['x_argmin'] = pd.Series(x_items_test).apply(lambda x: np.argmin(x))
X_testing['y_argmin'] = pd.Series(y_items_test).apply(lambda x: np.argmin(x))
X_testing['z_argmin'] = pd.Series(z_items_test).apply(lambda x: np.argmin(x))

# absolute difference between above indices
X_testing['x_arg_diff'] = abs(X_testing['x_argmax'] - X_testing['x_argmin'])
X_testing['y_arg_diff'] = abs(X_testing['y_argmax'] - X_testing['y_argmin'])
X_testing['z_arg_diff'] = abs(X_testing['z_argmax'] - X_testing['z_argmin'])

# index of max value in frequency domain
X_testing['x_argmax_fft'] = pd.Series(x_fft_test).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
X_testing['y_argmax_fft'] = pd.Series(y_fft_test).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
X_testing['z_argmax_fft'] = pd.Series(z_fft_test).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))

# index of min value in frequency domain
X_testing['x_argmin_fft'] = pd.Series(x_fft_test).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
X_testing['y_argmin_fft'] = pd.Series(y_fft_test).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
X_testing['z_argmin_fft'] = pd.Series(z_fft_test).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))

# absolute difference between above indices
X_testing['x_arg_diff_fft'] = abs(X_testing['x_argmax_fft'] - X_testing['x_argmin_fft'])
X_testing['y_arg_diff_fft'] = abs(X_testing['y_argmax_fft'] - X_testing['y_argmin_fft'])
X_testing['z_arg_diff_fft'] = abs(X_testing['z_argmax_fft'] - X_testing['z_argmin_fft'])


y_train = np.array(train_labels)
y_test = np.array(test_labels)


# model for User 33
rf = RandomForestClassifier(random_state = 21)
k=5
folds = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
scores = cross_val_score(rf, X_training, y_train, cv=folds, scoring='accuracy')

rf.fit(X_training, y_train)
y_pred = rf.predict(X_testing)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy of model trained on WISDM User 33:", accuracy)
print("Cross validation score:", scores)
print("Cross validation mean:", np.mean(scores))
print(classification_report(y_test, y_pred))

labels = ['Downstairs', 'Jogging', 'Sitting', 'Standing', 'Upstairs', 'Walking']
confusion_matrix_one = confusion_matrix(y_test, y_pred)
sns.heatmap(confusion_matrix_one, xticklabels=labels, yticklabels=labels, annot=True,linewidths = 0.1, fmt="d", cmap = 'YlGnBu')
plt.title("Confusion matrix", fontsize = 15)
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()



user_two = wisdm[wisdm['user'] == 8]

training_two, testing_two = [], []

for label, group in user_two.groupby('activity'): 
  group = group.sort_values(by='timestamp')
  split_two = int(len(group) * 0.8)
  train_two = group.iloc[:split_two]
  test_two = group.iloc[split_two:]

  training_two.append(train_two)
  testing_two.append(test_two)

train_df_two= pd.concat(training_two) 
test_df_two= pd.concat(testing_two) 


train_df_two = train_df_two.sort_values(by = ['timestamp'], ignore_index=True)
test_df_two = test_df_two.sort_values(by = ['timestamp'], ignore_index=True)

x_items_two = []
y_items_two = []
z_items_two = []
train_labels_two = []

window = 100
step = 50


for i in range(0, train_df_two.shape[0] - window, step):
  xs = train_df_two['x-axis'].values[i: i + 100]
  ys = train_df_two['y-axis'].values[i: i + 100]
  zs = train_df_two['z-axis'].values[i: i + 100]
  label = train_df_two['activity'][i: i + 100].mode()[0]
  
  x_items_two.append(xs)
  y_items_two.append(ys)
  z_items_two.append(zs)
  train_labels_two.append(label)


X_training_two = pd.DataFrame()
  
# mean
X_training_two['x_mean'] = pd.Series(x_items_two).apply(lambda x: x.mean())
X_training_two['y_mean'] = pd.Series(y_items_two).apply(lambda x: x.mean())
X_training_two['z_mean'] = pd.Series(z_items_two).apply(lambda x: x.mean())

# std dev
X_training_two['x_std'] = pd.Series(x_items_two).apply(lambda x: x.std())
X_training_two['y_std'] = pd.Series(y_items_two).apply(lambda x: x.std())
X_training_two['z_std'] = pd.Series(z_items_two).apply(lambda x: x.std())

# avg absolute diff
X_training_two['x_aad'] = pd.Series(x_items_two).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_training_two['y_aad'] = pd.Series(y_items_two).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_training_two['z_aad'] = pd.Series(z_items_two).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

# min
X_training_two['x_min'] = pd.Series(x_items_two).apply(lambda x: x.min())
X_training_two['y_min'] = pd.Series(y_items_two).apply(lambda x: x.min())
X_training_two['z_min'] = pd.Series(z_items_two).apply(lambda x: x.min())

# max
X_training_two['x_max'] = pd.Series(x_items_two).apply(lambda x: x.max())
X_training_two['y_max'] = pd.Series(y_items_two).apply(lambda x: x.max())
X_training_two['z_max'] = pd.Series(z_items_two).apply(lambda x: x.max())

# max-min diff
X_training_two['x_maxmin_diff'] = X_training_two['x_max'] - X_training_two['x_min']
X_training_two['y_maxmin_diff'] = X_training_two['y_max'] - X_training_two['y_min']
X_training_two['z_maxmin_diff'] = X_training_two['z_max'] - X_training_two['z_min']

# median
X_training_two['x_median'] = pd.Series(x_items_two).apply(lambda x: np.median(x))
X_training_two['y_median'] = pd.Series(y_items_two).apply(lambda x: np.median(x))
X_training_two['z_median'] = pd.Series(z_items_two).apply(lambda x: np.median(x))

# median abs dev 
X_training_two['x_mad'] = pd.Series(x_items_two).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_training_two['y_mad'] = pd.Series(y_items_two).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_training_two['z_mad'] = pd.Series(z_items_two).apply(lambda x: np.median(np.absolute(x - np.median(x))))

# interquartile range
X_training_two['x_IQR'] = pd.Series(x_items_two).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_training_two['y_IQR'] = pd.Series(y_items_two).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_training_two['z_IQR'] = pd.Series(z_items_two).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

# negtive count
X_training_two['x_neg_count'] = pd.Series(x_items_two).apply(lambda x: np.sum(x < 0))
X_training_two['y_neg_count'] = pd.Series(y_items_two).apply(lambda x: np.sum(x < 0))
X_training_two['z_neg_count'] = pd.Series(z_items_two).apply(lambda x: np.sum(x < 0))

# positive count
X_training_two['x_pos_count'] = pd.Series(x_items_two).apply(lambda x: np.sum(x > 0))
X_training_two['y_pos_count'] = pd.Series(y_items_two).apply(lambda x: np.sum(x > 0))
X_training_two['z_pos_count'] = pd.Series(z_items_two).apply(lambda x: np.sum(x > 0))

# values above mean
X_training_two['x_above_mean'] = pd.Series(x_items_two).apply(lambda x: np.sum(x > x.mean()))
X_training_two['y_above_mean'] = pd.Series(y_items_two).apply(lambda x: np.sum(x > x.mean()))
X_training_two['z_above_mean'] = pd.Series(z_items_two).apply(lambda x: np.sum(x > x.mean()))

# number of peaks
X_training_two['x_peak_count'] = pd.Series(x_items_two).apply(lambda x: len(find_peaks(x)[0]))
X_training_two['y_peak_count'] = pd.Series(y_items_two).apply(lambda x: len(find_peaks(x)[0]))
X_training_two['z_peak_count'] = pd.Series(z_items_two).apply(lambda x: len(find_peaks(x)[0]))

# skewness
X_training_two['x_skewness'] = pd.Series(x_items_two).apply(lambda x: stats.skew(x))
X_training_two['y_skewness'] = pd.Series(y_items_two).apply(lambda x: stats.skew(x))
X_training_two['z_skewness'] = pd.Series(z_items_two).apply(lambda x: stats.skew(x))

# kurtosis
X_training_two['x_kurtosis'] = pd.Series(x_items_two).apply(lambda x: stats.kurtosis(x))
X_training_two['y_kurtosis'] = pd.Series(y_items_two).apply(lambda x: stats.kurtosis(x))
X_training_two['z_kurtosis'] = pd.Series(z_items_two).apply(lambda x: stats.kurtosis(x))

# energy
X_training_two['x_energy'] = pd.Series(x_items_two).apply(lambda x: np.sum(x**2)/100)
X_training_two['y_energy'] = pd.Series(y_items_two).apply(lambda x: np.sum(x**2)/100)
X_training_two['z_energy'] = pd.Series(z_items_two).apply(lambda x: np.sum(x**2/100))

# avg resultant
X_training_two['avg_result_accl'] = [i.mean() for i in ((pd.Series(x_items_two)**2 + pd.Series(y_items_two)**2 + pd.Series(z_items_two)**2)**0.5)]

# signal magnitude area
X_training_two['sma'] =    pd.Series(x_items_two).apply(lambda x: np.sum(abs(x)/100)) + pd.Series(y_items_two).apply(lambda x: np.sum(abs(x)/100)) \
                  + pd.Series(z_items_two).apply(lambda x: np.sum(abs(x)/100))



# fft: chaning time domain signals to frequency domain
x_fft_two = pd.Series(x_items_two).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
y_fft_two = pd.Series(y_items_two).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
z_fft_two = pd.Series(z_items_two).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))

# Statistical Features on raw x, y and z in frequency domain
# FFT mean
X_training_two['x_mean_fft'] = pd.Series(x_fft_two).apply(lambda x: x.mean())
X_training_two['y_mean_fft'] = pd.Series(y_fft_two).apply(lambda x: x.mean())
X_training_two['z_mean_fft'] = pd.Series(z_fft_two).apply(lambda x: x.mean())

# FFT std dev
X_training_two['x_std_fft'] = pd.Series(x_fft_two).apply(lambda x: x.std())
X_training_two['y_std_fft'] = pd.Series(y_fft_two).apply(lambda x: x.std())
X_training_two['z_std_fft'] = pd.Series(z_fft_two).apply(lambda x: x.std())

# FFT avg absolute diff
X_training_two['x_aad_fft'] = pd.Series(x_fft_two).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_training_two['y_aad_fft'] = pd.Series(y_fft_two).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_training_two['z_aad_fft'] = pd.Series(z_fft_two).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

# FFT min
X_training_two['x_min_fft'] = pd.Series(x_fft_two).apply(lambda x: x.min())
X_training_two['y_min_fft'] = pd.Series(y_fft_two).apply(lambda x: x.min())
X_training_two['z_min_fft'] = pd.Series(z_fft_two).apply(lambda x: x.min())

# FFT max
X_training_two['x_max_fft'] = pd.Series(x_fft_two).apply(lambda x: x.max())
X_training_two['y_max_fft'] = pd.Series(y_fft_two).apply(lambda x: x.max())
X_training_two['z_max_fft'] = pd.Series(z_fft_two).apply(lambda x: x.max())

# FFT max-min diff
X_training_two['x_maxmin_diff_fft'] = X_training_two['x_max_fft'] - X_training_two['x_min_fft']
X_training_two['y_maxmin_diff_fft'] = X_training_two['y_max_fft'] - X_training_two['y_min_fft']
X_training_two['z_maxmin_diff_fft'] = X_training_two['z_max_fft'] - X_training_two['z_min_fft']

# FFT median
X_training_two['x_median_fft'] = pd.Series(x_fft_two).apply(lambda x: np.median(x))
X_training_two['y_median_fft'] = pd.Series(y_fft_two).apply(lambda x: np.median(x))
X_training_two['z_median_fft'] = pd.Series(z_fft_two).apply(lambda x: np.median(x))

# FFT median abs dev 
X_training_two['x_mad_fft'] = pd.Series(x_fft_two).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_training_two['y_mad_fft'] = pd.Series(y_fft_two).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_training_two['z_mad_fft'] = pd.Series(z_fft_two).apply(lambda x: np.median(np.absolute(x - np.median(x))))

# FFT Interquartile range
X_training_two['x_IQR_fft'] = pd.Series(x_fft_two).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_training_two['y_IQR_fft'] = pd.Series(y_fft_two).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_training_two['z_IQR_fft'] = pd.Series(z_fft_two).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

# FFT values above mean
X_training_two['x_above_mean_fft'] = pd.Series(x_fft_two).apply(lambda x: np.sum(x > x.mean()))
X_training_two['y_above_mean_fft'] = pd.Series(y_fft_two).apply(lambda x: np.sum(x > x.mean()))
X_training_two['z_above_mean_fft'] = pd.Series(z_fft_two).apply(lambda x: np.sum(x > x.mean()))

# FFT number of peaks
X_training_two['x_peak_count_fft'] = pd.Series(x_fft_two).apply(lambda x: len(find_peaks(x)[0]))
X_training_two['y_peak_count_fft'] = pd.Series(y_fft_two).apply(lambda x: len(find_peaks(x)[0]))
X_training_two['z_peak_count_fft'] = pd.Series(z_fft_two).apply(lambda x: len(find_peaks(x)[0]))

# FFT skewness
X_training_two['x_skewness_fft'] = pd.Series(x_fft_two).apply(lambda x: stats.skew(x))
X_training_two['y_skewness_fft'] = pd.Series(y_fft_two).apply(lambda x: stats.skew(x))
X_training_two['z_skewness_fft'] = pd.Series(z_fft_two).apply(lambda x: stats.skew(x))

# FFT kurtosis
X_training_two['x_kurtosis_fft'] = pd.Series(x_fft_two).apply(lambda x: stats.kurtosis(x))
X_training_two['y_kurtosis_fft'] = pd.Series(y_fft_two).apply(lambda x: stats.kurtosis(x))
X_training_two['z_kurtosis_fft'] = pd.Series(z_fft_two).apply(lambda x: stats.kurtosis(x))

# FFT energy
X_training_two['x_energy_fft'] = pd.Series(x_fft_two).apply(lambda x: np.sum(x**2)/50)
X_training_two['y_energy_fft'] = pd.Series(y_fft_two).apply(lambda x: np.sum(x**2)/50)
X_training_two['z_energy_fft'] = pd.Series(z_fft_two).apply(lambda x: np.sum(x**2/50))

# FFT avg resultant
X_training_two['avg_result_accl_fft'] = [i.mean() for i in ((pd.Series(x_fft_two)**2 + pd.Series(y_fft_two)**2 + pd.Series(z_fft_two)**2)**0.5)]

# FFT Signal magnitude area
X_training_two['sma_fft'] = pd.Series(x_fft_two).apply(lambda x: np.sum(abs(x)/50)) + pd.Series(y_fft_two).apply(lambda x: np.sum(abs(x)/50)) \
                     + pd.Series(z_fft_two).apply(lambda x: np.sum(abs(x)/50))


# calculating max & min indices

# index of max value in time domain
X_training_two['x_argmax'] = pd.Series(x_items_two).apply(lambda x: np.argmax(x))
X_training_two['y_argmax'] = pd.Series(y_items_two).apply(lambda x: np.argmax(x))
X_training_two['z_argmax'] = pd.Series(z_items_two).apply(lambda x: np.argmax(x))

# index of min value in time domain
X_training_two['x_argmin'] = pd.Series(x_items_two).apply(lambda x: np.argmin(x))
X_training_two['y_argmin'] = pd.Series(y_items_two).apply(lambda x: np.argmin(x))
X_training_two['z_argmin'] = pd.Series(z_items_two).apply(lambda x: np.argmin(x))

# absolute difference between above indices
X_training_two['x_arg_diff'] = abs(X_training_two['x_argmax'] - X_training_two['x_argmin'])
X_training_two['y_arg_diff'] = abs(X_training_two['y_argmax'] - X_training_two['y_argmin'])
X_training_two['z_arg_diff'] = abs(X_training_two['z_argmax'] - X_training_two['z_argmin'])

# index of max value in frequency domain
X_training_two['x_argmax_fft'] = pd.Series(x_fft_two).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
X_training_two['y_argmax_fft'] = pd.Series(y_fft_two).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
X_training_two['z_argmax_fft'] = pd.Series(z_fft_two).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))

# index of min value in frequency domain
X_training_two['x_argmin_fft'] = pd.Series(x_fft_two).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
X_training_two['y_argmin_fft'] = pd.Series(y_fft_two).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
X_training_two['z_argmin_fft'] = pd.Series(z_fft_two).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))

# absolute difference between above indices
X_training_two['x_arg_diff_fft'] = abs(X_training_two['x_argmax_fft'] - X_training_two['x_argmin_fft'])
X_training_two['y_arg_diff_fft'] = abs(X_training_two['y_argmax_fft'] - X_training_two['y_argmin_fft'])
X_training_two['z_arg_diff_fft'] = abs(X_training_two['z_argmax_fft'] - X_training_two['z_argmin_fft'])


# do the same for test data

x_items_two_test = []
y_items_two_test = []
z_items_two_test = []
test_labels_two = []

window = 100
step = 50


for i in range(0, test_df_two.shape[0] - window, step):
  xs_test = test_df_two['x-axis'].values[i: i + 100]
  ys_test = test_df_two['y-axis'].values[i: i + 100]
  zs_test = test_df_two['z-axis'].values[i: i + 100]
  test_label = test_df_two['activity'][i: i + 100].mode()[0]
  
  x_items_two_test.append(xs_test)
  y_items_two_test.append(ys_test)
  z_items_two_test.append(zs_test)
  test_labels_two.append(test_label)

X_testing_two = pd.DataFrame()
  
# mean
X_testing_two['x_mean'] = pd.Series(x_items_two_test).apply(lambda x: x.mean())
X_testing_two['y_mean'] = pd.Series(y_items_two_test).apply(lambda x: x.mean())
X_testing_two['z_mean'] = pd.Series(z_items_two_test).apply(lambda x: x.mean())

# std dev
X_testing_two['x_std'] = pd.Series(x_items_two_test).apply(lambda x: x.std())
X_testing_two['y_std'] = pd.Series(y_items_two_test).apply(lambda x: x.std())
X_testing_two['z_std'] = pd.Series(z_items_two_test).apply(lambda x: x.std())

# avg absolute diff
X_testing_two['x_aad'] = pd.Series(x_items_two_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_testing_two['y_aad'] = pd.Series(y_items_two_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_testing_two['z_aad'] = pd.Series(z_items_two_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

# min
X_testing_two['x_min'] = pd.Series(x_items_two_test).apply(lambda x: x.min())
X_testing_two['y_min'] = pd.Series(y_items_two_test).apply(lambda x: x.min())
X_testing_two['z_min'] = pd.Series(z_items_two_test).apply(lambda x: x.min())

# max
X_testing_two['x_max'] = pd.Series(x_items_two_test).apply(lambda x: x.max())
X_testing_two['y_max'] = pd.Series(y_items_two_test).apply(lambda x: x.max())
X_testing_two['z_max'] = pd.Series(z_items_two_test).apply(lambda x: x.max())

# max-min diff
X_testing_two['x_maxmin_diff'] = X_testing_two['x_max'] - X_testing_two['x_min']
X_testing_two['y_maxmin_diff'] = X_testing_two['y_max'] - X_testing_two['y_min']
X_testing_two['z_maxmin_diff'] = X_testing_two['z_max'] - X_testing_two['z_min']

# median
X_testing_two['x_median'] = pd.Series(x_items_two_test).apply(lambda x: np.median(x))
X_testing_two['y_median'] = pd.Series(y_items_two_test).apply(lambda x: np.median(x))
X_testing_two['z_median'] = pd.Series(z_items_two_test).apply(lambda x: np.median(x))

# median abs dev 
X_testing_two['x_mad'] = pd.Series(x_items_two_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_testing_two['y_mad'] = pd.Series(y_items_two_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_testing_two['z_mad'] = pd.Series(z_items_two_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))

# interquartile range
X_testing_two['x_IQR'] = pd.Series(x_items_two_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_testing_two['y_IQR'] = pd.Series(y_items_two_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_testing_two['z_IQR'] = pd.Series(z_items_two_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

# negtive count
X_testing_two['x_neg_count'] = pd.Series(x_items_two_test).apply(lambda x: np.sum(x < 0))
X_testing_two['y_neg_count'] = pd.Series(y_items_two_test).apply(lambda x: np.sum(x < 0))
X_testing_two['z_neg_count'] = pd.Series(z_items_two_test).apply(lambda x: np.sum(x < 0))

# positive count
X_testing_two['x_pos_count'] = pd.Series(x_items_two_test).apply(lambda x: np.sum(x > 0))
X_testing_two['y_pos_count'] = pd.Series(y_items_two_test).apply(lambda x: np.sum(x > 0))
X_testing_two['z_pos_count'] = pd.Series(z_items_two_test).apply(lambda x: np.sum(x > 0))

# values above mean
X_testing_two['x_above_mean'] = pd.Series(x_items_two_test).apply(lambda x: np.sum(x > x.mean()))
X_testing_two['y_above_mean'] = pd.Series(y_items_two_test).apply(lambda x: np.sum(x > x.mean()))
X_testing_two['z_above_mean'] = pd.Series(z_items_two_test).apply(lambda x: np.sum(x > x.mean()))

# number of peaks
X_testing_two['x_peak_count'] = pd.Series(x_items_two_test).apply(lambda x: len(find_peaks(x)[0]))
X_testing_two['y_peak_count'] = pd.Series(y_items_two_test).apply(lambda x: len(find_peaks(x)[0]))
X_testing_two['z_peak_count'] = pd.Series(z_items_two_test).apply(lambda x: len(find_peaks(x)[0]))

# skewness
X_testing_two['x_skewness'] = pd.Series(x_items_two_test).apply(lambda x: stats.skew(x))
X_testing_two['y_skewness'] = pd.Series(y_items_two_test).apply(lambda x: stats.skew(x))
X_testing_two['z_skewness'] = pd.Series(z_items_two_test).apply(lambda x: stats.skew(x))

# kurtosis
X_testing_two['x_kurtosis'] = pd.Series(x_items_two_test).apply(lambda x: stats.kurtosis(x))
X_testing_two['y_kurtosis'] = pd.Series(y_items_two_test).apply(lambda x: stats.kurtosis(x))
X_testing_two['z_kurtosis'] = pd.Series(z_items_two_test).apply(lambda x: stats.kurtosis(x))

# energy
X_testing_two['x_energy'] = pd.Series(x_items_two_test).apply(lambda x: np.sum(x**2)/100)
X_testing_two['y_energy'] = pd.Series(y_items_two_test).apply(lambda x: np.sum(x**2)/100)
X_testing_two['z_energy'] = pd.Series(z_items_two_test).apply(lambda x: np.sum(x**2/100))

# avg resultant
X_testing_two['avg_result_accl'] = [i.mean() for i in ((pd.Series(x_items_two_test)**2 + pd.Series(y_items_two_test)**2 + pd.Series(z_items_two_test)**2)**0.5)]

# signal magnitude area
X_testing_two['sma'] =    pd.Series(x_items_two_test).apply(lambda x: np.sum(abs(x)/100)) + pd.Series(y_items_two_test).apply(lambda x: np.sum(abs(x)/100)) \
                  + pd.Series(z_items_two_test).apply(lambda x: np.sum(abs(x)/100))




# fft: chaning time domain signals to frequency domain
x_fft_two_test = pd.Series(x_items_two_test).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
y_fft_two_test = pd.Series(y_items_two_test).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
z_fft_two_test = pd.Series(z_items_two_test).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))

# Statistical Features on raw x, y and z in frequency domain
# FFT mean
X_testing_two['x_mean_fft'] = pd.Series(x_fft_two_test).apply(lambda x: x.mean())
X_testing_two['y_mean_fft'] = pd.Series(y_fft_two_test).apply(lambda x: x.mean())
X_testing_two['z_mean_fft'] = pd.Series(z_fft_two_test).apply(lambda x: x.mean())

# FFT std dev
X_testing_two['x_std_fft'] = pd.Series(x_fft_two_test).apply(lambda x: x.std())
X_testing_two['y_std_fft'] = pd.Series(y_fft_two_test).apply(lambda x: x.std())
X_testing_two['z_std_fft'] = pd.Series(z_fft_two_test).apply(lambda x: x.std())

# FFT avg absolute diff
X_testing_two['x_aad_fft'] = pd.Series(x_fft_two_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_testing_two['y_aad_fft'] = pd.Series(y_fft_two_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_testing_two['z_aad_fft'] = pd.Series(z_fft_two_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

# FFT min
X_testing_two['x_min_fft'] = pd.Series(x_fft_two_test).apply(lambda x: x.min())
X_testing_two['y_min_fft'] = pd.Series(y_fft_two_test).apply(lambda x: x.min())
X_testing_two['z_min_fft'] = pd.Series(z_fft_two_test).apply(lambda x: x.min())

# FFT max
X_testing_two['x_max_fft'] = pd.Series(x_fft_two_test).apply(lambda x: x.max())
X_testing_two['y_max_fft'] = pd.Series(y_fft_two_test).apply(lambda x: x.max())
X_testing_two['z_max_fft'] = pd.Series(z_fft_two_test).apply(lambda x: x.max())

# FFT max-min diff
X_testing_two['x_maxmin_diff_fft'] = X_testing_two['x_max_fft'] - X_testing_two['x_min_fft']
X_testing_two['y_maxmin_diff_fft'] = X_testing_two['y_max_fft'] - X_testing_two['y_min_fft']
X_testing_two['z_maxmin_diff_fft'] = X_testing_two['z_max_fft'] - X_testing_two['z_min_fft']

# FFT median
X_testing_two['x_median_fft'] = pd.Series(x_fft_two_test).apply(lambda x: np.median(x))
X_testing_two['y_median_fft'] = pd.Series(y_fft_two_test).apply(lambda x: np.median(x))
X_testing_two['z_median_fft'] = pd.Series(z_fft_two_test).apply(lambda x: np.median(x))

# FFT median abs dev 
X_testing_two['x_mad_fft'] = pd.Series(x_fft_two_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_testing_two['y_mad_fft'] = pd.Series(y_fft_two_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_testing_two['z_mad_fft'] = pd.Series(z_fft_two_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))

# FFT Interquartile range
X_testing_two['x_IQR_fft'] = pd.Series(x_fft_two_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_testing_two['y_IQR_fft'] = pd.Series(y_fft_two_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_testing_two['z_IQR_fft'] = pd.Series(z_fft_two_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

# FFT values above mean
X_testing_two['x_above_mean_fft'] = pd.Series(x_fft_two_test).apply(lambda x: np.sum(x > x.mean()))
X_testing_two['y_above_mean_fft'] = pd.Series(y_fft_two_test).apply(lambda x: np.sum(x > x.mean()))
X_testing_two['z_above_mean_fft'] = pd.Series(z_fft_two_test).apply(lambda x: np.sum(x > x.mean()))

# FFT number of peaks
X_testing_two['x_peak_count_fft'] = pd.Series(x_fft_two_test).apply(lambda x: len(find_peaks(x)[0]))
X_testing_two['y_peak_count_fft'] = pd.Series(y_fft_two_test).apply(lambda x: len(find_peaks(x)[0]))
X_testing_two['z_peak_count_fft'] = pd.Series(z_fft_two_test).apply(lambda x: len(find_peaks(x)[0]))

# FFT skewness
X_testing_two['x_skewness_fft'] = pd.Series(x_fft_two_test).apply(lambda x: stats.skew(x))
X_testing_two['y_skewness_fft'] = pd.Series(y_fft_two_test).apply(lambda x: stats.skew(x))
X_testing_two['z_skewness_fft'] = pd.Series(z_fft_two_test).apply(lambda x: stats.skew(x))

# FFT kurtosis
X_testing_two['x_kurtosis_fft'] = pd.Series(x_fft_two_test).apply(lambda x: stats.kurtosis(x))
X_testing_two['y_kurtosis_fft'] = pd.Series(y_fft_two_test).apply(lambda x: stats.kurtosis(x))
X_testing_two['z_kurtosis_fft'] = pd.Series(z_fft_two_test).apply(lambda x: stats.kurtosis(x))

# FFT energy
X_testing_two['x_energy_fft'] = pd.Series(x_fft_two_test).apply(lambda x: np.sum(x**2)/50)
X_testing_two['y_energy_fft'] = pd.Series(y_fft_two_test).apply(lambda x: np.sum(x**2)/50)
X_testing_two['z_energy_fft'] = pd.Series(z_fft_two_test).apply(lambda x: np.sum(x**2/50))

# FFT avg resultant
X_testing_two['avg_result_accl_fft'] = [i.mean() for i in ((pd.Series(x_fft_two_test)**2 + pd.Series(y_fft_two_test)**2 + pd.Series(z_fft_two_test)**2)**0.5)]

# FFT Signal magnitude area
X_testing_two['sma_fft'] = pd.Series(x_fft_two_test).apply(lambda x: np.sum(abs(x)/50)) + pd.Series(y_fft_two_test).apply(lambda x: np.sum(abs(x)/50)) \
                     + pd.Series(z_fft_two_test).apply(lambda x: np.sum(abs(x)/50))


# calculating max & min indices

# index of max value in time domain
X_testing_two['x_argmax'] = pd.Series(x_items_two_test).apply(lambda x: np.argmax(x))
X_testing_two['y_argmax'] = pd.Series(y_items_two_test).apply(lambda x: np.argmax(x))
X_testing_two['z_argmax'] = pd.Series(z_items_two_test).apply(lambda x: np.argmax(x))

# index of min value in time domain
X_testing_two['x_argmin'] = pd.Series(x_items_two_test).apply(lambda x: np.argmin(x))
X_testing_two['y_argmin'] = pd.Series(y_items_two_test).apply(lambda x: np.argmin(x))
X_testing_two['z_argmin'] = pd.Series(z_items_two_test).apply(lambda x: np.argmin(x))

# absolute difference between above indices
X_testing_two['x_arg_diff'] = abs(X_testing_two['x_argmax'] - X_testing_two['x_argmin'])
X_testing_two['y_arg_diff'] = abs(X_testing_two['y_argmax'] - X_testing_two['y_argmin'])
X_testing_two['z_arg_diff'] = abs(X_testing_two['z_argmax'] - X_testing_two['z_argmin'])

# index of max value in frequency domain
X_testing_two['x_argmax_fft'] = pd.Series(x_fft_two_test).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
X_testing_two['y_argmax_fft'] = pd.Series(y_fft_two_test).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
X_testing_two['z_argmax_fft'] = pd.Series(z_fft_two_test).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))

# index of min value in frequency domain
X_testing_two['x_argmin_fft'] = pd.Series(x_fft_two_test).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
X_testing_two['y_argmin_fft'] = pd.Series(y_fft_two_test).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
X_testing_two['z_argmin_fft'] = pd.Series(z_fft_two_test).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))

# absolute difference between above indices
X_testing_two['x_arg_diff_fft'] = abs(X_testing_two['x_argmax_fft'] - X_testing_two['x_argmin_fft'])
X_testing_two['y_arg_diff_fft'] = abs(X_testing_two['y_argmax_fft'] - X_testing_two['y_argmin_fft'])
X_testing_two['z_arg_diff_fft'] = abs(X_testing_two['z_argmax_fft'] - X_testing_two['z_argmin_fft'])


y_train_two = np.array(train_labels_two)
y_test_two = np.array(test_labels_two)

# model for User 8
rf_two = RandomForestClassifier(random_state = 21)
k=5
folds_two = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
scores_two= cross_val_score(rf_two, X_training_two, y_train_two, cv=folds_two, scoring='accuracy')

rf_two.fit(X_training_two, y_train_two)
y_pred_two = rf_two.predict(X_testing_two)
accuracy_two = accuracy_score(y_test_two, y_pred_two)
print("Accuracy of model trained on WISDM User 8:", accuracy_two)
print("Cross validation score:", scores_two)
print("Cross validation mean:", np.mean(scores_two))
print(classification_report(y_test_two, y_pred_two))


labels = ['Downstairs', 'Jogging', 'Sitting', 'Standing', 'Upstairs', 'Walking']
confusion_matrix_two = confusion_matrix(y_test_two, y_pred_two)
sns.heatmap(confusion_matrix_two, xticklabels=labels, yticklabels=labels, annot=True,linewidths = 0.1, fmt="d", cmap = 'YlGnBu')
plt.title("Confusion matrix", fontsize = 15)
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()


# using model of User 33 on User 8
y_pred_three = rf.predict(X_testing_two)
accuracy_three = accuracy_score(y_test_two, y_pred_three)
print("Accuracy of predicting User 8 data with model for User 33:", accuracy_three)
print(classification_report(y_test_two, y_pred_three))


labels = ['Downstairs', 'Jogging', 'Sitting', 'Standing', 'Upstairs', 'Walking']
confusion_matrix_three = confusion_matrix(y_test_two, y_pred_three)
sns.heatmap(confusion_matrix_three, xticklabels=labels, yticklabels=labels, annot=True,linewidths = 0.1, fmt="d", cmap = 'YlGnBu')
plt.title("Confusion matrix", fontsize = 15)
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()


# using model of User 8 on User 33
y_pred_four = rf_two.predict(X_testing)
accuracy_four = accuracy_score(y_test, y_pred_four)
print("Accuracy of predicting User 33 data with model for User 8:", accuracy_four)
print(classification_report(y_test, y_pred_four))


labels = ['Downstairs', 'Jogging', 'Sitting', 'Standing', 'Upstairs', 'Walking']
confusion_matrix_four = confusion_matrix(y_test, y_pred_four)
sns.heatmap(confusion_matrix_four, xticklabels=labels, yticklabels=labels, annot=True,linewidths = 0.1, fmt="d", cmap = 'YlGnBu')
plt.title("Confusion matrix", fontsize = 15)
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()







