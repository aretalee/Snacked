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
from scipy.stats import randint
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score



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


# # linear model for activity prediction
y_train = np.array(train_labels)
y_test = np.array(test_labels)


# random forest model

rf = RandomForestClassifier(random_state = 21)
k=5
folds = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
scores = cross_val_score(rf, X_train, y_train, cv=folds, scoring='accuracy')

rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy of model trained on watch data:", accuracy)
print("Cross validation score:", scores)
print("Cross validation mean:", np.mean(scores))
print(classification_report(y_test, y_pred))


labels = ['Brushing teeth', 'Drinking water', 'Eating soup', 'Snacking chips', 'Snacking on chocolate', 'Walking']
confusion_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(confusion_matrix, xticklabels=labels, yticklabels=labels, annot=True,linewidths = 0.1, fmt="d", cmap = 'YlGnBu')
plt.title("Confusion matrix", fontsize = 15)
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()


