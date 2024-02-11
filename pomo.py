import tkinter as tk
import threading
import time
import pygame

class PomodoroTimer:
    def __init__(self, master):
        pygame.mixer.init()

        self.master = master
        self.master.title("Pomodoro Timer")
        self.master.geometry("500x500+100+100")  # Set window size and position
        self.master.configure(bg='lightblue')  # Set background color
        self.timer_running = False
        self.time_left = 0
        self.session_count = 0

        self.label = tk.Label(master, text="00:00", bg='lightblue', fg='red', font=('Helvetica', 18, 'bold'))
        self.label.pack(padx=10, pady=10)  # Add padding
        self.label.pack()

        self.work_time_label = tk.Label(master, text="Work Time (minutes)")
        self.work_time_label.pack()
        self.work_time_entry = tk.Entry(master)
        self.work_time_entry.pack()
        self.work_time_entry.insert(0, "25")

        self.short_break_label = tk.Label(master, text="Short Break Time (minutes)")
        self.short_break_label.pack()
        self.short_break_entry = tk.Entry(master)
        self.short_break_entry.pack()
        self.short_break_entry.insert(0, "5")

        self.long_break_label = tk.Label(master, text="Long Break Time (minutes)")
        self.long_break_label.pack()
        self.long_break_entry = tk.Entry(master)
        self.long_break_entry.pack()
        self.long_break_entry.insert(0, "15")

        self.rounds_label = tk.Label(master, text="Number of Rounds")
        self.rounds_label.pack()
        self.rounds_entry = tk.Entry(master)
        self.rounds_entry.pack()
        self.rounds_entry.insert(0, "1")

        self.short_breaks_label = tk.Label(master, text="Short Breaks per Round")
        self.short_breaks_label.pack()
        self.short_breaks_per_round_entry = tk.Entry(master)
        self.short_breaks_per_round_entry.pack()
        self.short_breaks_per_round_entry.insert(0, "4")

        self.sound_file_label = tk.Label(master, text="Sound File")
        self.sound_file_label.pack()
        self.sound_file_entry = tk.Entry(master)
        self.sound_file_entry.pack()
        self.sound_file_entry.insert(0, "./sounds/microwave-timer-117077.mp3")

        self.start_button = tk.Button(master, text="Start", command=self.start_timer)
        self.start_button.pack()

        self.pause_button = tk.Button(master, text="Pause", command=self.pause_timer)
        self.pause_button.pack()

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_timer)
        self.reset_button.pack()

    def start_timer(self):
        if not self.timer_running:
            self.work_time = int(self.work_time_entry.get()) * 60
            self.short_break = int(self.short_break_entry.get()) * 60
            self.long_break = int(self.long_break_entry.get()) * 60
            self.rounds = int(self.rounds_entry.get())
            self.short_breaks_per_round = int(self.short_breaks_per_round_entry.get())
            self.sound_file = self.sound_file_entry.get()

            self.time_left = self.work_time
            self.timer_running = True
            self.update_timer()

    def pause_timer(self):
        if self.timer_running:
            self.timer_running = False

    def reset_timer(self):
        self.time_left = 0
        self.timer_running = False
        self.session_count = 0
        self.label.config(text="00:00")

    def update_timer(self):
        if self.timer_running and self.time_left > 0:
            mins, secs = divmod(self.time_left, 60)
            self.label.config(text=f"{mins:02d}:{secs:02d}")
            self.time_left -= 1
            self.master.after(1000, self.update_timer)
        elif self.timer_running and self.time_left == 0:
            pygame.mixer.music.load(self.sound_file)
            pygame.mixer.music.play()
            self.session_count += 1
            if self.session_count % (self.short_breaks_per_round * 2 + 2) == 0:
                self.time_left = self.long_break
            elif self.session_count % 2 == 0:
                self.time_left = self.work_time
            else:
                self.time_left = self.short_break
            if self.session_count // (self.short_breaks_per_round * 2 + 2) >= self.rounds:
                self.timer_running = False
            else:
                self.master.after(1000, self.update_timer)

root = tk.Tk()
timer = PomodoroTimer(root)
root.mainloop()