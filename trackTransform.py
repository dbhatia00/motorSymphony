import librosa
import numpy as np
from pydub import AudioSegment
from tqdm import tqdm
from basic_pitch.inference import predict, Model
from basic_pitch import ICASSP_2022_MODEL_PATH
import pretty_midi
from IPython.display import Audio
import os

basic_pitch_model = Model(ICASSP_2022_MODEL_PATH)

def mp3_to_wav(mp3_file_path, wav_output_path):
    """Converts an MP3 file to WAV format."""
    audio = AudioSegment.from_mp3(mp3_file_path)
    audio.export(wav_output_path, format="wav")


# Uses the spotify basic_pitch lib - https://github.com/spotify/basic-pitch
def convert_to_midi(audio_file_path, output_dir):
    _, midi_data, _ = predict(audio_path=audio_file_path)
    # Save the MIDI data to a file
    midi_data.write(output_dir)
    print(f"MIDI file saved to: {output_dir}")


print("\n\n\n\nRunning..")
mp3_file = 'audioTestFiles/Thunderstruck.mp3'
wav_file = 'tempFileDump/temp_output.wav'
output_midi_file = 'tempFileDump/temp_output.midi'
mp3_to_wav(mp3_file_path=mp3_file, wav_output_path=wav_file)
notes = convert_to_midi(audio_file_path=wav_file, output_dir=output_midi_file)
