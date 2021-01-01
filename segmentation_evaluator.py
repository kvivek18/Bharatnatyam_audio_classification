import pathlib
import os
import shutil
import xlsxwriter
import matplotlib.pyplot as plt
import wave
import xlrd
from experience.bols_beats_seperator_failed import *
from freq_calculator import freqCalculator
import wave, struct, math, random

root_dir = 'C:\\Users\\hp\\Desktop\\BTP_stuff\\segmentation_checker\\my_seg\\SP1\\'
comp_files_list1 = []
for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        curr_file = str(os.path.join(subdir, file))
        if curr_file[-4:] == 'xlsx':
            comp_files_list1.append(curr_file)

root_dir = 'C:\\Users\\hp\\Desktop\\BTP_stuff\\segmentation_checker\\correct_seg\\SP1\\'
comp_files_list2 = []
for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        curr_file = str(os.path.join(subdir, file))
        if curr_file[-3:] == 'csv':
            comp_files_list2.append(curr_file)

total_beats = 0
miss_matches = 0

for i in range(len(comp_files_list2)):
    df_my = pd.DataFrame(pd.read_excel(comp_files_list1[i], header=None))
    df_cor = pd.read_csv(comp_files_list2[i], header=None)
    j = 0
    k = 0
    while j < len(df_my) and k < len(df_cor):
        my_beat = str(df_my.iloc[j][0])
        my_st = float(df_my.iloc[j][1])
        my_end = float(df_my.iloc[j][2])
        cor_end = float(df_cor.iloc[k][0])
        cor_st = float(df_cor.iloc[k][1])
        cor_beat = str(df_cor.iloc[k][2])
        if abs(my_st - cor_st) < 0.1 and abs(my_end - cor_end) < 0.1:
            total_beats = total_beats + 1
            if cor_beat == 'SB':
                if my_beat != 'stick beat':
                    miss_matches = miss_matches + 1
            j = j + 1
            k = k + 1
        if my_st > cor_st and my_end > cor_end:
            k = k + 1
            continue
        if cor_st > my_st and cor_end > my_end:
            j = j + 1
            continue
        else:
            total_beats = total_beats + 1
            if cor_beat == 'SB':
                if my_beat != 'stick beat':
                    miss_matches = miss_matches + 1
            j = j + 1
            k = k + 1
print(total_beats, miss_matches, (total_beats - miss_matches) * 100 / total_beats)
print(len(comp_files_list1), len(comp_files_list2))


# HM1 total = 1032 , miss_matched = 63 (93.9% accuracy)
# HM2 total = 4125 , miss_matched = 135 (96.7% accuracy)
# HM3 total = 880 , miss_matched = 18 (97.95% accuracy)
# HM4 total = 2727, miss_matched = 9 (99.7% accuracy)
# SP1 total = 2150, miss_matched = 27 (98.74% accuracy)

# TOTAL = 10914, miss_matched = 252 (97.6% accuracy)
# TODO (HM3 archives has been left out due to improper correct data) (HM4 joining_adavu_2 has been left out)
