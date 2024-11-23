import pandas as pd

# Converts MIDI note to frequency in Hz using formula
# https://inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
# https://newt.phys.unsw.edu.au/jw/notes.html
def midi_to_frequency(midi_note):
    return 440.0 * (2 ** ((midi_note - 69) / 12))

# return a csv containing frequency (no modifications to start_time & end_time)
def freq_to_csv(csv_file_path, output_file_path):
    df = pd.read_csv(csv_file_path)
    
    # Convert the 'Note' column to freq and rename it
    df['Freq'] = df['Note'].apply(midi_to_frequency)
    df.drop(columns=['Note'], inplace=True)
    
    # Save the updated df to a new CSV file
    df.to_csv(output_file_path, index=False)

def csv_to_arduino_struct(csv_file_path, output_file_path):
    df = pd.read_csv(csv_file_path)
    
    # Start struct array as string
    struct_code = "struct Note {\n    int frequency;\n    float timeOn;\n    float timeOff;\n};\n\n"
    struct_code += "Note noteSchedule[] = {\n"
    
    # Format each row into struct syntax
    for index, row in df.iterrows():
        frequency = row['Freq']
        time_on = row['Time On (s)']
        time_off = row['Time Off (s)']
        struct_code += f"    {{ {frequency}, {time_on}, {time_off} }},\n"
    
    # Remove trailing comma & newline
    struct_code = struct_code.rstrip(",\n")  
    struct_code += "\n};\n"
    
    # Write struct code to a txt file
    with open(output_file_path, 'w') as file:
        file.write(struct_code)

