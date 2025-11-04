import mido
from rtmidi2 import MidiIn, NOTEON, CC, splitchannel
global simul_click
global notes 
notes = []
simul_click = []
# Helper: convert MIDI note number (0-127) to name, e.g. 60 -> C4
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

simul_click = 0.05  # seconds between simulated clicks
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


midiin = MidiIn()
midiin.open_port()  # Get messages from default port
#msg is split into 3,1.keypressed[144] or released[released], 2.note, 3.velocity
def callback(msg: list, timestamp: float):
    simul_click_time = 0.05
    # message is a list of 1-byte strings
    # timestamp is a float with the time elapsed since the previous message
    msgtype, channel = splitchannel(msg[0])
    if msgtype == NOTEON:
        note = msg[1]
        velocity = msg[2]
        note_name = midi_note_to_name(note)
        print(f"Note On: Channel {channel}, Note {note} ({note_name}), Velocity {velocity} at {timestamp:.2f}s")

    elif msgtype == CC:
        controller = msg[1]
        value = msg[2]
        print(f"Control Change: Channel {channel}, Controller {controller}, Value {value}")
midiin.callback = callback









try:
    print("Listening for MIDI input... Press Ctrl-C to exit.")
    while True:
        pass  # Keep the script running to listen for MIDI messages
except KeyboardInterrupt:
    print("Exiting...")
    midiin.close_port()

