from mido import MidiFile
class MIDIFileInterpreter:
    def __init__(self, file_path):
        self.midi = MidiFile(file_path)
        for msg in self.midi.tracks[0]:
            print(msg)


file = MIDIFileInterpreter("test.mid")