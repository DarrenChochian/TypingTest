import tkinter as tk
import time
import random
import threading

class TypingTestApp:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Typing Test")
        self.master.geometry("800x600") # window changes

        self.words = open("words.txt", "r").read().split("\n")

        self.frame = tk.Frame(self.master)

        # Choose a random set of 30 words to form a sentence
        random_words = random.sample(self.words, 30)
        self.sentence_text = " ".join(random_words)
        self.sentence = tk.Label(self.frame, text=self.sentence_text, font=("Helvetica", 16), wraplength=700, justify='left')
        self.sentence.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.textbox = tk.Entry(self.frame, width=60, font=("Helvetica", 16))
        self.textbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.textbox.bind("<KeyPress>", self.start)
        self.textbox.bind("<BackSpace>", self.count_backspaces)

        self.stats = tk.Label(self.frame, text="Speed: \n0.00 WPM\nAccuracy: 0.00%\nTime: 0.00 seconds", font=("Helvetica", 16))
        self.stats.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.personal_best_label = tk.Label(self.frame, text="", font=("Helvetica", 16, "bold"), fg="yellow")
        self.personal_best_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset)
        self.reset_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

        self.frame.pack(expand=True)

        self.counter = 0
        self.start_time = 0
        self.errors = 0
        self.running = False
        self.personal_best_wpm = 0  # Keep track of personal best WPM

        self.master.mainloop()

    def start(self, event):
        if not self.running:
            if not event.keycode in [16, 17, 18]:
                self.running = True
                self.start_time = time.time()
                t = threading.Thread(target=self.time_thread)
                t.start()
        if not self.sentence.cget('text').startswith(self.textbox.get()):
            self.textbox.config(fg="red")
        else:
            self.textbox.config(fg="black")
        if self.textbox.get() == self.sentence.cget('text'):
            self.running = False
            self.textbox.config(fg="green")
            self.check_personal_best()

    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            elapsed_time = time.time() - self.start_time
            self.counter += 0.1
            wps = len(self.textbox.get().split(" ")) / self.counter
            wpm = wps * 60
            accuracy = self.calculate_accuracy(self.textbox.get(), self.sentence.cget('text'))
            self.stats.config(text=f"Speed: \n{wpm:.2f} WPM\nAccuracy: {accuracy:.2f}%\nTime: {elapsed_time:.2f} seconds")

    def calculate_accuracy(self, user_input, actual_sentence):
        total_chars = len(actual_sentence)
        correct_chars = total_chars - self.errors
        accuracy_percentage = (correct_chars / total_chars) * 100
        return accuracy_percentage

    def count_backspaces(self, event):
        self.errors += 1

    def reset(self):
        self.running = False
        self.counter = 0
        self.start_time = 0
        self.errors = 0
        self.stats.config(text="Speed: \n0.00 WPM\nAccuracy: 0.00%\nTime: 0.00 seconds")
        self.personal_best_label.config(text="")
        random_words = random.sample(self.words, 30)
        self.sentence_text = " ".join(random_words)
        self.sentence.config(text=self.sentence_text)
        self.textbox.delete(0, tk.END)

    def check_personal_best(self):
        current_wpm = len(self.textbox.get().split(" ")) / self.counter * 60
        if current_wpm > self.personal_best_wpm:
            self.personal_best_wpm = current_wpm
            self.personal_best_label.config(text="NEW PERSONAL BEST ★")  #PBSS


TypingTestApp()