import sys
import librosa
import librosa.display
import os
import numpy as np
# from config import *
from statistics import mean

LABELS = {
    '01_a': 1,
    '02_da': 2,
    '03_dha': 3,
    '04_dhat': 4,
    '05_dhi': 5,
    '06_dhin': 6,
    '07_dhit': 7,
    '08_ding': 8,
    '09_e': 9,
    '10_gadu': 10,
    '11_gin': 11,
    '12_ha': 12,
    '13_hat': 13,
    '14_hi': 14,
    '15_jag': 15,
    '16_jham': 16,
    '17_ka': 17,
    '18_ki': 18,
    '19_ku': 19,
    '20_na': 20,
    '21_ri': 21,
    '22_ta': 22,
    '23_tak': 23,
    '24_tam': 24,
    '25_tan': 25,
    '26_tat': 26,
    '27_tei': 27,
    '28_tom': 28,
    '29_tta': 29,
    '30_ya': 30,
    '31_yum': 31,
    '32_stickbeats': 32
}

train_data = []
count = 0
curr_loc = 'C:\\Users\\hp\\Desktop\\BTP_stuff\\Data_Session_1\\Audio Data Set for Shubham\\0. Bol Recognizer\\All_TrainWordss'
for subdir, dirs, files in os.walk(curr_loc):
    print(subdir)
    for file in files:
        curr_file = str(os.path.join(subdir, file))
        if curr_file[-3:] == 'wav':
            x, sr = librosa.load(curr_file)
            sum = 0
            for i in x:
                sum = sum + i
            curr_mean = sum / len(x)
            x = np.array([i - curr_mean for i in x])
            mfccs = list(np.mean(librosa.feature.mfcc(y=x, sr=sr, n_mfcc=40).T, axis=0))
            mfccs_delta = list(librosa.feature.delta(mfccs))
            mfccs_delta2 = list(librosa.feature.delta(mfccs, order=2))
            features = mfccs + mfccs_delta + mfccs_delta2
            # feature has a dimension of 120x1 containg all important features
            train_data.append([features, LABELS[str(subdir.split('\\')[-1])]])  # features

import pandas as pd

train_data_df = pd.DataFrame(train_data, columns=['Features', 'class_label'])
train_data_df.to_csv('Training_Data.csv')


test_data = []
curr_loc = 'C:\\Users\\hp\\Desktop\\BTP_stuff\\Data_Session_1\\Audio Data Set for Shubham\\0. Bol Recognizer\\All_testWords'
for subdir, dirs, files in os.walk(curr_loc):
    print(subdir)
    for file in files:
        curr_file = str(os.path.join(subdir, file))
        if curr_file[-3:] == 'wav':
            x, sr = librosa.load(curr_file)
            sum = 0
            for i in x:
                sum = sum + i
            curr_mean = sum / len(x)
            x = np.array([i - curr_mean for i in x])
            mfccs = list(
                np.mean(librosa.feature.mfcc(y=x, sr=sr, n_mfcc=40).T, axis=0))  # n_mfcc can be a hyper-parameter
            mfccs_delta = list(librosa.feature.delta(mfccs))
            mfccs_delta2 = list(librosa.feature.delta(mfccs, order=2))
            features = mfccs + mfccs_delta + mfccs_delta2
            # feature has a dimension of 120x1 containg all important features
            test_data.append([features, LABELS[str(subdir.split('\\')[-1])]])


import pandas as pd

test_data_df = pd.DataFrame(test_data, columns=['Features', 'class_label'])
test_data_df.to_csv('Testing_Data.csv')

import pandas as pd

train_data_df = pd.read_csv('Training_Data.csv')
test_data_df = pd.read_csv('Testing_Data.csv')

total_data = pd.concat([train_data_df, test_data_df])
total_data = total_data.drop(columns=[total_data.columns[0]])
total_data = total_data.reset_index(drop=True)
final_data = []
for i in range(len(total_data)):
    feat = total_data.iloc[i][0][1:-2].split(',')
    feat = [float(feat[j]) for j in range(len(feat))]
    final_data.append([feat, total_data.iloc[i][1]])
final_data = pd.DataFrame(final_data, columns=['Features', 'class_label'])
final_data.to_csv('Total_Data.csv')
