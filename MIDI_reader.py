import mido
from rtmidi2 import MidiIn, NOTEON, CC, splitchannel
import time
class MIDIReader:
    def __init__(self,):
        self.active_keys = set()
        self.midiin = MidiIn()
        self.midiin.open_port()  # Get messages from default port
        self.chords = {
    (69, 73, 76): "A Major",
    (69, 72, 76): "A Minor",
    (71, 75, 78): "B Major",
    (71, 74, 78): "B Minor",
    (60, 64, 67): "C Major",
    (60, 63, 67): "C Minor",
    (62, 66, 69): "D Major",
    (62, 65, 69): "D Minor",
    (64, 68, 71): "E Major",
    (64, 67, 71): "E Minor",
    (65, 69, 72): "F Major",
    (65, 68, 72): "F Minor",
    (67, 71, 74): "G Major",
    (67, 70, 74): "G Minor",
    (68, 72, 75): "Ab Major",
    (68, 71, 75): "Ab Minor",
    (70, 74, 77): "Bb Major",
    (70, 73, 77): "Bb Minor",
    (61, 65, 68): "Db Major",
    (61, 64, 68): "Db Minor",
    (63, 67, 70): "Eb Major",
    (63, 66, 70): "Eb Minor",
    (66, 70, 73): "Gb Major",
    (66, 69, 73): "Gb Minor"
}
        self.all_chords = {
    "A Major": [69, 73, 76], "A Minor": [69, 72, 76],
    "B Major": [71, 75, 78], "B Minor": [71, 74, 78],
    "C Major": [60, 64, 67], "C Minor": [60, 63, 67],
    "D Major": [62, 66, 69], "D Minor": [62, 65, 69],
    "E Major": [64, 68, 71], "E Minor": [64, 67, 71],
    "F Major": [65, 69, 72], "F Minor": [65, 68, 72],
    "G Major": [67, 71, 74], "G Minor": [67, 70, 74],
    "Ab Major": [68, 72, 75], "Ab Minor": [68, 71, 75],
    "Bb Major": [70, 74, 77], "Bb Minor": [70, 73, 77],
    "Db Major": [61, 65, 68], "Db Minor": [61, 64, 68],
    "Eb Major": [63, 67, 70], "Eb Minor": [63, 66, 70],
    "Gb Major": [66, 70, 73], "Gb Minor": [66, 69, 73]
}
        self.NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def midi_note_to_name(self,note: int):
        if note is None:
            return ''
        try:
            n = int(note)
        except (TypeError, ValueError):
            return ''
        if n < 0 or n > 127:
            return ''
        name = self.NOTE_NAMES[n % 12]
        return f"{name}"
    def check_chord(self):
        keys_list = list(self.active_keys)
        keys_list.sort()
        print(f"Current active keys for chord detection: {keys_list}")
        chords = self.all_chords.values()
        if keys_list in chords:
            chord = [name for name, notes in self.all_chords.items() if notes == keys_list][0]
            print(f"Detected Chord: {chord}")
    def callback(self,msg: list, timestamp: float):
        time.sleep(0.01)

        # message is a list of 1-byte strings
        # timestamp is a float with the time elapsed since the previous message
        msgtype, channel = splitchannel(msg[0])
        if msgtype == NOTEON:
            self.active_keys.add(msg[1])
            note = msg[1]
            velocity = msg[2]
            note_name = self.midi_note_to_name(note)
            #print(f"Note On: Channel {channel}, Note {note} ({note_name}), Velocity {velocity} at {timestamp:.2f}s")
        elif msg[0] == 128: # note off 
            if msg[1] in self.active_keys:
                self.active_keys.remove(msg[1])

        print(f"Active keys: {[self.midi_note_to_name(n) for n in self.active_keys]}")
        self.check_chord()
##############IGNORE FOR NOW##############
    # elif msgtype == CC:
    #     controller = msg[1]
    #     value = msg[2]
    #     print(f"Control Change: Channel {channel}, Controller {controller}, Value {value}")
    def start_listening(self):
        self.midiin.callback = self.callback



        try:
            print("Listening for MIDI input... Press Ctrl-C to exit.")
            while True:
                pass  # Keep the script running to listen for MIDI messages
        except KeyboardInterrupt:
            print("Exiting...")
            self.midiin.close_port()

piano = MIDIReader()
piano.start_listening()