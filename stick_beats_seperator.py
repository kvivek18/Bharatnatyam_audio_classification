import pathlib
import os
import xlsxwriter
import matplotlib.pyplot as plt
import wave
from experience.bols_beats_seperator_failed import *
from freq_calculator import freqCalculator
import wave, struct, math, random


def get_excel_file_name(words):
    str = ''
    str = str + words[-3] + '_' + words[-2] + '_' + words[-1][:-4]
    return str


rootdir = 'C:\\Users\\hp\\Desktop\\BTP_stuff\\Data_Session_2\\SP1\\'
comp_files_list = []
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        curr_file = str(os.path.join(subdir, file))
        if curr_file[-3:] == 'wav':
            comp_files_list.append(curr_file)

reqd_dest = rootdir

for curr_file in comp_files_list:
    curr_excel_name = get_excel_file_name(curr_file.split('\\')) + '.xlsx'
    curr_excel_sheet = xlsxwriter.Workbook(reqd_dest + curr_excel_name)
    worksheet = curr_excel_sheet.add_worksheet()
    spf = wave.open(curr_file, "r")

    signal = spf.readframes(-1)
    signal = np.fromstring(signal, "Int16")
    fs = spf.getframerate()
    frames = spf.getnframes()
    rate = spf.getframerate()
    duration = frames / float(rate)
    each_it = duration / len(signal)
    n_channels = spf.getnchannels()
    samp_width = spf.getsampwidth()
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
    curr_count = 1

    # Still need to check, some stick beats have freq less than 2000

    for i in range(len(beat_period)):
        curr_freq = freqCalculator.get_frequency(signal[beat_start[i]:beat_end[i]], fs)
        if curr_freq > 3300:
            print('stick beat', beat_period[i] * each_it, beat_start[i] * each_it,
                  freqCalculator.get_frequency(signal[beat_start[i]:beat_end[i]], fs))

            # Uncomment the below code if want the bols to be stored in audio files
            # obj = wave.open(reqd_dest+'audio_chunk_'+str(curr_count)+'.wav', 'w')
            # obj.setnchannels(n_channels)  # mono
            # obj.setsampwidth(samp_width)
            # obj.setframerate(fs)
            # for l in range(beat_period[i]):
            #     value = signal[beat_start[i]+l]
            #     data = struct.pack('<h', value)
            #     obj.writeframesraw(data)
            # obj.close()

            curr_count = curr_count + 1
            worksheet.write(i, 0, 'stick beat')
            worksheet.write(i, 1, beat_start[i] * each_it)
            worksheet.write(i, 2, beat_end[i] * each_it)
            count_stick_beats = count_stick_beats + 1
            continue
        if 1000 >= curr_freq > 200:
            print('voice bol', beat_period[i] * each_it, beat_start[i] * each_it,
                  freqCalculator.get_frequency(signal[beat_start[i]:beat_end[i]], fs))
            count_voice_bols = count_voice_bols + 1

            # Uncomment the below code if want the bols to be stored in audio files
            # obj = wave.open(reqd_dest + 'audio_chunk_' + str(curr_count) + '.wav', 'w')
            # obj.setnchannels(n_channels)  # mono
            # obj.setsampwidth(samp_width)
            # obj.setframerate(fs)
            # for l in range(beat_period[i]):
            #     value = signal[beat_start[i] + l]
            #     data = struct.pack('<h', value)
            #     obj.writeframesraw(data)
            # obj.close()

            curr_count = curr_count + 1
            worksheet.write(i, 0, 'voice bol')
            worksheet.write(i, 1, beat_start[i] * each_it)
            worksheet.write(i, 2, beat_end[i] * each_it)
            continue
        if 3300 >= curr_freq > 1000:
            print('voice+stick beat', beat_period[i] * each_it, beat_start[i] * each_it,
                  freqCalculator.get_frequency(signal[beat_start[i]:beat_end[i]], fs))

            # Uncomment the below code if want the bols to be stored in audio files
            # obj = wave.open(reqd_dest + 'audio_chunk_' + str(curr_count) + '.wav', 'w')
            # obj.setnchannels(n_channels)  # mono
            # obj.setsampwidth(samp_width)
            # obj.setframerate(fs)
            # for l in range(beat_period[i]):
            #     value = signal[beat_start[i] + l]
            #     data = struct.pack('<h', value)
            #     obj.writeframesraw(data)
            # obj.close()

            curr_count = curr_count + 1
            worksheet.write(i, 0, 'voice+stick beat')
            worksheet.write(i, 1, beat_start[i] * each_it)
            worksheet.write(i, 2, beat_end[i] * each_it)

    curr_excel_sheet.close()

    # plt.plot(time, signal)
    # plt.show()
