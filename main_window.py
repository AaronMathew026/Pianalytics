import tkinter as tk

root  = tk.Tk()
root.title("Pianalytics")
root.minsize

class MainWindow:
    def __init__(self):
        self.label = tk.Label(root, text="Welcome to Pianalytics!", font=("Helvetica", 16,"bold"))
        self.label.pack(pady=20)

        self.start_button = tk.Button(root, text="Start",command= self.start_screen)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop MIDI Input",)
        self.stop_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", command=root.quit)
        self.exit_button.pack(pady=10)
        root.mainloop()
    def start_screen(self):
        self.label.config(text="Select Mode")
        self.chord_button = tk.Button(root, text="Chord Practice",)
        self.chord_button.pack(pady=5)
        self.scale_button = tk.Button(root, text="Scale Practice",)
        self.scale_button.pack(pady=5)
        self.realtime_button = tk.Button(root, text="Real-time Analysis",)
        self.realtime_button.pack(pady=5)
        root.mainloop()

main = MainWindow()
