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
har_df = pd.read_csv('WISDM_ar_v1.1_raw.txt', sep=',', on_bad_lines='skip', header = None, names = col)


har_df = har_df.dropna()
har_df.shape

har_df['z-axis'] = har_df['z-axis'].str.replace(';', '')
har_df['z-axis'] = har_df['z-axis'].apply(lambda x:float(x))


user_one = har_df[har_df['user'] == 33]

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

x_list = []
y_list = []
z_list = []
train_labels = []

window = 100
step = 50


for i in range(0, train_df.shape[0] - window, step):
  xs = train_df['x-axis'].values[i: i + 100]
  ys = train_df['y-axis'].values[i: i + 100]
  zs = train_df['z-axis'].values[i: i + 100]
  label = train_df['activity'][i: i + 100].mode()[0]
  
  x_list.append(xs)
  y_list.append(ys)
  z_list.append(zs)
  train_labels.append(label)


X_train = pd.DataFrame()
  
# mean
X_train['x_mean'] = pd.Series(x_list).apply(lambda x: x.mean())
X_train['y_mean'] = pd.Series(y_list).apply(lambda x: x.mean())
X_train['z_mean'] = pd.Series(z_list).apply(lambda x: x.mean())

# std dev
X_train['x_std'] = pd.Series(x_list).apply(lambda x: x.std())
X_train['y_std'] = pd.Series(y_list).apply(lambda x: x.std())
X_train['z_std'] = pd.Series(z_list).apply(lambda x: x.std())

# avg absolute diff
X_train['x_aad'] = pd.Series(x_list).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_train['y_aad'] = pd.Series(y_list).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_train['z_aad'] = pd.Series(z_list).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

# min
X_train['x_min'] = pd.Series(x_list).apply(lambda x: x.min())
X_train['y_min'] = pd.Series(y_list).apply(lambda x: x.min())
X_train['z_min'] = pd.Series(z_list).apply(lambda x: x.min())

# max
X_train['x_max'] = pd.Series(x_list).apply(lambda x: x.max())
X_train['y_max'] = pd.Series(y_list).apply(lambda x: x.max())
X_train['z_max'] = pd.Series(z_list).apply(lambda x: x.max())

# max-min diff
X_train['x_maxmin_diff'] = X_train['x_max'] - X_train['x_min']
X_train['y_maxmin_diff'] = X_train['y_max'] - X_train['y_min']
X_train['z_maxmin_diff'] = X_train['z_max'] - X_train['z_min']

# median
X_train['x_median'] = pd.Series(x_list).apply(lambda x: np.median(x))
X_train['y_median'] = pd.Series(y_list).apply(lambda x: np.median(x))
X_train['z_median'] = pd.Series(z_list).apply(lambda x: np.median(x))

# median abs dev 
X_train['x_mad'] = pd.Series(x_list).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_train['y_mad'] = pd.Series(y_list).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_train['z_mad'] = pd.Series(z_list).apply(lambda x: np.median(np.absolute(x - np.median(x))))

# interquartile range
X_train['x_IQR'] = pd.Series(x_list).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_train['y_IQR'] = pd.Series(y_list).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_train['z_IQR'] = pd.Series(z_list).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

# negtive count
X_train['x_neg_count'] = pd.Series(x_list).apply(lambda x: np.sum(x < 0))
X_train['y_neg_count'] = pd.Series(y_list).apply(lambda x: np.sum(x < 0))
X_train['z_neg_count'] = pd.Series(z_list).apply(lambda x: np.sum(x < 0))

# positive count
X_train['x_pos_count'] = pd.Series(x_list).apply(lambda x: np.sum(x > 0))
X_train['y_pos_count'] = pd.Series(y_list).apply(lambda x: np.sum(x > 0))
X_train['z_pos_count'] = pd.Series(z_list).apply(lambda x: np.sum(x > 0))

# values above mean
X_train['x_above_mean'] = pd.Series(x_list).apply(lambda x: np.sum(x > x.mean()))
X_train['y_above_mean'] = pd.Series(y_list).apply(lambda x: np.sum(x > x.mean()))
X_train['z_above_mean'] = pd.Series(z_list).apply(lambda x: np.sum(x > x.mean()))

# number of peaks
X_train['x_peak_count'] = pd.Series(x_list).apply(lambda x: len(find_peaks(x)[0]))
X_train['y_peak_count'] = pd.Series(y_list).apply(lambda x: len(find_peaks(x)[0]))
X_train['z_peak_count'] = pd.Series(z_list).apply(lambda x: len(find_peaks(x)[0]))

# skewness
X_train['x_skewness'] = pd.Series(x_list).apply(lambda x: stats.skew(x))
X_train['y_skewness'] = pd.Series(y_list).apply(lambda x: stats.skew(x))
X_train['z_skewness'] = pd.Series(z_list).apply(lambda x: stats.skew(x))

# kurtosis
X_train['x_kurtosis'] = pd.Series(x_list).apply(lambda x: stats.kurtosis(x))
X_train['y_kurtosis'] = pd.Series(y_list).apply(lambda x: stats.kurtosis(x))
X_train['z_kurtosis'] = pd.Series(z_list).apply(lambda x: stats.kurtosis(x))

# energy
X_train['x_energy'] = pd.Series(x_list).apply(lambda x: np.sum(x**2)/100)
X_train['y_energy'] = pd.Series(y_list).apply(lambda x: np.sum(x**2)/100)
X_train['z_energy'] = pd.Series(z_list).apply(lambda x: np.sum(x**2/100))

# avg resultant
X_train['avg_result_accl'] = [i.mean() for i in ((pd.Series(x_list)**2 + pd.Series(y_list)**2 + pd.Series(z_list)**2)**0.5)]

# signal magnitude area
X_train['sma'] =    pd.Series(x_list).apply(lambda x: np.sum(abs(x)/100)) + pd.Series(y_list).apply(lambda x: np.sum(abs(x)/100)) \
                  + pd.Series(z_list).apply(lambda x: np.sum(abs(x)/100))



# fft: chaning time domain signals to frequency domain
x_fft = pd.Series(x_list).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
y_fft = pd.Series(y_list).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
z_fft = pd.Series(z_list).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))

# Statistical Features on raw x, y and z in frequency domain
# FFT mean
X_train['x_mean_fft'] = pd.Series(x_fft).apply(lambda x: x.mean())
X_train['y_mean_fft'] = pd.Series(y_fft).apply(lambda x: x.mean())
X_train['z_mean_fft'] = pd.Series(z_fft).apply(lambda x: x.mean())

# FFT std dev
X_train['x_std_fft'] = pd.Series(x_fft).apply(lambda x: x.std())
X_train['y_std_fft'] = pd.Series(y_fft).apply(lambda x: x.std())
X_train['z_std_fft'] = pd.Series(z_fft).apply(lambda x: x.std())

# FFT avg absolute diff
X_train['x_aad_fft'] = pd.Series(x_fft).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_train['y_aad_fft'] = pd.Series(y_fft).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_train['z_aad_fft'] = pd.Series(z_fft).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

