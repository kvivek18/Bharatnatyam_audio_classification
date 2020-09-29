import os
import wave
import matplotlib.pyplot as plt
import pylab
import numpy as np
from scipy import stats
from pydub.playback import play
from pydub import AudioSegment


def graph_spectrogram(sound_info, frame_rate):
    # sound_info, frame_rate = get_wav_info(wav_file)
    spectrum, freqs, t, im = plt.specgram(sound_info, Fs=frame_rate, NFFT=128, noverlap=64, pad_to=512)
    # plt.show()
    return spectrum, freqs, t


def get_wav_info(wav_file):
    wav = wave.open(wav_file, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.fromstring(frames, 'Int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate


def chunks_calculator(signal, fs):
    threshold_times, beat_start, beat_end, beat_period, threshold_index = [], [], [], [], []
    i = 0
    while i < len(signal):
        if signal[i] > 10000:  # use 29000 if to avoid noise, 2000 if to take care of noise in other ways
            threshold_times = threshold_times + [i * 75 / 3302912]
            threshold_index = threshold_index + [i]
        i = i + 5
    count, check, i = 0, 0, 1
    curr = threshold_times[0]
    while i < len(threshold_times):
        if check == 0:
            curr = threshold_times[i]
            beat_start = beat_start + [threshold_index[i]]
            count = count + 1
            check = 1
            i = i + 1
            continue
        else:
            if threshold_times[i] - curr > 0.05:
                check = 0
                beat_end = beat_end + [threshold_index[i - 1]]
                beat_period = beat_period + [beat_end[len(beat_end) - 1] - beat_start[len(beat_start) - 1]]
                continue
            else:
                curr = threshold_times[i]
                i = i + 1
    beat_end = beat_end + [threshold_index[i - 1]]
    beat_period = beat_period + [beat_end[len(beat_end) - 1] - beat_start[len(beat_start) - 1]]
    return beat_start, beat_end, beat_period


if __name__ == '__main__':
    spf = wave.open("sample_data/5freq.wav", "r")
    signal = spf.readframes(-1)
    signal = np.fromstring(signal, "Int16")
    fs = spf.getframerate()
    time = np.linspace(0, len(signal) / fs, num=len(signal))  # Sampling rate is 44100. So time[x]-time[x-1] = 1/44100
    beat_start, beat_end, beat_period = chunks_calculator(signal, fs)
    bol_frequencies = []
    weights = np.array([k for k in range(257)])
    # len(beat_start)
    for i in range(len(beat_start)):
        spectrum, freqs, t = graph_spectrogram(signal[beat_start[i]:beat_end[i]], fs)
        max_index_col = np.argmax(spectrum, axis=0)
        # bol_frequencies.append(freqs[stats.mode(max_index_col)[0][0]])
        spectrum = np.transpose(spectrum)
        avg_index_col = []
        for j in range(len(spectrum)-1):
            avg_index_col.append(np.average(weights, weights=spectrum[j]))
        if len(avg_index_col)==0:
            continue
        # print(stats.mode(max_index_col)[0][0], round(np.average(avg_index_col)))
        bol_frequencies.append(freqs[round(np.average(avg_index_col))])
    beat_start_times = [i / 44100 for i in beat_start]
    beat_end_times = [i / 44100 for i in beat_end]
    for i in range(len(bol_frequencies)):
        print(bol_frequencies[i], beat_start_times[i], beat_end_times[i])
    plt.plot(time, signal)
    plt.show()
    # play(AudioSegment.from_wav('sample_data/kudittumettu.wav'))
