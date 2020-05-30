from pydub import AudioSegment
import os

# Converts all .mp3 files in [song_dir] to .wav files.
# The .mp3 files are then deleted.
song_dir = "../audio/songs"

song_paths = [os.path.join(song_dir, s) for s in os.listdir(song_dir)]

for path in song_paths:
    filename, extension = os.path.splitext(path)
    if extension == ".mp3":
        sound = AudioSegment.from_mp3(path)
        sound.export(filename + ".wav", format="wav")
        os.remove(path)