# FFT min
X_train['x_min_fft'] = pd.Series(x_fft).apply(lambda x: x.min())
X_train['y_min_fft'] = pd.Series(y_fft).apply(lambda x: x.min())
X_train['z_min_fft'] = pd.Series(z_fft).apply(lambda x: x.min())

# FFT max
X_train['x_max_fft'] = pd.Series(x_fft).apply(lambda x: x.max())
X_train['y_max_fft'] = pd.Series(y_fft).apply(lambda x: x.max())
X_train['z_max_fft'] = pd.Series(z_fft).apply(lambda x: x.max())

# FFT max-min diff
X_train['x_maxmin_diff_fft'] = X_train['x_max_fft'] - X_train['x_min_fft']
X_train['y_maxmin_diff_fft'] = X_train['y_max_fft'] - X_train['y_min_fft']
X_train['z_maxmin_diff_fft'] = X_train['z_max_fft'] - X_train['z_min_fft']

# FFT median
X_train['x_median_fft'] = pd.Series(x_fft).apply(lambda x: np.median(x))
X_train['y_median_fft'] = pd.Series(y_fft).apply(lambda x: np.median(x))
X_train['z_median_fft'] = pd.Series(z_fft).apply(lambda x: np.median(x))

# FFT median abs dev 
X_train['x_mad_fft'] = pd.Series(x_fft).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_train['y_mad_fft'] = pd.Series(y_fft).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_train['z_mad_fft'] = pd.Series(z_fft).apply(lambda x: np.median(np.absolute(x - np.median(x))))

# FFT Interquartile range
X_train['x_IQR_fft'] = pd.Series(x_fft).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_train['y_IQR_fft'] = pd.Series(y_fft).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_train['z_IQR_fft'] = pd.Series(z_fft).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

# FFT values above mean
X_train['x_above_mean_fft'] = pd.Series(x_fft).apply(lambda x: np.sum(x > x.mean()))
X_train['y_above_mean_fft'] = pd.Series(y_fft).apply(lambda x: np.sum(x > x.mean()))
X_train['z_above_mean_fft'] = pd.Series(z_fft).apply(lambda x: np.sum(x > x.mean()))

# FFT number of peaks
X_train['x_peak_count_fft'] = pd.Series(x_fft).apply(lambda x: len(find_peaks(x)[0]))
X_train['y_peak_count_fft'] = pd.Series(y_fft).apply(lambda x: len(find_peaks(x)[0]))
X_train['z_peak_count_fft'] = pd.Series(z_fft).apply(lambda x: len(find_peaks(x)[0]))

# FFT skewness
X_train['x_skewness_fft'] = pd.Series(x_fft).apply(lambda x: stats.skew(x))
X_train['y_skewness_fft'] = pd.Series(y_fft).apply(lambda x: stats.skew(x))
X_train['z_skewness_fft'] = pd.Series(z_fft).apply(lambda x: stats.skew(x))

# FFT kurtosis
X_train['x_kurtosis_fft'] = pd.Series(x_fft).apply(lambda x: stats.kurtosis(x))
X_train['y_kurtosis_fft'] = pd.Series(y_fft).apply(lambda x: stats.kurtosis(x))
X_train['z_kurtosis_fft'] = pd.Series(z_fft).apply(lambda x: stats.kurtosis(x))

# FFT energy
X_train['x_energy_fft'] = pd.Series(x_fft).apply(lambda x: np.sum(x**2)/50)
X_train['y_energy_fft'] = pd.Series(y_fft).apply(lambda x: np.sum(x**2)/50)
X_train['z_energy_fft'] = pd.Series(z_fft).apply(lambda x: np.sum(x**2/50))

# FFT avg resultant
X_train['avg_result_accl_fft'] = [i.mean() for i in ((pd.Series(x_fft)**2 + pd.Series(y_fft)**2 + pd.Series(z_fft)**2)**0.5)]

# FFT Signal magnitude area
X_train['sma_fft'] = pd.Series(x_fft).apply(lambda x: np.sum(abs(x)/50)) + pd.Series(y_fft).apply(lambda x: np.sum(abs(x)/50)) \
                     + pd.Series(z_fft).apply(lambda x: np.sum(abs(x)/50))


# calculating max & min indices

# index of max value in time domain
X_train['x_argmax'] = pd.Series(x_list).apply(lambda x: np.argmax(x))
X_train['y_argmax'] = pd.Series(y_list).apply(lambda x: np.argmax(x))
X_train['z_argmax'] = pd.Series(z_list).apply(lambda x: np.argmax(x))

# index of min value in time domain
X_train['x_argmin'] = pd.Series(x_list).apply(lambda x: np.argmin(x))
X_train['y_argmin'] = pd.Series(y_list).apply(lambda x: np.argmin(x))
X_train['z_argmin'] = pd.Series(z_list).apply(lambda x: np.argmin(x))

# absolute difference between above indices
X_train['x_arg_diff'] = abs(X_train['x_argmax'] - X_train['x_argmin'])
X_train['y_arg_diff'] = abs(X_train['y_argmax'] - X_train['y_argmin'])
X_train['z_arg_diff'] = abs(X_train['z_argmax'] - X_train['z_argmin'])

# index of max value in frequency domain
X_train['x_argmax_fft'] = pd.Series(x_fft).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
X_train['y_argmax_fft'] = pd.Series(y_fft).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
X_train['z_argmax_fft'] = pd.Series(z_fft).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))

# index of min value in frequency domain
X_train['x_argmin_fft'] = pd.Series(x_fft).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
X_train['y_argmin_fft'] = pd.Series(y_fft).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
X_train['z_argmin_fft'] = pd.Series(z_fft).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))

# absolute difference between above indices
X_train['x_arg_diff_fft'] = abs(X_train['x_argmax_fft'] - X_train['x_argmin_fft'])
X_train['y_arg_diff_fft'] = abs(X_train['y_argmax_fft'] - X_train['y_argmin_fft'])
X_train['z_arg_diff_fft'] = abs(X_train['z_argmax_fft'] - X_train['z_argmin_fft'])


# do the same for test data

x_list_test = []
y_list_test = []
z_list_test = []
test_labels = []

window = 100
step = 50


for i in range(0, test_df.shape[0] - window, step):
  xs_test = test_df['x-axis'].values[i: i + 100]
  ys_test = test_df['y-axis'].values[i: i + 100]
  zs_test = test_df['z-axis'].values[i: i + 100]
  test_label = test_df['activity'][i: i + 100].mode()[0]
  
  x_list_test.append(xs_test)
  y_list_test.append(ys_test)
  z_list_test.append(zs_test)
  test_labels.append(test_label)

X_test = pd.DataFrame()
  
# mean
X_test['x_mean'] = pd.Series(x_list_test).apply(lambda x: x.mean())
X_test['y_mean'] = pd.Series(y_list_test).apply(lambda x: x.mean())
X_test['z_mean'] = pd.Series(z_list_test).apply(lambda x: x.mean())

