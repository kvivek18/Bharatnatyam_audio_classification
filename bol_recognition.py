import pandas as pd

train_data_df = pd.read_csv('C:/Users/hp/BTP_data_features/Training_Data_NN.csv')
test_data_df = pd.read_csv('C:/Users/hp/BTP_data_features/Testing_Data_NN.csv')
total_data = pd.concat([train_data_df, test_data_df])
total_data = total_data.drop(columns=[total_data.columns[0]])
total_data = total_data.reset_index(drop=True)
final_data = []
for i in range(len(total_data)):
    feat = total_data.iloc[i][0][1:-2].split(',')
    feat = [float(feat[j]) for j in range(len(feat))]
    final_data.append([feat, total_data.iloc[i][1]])
final_data = pd.DataFrame(final_data, columns=['Features', 'class_label'])

import numpy as np

X = np.array(final_data.Features.tolist())
y = np.array(final_data.class_label.tolist())

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Support Vector Machine

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

clf = make_pipeline(StandardScaler(), SVC(kernel='rbf', gamma='auto', C=14))
clf.fit(x_train, y_train)

y_test_calc = clf.predict(x_test)
match = 0
for i in range(len(y_test)):
    if y_test[i] == y_test_calc[i]:
        match = match + 1
print('Accuracy of SVM Model is', match * 100 / len(y_test), '% ')

# calculating confusion matrix of our data

from sklearn.metrics import confusion_matrix

conf_mat = confusion_matrix(y_test, y_test_calc)

import sys
import seaborn as sb
import matplotlib.pyplot as plt

heat_map = sb.heatmap(conf_mat, vmin=0, cmap='RdBu_r', vmax=100,
                      xticklabels=['a', 'da', 'dha', 'dhat', 'dhi', 'dhin', 'dhit', 'ding', 'e', 'gadu', 'gin', 'ha',
                                   'hat', 'hi', 'jag', 'jham', 'ka', 'ki', 'ku', 'na', 'ri', 'ta', 'tak',
                                   'tam', 'tan', 'tat', 'tei', 'tom', 'tta', 'ya', 'yum'],
                      yticklabels=['a', 'da', 'dha', 'dhat', 'dhi', 'dhin', 'dhit', 'ding', 'e', 'gadu', 'gin', 'ha',
                                   'hat', 'hi', 'jag', 'jham', 'ka', 'ki', 'ku', 'na', 'ri', 'ta', 'tak',
                                   'tam', 'tan', 'tat', 'tei', 'tom', 'tta', 'ya', 'yum'])
plt.show()
