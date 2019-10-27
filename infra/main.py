#!/usr/bin/python3

import subprocess
import scipy.io.wavfile as wavfile

import pio
import tune


def main(input_wav, prediction_mid_name):

    # Setup useful variables
    cpp_input = "input"
    cpp_output = f"{cpp_input}_tuned"
    output_wav = f'{".".join(input_wav.split(".")[:-1])}_tuned.wav'

    print("Processing...")

    # Find optimal tunings from the midi file
    midi = pio.load_midi(prediction_mid_name)
    pio.parse_and_write_to_file(midi, cpp_input)
    subprocess.run(["c++/freqs", cpp_input], check=True)
    tuned_score = pio.read_tuned_file(cpp_output)
    subprocess.run(["rm", cpp_input, cpp_output], check=True)
    tunings = tune.tunings_at_events(midi, tuned_score)

    print("Tuning...")

    # Tune the wav file based on the tunings found
    fs, data = wavfile.read(input_wav)
    new_data = tune.tune(data, fs, tunings)
    wavfile.write(output_wav, fs, new_data)

    print()
    print("Done")
    print()


if __name__ == "__main__":
    main("mazurka.wav", "prediction.mid")
