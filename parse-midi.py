import pretty_midi
import csv 

def midi_to_monophonic(input_file, output_file):
    midi_data = pretty_midi.PrettyMIDI(input_file)
    monophonic = pretty_midi.PrettyMIDI()

    for instrument in midi_data.instruments:
        # Create a new instrument for monophonic output
        mono_instrument = pretty_midi.Instrument(program=instrument.program, is_drum=instrument.is_drum)
        
        # Sort notes by start time, then keep one note at a time
        sorted_notes = sorted(instrument.notes, key=lambda n: n.start)
        last_end = 0.0
        for note in sorted_notes:
            if note.start >= last_end:  # Ensure no overlap
                mono_instrument.notes.append(note)
                last_end = note.end  # Update end time for monophonic logic
        
        # Add monophonic instrument to output
        monophonic.instruments.append(mono_instrument)

    # Write the monophonic MIDI to file
    monophonic.write(output_file)

def monophonic_midi_to_csv(input_midi, output_csv):
    # Load the monophonic MIDI file
    midi_data = pretty_midi.PrettyMIDI(input_midi)

    # Open CSV for writing
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Note', 'Time On (ms)', 'Time Off (ms)'])

        # Process each instrument in the MIDI file
        for instrument in midi_data.instruments:
            for note in instrument.notes:
                # Convert start and end times to milliseconds
                time_on_ms = int(note.start * 1000)
                time_off_ms = int(note.end * 1000)

                # Write the note data to the CSV
                writer.writerow([note.pitch, time_on_ms, time_off_ms])


# Example usage
midi_to_monophonic('audioTestFiles/mario.mid', 'tempFileDump/output_monophonic.mid')

# Example usage
monophonic_midi_to_csv('tempFileDump/output_monophonic.mid', 'tempFileDump/output.csv')