# std dev
X_test['x_std'] = pd.Series(x_list_test).apply(lambda x: x.std())
X_test['y_std'] = pd.Series(y_list_test).apply(lambda x: x.std())
X_test['z_std'] = pd.Series(z_list_test).apply(lambda x: x.std())

# avg absolute diff
X_test['x_aad'] = pd.Series(x_list_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_test['y_aad'] = pd.Series(y_list_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_test['z_aad'] = pd.Series(z_list_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

# min
X_test['x_min'] = pd.Series(x_list_test).apply(lambda x: x.min())
X_test['y_min'] = pd.Series(y_list_test).apply(lambda x: x.min())
X_test['z_min'] = pd.Series(z_list_test).apply(lambda x: x.min())

# max
X_test['x_max'] = pd.Series(x_list_test).apply(lambda x: x.max())
X_test['y_max'] = pd.Series(y_list_test).apply(lambda x: x.max())
X_test['z_max'] = pd.Series(z_list_test).apply(lambda x: x.max())

# max-min diff
X_test['x_maxmin_diff'] = X_test['x_max'] - X_test['x_min']
X_test['y_maxmin_diff'] = X_test['y_max'] - X_test['y_min']
X_test['z_maxmin_diff'] = X_test['z_max'] - X_test['z_min']

# median
X_test['x_median'] = pd.Series(x_list_test).apply(lambda x: np.median(x))
X_test['y_median'] = pd.Series(y_list_test).apply(lambda x: np.median(x))
X_test['z_median'] = pd.Series(z_list_test).apply(lambda x: np.median(x))

# median abs dev 
X_test['x_mad'] = pd.Series(x_list_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_test['y_mad'] = pd.Series(y_list_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_test['z_mad'] = pd.Series(z_list_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))

# interquartile range
X_test['x_IQR'] = pd.Series(x_list_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_test['y_IQR'] = pd.Series(y_list_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_test['z_IQR'] = pd.Series(z_list_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

# negtive count
X_test['x_neg_count'] = pd.Series(x_list_test).apply(lambda x: np.sum(x < 0))
X_test['y_neg_count'] = pd.Series(y_list_test).apply(lambda x: np.sum(x < 0))
X_test['z_neg_count'] = pd.Series(z_list_test).apply(lambda x: np.sum(x < 0))

# positive count
X_test['x_pos_count'] = pd.Series(x_list_test).apply(lambda x: np.sum(x > 0))
X_test['y_pos_count'] = pd.Series(y_list_test).apply(lambda x: np.sum(x > 0))
X_test['z_pos_count'] = pd.Series(z_list_test).apply(lambda x: np.sum(x > 0))

# values above mean
X_test['x_above_mean'] = pd.Series(x_list_test).apply(lambda x: np.sum(x > x.mean()))
X_test['y_above_mean'] = pd.Series(y_list_test).apply(lambda x: np.sum(x > x.mean()))
X_test['z_above_mean'] = pd.Series(z_list_test).apply(lambda x: np.sum(x > x.mean()))

# number of peaks
X_test['x_peak_count'] = pd.Series(x_list_test).apply(lambda x: len(find_peaks(x)[0]))
X_test['y_peak_count'] = pd.Series(y_list_test).apply(lambda x: len(find_peaks(x)[0]))
X_test['z_peak_count'] = pd.Series(z_list_test).apply(lambda x: len(find_peaks(x)[0]))

# skewness
X_test['x_skewness'] = pd.Series(x_list_test).apply(lambda x: stats.skew(x))
X_test['y_skewness'] = pd.Series(y_list_test).apply(lambda x: stats.skew(x))
X_test['z_skewness'] = pd.Series(z_list_test).apply(lambda x: stats.skew(x))

# kurtosis
X_test['x_kurtosis'] = pd.Series(x_list_test).apply(lambda x: stats.kurtosis(x))
X_test['y_kurtosis'] = pd.Series(y_list_test).apply(lambda x: stats.kurtosis(x))
X_test['z_kurtosis'] = pd.Series(z_list_test).apply(lambda x: stats.kurtosis(x))

# energy
X_test['x_energy'] = pd.Series(x_list_test).apply(lambda x: np.sum(x**2)/100)
X_test['y_energy'] = pd.Series(y_list_test).apply(lambda x: np.sum(x**2)/100)
X_test['z_energy'] = pd.Series(z_list_test).apply(lambda x: np.sum(x**2/100))

# avg resultant
X_test['avg_result_accl'] = [i.mean() for i in ((pd.Series(x_list_test)**2 + pd.Series(y_list_test)**2 + pd.Series(z_list_test)**2)**0.5)]

# signal magnitude area
X_test['sma'] =    pd.Series(x_list_test).apply(lambda x: np.sum(abs(x)/100)) + pd.Series(y_list_test).apply(lambda x: np.sum(abs(x)/100)) \
                  + pd.Series(z_list_test).apply(lambda x: np.sum(abs(x)/100))




# fft: chaning time domain signals to frequency domain
x_fft_test = pd.Series(x_list_test).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
y_fft_test = pd.Series(y_list_test).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
z_fft_test = pd.Series(z_list_test).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))

# Statistical Features on raw x, y and z in frequency domain
# FFT mean
X_test['x_mean_fft'] = pd.Series(x_fft_test).apply(lambda x: x.mean())
X_test['y_mean_fft'] = pd.Series(y_fft_test).apply(lambda x: x.mean())
X_test['z_mean_fft'] = pd.Series(z_fft_test).apply(lambda x: x.mean())

# FFT std dev
X_test['x_std_fft'] = pd.Series(x_fft_test).apply(lambda x: x.std())
X_test['y_std_fft'] = pd.Series(y_fft_test).apply(lambda x: x.std())
X_test['z_std_fft'] = pd.Series(z_fft_test).apply(lambda x: x.std())

# FFT avg absolute diff
X_test['x_aad_fft'] = pd.Series(x_fft_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_test['y_aad_fft'] = pd.Series(y_fft_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_test['z_aad_fft'] = pd.Series(z_fft_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

# FFT min
X_test['x_min_fft'] = pd.Series(x_fft_test).apply(lambda x: x.min())
X_test['y_min_fft'] = pd.Series(y_fft_test).apply(lambda x: x.min())
X_test['z_min_fft'] = pd.Series(z_fft_test).apply(lambda x: x.min())

# FFT max
X_test['x_max_fft'] = pd.Series(x_fft_test).apply(lambda x: x.max())
X_test['y_max_fft'] = pd.Series(y_fft_test).apply(lambda x: x.max())
X_test['z_max_fft'] = pd.Series(z_fft_test).apply(lambda x: x.max())

# FFT max-min diff
X_test['x_maxmin_diff_fft'] = X_test['x_max_fft'] - X_test['x_min_fft']
X_test['y_maxmin_diff_fft'] = X_test['y_max_fft'] - X_test['y_min_fft']
X_test['z_maxmin_diff_fft'] = X_test['z_max_fft'] - X_test['z_min_fft']

# FFT median
X_test['x_median_fft'] = pd.Series(x_fft_test).apply(lambda x: np.median(x))
X_test['y_median_fft'] = pd.Series(y_fft_test).apply(lambda x: np.median(x))
X_test['z_median_fft'] = pd.Series(z_fft_test).apply(lambda x: np.median(x))

# FFT median abs dev 
X_test['x_mad_fft'] = pd.Series(x_fft_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_test['y_mad_fft'] = pd.Series(y_fft_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_test['z_mad_fft'] = pd.Series(z_fft_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))

# FFT Interquartile range
X_test['x_IQR_fft'] = pd.Series(x_fft_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_test['y_IQR_fft'] = pd.Series(y_fft_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_test['z_IQR_fft'] = pd.Series(z_fft_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

# FFT values above mean
X_test['x_above_mean_fft'] = pd.Series(x_fft_test).apply(lambda x: np.sum(x > x.mean()))
X_test['y_above_mean_fft'] = pd.Series(y_fft_test).apply(lambda x: np.sum(x > x.mean()))
X_test['z_above_mean_fft'] = pd.Series(z_fft_test).apply(lambda x: np.sum(x > x.mean()))

# FFT number of peaks
X_test['x_peak_count_fft'] = pd.Series(x_fft_test).apply(lambda x: len(find_peaks(x)[0]))
X_test['y_peak_count_fft'] = pd.Series(y_fft_test).apply(lambda x: len(find_peaks(x)[0]))
X_test['z_peak_count_fft'] = pd.Series(z_fft_test).apply(lambda x: len(find_peaks(x)[0]))

# FFT skewness
X_test['x_skewness_fft'] = pd.Series(x_fft_test).apply(lambda x: stats.skew(x))
X_test['y_skewness_fft'] = pd.Series(y_fft_test).apply(lambda x: stats.skew(x))
X_test['z_skewness_fft'] = pd.Series(z_fft_test).apply(lambda x: stats.skew(x))

# FFT kurtosis
X_test['x_kurtosis_fft'] = pd.Series(x_fft_test).apply(lambda x: stats.kurtosis(x))
X_test['y_kurtosis_fft'] = pd.Series(y_fft_test).apply(lambda x: stats.kurtosis(x))
X_test['z_kurtosis_fft'] = pd.Series(z_fft_test).apply(lambda x: stats.kurtosis(x))

# FFT energy
X_test['x_energy_fft'] = pd.Series(x_fft_test).apply(lambda x: np.sum(x**2)/50)
X_test['y_energy_fft'] = pd.Series(y_fft_test).apply(lambda x: np.sum(x**2)/50)
X_test['z_energy_fft'] = pd.Series(z_fft_test).apply(lambda x: np.sum(x**2/50))

# FFT avg resultant
X_test['avg_result_accl_fft'] = [i.mean() for i in ((pd.Series(x_fft_test)**2 + pd.Series(y_fft_test)**2 + pd.Series(z_fft_test)**2)**0.5)]

# FFT Signal magnitude area
X_test['sma_fft'] = pd.Series(x_fft_test).apply(lambda x: np.sum(abs(x)/50)) + pd.Series(y_fft_test).apply(lambda x: np.sum(abs(x)/50)) \
                     + pd.Series(z_fft_test).apply(lambda x: np.sum(abs(x)/50))


# calculating max & min indices

# index of max value in time domain
X_test['x_argmax'] = pd.Series(x_list_test).apply(lambda x: np.argmax(x))
X_test['y_argmax'] = pd.Series(y_list_test).apply(lambda x: np.argmax(x))
X_test['z_argmax'] = pd.Series(z_list_test).apply(lambda x: np.argmax(x))

# index of min value in time domain
X_test['x_argmin'] = pd.Series(x_list_test).apply(lambda x: np.argmin(x))
X_test['y_argmin'] = pd.Series(y_list_test).apply(lambda x: np.argmin(x))
X_test['z_argmin'] = pd.Series(z_list_test).apply(lambda x: np.argmin(x))

# absolute difference between above indices
X_test['x_arg_diff'] = abs(X_test['x_argmax'] - X_test['x_argmin'])
X_test['y_arg_diff'] = abs(X_test['y_argmax'] - X_test['y_argmin'])
X_test['z_arg_diff'] = abs(X_test['z_argmax'] - X_test['z_argmin'])

# index of max value in frequency domain
X_test['x_argmax_fft'] = pd.Series(x_fft_test).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
X_test['y_argmax_fft'] = pd.Series(y_fft_test).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
X_test['z_argmax_fft'] = pd.Series(z_fft_test).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))

# index of min value in frequency domain
X_test['x_argmin_fft'] = pd.Series(x_fft_test).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
X_test['y_argmin_fft'] = pd.Series(y_fft_test).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
X_test['z_argmin_fft'] = pd.Series(z_fft_test).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))

# absolute difference between above indices
X_test['x_arg_diff_fft'] = abs(X_test['x_argmax_fft'] - X_test['x_argmin_fft'])
X_test['y_arg_diff_fft'] = abs(X_test['y_argmax_fft'] - X_test['y_argmin_fft'])
X_test['z_arg_diff_fft'] = abs(X_test['z_argmax_fft'] - X_test['z_argmin_fft'])


y_train = np.array(train_labels)
y_test = np.array(test_labels)


# model for User 33
rf = RandomForestClassifier(random_state = 21)
k=5
folds = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
scores = cross_val_score(rf, X_train, y_train, cv=folds, scoring='accuracy')

rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
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



user_two = har_df[har_df['user'] == 8]

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

x_list_two = []
y_list_two = []
z_list_two = []
train_labels_two = []

window = 100
step = 50


for i in range(0, train_df_two.shape[0] - window, step):
  xs = train_df_two['x-axis'].values[i: i + 100]
  ys = train_df_two['y-axis'].values[i: i + 100]
  zs = train_df_two['z-axis'].values[i: i + 100]
  label = train_df_two['activity'][i: i + 100].mode()[0]
  
  x_list_two.append(xs)
  y_list_two.append(ys)
  z_list_two.append(zs)
  train_labels_two.append(label)


X_train_two = pd.DataFrame()
  
# mean
X_train_two['x_mean'] = pd.Series(x_list_two).apply(lambda x: x.mean())
X_train_two['y_mean'] = pd.Series(y_list_two).apply(lambda x: x.mean())
X_train_two['z_mean'] = pd.Series(z_list_two).apply(lambda x: x.mean())

# std dev
X_train_two['x_std'] = pd.Series(x_list_two).apply(lambda x: x.std())
X_train_two['y_std'] = pd.Series(y_list_two).apply(lambda x: x.std())
X_train_two['z_std'] = pd.Series(z_list_two).apply(lambda x: x.std())

# avg absolute diff
X_train_two['x_aad'] = pd.Series(x_list_two).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_train_two['y_aad'] = pd.Series(y_list_two).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_train_two['z_aad'] = pd.Series(z_list_two).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

# min
X_train_two['x_min'] = pd.Series(x_list_two).apply(lambda x: x.min())
X_train_two['y_min'] = pd.Series(y_list_two).apply(lambda x: x.min())
X_train_two['z_min'] = pd.Series(z_list_two).apply(lambda x: x.min())

# max
X_train_two['x_max'] = pd.Series(x_list_two).apply(lambda x: x.max())
X_train_two['y_max'] = pd.Series(y_list_two).apply(lambda x: x.max())
X_train_two['z_max'] = pd.Series(z_list_two).apply(lambda x: x.max())

# max-min diff
X_train_two['x_maxmin_diff'] = X_train_two['x_max'] - X_train_two['x_min']
X_train_two['y_maxmin_diff'] = X_train_two['y_max'] - X_train_two['y_min']
X_train_two['z_maxmin_diff'] = X_train_two['z_max'] - X_train_two['z_min']

# median
X_train_two['x_median'] = pd.Series(x_list_two).apply(lambda x: np.median(x))
X_train_two['y_median'] = pd.Series(y_list_two).apply(lambda x: np.median(x))
X_train_two['z_median'] = pd.Series(z_list_two).apply(lambda x: np.median(x))

# median abs dev 
X_train_two['x_mad'] = pd.Series(x_list_two).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_train_two['y_mad'] = pd.Series(y_list_two).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_train_two['z_mad'] = pd.Series(z_list_two).apply(lambda x: np.median(np.absolute(x - np.median(x))))

# interquartile range
X_train_two['x_IQR'] = pd.Series(x_list_two).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_train_two['y_IQR'] = pd.Series(y_list_two).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_train_two['z_IQR'] = pd.Series(z_list_two).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

# negtive count
X_train_two['x_neg_count'] = pd.Series(x_list_two).apply(lambda x: np.sum(x < 0))
X_train_two['y_neg_count'] = pd.Series(y_list_two).apply(lambda x: np.sum(x < 0))
X_train_two['z_neg_count'] = pd.Series(z_list_two).apply(lambda x: np.sum(x < 0))

# positive count
X_train_two['x_pos_count'] = pd.Series(x_list_two).apply(lambda x: np.sum(x > 0))
X_train_two['y_pos_count'] = pd.Series(y_list_two).apply(lambda x: np.sum(x > 0))
X_train_two['z_pos_count'] = pd.Series(z_list_two).apply(lambda x: np.sum(x > 0))

# values above mean
X_train_two['x_above_mean'] = pd.Series(x_list_two).apply(lambda x: np.sum(x > x.mean()))
X_train_two['y_above_mean'] = pd.Series(y_list_two).apply(lambda x: np.sum(x > x.mean()))
X_train_two['z_above_mean'] = pd.Series(z_list_two).apply(lambda x: np.sum(x > x.mean()))

# number of peaks
X_train_two['x_peak_count'] = pd.Series(x_list_two).apply(lambda x: len(find_peaks(x)[0]))
X_train_two['y_peak_count'] = pd.Series(y_list_two).apply(lambda x: len(find_peaks(x)[0]))
X_train_two['z_peak_count'] = pd.Series(z_list_two).apply(lambda x: len(find_peaks(x)[0]))

# skewness
X_train_two['x_skewness'] = pd.Series(x_list_two).apply(lambda x: stats.skew(x))
X_train_two['y_skewness'] = pd.Series(y_list_two).apply(lambda x: stats.skew(x))
X_train_two['z_skewness'] = pd.Series(z_list_two).apply(lambda x: stats.skew(x))

# kurtosis
X_train_two['x_kurtosis'] = pd.Series(x_list_two).apply(lambda x: stats.kurtosis(x))
X_train_two['y_kurtosis'] = pd.Series(y_list_two).apply(lambda x: stats.kurtosis(x))
X_train_two['z_kurtosis'] = pd.Series(z_list_two).apply(lambda x: stats.kurtosis(x))

# energy
X_train_two['x_energy'] = pd.Series(x_list_two).apply(lambda x: np.sum(x**2)/100)
X_train_two['y_energy'] = pd.Series(y_list_two).apply(lambda x: np.sum(x**2)/100)
X_train_two['z_energy'] = pd.Series(z_list_two).apply(lambda x: np.sum(x**2/100))

# avg resultant
X_train_two['avg_result_accl'] = [i.mean() for i in ((pd.Series(x_list_two)**2 + pd.Series(y_list_two)**2 + pd.Series(z_list_two)**2)**0.5)]

# signal magnitude area
X_train_two['sma'] =    pd.Series(x_list_two).apply(lambda x: np.sum(abs(x)/100)) + pd.Series(y_list_two).apply(lambda x: np.sum(abs(x)/100)) \
                  + pd.Series(z_list_two).apply(lambda x: np.sum(abs(x)/100))



# fft: chaning time domain signals to frequency domain
x_fft_two = pd.Series(x_list_two).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
y_fft_two = pd.Series(y_list_two).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
z_fft_two = pd.Series(z_list_two).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))

# Statistical Features on raw x, y and z in frequency domain
# FFT mean
X_train_two['x_mean_fft'] = pd.Series(x_fft_two).apply(lambda x: x.mean())
X_train_two['y_mean_fft'] = pd.Series(y_fft_two).apply(lambda x: x.mean())
X_train_two['z_mean_fft'] = pd.Series(z_fft_two).apply(lambda x: x.mean())

# FFT std dev
X_train_two['x_std_fft'] = pd.Series(x_fft_two).apply(lambda x: x.std())
X_train_two['y_std_fft'] = pd.Series(y_fft_two).apply(lambda x: x.std())
X_train_two['z_std_fft'] = pd.Series(z_fft_two).apply(lambda x: x.std())

# FFT avg absolute diff
X_train_two['x_aad_fft'] = pd.Series(x_fft_two).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_train_two['y_aad_fft'] = pd.Series(y_fft_two).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_train_two['z_aad_fft'] = pd.Series(z_fft_two).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

# FFT min
X_train_two['x_min_fft'] = pd.Series(x_fft_two).apply(lambda x: x.min())
X_train_two['y_min_fft'] = pd.Series(y_fft_two).apply(lambda x: x.min())
X_train_two['z_min_fft'] = pd.Series(z_fft_two).apply(lambda x: x.min())

# FFT max
X_train_two['x_max_fft'] = pd.Series(x_fft_two).apply(lambda x: x.max())
X_train_two['y_max_fft'] = pd.Series(y_fft_two).apply(lambda x: x.max())
X_train_two['z_max_fft'] = pd.Series(z_fft_two).apply(lambda x: x.max())

# FFT max-min diff
X_train_two['x_maxmin_diff_fft'] = X_train_two['x_max_fft'] - X_train_two['x_min_fft']
X_train_two['y_maxmin_diff_fft'] = X_train_two['y_max_fft'] - X_train_two['y_min_fft']
X_train_two['z_maxmin_diff_fft'] = X_train_two['z_max_fft'] - X_train_two['z_min_fft']

# FFT median
X_train_two['x_median_fft'] = pd.Series(x_fft_two).apply(lambda x: np.median(x))
X_train_two['y_median_fft'] = pd.Series(y_fft_two).apply(lambda x: np.median(x))
X_train_two['z_median_fft'] = pd.Series(z_fft_two).apply(lambda x: np.median(x))

# FFT median abs dev 
X_train_two['x_mad_fft'] = pd.Series(x_fft_two).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_train_two['y_mad_fft'] = pd.Series(y_fft_two).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_train_two['z_mad_fft'] = pd.Series(z_fft_two).apply(lambda x: np.median(np.absolute(x - np.median(x))))

# FFT Interquartile range
X_train_two['x_IQR_fft'] = pd.Series(x_fft_two).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_train_two['y_IQR_fft'] = pd.Series(y_fft_two).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_train_two['z_IQR_fft'] = pd.Series(z_fft_two).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

# FFT values above mean
X_train_two['x_above_mean_fft'] = pd.Series(x_fft_two).apply(lambda x: np.sum(x > x.mean()))
X_train_two['y_above_mean_fft'] = pd.Series(y_fft_two).apply(lambda x: np.sum(x > x.mean()))
X_train_two['z_above_mean_fft'] = pd.Series(z_fft_two).apply(lambda x: np.sum(x > x.mean()))

# FFT number of peaks
X_train_two['x_peak_count_fft'] = pd.Series(x_fft_two).apply(lambda x: len(find_peaks(x)[0]))
X_train_two['y_peak_count_fft'] = pd.Series(y_fft_two).apply(lambda x: len(find_peaks(x)[0]))
X_train_two['z_peak_count_fft'] = pd.Series(z_fft_two).apply(lambda x: len(find_peaks(x)[0]))

# FFT skewness
X_train_two['x_skewness_fft'] = pd.Series(x_fft_two).apply(lambda x: stats.skew(x))
X_train_two['y_skewness_fft'] = pd.Series(y_fft_two).apply(lambda x: stats.skew(x))
X_train_two['z_skewness_fft'] = pd.Series(z_fft_two).apply(lambda x: stats.skew(x))

# FFT kurtosis
X_train_two['x_kurtosis_fft'] = pd.Series(x_fft_two).apply(lambda x: stats.kurtosis(x))
X_train_two['y_kurtosis_fft'] = pd.Series(y_fft_two).apply(lambda x: stats.kurtosis(x))
X_train_two['z_kurtosis_fft'] = pd.Series(z_fft_two).apply(lambda x: stats.kurtosis(x))

# FFT energy
X_train_two['x_energy_fft'] = pd.Series(x_fft_two).apply(lambda x: np.sum(x**2)/50)
X_train_two['y_energy_fft'] = pd.Series(y_fft_two).apply(lambda x: np.sum(x**2)/50)
X_train_two['z_energy_fft'] = pd.Series(z_fft_two).apply(lambda x: np.sum(x**2/50))

# FFT avg resultant
X_train_two['avg_result_accl_fft'] = [i.mean() for i in ((pd.Series(x_fft_two)**2 + pd.Series(y_fft_two)**2 + pd.Series(z_fft_two)**2)**0.5)]

# FFT Signal magnitude area
X_train_two['sma_fft'] = pd.Series(x_fft_two).apply(lambda x: np.sum(abs(x)/50)) + pd.Series(y_fft_two).apply(lambda x: np.sum(abs(x)/50)) \
                     + pd.Series(z_fft_two).apply(lambda x: np.sum(abs(x)/50))


# calculating max & min indices

# index of max value in time domain
X_train_two['x_argmax'] = pd.Series(x_list_two).apply(lambda x: np.argmax(x))
X_train_two['y_argmax'] = pd.Series(y_list_two).apply(lambda x: np.argmax(x))
X_train_two['z_argmax'] = pd.Series(z_list_two).apply(lambda x: np.argmax(x))

# index of min value in time domain
X_train_two['x_argmin'] = pd.Series(x_list_two).apply(lambda x: np.argmin(x))
X_train_two['y_argmin'] = pd.Series(y_list_two).apply(lambda x: np.argmin(x))
X_train_two['z_argmin'] = pd.Series(z_list_two).apply(lambda x: np.argmin(x))

# absolute difference between above indices
X_train_two['x_arg_diff'] = abs(X_train_two['x_argmax'] - X_train_two['x_argmin'])
X_train_two['y_arg_diff'] = abs(X_train_two['y_argmax'] - X_train_two['y_argmin'])
X_train_two['z_arg_diff'] = abs(X_train_two['z_argmax'] - X_train_two['z_argmin'])

# index of max value in frequency domain
X_train_two['x_argmax_fft'] = pd.Series(x_fft_two).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
X_train_two['y_argmax_fft'] = pd.Series(y_fft_two).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
X_train_two['z_argmax_fft'] = pd.Series(z_fft_two).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))

# index of min value in frequency domain
X_train_two['x_argmin_fft'] = pd.Series(x_fft_two).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
X_train_two['y_argmin_fft'] = pd.Series(y_fft_two).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
X_train_two['z_argmin_fft'] = pd.Series(z_fft_two).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))

# absolute difference between above indices
X_train_two['x_arg_diff_fft'] = abs(X_train_two['x_argmax_fft'] - X_train_two['x_argmin_fft'])
X_train_two['y_arg_diff_fft'] = abs(X_train_two['y_argmax_fft'] - X_train_two['y_argmin_fft'])
X_train_two['z_arg_diff_fft'] = abs(X_train_two['z_argmax_fft'] - X_train_two['z_argmin_fft'])


# do the same for test data

x_list_two_test = []
y_list_two_test = []
z_list_two_test = []
test_labels_two = []

window = 100
step = 50


for i in range(0, test_df_two.shape[0] - window, step):
  xs_test = test_df_two['x-axis'].values[i: i + 100]
  ys_test = test_df_two['y-axis'].values[i: i + 100]
  zs_test = test_df_two['z-axis'].values[i: i + 100]
  test_label = test_df_two['activity'][i: i + 100].mode()[0]
  
  x_list_two_test.append(xs_test)
  y_list_two_test.append(ys_test)
  z_list_two_test.append(zs_test)
  test_labels_two.append(test_label)

X_test_two = pd.DataFrame()
  
# mean
X_test_two['x_mean'] = pd.Series(x_list_two_test).apply(lambda x: x.mean())
X_test_two['y_mean'] = pd.Series(y_list_two_test).apply(lambda x: x.mean())
X_test_two['z_mean'] = pd.Series(z_list_two_test).apply(lambda x: x.mean())

# std dev
X_test_two['x_std'] = pd.Series(x_list_two_test).apply(lambda x: x.std())
X_test_two['y_std'] = pd.Series(y_list_two_test).apply(lambda x: x.std())
X_test_two['z_std'] = pd.Series(z_list_two_test).apply(lambda x: x.std())

# avg absolute diff
X_test_two['x_aad'] = pd.Series(x_list_two_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_test_two['y_aad'] = pd.Series(y_list_two_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_test_two['z_aad'] = pd.Series(z_list_two_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

# min
X_test_two['x_min'] = pd.Series(x_list_two_test).apply(lambda x: x.min())
X_test_two['y_min'] = pd.Series(y_list_two_test).apply(lambda x: x.min())
X_test_two['z_min'] = pd.Series(z_list_two_test).apply(lambda x: x.min())

# max
X_test_two['x_max'] = pd.Series(x_list_two_test).apply(lambda x: x.max())
X_test_two['y_max'] = pd.Series(y_list_two_test).apply(lambda x: x.max())
X_test_two['z_max'] = pd.Series(z_list_two_test).apply(lambda x: x.max())

# max-min diff
X_test_two['x_maxmin_diff'] = X_test_two['x_max'] - X_test_two['x_min']
X_test_two['y_maxmin_diff'] = X_test_two['y_max'] - X_test_two['y_min']
X_test_two['z_maxmin_diff'] = X_test_two['z_max'] - X_test_two['z_min']

# median
X_test_two['x_median'] = pd.Series(x_list_two_test).apply(lambda x: np.median(x))
X_test_two['y_median'] = pd.Series(y_list_two_test).apply(lambda x: np.median(x))
X_test_two['z_median'] = pd.Series(z_list_two_test).apply(lambda x: np.median(x))

# median abs dev 
X_test_two['x_mad'] = pd.Series(x_list_two_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_test_two['y_mad'] = pd.Series(y_list_two_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_test_two['z_mad'] = pd.Series(z_list_two_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))

# interquartile range
X_test_two['x_IQR'] = pd.Series(x_list_two_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_test_two['y_IQR'] = pd.Series(y_list_two_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_test_two['z_IQR'] = pd.Series(z_list_two_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

# negtive count
X_test_two['x_neg_count'] = pd.Series(x_list_two_test).apply(lambda x: np.sum(x < 0))
X_test_two['y_neg_count'] = pd.Series(y_list_two_test).apply(lambda x: np.sum(x < 0))
X_test_two['z_neg_count'] = pd.Series(z_list_two_test).apply(lambda x: np.sum(x < 0))

# positive count
X_test_two['x_pos_count'] = pd.Series(x_list_two_test).apply(lambda x: np.sum(x > 0))
X_test_two['y_pos_count'] = pd.Series(y_list_two_test).apply(lambda x: np.sum(x > 0))
X_test_two['z_pos_count'] = pd.Series(z_list_two_test).apply(lambda x: np.sum(x > 0))

# values above mean
X_test_two['x_above_mean'] = pd.Series(x_list_two_test).apply(lambda x: np.sum(x > x.mean()))
X_test_two['y_above_mean'] = pd.Series(y_list_two_test).apply(lambda x: np.sum(x > x.mean()))
X_test_two['z_above_mean'] = pd.Series(z_list_two_test).apply(lambda x: np.sum(x > x.mean()))

# number of peaks
X_test_two['x_peak_count'] = pd.Series(x_list_two_test).apply(lambda x: len(find_peaks(x)[0]))
X_test_two['y_peak_count'] = pd.Series(y_list_two_test).apply(lambda x: len(find_peaks(x)[0]))
X_test_two['z_peak_count'] = pd.Series(z_list_two_test).apply(lambda x: len(find_peaks(x)[0]))

# skewness
X_test_two['x_skewness'] = pd.Series(x_list_two_test).apply(lambda x: stats.skew(x))
X_test_two['y_skewness'] = pd.Series(y_list_two_test).apply(lambda x: stats.skew(x))
X_test_two['z_skewness'] = pd.Series(z_list_two_test).apply(lambda x: stats.skew(x))

# kurtosis
X_test_two['x_kurtosis'] = pd.Series(x_list_two_test).apply(lambda x: stats.kurtosis(x))
X_test_two['y_kurtosis'] = pd.Series(y_list_two_test).apply(lambda x: stats.kurtosis(x))
X_test_two['z_kurtosis'] = pd.Series(z_list_two_test).apply(lambda x: stats.kurtosis(x))

# energy
X_test_two['x_energy'] = pd.Series(x_list_two_test).apply(lambda x: np.sum(x**2)/100)
X_test_two['y_energy'] = pd.Series(y_list_two_test).apply(lambda x: np.sum(x**2)/100)
X_test_two['z_energy'] = pd.Series(z_list_two_test).apply(lambda x: np.sum(x**2/100))

# avg resultant
X_test_two['avg_result_accl'] = [i.mean() for i in ((pd.Series(x_list_two_test)**2 + pd.Series(y_list_two_test)**2 + pd.Series(z_list_two_test)**2)**0.5)]

# signal magnitude area
X_test_two['sma'] =    pd.Series(x_list_two_test).apply(lambda x: np.sum(abs(x)/100)) + pd.Series(y_list_two_test).apply(lambda x: np.sum(abs(x)/100)) \
                  + pd.Series(z_list_two_test).apply(lambda x: np.sum(abs(x)/100))




# fft: chaning time domain signals to frequency domain
x_fft_two_test = pd.Series(x_list_two_test).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
y_fft_two_test = pd.Series(y_list_two_test).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
z_fft_two_test = pd.Series(z_list_two_test).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))

# Statistical Features on raw x, y and z in frequency domain
# FFT mean
X_test_two['x_mean_fft'] = pd.Series(x_fft_two_test).apply(lambda x: x.mean())
X_test_two['y_mean_fft'] = pd.Series(y_fft_two_test).apply(lambda x: x.mean())
X_test_two['z_mean_fft'] = pd.Series(z_fft_two_test).apply(lambda x: x.mean())

# FFT std dev
X_test_two['x_std_fft'] = pd.Series(x_fft_two_test).apply(lambda x: x.std())
X_test_two['y_std_fft'] = pd.Series(y_fft_two_test).apply(lambda x: x.std())
X_test_two['z_std_fft'] = pd.Series(z_fft_two_test).apply(lambda x: x.std())

# FFT avg absolute diff
X_test_two['x_aad_fft'] = pd.Series(x_fft_two_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_test_two['y_aad_fft'] = pd.Series(y_fft_two_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_test_two['z_aad_fft'] = pd.Series(z_fft_two_test).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

# FFT min
X_test_two['x_min_fft'] = pd.Series(x_fft_two_test).apply(lambda x: x.min())
X_test_two['y_min_fft'] = pd.Series(y_fft_two_test).apply(lambda x: x.min())
X_test_two['z_min_fft'] = pd.Series(z_fft_two_test).apply(lambda x: x.min())

# FFT max
X_test_two['x_max_fft'] = pd.Series(x_fft_two_test).apply(lambda x: x.max())
X_test_two['y_max_fft'] = pd.Series(y_fft_two_test).apply(lambda x: x.max())
X_test_two['z_max_fft'] = pd.Series(z_fft_two_test).apply(lambda x: x.max())

# FFT max-min diff
X_test_two['x_maxmin_diff_fft'] = X_test_two['x_max_fft'] - X_test_two['x_min_fft']
X_test_two['y_maxmin_diff_fft'] = X_test_two['y_max_fft'] - X_test_two['y_min_fft']
X_test_two['z_maxmin_diff_fft'] = X_test_two['z_max_fft'] - X_test_two['z_min_fft']

# FFT median
X_test_two['x_median_fft'] = pd.Series(x_fft_two_test).apply(lambda x: np.median(x))
X_test_two['y_median_fft'] = pd.Series(y_fft_two_test).apply(lambda x: np.median(x))
X_test_two['z_median_fft'] = pd.Series(z_fft_two_test).apply(lambda x: np.median(x))

# FFT median abs dev 
X_test_two['x_mad_fft'] = pd.Series(x_fft_two_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_test_two['y_mad_fft'] = pd.Series(y_fft_two_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_test_two['z_mad_fft'] = pd.Series(z_fft_two_test).apply(lambda x: np.median(np.absolute(x - np.median(x))))

# FFT Interquartile range
X_test_two['x_IQR_fft'] = pd.Series(x_fft_two_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_test_two['y_IQR_fft'] = pd.Series(y_fft_two_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_test_two['z_IQR_fft'] = pd.Series(z_fft_two_test).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

# FFT values above mean
X_test_two['x_above_mean_fft'] = pd.Series(x_fft_two_test).apply(lambda x: np.sum(x > x.mean()))
X_test_two['y_above_mean_fft'] = pd.Series(y_fft_two_test).apply(lambda x: np.sum(x > x.mean()))
X_test_two['z_above_mean_fft'] = pd.Series(z_fft_two_test).apply(lambda x: np.sum(x > x.mean()))

# FFT number of peaks
X_test_two['x_peak_count_fft'] = pd.Series(x_fft_two_test).apply(lambda x: len(find_peaks(x)[0]))
X_test_two['y_peak_count_fft'] = pd.Series(y_fft_two_test).apply(lambda x: len(find_peaks(x)[0]))
X_test_two['z_peak_count_fft'] = pd.Series(z_fft_two_test).apply(lambda x: len(find_peaks(x)[0]))

# FFT skewness
X_test_two['x_skewness_fft'] = pd.Series(x_fft_two_test).apply(lambda x: stats.skew(x))
X_test_two['y_skewness_fft'] = pd.Series(y_fft_two_test).apply(lambda x: stats.skew(x))
X_test_two['z_skewness_fft'] = pd.Series(z_fft_two_test).apply(lambda x: stats.skew(x))

# FFT kurtosis
X_test_two['x_kurtosis_fft'] = pd.Series(x_fft_two_test).apply(lambda x: stats.kurtosis(x))
X_test_two['y_kurtosis_fft'] = pd.Series(y_fft_two_test).apply(lambda x: stats.kurtosis(x))
X_test_two['z_kurtosis_fft'] = pd.Series(z_fft_two_test).apply(lambda x: stats.kurtosis(x))

# FFT energy
X_test_two['x_energy_fft'] = pd.Series(x_fft_two_test).apply(lambda x: np.sum(x**2)/50)
X_test_two['y_energy_fft'] = pd.Series(y_fft_two_test).apply(lambda x: np.sum(x**2)/50)
X_test_two['z_energy_fft'] = pd.Series(z_fft_two_test).apply(lambda x: np.sum(x**2/50))

# FFT avg resultant
X_test_two['avg_result_accl_fft'] = [i.mean() for i in ((pd.Series(x_fft_two_test)**2 + pd.Series(y_fft_two_test)**2 + pd.Series(z_fft_two_test)**2)**0.5)]

# FFT Signal magnitude area
X_test_two['sma_fft'] = pd.Series(x_fft_two_test).apply(lambda x: np.sum(abs(x)/50)) + pd.Series(y_fft_two_test).apply(lambda x: np.sum(abs(x)/50)) \
                     + pd.Series(z_fft_two_test).apply(lambda x: np.sum(abs(x)/50))


# calculating max & min indices

# index of max value in time domain
X_test_two['x_argmax'] = pd.Series(x_list_two_test).apply(lambda x: np.argmax(x))
X_test_two['y_argmax'] = pd.Series(y_list_two_test).apply(lambda x: np.argmax(x))
X_test_two['z_argmax'] = pd.Series(z_list_two_test).apply(lambda x: np.argmax(x))

# index of min value in time domain
X_test_two['x_argmin'] = pd.Series(x_list_two_test).apply(lambda x: np.argmin(x))
X_test_two['y_argmin'] = pd.Series(y_list_two_test).apply(lambda x: np.argmin(x))
X_test_two['z_argmin'] = pd.Series(z_list_two_test).apply(lambda x: np.argmin(x))

# absolute difference between above indices
X_test_two['x_arg_diff'] = abs(X_test_two['x_argmax'] - X_test_two['x_argmin'])
X_test_two['y_arg_diff'] = abs(X_test_two['y_argmax'] - X_test_two['y_argmin'])
X_test_two['z_arg_diff'] = abs(X_test_two['z_argmax'] - X_test_two['z_argmin'])

# index of max value in frequency domain
X_test_two['x_argmax_fft'] = pd.Series(x_fft_two_test).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
X_test_two['y_argmax_fft'] = pd.Series(y_fft_two_test).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
X_test_two['z_argmax_fft'] = pd.Series(z_fft_two_test).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))

# index of min value in frequency domain
X_test_two['x_argmin_fft'] = pd.Series(x_fft_two_test).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
X_test_two['y_argmin_fft'] = pd.Series(y_fft_two_test).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
X_test_two['z_argmin_fft'] = pd.Series(z_fft_two_test).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))

# absolute difference between above indices
X_test_two['x_arg_diff_fft'] = abs(X_test_two['x_argmax_fft'] - X_test_two['x_argmin_fft'])
X_test_two['y_arg_diff_fft'] = abs(X_test_two['y_argmax_fft'] - X_test_two['y_argmin_fft'])
X_test_two['z_arg_diff_fft'] = abs(X_test_two['z_argmax_fft'] - X_test_two['z_argmin_fft'])


y_train_two = np.array(train_labels_two)
y_test_two = np.array(test_labels_two)

# model for User 8
rf_two = RandomForestClassifier(random_state = 21)
k=5
folds_two = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
scores_two= cross_val_score(rf_two, X_train_two, y_train_two, cv=folds_two, scoring='accuracy')

rf_two.fit(X_train_two, y_train_two)
y_pred_two = rf_two.predict(X_test_two)
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
y_pred_three = rf.predict(X_test_two)
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
y_pred_four = rf_two.predict(X_test)
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







