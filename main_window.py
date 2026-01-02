import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from game_modes import Game_Select
from MIDI_player import music_player
import time
import random
class MainWindow(tk.Tk):
    def __init__(self):


        # self.style = ttk.Style()
        # self.style.configure(
        #     "Custom.TButton",
        #     font = ("Helvetica",12,"bold"),
        #     foreground = "blue",
        #     padding = 10

        # )
        # self.style.map(
        #     "Custom.TButton",
        #     foreground = [("pressed","white"),("active","red")],
        #     background = [("pressed","#333"),("active","#ddd")]

        # )
        self.button_font = ("Helvetica",16)
        self.game_select = Game_Select()
        super().__init__()
        self.title("Pianalytics")
        self.geometry("800x600")
        self.label = tk.Label(self, text="Welcome to Pianalytics!", font=("Helvetica", 16))
        self.label.pack(anchor = "center", pady=20)

        self.start_button = tk.Button(self, text = "Start", command = self.start_window)
        self.start_button.config(width=20, height=2)
        self.start_button.pack(pady=10)

        self.exit_button = tk.Button(self, text = "Exit", command = self.exit_window)
        self.exit_button.config(width=20, height=2)
        self.exit_button.pack(pady=10)

        self.menu_image = tk.PhotoImage(file="j2em16zv5s2f1.gif")
        self.image_label = tk.Label(self, image=self.menu_image)
        self.image_label.pack(pady=20)
    def start_window(self):


        self.start_window = tk.Toplevel(self)
        self.start_window.title("Start Menu")
        self.start_window.geometry("400x300")
       
        start_menu = tk.Menu(self)
        options_menu = tk.Menu(start_menu,tearoff= 0 )
        options_menu.add_command(label= "Exit",command=self.exit_window)
        start_menu.add_cascade(label = "Options",menu = options_menu)
        self.start_window.config(menu = start_menu)


        self.start_window_label = tk.Label(self.start_window, text="Start Menu", font=("Helvetica", 14))
        self.start_window_label.pack(pady=20)

        self.RTA_button = tk.Button(self.start_window, text="Real-time Analysis", command=self.test_window)
        self.RTA_button.config(width=25, height=2)
        self.RTA_button.pack(pady=10)

        self.midi_play_button = tk.Button(self.start_window, text="MIDI Playback", command=self.midi_play_window)
        self.midi_play_button.config(width=25, height=2)
        self.midi_play_button.pack(pady=10)

    def test_window(self):
        
        self.start_window.destroy()
        self.test_window = tk.Toplevel(self)
        self.test_window.title("Real-time Analysis")
        self.test_window.geometry("400x300")

        self.test_window_label = tk.Label(self.test_window, text="Real-time Analysis Mode", font=("Helvetica", 14))
        self.test_window_label.pack(pady=20)

        self.note_label = tk.Label(self.test_window, text="Listening for notes...", font=("Helvetica", 12))
        self.note_label.pack(pady=10)
        self.game_select.real_time_analysis()
        self.update_active_keys()

        self.exit_button = tk.Button(self.test_window, text="Exit",command = self.test_window.destroy)
        self.exit_button.config(width=20, height=2)
        self.exit_button.pack(pady=10)

    def midi_play_window(self):
        music = music_player()
        self.start_window.destroy()
        self.midi_play_window = tk.Toplevel(self)
        self.midi_play_window.title("MIDI Playback")
        self.midi_play_window.geometry("400x300")

        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label = "Open", command = self.file_select_window)
        menu_bar.add_cascade(label="File", menu=file_menu)

        options_menu  = tk.Menu(menu_bar,tearoff= 0 )
        options_menu.add_command(label = "Exit", command = self.exit_window)
        menu_bar.add_cascade(label = "Options", menu = options_menu)
        self.midi_play_window.config(menu=menu_bar)

        self.midi_play_window_label = tk.Label(self.midi_play_window, text="MIDI Playback Mode", font=("Helvetica", 14))
        self.midi_play_window_label.pack(fill="x",)

        self.song_title = tk.Label(self.midi_play_window,text = "Please Select a song")
        self.song_title.pack(fill = "both")
        try:
        
            self.midi_play_button = tk.Button(self.midi_play_window, text="Play MIDI",command =  lambda: music.play_music(self.file_name) , font=("Helvetica",14))
            self.midi_play_button.pack(fill="both")
            self.pause_unpause_button = tk.Button(self.midi_play_window,text = "Pause/Unpause",command = music.play_pause, font = self.button_font )
            self.pause_unpause_button.pack(fill = "both")
        except AttributeError:
            messagebox.showerror("Error!",message=" No file Found!")
        self.midi_play_window.lift()
        self.midi_play_window.attributes("-topmost",True)
    def file_select_window(self):
        try:
            self.file_name = filedialog.askopenfilename(
                title = "Select a MIDI file to Play",
                filetypes=[("MIDI Files", "*.mid")]

            )
            if self.file_name:
                messagebox.showinfo("Information", "File Successfully uploaded")
                print(self.file_name)
                self.song_title.config(text = f"{self.file_name}")
            return True
        except tk.TclError:
            messagebox.showerror("Error!","This file is not supported")
        pass
    def update_active_keys(self):
        keys = getattr(self.game_select.piano, 'active_keys', set()) # Grabs active keys from MIDIReader
        if keys:
            note_names = [self.game_select.piano.midi_note_to_name(n) for n in keys]
            self.note_label.config(text=f"Active Notes: {', '.join(note_names)}")
        else:
            self.note_label.config(text="No active notes.")

        if hasattr(self.game_select.piano, 'active_keys'):
            self.after(100, self.update_active_keys)  # Update every 100 ms



    def exit_window(self):
        self.destroy()
        
main = MainWindow()
main.mainloop()

