import mido
from mido import MidiFile
import math
import csv

# Define frequency ranges and corresponding MIDI note numbers
# Reference: https://www.gear4music.com/blog/audio-frequency-range/
frequency_ranges = [
    (60, 250),   # Bass
    (250, 500),  # Low Midrange
    (500, 1250), # Mid Midrange
    (1250, 2000), # High Midrange
    (2000, 8000) # High Frequencies
]

# Converts raw frequencies to MIDI note numbers
# Reference: https://newt.phys.unsw.edu.au/jw/notes.html
def frequency_to_midi_note_number(frequency):
    return int(round(69 + 12 * math.log2(frequency / 440)))

# Convert frequency ranges to MIDI note number ranges
note_number_ranges = []
for freq_range in frequency_ranges:
    low_note = frequency_to_midi_note_number(freq_range[0])
    high_note = frequency_to_midi_note_number(freq_range[1])
    note_number_ranges.append((low_note, high_note))

# Prepare CSV writers for each frequency range
csv_files = []
csv_writers = []
for i in range(5):
    f = open(f'frequency_range_{i+1}.csv', 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(['Note', 'Time On (s)', 'Time Off (s)'])
    csv_files.append(f)
    csv_writers.append(writer)

# Read the MIDI file
mid = MidiFile('audioTestFiles/holiday.mid') 

# Identify instrument channels (guitar and piano)
instrument_channels = set()

# Map to store tempo changes
# Default tempo is 500,000 microseconds per beat (120 BPM)
tempo_map = [(0, 500000)]  

# Time per tick
ticks_per_beat = mid.ticks_per_beat

# Function to convert ticks to seconds
def ticks_to_seconds(ticks, tempo):
    return ticks * (tempo / 1_000_000) / ticks_per_beat

# First pass: Build the map of tempos and identify guitar/piano channels
# Reference: https://mido.readthedocs.io/en/stable/backends/index.html
for track in mid.tracks:
    current_program = {}            # Dict for current instrument for each channel
    time = 0                        # Reset cumulative time for the track
    for msg in track:
        time += msg.time            # Increment cumulative time by delta time
        if msg.type == 'set_tempo': 
            # Record tempo changes with their corresponding times
            tempo_map.append((time, msg.tempo)) 
        elif msg.type == 'program_change':
            # Check if the program number corresponds to guitar (24-31) or piano (0-7)
            if (24 <= msg.program <= 31) or (0 <= msg.program <= 7):
                # Update the current program for the channel
                current_program[msg.channel] = msg.program  
                # Add the channel to the set of instrument channels
                instrument_channels.add(msg.channel)
        elif msg.type == 'note_on' and msg.velocity > 0:
            # Found a note being played
            # Ensure the channel is assigned to guitar or piano
            if msg.channel in current_program and (
                current_program[msg.channel] in range(24, 32) or
                current_program[msg.channel] in range(0, 8)
            ):
                instrument_channels.add(msg.channel)

# Sort the tempo map by time
tempo_map.sort(key=lambda x: x[0])

# Function to get the current tempo at a given tick
def get_tempo_at(tick):
    tempo = tempo_map[0][1]     # Start with the first tempo
    for t, temp in tempo_map:
        if tick >= t:
            tempo = temp        # Update to the current tempo
        else:
            break
    return tempo

# Second pass: Process the instrument notes (guitar and piano)
for track in mid.tracks:
    time = 0
    ongoing_notes = {}  # Dict to keep track of ongoing notes per channel
    for msg in track:
        time += msg.time
        if msg.type == 'set_tempo':
            continue  # Tempo changes are handled by get_tempo_at()
        elif msg.type == 'note_on' and msg.velocity > 0 and msg.channel in instrument_channels:
            # Note On event for guitar or piano
            tempo = get_tempo_at(time)                  
            time_on = ticks_to_seconds(time, tempo)     # Convert ticks to seconds
            note = msg.note                             # MIDI note number
            # Ensure there's an entry for the current channel
            ongoing_notes.setdefault(msg.channel, {})
            # Record the start time of the note
            ongoing_notes[msg.channel][note] = time_on
        elif (msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)) and msg.channel in instrument_channels:
            # Note Off event for guitar or piano
            tempo = get_tempo_at(time)                  # Get the current tempo
            time_off = ticks_to_seconds(time, tempo)   
            note = msg.note

            # Check if the note was previously started
            if msg.channel in ongoing_notes and note in ongoing_notes[msg.channel]:
                # Retrieve and remove the start time from ongoing_notes
                time_on = ongoing_notes[msg.channel].pop(note)
                
                # Calculate the frequency of the note
                frequency = 440 * (2 ** ((note - 69) / 12))
                # Determine which frequency range the note belongs to
                for idx, (low_note, high_note) in enumerate(note_number_ranges):
                    if low_note <= note <= high_note:
                        # Write the note information to the corresponding CSV file
                        csv_writers[idx].writerow([note, time_on, time_off])
                        break

# Close CSV files
for f in csv_files:
    f.close()

print("Processing complete. CSV files have been generated.")
