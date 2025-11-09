from MIDI_reader import MIDIReader
import mido
from rtmidi2 import MidiIn, NOTEON, CC, splitchannel
import time
import random

def grab_user_input(prompt,):
    user_input = (input(prompt)).lower()
    while user_input not in ("y", "n"):
        user_input = input(f"Invalid option. Please select y or n: \n")
    if user_input == "y":
        return True
    else:
        return False

class Main:
    def __init__(self):
        self.mode = "home"
        self.user_name = "User"
        self.piano = MIDIReader()
        self.piano_state = "stopped"
    
    def Home(self):
        print(f"Welcome to Pianalytics! {self.user_name}. \n You are in {self.mode} mode. \n Please select an option to continue.")
        self.user_input = input("Options: \n 1. Start Reading MIDI Input \n 2. Stop Reading MIDI Input \n 3. Exit \n")
        while self.user_input not in ["1", "2", "3"]:
            self.user_input = input("Invalid option. Please select 1, 2, or 3: \n")
        if self.user_input == "1":
            self.user_input = input("Which mode would you like to use? \n 1. Chord Practice \n 2. Scale Practice \n 3. Real-time Analysis \n")
            while self.user_input not in ["1", "2", "3"]:
                self.user_input = input("Invalid option. Please select 1, 2, or 3: \n")
            if self.user_input == "1":
                print("Chord Practice mode selected.")
                self.mode = "Chord Practice"
                self.chord_practice()
                #self.piano.chord_practice()
            elif self.user_input == "2":
                print("Scale Practice mode selected.")
                self.mode = "Scale Practice"
                self.scale_practice()
            elif self.user_input == "3":
                print("Real-time Analysis mode selected.")
                self.mode = "Real-time Analysis"
                #self.Real_time_analysis()
            else:
                print("Invalid option selected.")
        elif self.user_input == "2":
            if self.piano_state == "listening":
                self.piano.midiin.close_port()
                self.piano_state = "stopped"
                print("MIDI input reading stopped.")
            else:
                print("MIDI input is not currently being read.")
        elif self.user_input == "3":
            print("Exiting Pianalytics. Goodbye!")
            exit() 

    def chord_practice(self):
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
            notes_in_scale = self.piano.scales[new_scale]
            scale_played = False
            while not scale_played:
                print(f"Please play the following scale: {new_scale}")
                if self.piano.check_scale(notes_in_scale):
                    print("Correct scale played!")
                    scale_played = True
                else:
                    print("Incorrect scale. Try again.")
                

if __name__ == "__main__":
    app = Main()
    app.Home()