import mido
from mido import MidiFile
import math
import csv

# Define frequency ranges and corresponding MIDI note numbers
# May wanna shift to a different range (more midrange, get rid of sub-base)
# https://www.gear4music.com/blog/audio-frequency-range/
frequency_ranges = [
    (20, 60),    # Sub-bass
    (60, 250),   # Bass
    (250, 500),  # Low Midrange
    (500, 2000), # Midrange
    (2000, 8000) # High Frequencies
]

# Converts raw frequencies to Midi Note Numbers
# https://newt.phys.unsw.edu.au/jw/notes.html
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

# Read the test MIDI file
mid = MidiFile('audioTestFiles/twinkle-twinkle-little-star.mid') 

# Identify guitar channels
guitar_channels = set()

# Map to store tempo changes
# might need this to be modular to avoid distorting the song
tempo_map = [(0, 500000)]  # Default tempo is 500,000 microseconds per beat (120 BPM)

# Time per tick
ticks_per_beat = mid.ticks_per_beat

# Function to convert ticks to seconds
def ticks_to_seconds(ticks, tempo):
    return ticks * (tempo / 1_000_000) / ticks_per_beat

# First pass: Build the tempo map and identify guitar channels
# Lots of this was stolen from https://mido.readthedocs.io/en/stable/backends/index.html
for track in mid.tracks:
    current_program = {}            # Dict for current instrument for each channel within the file
    time = 0                        # Reset time 
    for msg in track:
        time += msg.time            # Increment cumulative time with change in time
        if msg.type == 'set_tempo': 
            # Tempo change
            tempo_map.append((time, msg.tempo)) 
        elif msg.type == 'program_change':
            # Check if the program number corresponds to guitar (24-31)
            # May wanna expand to piano?
            if 24 <= msg.program <= 31:
                current_program[msg.channel] = msg.program  
                guitar_channels.add(msg.channel)
        elif msg.type == 'note_on' and msg.velocity > 0:
            # Found a guitar note that exists! Add it to the channel
            # Channel check to avoid breaking
            if msg.channel in current_program and current_program[msg.channel] in range(24, 32):
                guitar_channels.add(msg.channel)

# Sort the tempo map by time
# Found this online somewhere, don't ask
tempo_map.sort(key=lambda x: x[0])

# Function to get the current tempo at a given tick
def get_tempo_at(tick):
    tempo = tempo_map[0][1]     # first tempo
    for t, temp in tempo_map:
        if tick >= t:
            tempo = temp        # correct tempo
        else:
            break
    return tempo

# Second pass: Process the guitar notes
for track in mid.tracks:
    time = 0
    ongoing_notes = {}  # Dict to keep track of ongoing notes per channel
    for msg in track:
        time += msg.time
        if msg.type == 'set_tempo':
            continue  # Tempo changes handled in get_tempo_at()
        elif msg.type == 'note_on' and msg.velocity > 0 and msg.channel in guitar_channels:
            # Note On event
            tempo = get_tempo_at(time)                  
            time_on = ticks_to_seconds(time, tempo)     # Convert passed ticks to seconds
            note = msg.note                             # Midi Note Equiv
            ongoing_notes.setdefault(msg.channel, {})   # Ensure there's an entry for the current channel (instrument) in the dict
            ongoing_notes[msg.channel][note] = time_on  # We need the start time of the note
        elif (msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)) and msg.channel in guitar_channels:
            # Note Off event
            tempo = get_tempo_at(time)                  # Align tempo
            time_off = ticks_to_seconds(time, tempo)   
            note = msg.note

            # check if note has been started
            if msg.channel in ongoing_notes and note in ongoing_notes[msg.channel]:
                # Retrieve start time, get rid of it from ongoing note
                time_on = ongoing_notes[msg.channel].pop(note)
                
                # Determine which frequency range the note belongs to
                # Established freq conversion from midi
                frequency = 440 * (2 ** ((note - 69) / 12))
                for idx, (low_note, high_note) in enumerate(note_number_ranges):
                    if low_note <= note <= high_note:
                        # Write to the corresponding CSV file
                        csv_writers[idx].writerow([note, time_on, time_off])
                        break

# Close CSV files
for f in csv_files:
    f.close()

print("Processing complete. CSV files have been generated.")
