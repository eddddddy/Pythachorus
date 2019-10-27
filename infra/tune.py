import numpy as np

import utils
import pitch_shift


def tunings_at_events(midi, tuned_score):
    """
    Return a list of [pitches, freqs, time_diff] triples at each midi event.
    Relies on the fact that midi events are in order.
    """
    tunings = []

    curr_pitches = set()
    curr_time = 1
    acc_time_diff = 0
    msgs_in_batch = []

    for track in midi.tracks:
        for msg in track:
            if msg.type not in ['note_on', 'note_off']:
                continue

            if msg.time == 0 or not msgs_in_batch:
                msgs_in_batch.append(msg)
                continue

            if curr_pitches:
                curr_time += 1

            for m in msgs_in_batch:
                if m.type == 'note_off' or m.velocity == 0:
                    curr_pitches.remove(utils.get_note_and_octave_from_midi_note(m.note))
                else:
                    curr_pitches.add(utils.get_note_and_octave_from_midi_note(m.note))

            if not curr_pitches:
                acc_time_diff = msgs_in_batch[0].time
                msgs_in_batch = [msg]
                continue

            pitches = list(curr_pitches)
            freqs = [tuned_score.score[curr_time][p] for p in pitches]
            tunings.append([pitches, freqs, (acc_time_diff + msgs_in_batch[0].time) / (midi.ticks_per_beat * 2)])

            msgs_in_batch = [msg]
            acc_time_diff = 0

    return tunings


def tune(data, fs, tunings):
    tuned_data = []
    curr_sample = 0

    curr_sample += int(fs * tunings[0][2])
    tuned_data.extend(data[:curr_sample])
    tuned_data = np.array(tuned_data)

    for i in range(len(tunings)):
        sub_data = []
        if i == len(tunings) - 1:
            sub_data = data[curr_sample:]
        else:
            inc = int(fs * tunings[i + 1][2])
            sub_data = data[curr_sample : curr_sample + inc]
            curr_sample += inc
        correct_sub_data = pitch_shift.correct_data(sub_data, fs, tunings[i][0], tunings[i][1])
        tuned_data = np.append(tuned_data, correct_sub_data, axis=0)

    return tuned_data

