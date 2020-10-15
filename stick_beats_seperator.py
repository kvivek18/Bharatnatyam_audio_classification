import matplotlib.pyplot as plt
import wave
from experience.bols_beats_seperator_failed import *
from freq_calculator import freqCalculator
import os

for file in os.listdir("sample_data/32_stickbeats"):
    # print("*******************************", folder, '************************************')
    # for file in os.listdir("sample_data/HM3_TrainWords/" + folder):
    print('................', file, '...............')
    # folder + "/" +
    spf = wave.open("sample_data/32_stickbeats/" + file, "r")

    # Extract Raw Audio from Wav File
    signal = spf.readframes(-1)
    signal = np.fromstring(signal, "Int16")
    fs = spf.getframerate()
    time = np.linspace(0, len(signal) / fs,
                       num=len(signal))  # Sampling rate is 44100. So time[x]-time[x-1] = 1/44100

    threshold_times, beat_start, beat_end, beat_period, threshold_index = [], [], [], [], []
    i = 0
    while i < len(signal):
        if signal[i] > 2000:  # use 29000 if to avoid noise, 2000 if to take care of noise in other ways
            threshold_times = threshold_times + [i * 75 / 3302912]
            threshold_index = threshold_index + [i]
        i = i + 5
    count_stick_beats, check, i = 0, 0, 1
    if len(threshold_times)==0:
        continue
    curr = threshold_times[0]
    while i < len(threshold_times):
        if check == 0:
            curr = threshold_times[i]
            beat_start = beat_start + [threshold_index[i]]
            count_stick_beats = count_stick_beats + 1
            check = 1
            i = i + 1
            continue
        else:
            if threshold_times[i] - curr > 0.15:
                check = 0
                beat_end = beat_end + [threshold_index[i - 1]]
                beat_period = beat_period + [beat_end[len(beat_end) - 1] - beat_start[len(beat_start) - 1]]
                continue
            else:
                curr = threshold_times[i]
                i = i + 1
    beat_end = beat_end + [threshold_index[i - 1]]
    beat_period = beat_period + [beat_end[len(beat_end) - 1] - beat_start[len(beat_start) - 1]]
    count_stick_beats = 0
    count_voice_bols = 0
    for i in range(len(beat_period)):
        curr_freq = freqCalculator.get_frequency(signal[beat_start[i]:beat_end[i]], fs)
        if curr_freq > 3200:    # Still need to check, some stick beats have freq less than 2000
            print('stick beat', beat_period[i] * 1 / 44100, beat_start[i] * 1 / 44100,
                  freqCalculator.get_frequency(signal[beat_start[i]:beat_end[i]], fs))
            count_stick_beats = count_stick_beats + 1
            continue
        if 1000 >= curr_freq > 200:
            print('voice bol', beat_period[i] * 1 / 44100, beat_start[i] * 1 / 44100,
                  freqCalculator.get_frequency(signal[beat_start[i]:beat_end[i]], fs))
            count_voice_bols = count_voice_bols + 1
            continue
        if 4000 >= curr_freq > 1000:
            print('voice+stick beat', beat_period[i] * 1 / 44100, beat_start[i] * 1 / 44100,
                  freqCalculator.get_frequency(signal[beat_start[i]:beat_end[i]], fs))
# print(len(beat_period))
# print(count_stick_beats)
#
# plt.plot(time, signal)
# plt.show()
