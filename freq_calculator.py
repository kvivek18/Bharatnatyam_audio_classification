import wave
import matplotlib.pyplot as plt
import pylab
import numpy as np


class freqCalculator:
    @staticmethod
    def get_frequency(sound_info, frame_rate):
        spectrum, freqs, t, im = plt.specgram(sound_info, Fs=frame_rate, NFFT=128, noverlap=64, pad_to=512)
        max_index_col = np.argmax(spectrum, axis=0)
        spectrum = np.transpose(spectrum)
        avg_index_col = []
        for j in range(len(spectrum) - 1):
            weights = np.array([k for k in range(len(spectrum[j]))])
            avg_index_col.append(np.average(weights, weights=spectrum[j]))
        if len(avg_index_col) == 0:
            return -1
        return freqs[round(np.average(avg_index_col))]