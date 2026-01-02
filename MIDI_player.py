import pygame
from tkinter import messagebox




class music_player():
  def __init__(self):
    self.freq = 44100  # audio CD quality
    self.bitsize = -16   # unsigned 16 bit
    self.channels = 2  # 1 is mono, 2 is stereo
    self.buffer = 1024   # number of samples
    pygame.mixer.init(self.freq, self.bitsize, self.channels, self.buffer)

    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(0.8)

  def play_music(self,midi_filename):
    if midi_filename:
      '''Stream music_file in a blocking manner'''
      pygame.mixer.music.load(midi_filename)
      pygame.mixer.music.play()
    else:
      messagebox.showerror("Error!",message=" No file Found!")

      return False

  def play_pause(self):
    if pygame.mixer.music.get_busy():
      pygame.mixer.music.pause()
    else:
      pygame.mixer.music.unpause()

