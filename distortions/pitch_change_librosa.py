import librosa
import numpy as np
import soundfile as sf
import os
from os import path

# ../audio/samples/original contains folders labeled with the names of
# various artists.
samples_dir = "../audio/samples/vocals/"
edited_dir = "../audio/samples/edited/"

for name in os.listdir(samples_dir):
    for sample_name in os.listdir(samples_dir + name):
        sample_path = path.join(samples_dir, name, sample_name)

        # y is a numpy array of the wav file, sr = sample rate (1/s)
        wav, sr = librosa.load(sample_path, sr=44100)

        # Apply pitch shifts in + and - directions:

        # [num_intervals] should be an odd number for symmetric pitch shifting
        num_intervals = 11

        # Units = semitones (floats accepted)
        max_shift = 3

        steps = np.linspace(-max_shift, max_shift, num_intervals)

        output_dir = os.path.join(edited_dir, name[:-4], sample_name)
        if not path.exists(output_dir):
            os.makedirs(output_dir)

        for file in [path.join(output_dir, f) for f in os.listdir(output_dir)]:
            os.remove(file)

        for step in steps:
            shifted_wav = librosa.effects.pitch_shift(
                wav, sr, n_steps=step, res_type='fft')
            sf.write(
                path.join(
                    output_dir,
                    'pitch' +
                    ("+" if step > 0 else "") + str(round(step, 2)) +
                    '.wav'
                ), shifted_wav, 44100, 'PCM_24'
            )
