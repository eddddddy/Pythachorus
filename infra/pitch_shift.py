import numpy as np
from scipy.signal import butter, sosfiltfilt, hilbert
from scipy.fftpack import next_fast_len

import utils


FS = -1
SEMITONE_FILTERS = []


def create_filter(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    return butter(order, [low, high], analog=False, btype='band', output='sos')


def apply_filter(data, filt):
    if len(data.shape) == 1:
        return sosfiltfilt(filt, data)
    else:
        return np.stack([sosfiltfilt(filt, data[:][:,0]), sosfiltfilt(filt, data[:][:,1])], axis=-1)


def fast_hilbert(data):
    return hilbert(data, next_fast_len(len(data)))[:len(data)]


def get_semitone_filters(fs, order=5):
    """
    Access the filter by: f = filters[pitch][octave]
    """
    filters = []
    for pitch in range(12):
        filters_by_pitch = []
        for octave in range(9):
            # it doesn't matter if pitch goes below 0 or above 11,
            #   since this function is robust
            lowcut = utils.get_eq_freq(pitch, octave) * np.power(2, -1 / 24)
            highcut = utils.get_eq_freq(pitch, octave) * np.power(2, 1 / 24)
            filters_by_pitch.append(create_filter(lowcut, highcut, fs, order=order))
        filters.append(filters_by_pitch)
    return filters


def freq_shift(data, shift, fs):
    if len(data.shape) == 1:
        U = hilbert(data)
        X1, X2 = np.real(U), np.imag(U)

        L = np.array(range(len(data))) / fs * 2 * np.pi * shift
        M1, M2 = np.cos(L), np.sin(L)

        return X1 * M1 - X2 * M2
    else:
        U1, U2 = fast_hilbert(data[:][:,0]), fast_hilbert(data[:][:,1])
        X11, X21, X12, X22 = np.real(U1), np.imag(U1), np.real(U2), np.imag(U2)

        L = np.array(range(len(data))) / fs * 2 * np.pi * shift
        M1, M2 = np.cos(L), np.sin(L)

        return np.stack([X11 * M1 - X21 * M2, X12 * M1 - X22 * M2], axis=1)


def correct_data(data, fs, pitches, freqs):
    """
    data must have dtype as int16
    return value is also in int16
    """
    global FS
    global SEMITONE_FILTERS
    if fs != FS:
        FS = fs
        SEMITONE_FILTERS = get_semitone_filters(fs)
    
    data = data / 32767.0

    filtered_data = np.zeros(data.shape)
    corrected_filtered_data = np.zeros(data.shape)
    for i in range(len(pitches)):
        filtered = apply_filter(data, SEMITONE_FILTERS[pitches[i][0]][pitches[i][1]])
        filtered_data += filtered
        corrected = freq_shift(filtered, freqs[i] - utils.get_eq_freq(pitches[i][0], pitches[i][1]), fs)
        corrected_filtered_data += corrected

    residue = data - filtered_data
    corrected = corrected_filtered_data + residue
    return np.asarray(corrected * 32767, dtype=np.int16)
   
    """ 
    # Get a dict of unique pitches mapping to the lowest octave they occur
    pitch_octave_map = {}
    for pitch in pitches:
        if ((pitch[0] in pitch_octave_map and pitch[1] < pitch_octave_map[pitch[0]]) or
            pitch[0] not in pitch_octave_map):
                pitch_octave_map[pitch[0]] = pitch[1]

    filtered_data = np.zeros(data.shape)
    corrected_filtered_data = np.zeros(data.shape)
    for pitch, lowest_octave in pitch_octave_map.items():
        shift_amount = freqs[pitches.index((pitch, lowest_octave))] - utils.get_eq_freq(pitch, lowest_octave)
        for octave in range(lowest_octave, 9):
            filtered = apply_filter(data, SEMITONE_FILTERS[pitch][octave])
            filtered_data += filtered
            corrected_filtered_data += freq_shift(filtered, shift_amount * np.power(2, octave - lowest_octave), fs)
        
    residue = data - filtered_data
    corrected = corrected_filtered_data + residue
    return np.asarray(corrected * 32767, dtype=np.int16)
    """

