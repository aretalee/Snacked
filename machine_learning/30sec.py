import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.signal import find_peaks
import warnings
warnings.filterwarnings('ignore')

from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('alLData.csv', sep=',')


df = df.dropna()
df.shape
brush = df[df['activity'] == 'Brushing teeth'].head(1200)
drink = df[df['activity'] == 'Drinking water'].head(1200)
chips = df[df['activity'] == 'Snacking on chips'].head(1200)
choco = df[df['activity'] == 'Snacking on chocolate bar'].head(1200)
walk = df[df['activity'] == 'Walking'].head(1200)
soup = df[df['activity'] == 'Eating soup'].head(1200)

balanced = pd.DataFrame()
balanced = pd.concat([brush, drink, chips, choco, walk, soup])


training, testing = [], []

for label, group in balanced.groupby('activity'): 
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


rf = RandomForestClassifier(random_state = 21)
rf.fit(X_training, y_train)


# predicting 30 second data streams

stream = pd.read_csv("30sec_test1.csv", sep=',', on_bad_lines='skip')
# stream = pd.read_csv("30sec_test2.csv", sep=',', on_bad_lines='skip')
# stream = pd.read_csv("30sec_test3.csv", sep=',', on_bad_lines='skip')
stream = stream.dropna()
stream.shape
stream['Z'] = stream['Z'].apply(lambda x:float(x))

pred_df = stream[stream['TimeStamp'] != 0].sort_values(by = ['TimeStamp'], ignore_index=True)

x_items_real = []
y_items_real = []
z_items_real = []

window = 100
step = 50


for i in range(0, pred_df.shape[0] - window, step):
  xs = pred_df['X'].values[i: i + 100]
  ys = pred_df['Y'].values[i: i + 100]
  zs = pred_df['Z'].values[i: i + 100]
  
  x_items_real.append(xs)
  y_items_real.append(ys)
  z_items_real.append(zs)


X_pred = pd.DataFrame()

# mean
X_pred['x_mean'] = pd.Series(x_items_real).apply(lambda x: x.mean())
X_pred['y_mean'] = pd.Series(y_items_real).apply(lambda x: x.mean())
X_pred['z_mean'] = pd.Series(z_items_real).apply(lambda x: x.mean())

# std dev
X_pred['x_std'] = pd.Series(x_items_real).apply(lambda x: x.std())
X_pred['y_std'] = pd.Series(y_items_real).apply(lambda x: x.std())
X_pred['z_std'] = pd.Series(z_items_real).apply(lambda x: x.std())

# avg absolute diff
X_pred['x_aad'] = pd.Series(x_items_real).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_pred['y_aad'] = pd.Series(y_items_real).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_pred['z_aad'] = pd.Series(z_items_real).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

# min
X_pred['x_min'] = pd.Series(x_items_real).apply(lambda x: x.min())
X_pred['y_min'] = pd.Series(y_items_real).apply(lambda x: x.min())
X_pred['z_min'] = pd.Series(z_items_real).apply(lambda x: x.min())

# max
X_pred['x_max'] = pd.Series(x_items_real).apply(lambda x: x.max())
X_pred['y_max'] = pd.Series(y_items_real).apply(lambda x: x.max())
X_pred['z_max'] = pd.Series(z_items_real).apply(lambda x: x.max())

# max-min diff
X_pred['x_maxmin_diff'] = X_pred['x_max'] - X_pred['x_min']
X_pred['y_maxmin_diff'] = X_pred['y_max'] - X_pred['y_min']
X_pred['z_maxmin_diff'] = X_pred['z_max'] - X_pred['z_min']

# median
X_pred['x_median'] = pd.Series(x_items_real).apply(lambda x: np.median(x))
X_pred['y_median'] = pd.Series(y_items_real).apply(lambda x: np.median(x))
X_pred['z_median'] = pd.Series(z_items_real).apply(lambda x: np.median(x))

