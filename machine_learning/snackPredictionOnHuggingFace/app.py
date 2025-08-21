from io import StringIO
import gradio as gr
import datetime
import numpy as np 
import pandas as pd
from scipy import stats
from scipy.signal import find_peaks
import joblib

from sklearn.ensemble import RandomForestClassifier
from claspy.segmentation import BinaryClaSPSegmentation

import os
from supabase import create_client

def predict(csv):
    try:  
        har_df = pd.read_csv(StringIO(csv), sep=',', on_bad_lines='skip')
        har_df = har_df.dropna()
        har_df.shape
        har_df['Z'] = har_df['Z'].apply(lambda x:float(x))

        pred_df = har_df[har_df['TimeStamp'] != 0].sort_values(by = ['TimeStamp'], ignore_index=True)

        x_list = []
        y_list = []
        z_list = []

        xs = pred_df['X'].values
        ys = pred_df['Y'].values
        zs = pred_df['Z'].values

        mv_data = np.column_stack((xs, ys, zs))
        tclasp = BinaryClaSPSegmentation()
        points = [int(i) for i in tclasp.fit_predict(mv_data)]

        seg_length = []
        init = 0
        for i in points + [len(mv_data)]:
            x_seg = xs[init:i]
            y_seg = ys[init:i]
            z_seg = zs[init:i]
            seg_length.append(i - init)
            init = i
            
            x_list.append(x_seg)
            y_list.append(y_seg)
            z_list.append(z_seg)



        X_pred = pd.DataFrame()
        
        # mean
        X_pred['x_mean'] = pd.Series(x_list).apply(lambda x: x.mean())
        X_pred['y_mean'] = pd.Series(y_list).apply(lambda x: x.mean())
        X_pred['z_mean'] = pd.Series(z_list).apply(lambda x: x.mean())

        # std dev
        X_pred['x_std'] = pd.Series(x_list).apply(lambda x: x.std())
        X_pred['y_std'] = pd.Series(y_list).apply(lambda x: x.std())
        X_pred['z_std'] = pd.Series(z_list).apply(lambda x: x.std())

        # avg absolute diff
        X_pred['x_aad'] = pd.Series(x_list).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
        X_pred['y_aad'] = pd.Series(y_list).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
        X_pred['z_aad'] = pd.Series(z_list).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

        # min
        X_pred['x_min'] = pd.Series(x_list).apply(lambda x: x.min())
        X_pred['y_min'] = pd.Series(y_list).apply(lambda x: x.min())
        X_pred['z_min'] = pd.Series(z_list).apply(lambda x: x.min())

        # max
        X_pred['x_max'] = pd.Series(x_list).apply(lambda x: x.max())
        X_pred['y_max'] = pd.Series(y_list).apply(lambda x: x.max())
        X_pred['z_max'] = pd.Series(z_list).apply(lambda x: x.max())

        # max-min diff
        X_pred['x_maxmin_diff'] = X_pred['x_max'] - X_pred['x_min']
        X_pred['y_maxmin_diff'] = X_pred['y_max'] - X_pred['y_min']
        X_pred['z_maxmin_diff'] = X_pred['z_max'] - X_pred['z_min']

        # median
        X_pred['x_median'] = pd.Series(x_list).apply(lambda x: np.median(x))
        X_pred['y_median'] = pd.Series(y_list).apply(lambda x: np.median(x))
        X_pred['z_median'] = pd.Series(z_list).apply(lambda x: np.median(x))

        # median abs dev 
        X_pred['x_mad'] = pd.Series(x_list).apply(lambda x: np.median(np.absolute(x - np.median(x))))
        X_pred['y_mad'] = pd.Series(y_list).apply(lambda x: np.median(np.absolute(x - np.median(x))))
        X_pred['z_mad'] = pd.Series(z_list).apply(lambda x: np.median(np.absolute(x - np.median(x))))

        # interquartile range
        X_pred['x_IQR'] = pd.Series(x_list).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
        X_pred['y_IQR'] = pd.Series(y_list).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
        X_pred['z_IQR'] = pd.Series(z_list).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

        # negtive count
        X_pred['x_neg_count'] = pd.Series(x_list).apply(lambda x: np.sum(x < 0))
        X_pred['y_neg_count'] = pd.Series(y_list).apply(lambda x: np.sum(x < 0))
        X_pred['z_neg_count'] = pd.Series(z_list).apply(lambda x: np.sum(x < 0))

        # positive count
        X_pred['x_pos_count'] = pd.Series(x_list).apply(lambda x: np.sum(x > 0))
        X_pred['y_pos_count'] = pd.Series(y_list).apply(lambda x: np.sum(x > 0))
        X_pred['z_pos_count'] = pd.Series(z_list).apply(lambda x: np.sum(x > 0))

        # values above mean
        X_pred['x_above_mean'] = pd.Series(x_list).apply(lambda x: np.sum(x > x.mean()))
        X_pred['y_above_mean'] = pd.Series(y_list).apply(lambda x: np.sum(x > x.mean()))
        X_pred['z_above_mean'] = pd.Series(z_list).apply(lambda x: np.sum(x > x.mean()))

        # number of peaks
        X_pred['x_peak_count'] = pd.Series(x_list).apply(lambda x: len(find_peaks(x)[0]))
        X_pred['y_peak_count'] = pd.Series(y_list).apply(lambda x: len(find_peaks(x)[0]))
        X_pred['z_peak_count'] = pd.Series(z_list).apply(lambda x: len(find_peaks(x)[0]))

        # skewness
        X_pred['x_skewness'] = pd.Series(x_list).apply(lambda x: stats.skew(x))
        X_pred['y_skewness'] = pd.Series(y_list).apply(lambda x: stats.skew(x))
        X_pred['z_skewness'] = pd.Series(z_list).apply(lambda x: stats.skew(x))

        # kurtosis
        X_pred['x_kurtosis'] = pd.Series(x_list).apply(lambda x: stats.kurtosis(x))
        X_pred['y_kurtosis'] = pd.Series(y_list).apply(lambda x: stats.kurtosis(x))
        X_pred['z_kurtosis'] = pd.Series(z_list).apply(lambda x: stats.kurtosis(x))

        # energy
        X_pred['x_energy'] = pd.Series(x_list).apply(lambda x: np.sum(x**2)/100)
        X_pred['y_energy'] = pd.Series(y_list).apply(lambda x: np.sum(x**2)/100)
        X_pred['z_energy'] = pd.Series(z_list).apply(lambda x: np.sum(x**2/100))

        # avg resultant
        X_pred['avg_result_accl'] = [i.mean() for i in ((pd.Series(x_list)**2 + pd.Series(y_list)**2 + pd.Series(z_list)**2)**0.5)]

        # signal magnitude area
        X_pred['sma'] =    pd.Series(x_list).apply(lambda x: np.sum(abs(x)/100)) + pd.Series(y_list).apply(lambda x: np.sum(abs(x)/100)) \
                        + pd.Series(z_list).apply(lambda x: np.sum(abs(x)/100))



        # fft: chaning time domain signals to frequency domain
        x_fft = pd.Series(x_list).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
        y_fft = pd.Series(y_list).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))
        z_fft = pd.Series(z_list).apply(lambda x: np.abs(np.fft.fft(x)[1:51]))


        # Statistical Features on raw x, y and z in frequency domain
        # FFT mean
        X_pred['x_mean_fft'] = pd.Series(x_fft).apply(lambda x: x.mean())
        X_pred['y_mean_fft'] = pd.Series(y_fft).apply(lambda x: x.mean())
        X_pred['z_mean_fft'] = pd.Series(z_fft).apply(lambda x: x.mean())

        # FFT std dev
        X_pred['x_std_fft'] = pd.Series(x_fft).apply(lambda x: x.std())
        X_pred['y_std_fft'] = pd.Series(y_fft).apply(lambda x: x.std())
        X_pred['z_std_fft'] = pd.Series(z_fft).apply(lambda x: x.std())

        # FFT avg absolute diff
        X_pred['x_aad_fft'] = pd.Series(x_fft).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
        X_pred['y_aad_fft'] = pd.Series(y_fft).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))
        X_pred['z_aad_fft'] = pd.Series(z_fft).apply(lambda x: np.mean(np.absolute(x - np.mean(x))))

        # FFT min
        X_pred['x_min_fft'] = pd.Series(x_fft).apply(lambda x: x.min())
        X_pred['y_min_fft'] = pd.Series(y_fft).apply(lambda x: x.min())
        X_pred['z_min_fft'] = pd.Series(z_fft).apply(lambda x: x.min())

        # FFT max
        X_pred['x_max_fft'] = pd.Series(x_fft).apply(lambda x: x.max())
        X_pred['y_max_fft'] = pd.Series(y_fft).apply(lambda x: x.max())
        X_pred['z_max_fft'] = pd.Series(z_fft).apply(lambda x: x.max())

        # FFT max-min diff
        X_pred['x_maxmin_diff_fft'] = X_pred['x_max_fft'] - X_pred['x_min_fft']
        X_pred['y_maxmin_diff_fft'] = X_pred['y_max_fft'] - X_pred['y_min_fft']
        X_pred['z_maxmin_diff_fft'] = X_pred['z_max_fft'] - X_pred['z_min_fft']

        # FFT median
        X_pred['x_median_fft'] = pd.Series(x_fft).apply(lambda x: np.median(x))
        X_pred['y_median_fft'] = pd.Series(y_fft).apply(lambda x: np.median(x))
        X_pred['z_median_fft'] = pd.Series(z_fft).apply(lambda x: np.median(x))

        # FFT median abs dev 
        X_pred['x_mad_fft'] = pd.Series(x_fft).apply(lambda x: np.median(np.absolute(x - np.median(x))))
        X_pred['y_mad_fft'] = pd.Series(y_fft).apply(lambda x: np.median(np.absolute(x - np.median(x))))
        X_pred['z_mad_fft'] = pd.Series(z_fft).apply(lambda x: np.median(np.absolute(x - np.median(x))))

        # FFT Interquartile range
        X_pred['x_IQR_fft'] = pd.Series(x_fft).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
        X_pred['y_IQR_fft'] = pd.Series(y_fft).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
        X_pred['z_IQR_fft'] = pd.Series(z_fft).apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))

        # FFT values above mean
        X_pred['x_above_mean_fft'] = pd.Series(x_fft).apply(lambda x: np.sum(x > x.mean()))
        X_pred['y_above_mean_fft'] = pd.Series(y_fft).apply(lambda x: np.sum(x > x.mean()))
        X_pred['z_above_mean_fft'] = pd.Series(z_fft).apply(lambda x: np.sum(x > x.mean()))

        # FFT number of peaks
        X_pred['x_peak_count_fft'] = pd.Series(x_fft).apply(lambda x: len(find_peaks(x)[0]))
        X_pred['y_peak_count_fft'] = pd.Series(y_fft).apply(lambda x: len(find_peaks(x)[0]))
        X_pred['z_peak_count_fft'] = pd.Series(z_fft).apply(lambda x: len(find_peaks(x)[0]))

        # FFT skewness
        X_pred['x_skewness_fft'] = pd.Series(x_fft).apply(lambda x: stats.skew(x))
        X_pred['y_skewness_fft'] = pd.Series(y_fft).apply(lambda x: stats.skew(x))
        X_pred['z_skewness_fft'] = pd.Series(z_fft).apply(lambda x: stats.skew(x))

        # FFT kurtosis
        X_pred['x_kurtosis_fft'] = pd.Series(x_fft).apply(lambda x: stats.kurtosis(x))
        X_pred['y_kurtosis_fft'] = pd.Series(y_fft).apply(lambda x: stats.kurtosis(x))
        X_pred['z_kurtosis_fft'] = pd.Series(z_fft).apply(lambda x: stats.kurtosis(x))

        # FFT energy
        X_pred['x_energy_fft'] = pd.Series(x_fft).apply(lambda x: np.sum(x**2)/50)
        X_pred['y_energy_fft'] = pd.Series(y_fft).apply(lambda x: np.sum(x**2)/50)
        X_pred['z_energy_fft'] = pd.Series(z_fft).apply(lambda x: np.sum(x**2/50))

        # FFT avg resultant
        X_pred['avg_result_accl_fft'] = [i.mean() for i in ((pd.Series(x_fft)**2 + pd.Series(y_fft)**2 + pd.Series(z_fft)**2)**0.5)]

        # FFT Signal magnitude area
        X_pred['sma_fft'] = pd.Series(x_fft).apply(lambda x: np.sum(abs(x)/50)) + pd.Series(y_fft).apply(lambda x: np.sum(abs(x)/50)) \
                            + pd.Series(z_fft).apply(lambda x: np.sum(abs(x)/50))


        # calculating max & min indices

        # index of max value in time domain
        X_pred['x_argmax'] = pd.Series(x_list).apply(lambda x: np.argmax(x))
        X_pred['y_argmax'] = pd.Series(y_list).apply(lambda x: np.argmax(x))
        X_pred['z_argmax'] = pd.Series(z_list).apply(lambda x: np.argmax(x))

        # index of min value in time domain
        X_pred['x_argmin'] = pd.Series(x_list).apply(lambda x: np.argmin(x))
        X_pred['y_argmin'] = pd.Series(y_list).apply(lambda x: np.argmin(x))
        X_pred['z_argmin'] = pd.Series(z_list).apply(lambda x: np.argmin(x))

        # absolute difference between above indices
        X_pred['x_arg_diff'] = abs(X_pred['x_argmax'] - X_pred['x_argmin'])
        X_pred['y_arg_diff'] = abs(X_pred['y_argmax'] - X_pred['y_argmin'])
        X_pred['z_arg_diff'] = abs(X_pred['z_argmax'] - X_pred['z_argmin'])

        # index of max value in frequency domain
        X_pred['x_argmax_fft'] = pd.Series(x_fft).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
        X_pred['y_argmax_fft'] = pd.Series(y_fft).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))
        X_pred['z_argmax_fft'] = pd.Series(z_fft).apply(lambda x: np.argmax(np.abs(np.fft.fft(x))[1:51]))

        # index of min value in frequency domain
        X_pred['x_argmin_fft'] = pd.Series(x_fft).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
        X_pred['y_argmin_fft'] = pd.Series(y_fft).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))
        X_pred['z_argmin_fft'] = pd.Series(z_fft).apply(lambda x: np.argmin(np.abs(np.fft.fft(x))[1:51]))

        # absolute difference between above indices
        X_pred['x_arg_diff_fft'] = abs(X_pred['x_argmax_fft'] - X_pred['x_argmin_fft'])
        X_pred['y_arg_diff_fft'] = abs(X_pred['y_argmax_fft'] - X_pred['y_argmin_fft'])
        X_pred['z_arg_diff_fft'] = abs(X_pred['z_argmax_fft'] - X_pred['z_argmin_fft'])


        rf = RandomForestClassifier(random_state = 21)
        model = joblib.load("model.pkl")
        pred = model.predict(X_pred)


        # logic to get snacking and eating data
        snacking = ['Snacking on chocolate bar', 'Snacking on chips']
        eating = ['Snacking on chocolate bar', 'Snacking on chips', 'Eating soup']

        sampling_rate = 20 
        seg_min = [length/sampling_rate/60 for length in seg_length]
        snack_total = 0
        eat_total = 0
        for i in range(len(pred)):
          if (pred[i] in eating):
            eat_total += seg_min[i]
            if (pred[i] in snacking):
              snack_total += seg_min[i]

        date = datetime.date.today().strftime('%Y%m%d')

        
        # save to Supabase database
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        supabase = create_client(url, key)

        response = (
            supabase.table("snackingdata").insert({
                "watchid": "Areta", 
                "date": date, 
                "activitytype": "Snacking", 
                "duration": snack_total 
            }).execute()
        )
        responseTwo = (
            supabase.table("snackingdata").insert({
                "watchid": "Areta", 
                "date": date, 
                "activitytype": "Eating",
                "duration": eat_total 
            }).execute()
        )

        return f"Saved"
    except Exception as e:
        return f"Error: {str(e)}"

func = gr.Interface(fn=predict, inputs="text", outputs="text")
func.launch()


