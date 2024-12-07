import pandas as pd

# Converts MIDI note to frequency in Hz
def midi_to_frequency(midi_note):
    return 440.0 * (2 ** ((midi_note - 69) / 12))

# Convert CSV to formatted C-style array in a text file
def freq_to_c_array(csv_file_path, output_txt_file):
    df = pd.read_csv(csv_file_path)

    # Convert the 'Note' column to frequencies
    df['Note'] = df['Note'].apply(midi_to_frequency)

    with open(output_txt_file, 'w') as f:
        f.write("// Plan list containing {frequency, start time, end time} entries\n")
        f.write("int planList[][3] = {\n")

        for _, row in df.iterrows():
            frequency = row['Note']
            time_on = int(row['Time On (ms)'])
            time_off = int(row['Time Off (ms)'])
            f.write(f"  {{{frequency:.2f}, {time_on}, {time_off}}},\n")

        # Close the array
        f.write("};\n")

freq_to_c_array('tempFileDump/output.csv', 'tempFileDump/output.txt')
