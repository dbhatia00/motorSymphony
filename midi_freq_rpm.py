import pandas as pd

# Converts MIDI note to frequency in Hz
# https://inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
# https://newt.phys.unsw.edu.au/jw/notes.html
def midi_to_frequency(midi_note):
    return 440.0 * (2 ** ((midi_note - 69) / 12))

# Converts frequency in Hz to motor speed in RPM (very unsure if correct, still reseraching)
def frequency_to_rpm(frequency):
    return frequency * 60

# Example usage with CSV
def convert_csv_to_rpm(csv_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Assuming the CSV columns are ['midi_note', 'start_time', 'end_time']
    # Convert MIDI note to frequency and then to RPM
    df['frequency'] = df['midi_note'].apply(midi_to_frequency)
    df['rpm'] = df['frequency'].apply(frequency_to_rpm)
    
    return df[['midi_note', 'frequency', 'rpm']]

