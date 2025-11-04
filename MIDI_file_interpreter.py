from mido import MidiFile
class MIDIFileInterpreter:
    def __init__(self, file_path):
        self.midi = MidiFile(file_path)
        self.treble_notes = self.midi.tracks[0]  # Assuming track 1 is treble
        self.bass_notes = self.midi.tracks[1]    # Assuming track 2 is bass
    def get_treble_notes(self):
        return [(msg.note, msg.velocity, msg.time) for msg in self.treble_notes if msg.type == 'note_on']
    def get_bass_notes(self):
        return [(msg.note, msg.velocity, msg.time) for msg in self.bass_notes if msg.type == 'note_on']

file = MIDIFileInterpreter("test.mid")#

print(file.get_treble_notes())