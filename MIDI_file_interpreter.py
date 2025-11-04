from mido import MidiFile
class MIDIFileInterpreter:
    def __init__(self, file_path):
        self.midi = MidiFile(file_path)
        self.treble_notes = self.midi.tracks[0]  # Assuming track 1 is treble
        self.bass_notes = self.midi.tracks[1]    # Assuming track 2 is bass
        self.keys = []
    def get_treble_notes(self):
        return [(msg.note, msg.velocity, msg.time) for msg in self.treble_notes if msg.type == 'note_on']
    def get_bass_notes(self):
        return [(msg.note, msg.velocity, msg.time) for msg in self.bass_notes if msg.type == 'note_on']
    def get_notes_(self):
        self.notes = []
        for msg in self.midi:
            if msg.type == 'note_on' and msg.velocity > 0:     
                self.notes.append((msg.note))
            elif msg.type == "note_on" and msg.velocity == 0:
                if self.notes:
                    self.keys.append(self.notes)
                self.notes = []

file = MIDIFileInterpreter("test.mid")#

file.get_notes_()
print(file.keys)