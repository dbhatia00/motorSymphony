import mido

'''
This file will strip out the notes that we need to play from the midi file
Will packetize and figure out how to ship to Arduino
'''

midi_file = mido.MidiFile('audioTestFiles/Thunderstrick.midi')

note_events = []

for track in midi_file.tracks:
    for msg in track:
        if msg.type in ['note_on', 'note_off']:
            note_events.append({
                'time': msg.time,                   # The time delta since the previous note
                'note': msg.note,                   # The MIDI note number associated with the event.
                'velocity': msg.velocity,           # The velocity (or intensity) of the note event
                'type': msg.type                    # The type of MIDI message (either "note_on" or "note_off")
            })

print(note_events)