# median abs dev 
X_pred['x_mad'] = pd.Series(x_items_real).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_pred['y_mad'] = pd.Series(y_items_real).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_pred['z_mad'] = pd.Series(z_items_real).apply(lambda x: np.median(np.absolute(x - np.median(x))))

# interquartile range
X_pred['x_IQR'] = pd.Series(x_items_real).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_pred['y_IQR'] = pd.Series(y_items_real).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_pred['z_IQR'] = pd.Series(z_items_real).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

# negtive count
X_pred['x_neg_count'] = pd.Series(x_items_real).apply(lambda x: np.sum(x < 0))
X_pred['y_neg_count'] = pd.Series(y_items_real).apply(lambda x: np.sum(x < 0))
X_pred['z_neg_count'] = pd.Series(z_items_real).apply(lambda x: np.sum(x < 0))

# positive count
X_pred['x_pos_count'] = pd.Series(x_items_real).apply(lambda x: np.sum(x > 0))
X_pred['y_pos_count'] = pd.Series(y_items_real).apply(lambda x: np.sum(x > 0))
X_pred['z_pos_count'] = pd.Series(z_items_real).apply(lambda x: np.sum(x > 0))

# values above mean
X_pred['x_above_mean'] = pd.Series(x_items_real).apply(lambda x: np.sum(x > x.mean()))
X_pred['y_above_mean'] = pd.Series(y_items_real).apply(lambda x: np.sum(x > x.mean()))
X_pred['z_above_mean'] = pd.Series(z_items_real).apply(lambda x: np.sum(x > x.mean()))

# number of peaks
X_pred['x_peak_count'] = pd.Series(x_items_real).apply(lambda x: len(find_peaks(x)[0]))
X_pred['y_peak_count'] = pd.Series(y_items_real).apply(lambda x: len(find_peaks(x)[0]))
X_pred['z_peak_count'] = pd.Series(z_items_real).apply(lambda x: len(find_peaks(x)[0]))

# skewness
X_pred['x_skewness'] = pd.Series(x_items_real).apply(lambda x: stats.skew(x))
X_pred['y_skewness'] = pd.Series(y_items_real).apply(lambda x: stats.skew(x))
X_pred['z_skewness'] = pd.Series(z_items_real).apply(lambda x: stats.skew(x))

# kurtosis
X_pred['x_kurtosis'] = pd.Series(x_items_real).apply(lambda x: stats.kurtosis(x))
X_pred['y_kurtosis'] = pd.Series(y_items_real).apply(lambda x: stats.kurtosis(x))
X_pred['z_kurtosis'] = pd.Series(z_items_real).apply(lambda x: stats.kurtosis(x))

# energy
X_pred['x_energy'] = pd.Series(x_items_real).apply(lambda x: np.sum(x**2)/100)
X_pred['y_energy'] = pd.Series(y_items_real).apply(lambda x: np.sum(x**2)/100)
X_pred['z_energy'] = pd.Series(z_items_real).apply(lambda x: np.sum(x**2/100))

# avg resultant
X_pred['avg_result_accl'] = [i.mean() for i in ((pd.Series(x_items_real)**2 + pd.Series(y_items_real)**2 + pd.Series(z_items_real)**2)**0.5)]

# signal magnitude area
X_pred['sma'] =    pd.Series(x_items_real).apply(lambda x: np.sum(abs(x)/100)) + pd.Series(y_items_real).apply(lambda x: np.sum(abs(x)/100)) \
+ pd.Series(z_items_real).apply(lambda x: np.sum(abs(x)/100))



# fft: chaning time domain signals to frequency domain
x_fft_real = pd.Series(x_items_real).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
y_fft_real = pd.Series(y_items_real).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
z_fft_real = pd.Series(z_items_real).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))


# Statistical Features on raw x, y and z in frequency domain
# FFT mean
X_pred['x_mean_fft'] = pd.Series(x_fft_real).apply(lambda x: x.mean())
X_pred['y_mean_fft'] = pd.Series(y_fft_real).apply(lambda x: x.mean())
X_pred['z_mean_fft'] = pd.Series(z_fft_real).apply(lambda x: x.mean())

