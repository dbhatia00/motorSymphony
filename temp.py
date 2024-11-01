import csv
from mido import Message, MidiFile, MidiTrack, bpm2tempo

# Set the ticks per beat (you can adjust this as needed)
ticks_per_beat = 480

# Function to convert seconds to ticks
def seconds_to_ticks(seconds, tempo):
    return int((seconds * 1_000_000) / tempo * ticks_per_beat)

# Read the tempo from the original MIDI file (assuming it's constant)
tempo = 429000  # Default tempo (120 BPM)

for i in range(5):
    csv_filename = f'frequency_range_{i+1}.csv'
    midi_filename = f'frequency_range_{i+1}.mid'
    
    mid = MidiFile()
    mid.ticks_per_beat = ticks_per_beat
    track = MidiTrack()
    mid.tracks.append(track)
    
    # Set the tempo
    track.append(Message('program_change', program=25, time=0))
    
    with open(csv_filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        events = []
        for row in reader:
            note = int(row['Note'])
            time_on = float(row['Time On (s)'])
            time_off = float(row['Time Off (s)'])
            events.append({'note': note, 'time': time_on, 'type': 'note_on'})
            events.append({'note': note, 'time': time_off, 'type': 'note_off'})
        
        # Sort events by time
        events.sort(key=lambda x: x['time'])
        
        current_time = 0
        for event in events:
            event_time = event['time']
            delta_time = event_time - current_time
            ticks = seconds_to_ticks(delta_time, tempo)
            current_time = event_time
            
            msg = Message(event['type'], note=event['note'], velocity=64, time=ticks)
            track.append(msg)
    
    # Save the MIDI file
    mid.save(midi_filename)
    print(f"Created MIDI file: {midi_filename}")
