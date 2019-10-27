import numpy as np


class TunedNote:
    def __init__(self, pitch, octave, duration, start_beat, freq):
        self.pitch = int(pitch)
        self.octave = int(octave)
        self.duration = int(duration)
        self.start_beat = int(start_beat)
        self.freq = float(freq)

    def __repr__(self):
        return f"{self.pitch} {self.octave} {self.duration} {self.start_beat} {self.freq}"


class TunedScore:
    def __init__(self):
        self.score = {}

    def max_beat(self):
        return max(self.score.keys())

    def add(self, tuned_note):
        for t in range(tuned_note.start_beat, tuned_note.start_beat + tuned_note.duration):
            if t not in self.score:
                self.score[t] = {}
            self.score[t][(tuned_note.pitch, tuned_note.octave)] = tuned_note.freq
        return self


def get_eq_freq(pitch, octave):
    semitones = octave * 12 + pitch - 57
    return 440 * (np.power(2, semitones / 12))


def get_note_and_octave_from_midi_note(note):
    return note % 12, note // 12 - 1