# FFT std dev
X_pred['x_std_fft'] = pd.Series(x_fft_real).apply(lambda x: x.std())
X_pred['y_std_fft'] = pd.Series(y_fft_real).apply(lambda x: x.std())
X_pred['z_std_fft'] = pd.Series(z_fft_real).apply(lambda x: x.std())

# FFT avg absolute diff
X_pred['x_aad_fft'] = pd.Series(x_fft_real).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_pred['y_aad_fft'] = pd.Series(y_fft_real).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
X_pred['z_aad_fft'] = pd.Series(z_fft_real).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

# FFT min
X_pred['x_min_fft'] = pd.Series(x_fft_real).apply(lambda x: x.min())
X_pred['y_min_fft'] = pd.Series(y_fft_real).apply(lambda x: x.min())
X_pred['z_min_fft'] = pd.Series(z_fft_real).apply(lambda x: x.min())

# FFT max
X_pred['x_max_fft'] = pd.Series(x_fft_real).apply(lambda x: x.max())
X_pred['y_max_fft'] = pd.Series(y_fft_real).apply(lambda x: x.max())
X_pred['z_max_fft'] = pd.Series(z_fft_real).apply(lambda x: x.max())

# FFT max-min diff
X_pred['x_maxmin_diff_fft'] = X_pred['x_max_fft'] - X_pred['x_min_fft']
X_pred['y_maxmin_diff_fft'] = X_pred['y_max_fft'] - X_pred['y_min_fft']
X_pred['z_maxmin_diff_fft'] = X_pred['z_max_fft'] - X_pred['z_min_fft']

# FFT median
X_pred['x_median_fft'] = pd.Series(x_fft_real).apply(lambda x: np.median(x))
X_pred['y_median_fft'] = pd.Series(y_fft_real).apply(lambda x: np.median(x))
X_pred['z_median_fft'] = pd.Series(z_fft_real).apply(lambda x: np.median(x))

# FFT median abs dev 
X_pred['x_mad_fft'] = pd.Series(x_fft_real).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_pred['y_mad_fft'] = pd.Series(y_fft_real).apply(lambda x: np.median(np.absolute(x - np.median(x))))
X_pred['z_mad_fft'] = pd.Series(z_fft_real).apply(lambda x: np.median(np.absolute(x - np.median(x))))

# FFT Interquartile range
X_pred['x_IQR_fft'] = pd.Series(x_fft_real).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_pred['y_IQR_fft'] = pd.Series(y_fft_real).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
X_pred['z_IQR_fft'] = pd.Series(z_fft_real).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

# FFT values above mean
X_pred['x_above_mean_fft'] = pd.Series(x_fft_real).apply(lambda x: np.sum(x > x.mean()))
X_pred['y_above_mean_fft'] = pd.Series(y_fft_real).apply(lambda x: np.sum(x > x.mean()))
X_pred['z_above_mean_fft'] = pd.Series(z_fft_real).apply(lambda x: np.sum(x > x.mean()))

# FFT number of peaks
X_pred['x_peak_count_fft'] = pd.Series(x_fft_real).apply(lambda x: len(find_peaks(x)[0]))
X_pred['y_peak_count_fft'] = pd.Series(y_fft_real).apply(lambda x: len(find_peaks(x)[0]))
X_pred['z_peak_count_fft'] = pd.Series(z_fft_real).apply(lambda x: len(find_peaks(x)[0]))

# FFT skewness
X_pred['x_skewness_fft'] = pd.Series(x_fft_real).apply(lambda x: stats.skew(x))
X_pred['y_skewness_fft'] = pd.Series(y_fft_real).apply(lambda x: stats.skew(x))
X_pred['z_skewness_fft'] = pd.Series(z_fft_real).apply(lambda x: stats.skew(x))

