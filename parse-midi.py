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
                'time': msg.time,
                'note': msg.note,
                'velocity': msg.velocity,
                'type': msg.type
            })

print(note_events)