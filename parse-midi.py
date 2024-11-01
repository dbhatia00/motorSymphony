import mido
from mido import MidiFile
import math
import csv
import sys

# Define frequency ranges and corresponding MIDI note numbers
# Reference: https://www.gear4music.com/blog/audio-frequency-range/
frequency_ranges = [
    (60, 250),      # Bass
    (250, 500),     # Low Midrange
    (500, 1000),    # Mid Midrange
    (1000, 1500),   # High Midrange
    (1500, 8000)    # High Frequencies
]

# Converts raw frequencies to MIDI note numbers
# Reference: https://newt.phys.unsw.edu.au/jw/notes.html
def frequencytoMidiNoteNum(frequency):
    return int(round(69 + 12 * math.log2(frequency / 440)))

# Function to convert ticks to seconds
def ticks_to_seconds(ticks, tempo, ticksPerBeat):
    return ticks * (tempo / 1_000_000) / ticksPerBeat

# Convert frequency ranges to MIDI note number ranges
def convertFreqNumber():
    note_number_ranges = []
    for freq_range in frequency_ranges:
        low_note = frequencytoMidiNoteNum(freq_range[0])
        high_note = frequencytoMidiNoteNum(freq_range[1])
        note_number_ranges.append((low_note, high_note))
    return note_number_ranges

# Prepare CSV writers for each frequency range
def CSVPrep():
    csv_files = []
    csv_writers = []
    for i in range(5):
        f = open(f'tempFileDump/frequency_range_{i+1}.csv', 'w', newline='')
        writer = csv.writer(f)
        writer.writerow(['Note', 'Time On (s)', 'Time Off (s)'])
        csv_files.append(f)
        csv_writers.append(writer)
    
    return csv_files, csv_writers


# First pass: Build the map of tempos and identify guitar/piano channels
# Reference: https://mido.readthedocs.io/en/stable/backends/index.html
def stripInstruments(midiFile):
    
    # Map to store tempo changes
    # Default tempo is 500,000 microseconds per beat (120 BPM (most rock songs))
    tempo_map = [(0, 500000)]  
    
    # Identify instrument channels (guitar and piano)
    instrument_channels = set()

    for track in midiFile.tracks:
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

    return tempo_map, instrument_channels

# Function to get the current tempo at a given tick
def get_tempo_at(tick, tempo_map):
    tempo = tempo_map[0][1]     # Start with the first tempo
    for t, temp in tempo_map:
        if tick >= t:
            tempo = temp        # Update to the current tempo
        else:
            break
    return tempo

# Second pass: Process the instrument notes (guitar and piano)
def processNotes(mid, instrumentChannels, tempoMap, csvWriters, noteNumberRanges, tpb):
    for track in mid.tracks:
        time = 0
        ongoing_notes = {}  # Dict to keep track of ongoing notes per channel
        for msg in track:
            time += msg.time
            if msg.type == 'set_tempo':
                continue  # Tempo changes are handled by get_tempo_at()
            elif msg.type == 'note_on' and msg.velocity > 0 and msg.channel in instrumentChannels:
                # Note On event for guitar or piano
                tempo = get_tempo_at(time, tempoMap)                  
                time_on = ticks_to_seconds(time, tempo, tpb)     # Convert ticks to seconds
                note = msg.note                             # MIDI note number
                # Ensure there's an entry for the current channel
                ongoing_notes.setdefault(msg.channel, {})
                # Record the start time of the note
                ongoing_notes[msg.channel][note] = time_on
            elif (msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)) and msg.channel in instrumentChannels:
                # Note Off event for guitar or piano
                tempo = get_tempo_at(time, tempoMap)                  # Get the current tempo
                time_off = ticks_to_seconds(time, tempo, tpb)   
                note = msg.note

                # Check if the note was previously started
                if msg.channel in ongoing_notes and note in ongoing_notes[msg.channel]:
                    # Retrieve and remove the start time from ongoing_notes
                    time_on = ongoing_notes[msg.channel].pop(note)

                    # Determine which frequency range the note belongs to
                    for idx, (low_note, high_note) in enumerate(noteNumberRanges):
                        if low_note <= note <= high_note:
                            # Write the note information to the corresponding CSV file
                            csvWriters[idx].writerow([note, time_on, time_off])
                            break


def main():
    print('Performing preprocessing on ' + sys.argv[1] + '...')

    # Some setup stuff
    noteNumberRanges = convertFreqNumber()
    csvFiles, csvWriters = CSVPrep()

    # Read the MIDI file (could grab from command line)
    if not sys.argv[1:]:
        mid = MidiFile('audioTestFiles/holiday.mid') 
    else:
        mid = MidiFile(sys.argv[1])

    # Time per tick
    ticks_per_beat = mid.ticks_per_beat

    # Strip Out all of the instruments, grab their notes, generate a sliding tempo map
    tempoMap, instrumentChannels = stripInstruments(midiFile=mid)

    # Actually process the notes, based on the channels and 
    processNotes(mid=mid, instrumentChannels=instrumentChannels, tempoMap=tempoMap, 
            csvWriters=csvWriters, noteNumberRanges=noteNumberRanges, tpb=ticks_per_beat)

    # Close CSV files
    for f in csvFiles:
        f.close()

    print("Preprocessing Stage 1 complete. CSV files have been generated.")

if __name__ == "__main__":
    main()

