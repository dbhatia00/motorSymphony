import pandas as pd

# Converts MIDI note to frequency in Hz
# https://inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
# https://newt.phys.unsw.edu.au/jw/notes.html
def midi_to_frequency(midi_note):
    return 440.0 * (2 ** ((midi_note - 69) / 12))

# return a csv containing frequency (no modifications to start_time & end_time)
def freq_to_csv(csv_file_path, output_file_path):
    df = pd.read_csv(csv_file_path)
    
    # Convert the 'Note' column to frequencies and rename it
    df['Freq'] = df['Note'].apply(midi_to_frequency)
    df.drop(columns=['Note'], inplace=True)
    
    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_file_path, index=False)