# FFT kurtosis
X_pred['x_kurtosis_fft'] = pd.Series(x_fft_real).apply(lambda x: stats.kurtosis(x))
X_pred['y_kurtosis_fft'] = pd.Series(y_fft_real).apply(lambda x: stats.kurtosis(x))
X_pred['z_kurtosis_fft'] = pd.Series(z_fft_real).apply(lambda x: stats.kurtosis(x))

# FFT energy
X_pred['x_energy_fft'] = pd.Series(x_fft_real).apply(lambda x: np.sum(x**2)/50)
X_pred['y_energy_fft'] = pd.Series(y_fft_real).apply(lambda x: np.sum(x**2)/50)
X_pred['z_energy_fft'] = pd.Series(z_fft_real).apply(lambda x: np.sum(x**2/50))

# FFT avg resultant
X_pred['avg_result_accl_fft'] = [i.mean() for i in ((pd.Series(x_fft_real)**2 + pd.Series(y_fft_real)**2 + pd.Series(z_fft_real)**2)**0.5)]

# FFT Signal magnitude area
X_pred['sma_fft'] = pd.Series(x_fft_real).apply(lambda x: np.sum(abs(x)/50)) + pd.Series(y_fft_real).apply(lambda x: np.sum(abs(x)/50)) \
    + pd.Series(z_fft_real).apply(lambda x: np.sum(abs(x)/50))


# calculating max & min indices

# index of max value in time domain
X_pred['x_argmax'] = pd.Series(x_items_real).apply(lambda x: np.argmax(x))
X_pred['y_argmax'] = pd.Series(y_items_real).apply(lambda x: np.argmax(x))
X_pred['z_argmax'] = pd.Series(z_items_real).apply(lambda x: np.argmax(x))

# index of min value in time domain
X_pred['x_argmin'] = pd.Series(x_items_real).apply(lambda x: np.argmin(x))
X_pred['y_argmin'] = pd.Series(y_items_real).apply(lambda x: np.argmin(x))
X_pred['z_argmin'] = pd.Series(z_items_real).apply(lambda x: np.argmin(x))

# absolute difference between above indices
X_pred['x_arg_diff'] = abs(X_pred['x_argmax'] - X_pred['x_argmin'])
X_pred['y_arg_diff'] = abs(X_pred['y_argmax'] - X_pred['y_argmin'])
X_pred['z_arg_diff'] = abs(X_pred['z_argmax'] - X_pred['z_argmin'])

# index of max value in frequency domain
X_pred['x_argmax_fft'] = pd.Series(x_fft_real).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
X_pred['y_argmax_fft'] = pd.Series(y_fft_real).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
X_pred['z_argmax_fft'] = pd.Series(z_fft_real).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))

# index of min value in frequency domain
X_pred['x_argmin_fft'] = pd.Series(x_fft_real).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
X_pred['y_argmin_fft'] = pd.Series(y_fft_real).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
X_pred['z_argmin_fft'] = pd.Series(z_fft_real).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))

# absolute difference between above indices
X_pred['x_arg_diff_fft'] = abs(X_pred['x_argmax_fft'] - X_pred['x_argmin_fft'])
X_pred['y_arg_diff_fft'] = abs(X_pred['y_argmax_fft'] - X_pred['y_argmin_fft'])
X_pred['z_arg_diff_fft'] = abs(X_pred['z_argmax_fft'] - X_pred['z_argmin_fft'])


pred = rf.predict(X_pred)

# logic to approxiimate snacking and eating data from sliding windows

sampling_rate = 20 
snack_seg = np.sum((pred == 'Snacking on chocolate bar') | (pred == 'Snacking on chips'))
eat_seg = np.sum((pred == 'Snacking on chocolate bar') | (pred == 'Snacking on chips') | (pred == 'Eating soup'))

print('Predcitions in sec:')
print(snack_seg * 50 / sampling_rate)
print(eat_seg * 50 / sampling_rate)

