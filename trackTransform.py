import librosa
import numpy as np
from pydub import AudioSegment
import mido
from tqdm import tqdm


def mp3_to_wav(mp3_file_path, wav_output_path):
    """Converts an MP3 file to WAV format."""
    audio = AudioSegment.from_mp3(mp3_file_path)
    audio.export(wav_output_path, format="wav")


# sr = sample rate, 44100hz is cd quality and 22050hz is used for tested 
def extract_notes_from_audio(audio_file_path, sr=44100):
    """Extracts the pitches from an audio file and maps them to musical notes."""
    y, sr = librosa.load(audio_file_path, sr=sr)

    # Use librosa's pitch detection to find the fundamental frequencies
    # Adapted from https://librosa.org/doc/main/generated/librosa.piptrack.html
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)

    notes = []
    for t in tqdm(range(pitches.shape[1]), desc="Loading", unit=" items"):
        index = magnitudes[:, t].argmax()  # Get the index of the strongest pitch at each frame
        pitch = pitches[index, t]
        note = librosa.hz_to_midi(pitch)  # Convert frequency to MIDI note
        volume = int(np.clip(magnitudes[index, t] / magnitudes.max() * 127, 0, 127))  # Scale magnitude to volume (guessed at conversion here)
        notes.append((int(round(note)), volume))  # Store both note and volume

    return notes


print("Running..")
mp3_file = 'audioTestFiles/Holiday.mp3'
wav_file = 'tempFileDump/temp_output.wav'
output_midi_file = 'tempFileDump/temp_output.mid'
mp3_to_wav(mp3_file_path=mp3_file, wav_output_path=wav_file)
notes = extract_notes_from_audio(audio_file_path=wav_file)
