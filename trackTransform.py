import librosa
import numpy as np
from pydub import AudioSegment
import mido

def mp3_to_wav(mp3_file_path, wav_output_path):
    """Converts an MP3 file to WAV format."""
    audio = AudioSegment.from_mp3(mp3_file_path)
    audio.export(wav_output_path, format="wav")

print("Running applciation")
mp3_file = 'audioTestFiles/Holiday.mp3'
wav_file = 'tempFileDump/ssssssstemp_output.wav'
mp3_to_wav(mp3_file_path=mp3_file, wav_output_path=wav_file)