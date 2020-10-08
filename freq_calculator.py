import wave
import matplotlib.pyplot as plt
import pylab
import numpy as np

class freqCalculator:
    @staticmethod
    def get_frequency(sound_info, frame_rate):
        # sound_info, frame_rate = get_wav_info(wav_file)
        spectrum, freqs, t, im = plt.specgram(sound_info, Fs=frame_rate, NFFT=128, noverlap=64, pad_to=512)
        # plt.show()
        # print(freqs[1]-freqs[0])
        max_index_col = np.argmax(spectrum, axis=0)
        # bol_frequencies.append(freqs[stats.mode(max_index_col)[0][0]])
        spectrum = np.transpose(spectrum)
        avg_index_col = []
        print(freqs[1] - freqs[0])
        for j in range(len(spectrum) - 1):
            weights = np.array([k for k in range(len(spectrum[j]))])
            avg_index_col.append(np.average(weights, weights=spectrum[j]))
        if len(avg_index_col) == 0:
            return -1
        # print(stats.mode(max_index_col)[0][0], round(np.average(avg_index_col)))
        return freqs[round(np.average(avg_index_col))]