# Pythachorus
An extension of [DynamicTuner](https://github.com/eddddddy/DynamicTuner "DynamicTuner") that dynamically tunes WAV files based on Pythagorean harmony.

Requires libfixeddata.a from [DynamicTuner](https://github.com/eddddddy/DynamicTuner "DynamicTuner").

The full pipeline also requires a working Magenta environment that is notoriously difficult to set up (even more so now that Python 2 has been deprecated) because of its reliance on its Onsets and Frames implementation for auto-transcribing. Currently, the program assumes that the transcription has already been done. This step of the pipeline might be added on a later date.
