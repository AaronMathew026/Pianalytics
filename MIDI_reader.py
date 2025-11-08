import mido
from rtmidi2 import MidiIn, NOTEON, CC, splitchannel
import time
class MIDIReader:
    def __init__(self,):
        self.active_keys = set()
        self.midiin = MidiIn()
        try:
            self.midiin.open_port()  # Get messages from default port
        except Exception as e:
            print(f"Error opening MIDI port: {e}")

        # background thread control
        self._running = False
        self._thread = None
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
        self.scales = {
        "C Major":   (60, 62, 64, 65, 67, 69, 71),
        "C Minor":   (60, 62, 63, 65, 67, 68, 71),
        "D Major":   (62, 64, 66, 67, 69, 71, 73),
        "D Minor":   (62, 64, 65, 67, 69, 70, 73),
        "E Major":   (64, 66, 68, 69, 71, 73, 76),
        "E Minor":   (64, 66, 67, 69, 71, 72, 76),
        "F Major":   (65, 67, 69, 70, 72, 74, 77),
        "F Minor":   (65, 67, 68, 70, 72, 73, 77),
        "G Major":   (67, 69, 71, 72, 74, 76, 79),
        "G Minor":   (67, 69, 70, 72, 74, 75, 79),
        "Ab Major":  (68, 70, 72, 73, 75, 77, 80),
        "Ab Minor":  (68, 70, 71, 73, 75, 76, 80),
        "Bb Major":  (70, 72, 74, 75, 77, 79, 82),
        "Bb Minor":  (70, 72, 73, 75, 77, 78, 82),
        "Db Major":  (61, 63, 65, 66, 68, 70, 73),
        "Db Minor":  (61, 63, 64, 66, 68, 69, 73),
        "Eb Major":  (63, 65, 67, 68, 70, 72, 75),
        "Eb Minor":  (63, 65, 66, 68, 70, 71, 75),
        "Gb Major":  (66, 68, 70, 71, 73, 75, 78),
        "Gb Minor":  (66, 68, 69, 71, 73, 74, 78),
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
        if not self.active_keys:
            return
        key = tuple(sorted(self.active_keys))
        if key in self.chords:
            #print("chord detected")
            #print(f"Detected Chord: {self.chords[key]}")
            return self.chords[key]
    def check_scale(self,scale):
        notes= list(scale)
        while True:
                if len(scale) == 0:
                    print("Scale completed!")
                    return True
                current_key_to_play = notes.pop(0)
                print(f"Please play the next note in the scale: {self.midi_note_to_name(current_key_to_play)}")
                if not self.active_keys:
                    if self.active_keys.pop(0) == current_key_to_play:
                        print("Correct note played in scale!")
                    else:
                        print("Incorrect note played in scale.")
                        return False



    def callback(self,msg: list, timestamp: float):
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

       # print(f"Active keys: {[self.midi_note_to_name(n) for n in self.active_keys]}")
        self.check_chord()
##############IGNORE FOR NOW##############
    # elif msgtype == CC:
    #     controller = msg[1]
    #     value = msg[2]
    #     print(f"Control Change: Channel {channel}, Controller {controller}, Value {value}")
    def start_listening(self):
        self.midiin.callback = self.callback

        if self._running:
            # already running
            return

        self._running = True

        def _loop():
            try:
                print("Listening for MIDI input (background)... Press stop to exit.")
                while self._running:
                    time.sleep(0.1)
            finally:
                try:
                    self.midiin.close_port()
                except Exception:
                    pass

        import threading
        self._thread = threading.Thread(target=_loop, daemon=True)
        self._thread.start()

    def stop_listening(self):
        if not self._running:
            return
        self._running = False
        # give the thread a moment to finish
        if self._thread is not None:
            self._thread.join(timeout=1.0)
            self._thread = None