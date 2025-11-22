
import mido
from rtmidi2 import MidiIn, NOTEON, CC, splitchannel
from game_modes import Game_Select
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
        self.gamemodes = Game_Select()
        self.piano_state = "stopped"
    
    def Home(self):
        print(f"Welcome to Pianalytics! {self.user_name}. \n You are in {self.mode} mode. \n Please select an option to continue.")
        self.user_input = input("Options: \n 1. Start \n 2. Exit \n")
        while self.user_input not in ["1", "2", "3"]:
            self.user_input = input("Invalid option. Please select 1, 2, or 3: \n")
        if self.user_input == "1":
            self.user_input = input("Which mode would you like to use? \n 1. Chord Practice \n 2. Scale Practice \n 3. Real-time Analysis \n")
            while self.user_input not in ["1", "2", "3"]:
                self.user_input = input("Invalid option. Please select 1, 2, or 3: \n")

            match self.user_input:
                case "1":
                    self.gamemodes.chord_practice()
                case "2":
                    self.gamemodes.scale_practice()
                case "3":
                    print("Real-time Analysis mode is under development. Please check back later.")
                    time.sleep(2)
                    self.Home()
        elif self.user_input == "2":
            print("Exiting Pianalytics. Goodbye!")
            exit() 
if __name__ == "__main__":
    app = Main()
    app.Home()