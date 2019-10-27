import mido

import utils


def load_midi(file_name):
    return mido.MidiFile(file_name)


def parse_and_write_to_file(midi, output_file):
    with open(output_file, 'w+') as f:

        note_to_start_beat_map = {}
        curr_beat = 1

        for track in midi.tracks:
            for msg in track:
                if msg.type not in ['note_on', 'note_off']:
                    continue

                if msg.time and note_to_start_beat_map:
                    curr_beat += 1

                pitch, octave = utils.get_note_and_octave_from_midi_note(msg.note)
                if msg.type == 'note_off' or msg.velocity == 0:
                    start_beat = note_to_start_beat_map.pop((pitch, octave))
                    duration = curr_beat - start_beat
                    f.write(f"{pitch} {octave} {duration} {start_beat}\n")
                else:
                    note_to_start_beat_map[(pitch, octave)] = curr_beat


def read_tuned_file(tuned_file):
    tuned_score = utils.TunedScore()
    with open(tuned_file, 'r') as f:
        for line in f:
            pitch, octave, duration, start_beat, freq = line.rstrip().split()
            tuned_score.add(utils.TunedNote(pitch, octave, duration, start_beat, freq))
    return tuned_score
