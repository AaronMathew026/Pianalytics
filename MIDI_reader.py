import mido
from rtmidi2 import MidiIn, NOTEON, CC, splitchannel

# Helper: convert MIDI note number (0-127) to name, e.g. 60 -> C4
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
# Dictionary of Major and Minor Triads with Note Letters
# The original dictionary
all_chords = {
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

# --- The Flipped Dictionary ---
# The note tuples are now the keys, and the names are the values.

chords = {
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
print("keys",chords.keys())
def midi_note_to_name(note: int):
    if note is None:
        return ''
    try:
        n = int(note)
    except (TypeError, ValueError):
        return ''
    if n < 0 or n > 127:
        return ''
    name = NOTE_NAMES[n % 12]
    return f"{name}"

active_keys = set()
midiin = MidiIn()
midiin.open_port()  # Get messages from default port
#msg is split into 3,1.keypressed[144] or released[released], 2.note, 3.velocity
def callback(msg: list, timestamp: float):

    # message is a list of 1-byte strings
    # timestamp is a float with the time elapsed since the previous message
    msgtype, channel = splitchannel(msg[0])
    if msgtype == NOTEON:
        active_keys.add(msg[1])
        note = msg[1]
        velocity = msg[2]
        note_name = midi_note_to_name(note)
        print(f"Note On: Channel {channel}, Note {note} ({note_name}), Velocity {velocity} at {timestamp:.2f}s")
    elif msg[0] == 128: # note off 
        if msg[1] in active_keys:
            active_keys.remove(msg[1])

    print(f"Active keys: {[midi_note_to_name(n) for n in active_keys]}")
    if len(active_keys) >= 3:
        chord_notes = sorted(tuple(active_keys))
        if chord_notes in chords:
            chord_name = chords[chord_notes]
            print(f"Detected Chord: {chord_name} with notes {[midi_note_to_name(n) for n in chord_notes]}")
##############IGNORE FOR NOW##############
    # elif msgtype == CC:
    #     controller = msg[1]
    #     value = msg[2]
    #     print(f"Control Change: Channel {channel}, Controller {controller}, Value {value}")
midiin.callback = callback



try:
    print("Listening for MIDI input... Press Ctrl-C to exit.")
    while True:
        pass  # Keep the script running to listen for MIDI messages
except KeyboardInterrupt:
    print("Exiting...")
    midiin.close_port()

