from MIDI_reader import MIDIReader
import random
def grab_user_input(prompt,):
    user_input = (input(prompt)).lower()
    while user_input not in ("y", "n"):
        user_input = input(f"Invalid option. Please select y or n: \n")
    if user_input == "y":
        return True
    else:
        return False

class Game_Select:
    def __init__(self):
        print("Initializing Game Modes...")
        self.piano = MIDIReader()
        pass
        
    def chord_practice(self):
        print("Starting Chord Practice mode.")
        self.piano.start_listening()
        chords = self.piano.chords.values()
        game_active = True
        while game_active:
            new_chord = random.choice(list(chords))
            print(f"Please play the following chord: {new_chord}")
            
            if grab_user_input("would you like to see the chord notes? (y/n): \n"):
                keys = [key for key, value in self.piano.chords.items() if value == new_chord][0]
                print("KEYS: ",keys)
                notes = [self.piano.midi_note_to_name(key) for key in keys]
                print("NOTES: ",notes)
            chord_played = False
            while not chord_played:
                if self.piano.check_chord() == new_chord:
                    print("Correct chord played!")
                    chord_played = True

            if grab_user_input("would you like to play another chord? (y/n): \n"):
                game_active = True
            else:
                game_active = False
                self.piano.stop_listening()
                print("Exiting Chord Practice mode.")
                self.main()
    def scale_practice(self):
        scales = list(self.piano.scales.keys())
        game_active = True
        self.piano.start_listening()
        while game_active:
            new_scale = random.choice(scales)
            scales.remove(new_scale)
            notes_in_scale = self.piano.scales[new_scale]
            scale_played = False
            while not scale_played:
                print(f"Please play the following scale: {new_scale}")
                if self.piano.check_scale(notes_in_scale):
                    print("Correct scale played!")
                    scale_played = True
                if grab_user_input("would you like to play another scale? (y/n): \n"):
                    game_active = True
                else:
                    game_active = False
                    self.piano.stop_listening()
                    print("Exiting Scale Practice mode.")
                    self.main()
            
