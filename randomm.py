import tkinter as tk
from tkinter import ttk, messagebox
import random
import os
import json
from playsound import playsound

# Vocabulary database
vocabulary = {
    "easy": {
        "apple": "A fruit that keeps the doctor away.",
        "blue": "The color of the sky on a clear day.",
        "dog": "A loyal domestic animal.",
    },
    "medium": {
        "harmony": "A pleasing arrangement of parts.",
        "journey": "An act of traveling from one place to another.",
        "library": "A place where books are kept.",
    },
    "hard": {
        "ephemeral": "Lasting for a very short time.",
        "ambiguous": "Open to more than one interpretation.",
        "perseverance": "Persistent effort in doing something.",
    }
}

# Save progress file
PROGRESS_FILE = "user_progress.json"

# Load user progress
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {}

# Save user progress
def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)

# Play sound effects
def play_sound(sound_file):
    try:
        playsound(sound_file)
    except Exception:
        pass

class EnglishLearningGame:
    def _init_(self, root):
        self.root = root
        self.root.title("English Language Learning Game")
        self.root.geometry("700x500")
        
        self.progress = load_progress()
        self.username = None
        self.difficulty = None
        self.words = []
        self.current_word = None
        self.score = 0
        self.total_questions = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        # Welcome Frame
        self.welcome_frame = ttk.Frame(self.root)
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.welcome_frame, text="Welcome to the English Language Learning Game!", font=("Arial", 18, "bold")).pack(pady=20)
        ttk.Label(self.welcome_frame, text="Enter your name:", font=("Arial", 14)).pack(pady=10)
        self.username_entry = ttk.Entry(self.welcome_frame, font=("Arial", 14))
        self.username_entry.pack(pady=10)
        ttk.Button(self.welcome_frame, text="Start", command=self.start_game).pack(pady=20)
        
        # Game Frame
        self.game_frame = ttk.Frame(self.root)
        self.question_label = ttk.Label(self.game_frame, text="", font=("Arial", 14), wraplength=600)
        self.answer_entry = ttk.Entry(self.game_frame, font=("Arial", 14))
        self.submit_button = ttk.Button(self.game_frame, text="Submit", command=self.check_answer)
        self.score_label = ttk.Label(self.game_frame, text="", font=("Arial", 14))
        
        # Restart Button
        self.restart_button = ttk.Button(self.root, text="Restart", command=self.restart_game)

    def start_game(self):
        self.username = self.username_entry.get().strip()
        if not self.username:
            messagebox.showerror("Error", "Please enter your name!")
            return
        
        self.welcome_frame.pack_forget()
        self.select_difficulty()
    
    def select_difficulty(self):
        self.difficulty_frame = ttk.Frame(self.root)
        self.difficulty_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.difficulty_frame, text=f"Hello, {self.username}!", font=("Arial", 18, "bold")).pack(pady=20)
        ttk.Label(self.difficulty_frame, text="Select Difficulty:", font=("Arial", 14)).pack(pady=10)
        ttk.Button(self.difficulty_frame, text="Easy", command=lambda: self.initialize_game("easy")).pack(pady=5)
        ttk.Button(self.difficulty_frame, text="Medium", command=lambda: self.initialize_game("medium")).pack(pady=5)
        ttk.Button(self.difficulty_frame, text="Hard", command=lambda: self.initialize_game("hard")).pack(pady=5)
    
    def initialize_game(self, difficulty):
        self.difficulty = difficulty
        self.words = list(vocabulary[difficulty].keys())
        random.shuffle(self.words)
        self.score = 0
        self.total_questions = len(self.words)
        
        self.difficulty_frame.pack_forget()
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        
        self.next_question()
    
    def next_question(self):
        if self.words:
            self.current_word = self.words.pop()
            self.question_label.config(text=f"Hint: {vocabulary[self.difficulty][self.current_word]}")
            self.question_label.pack(pady=10)
            self.answer_entry.pack(pady=10)
            self.submit_button.pack(pady=10)
            self.answer_entry.delete(0, tk.END)
        else:
            self.end_game()
    
    def check_answer(self):
        user_answer = self.answer_entry.get().strip().lower()
        if user_answer == self.current_word:
            self.score += 1
            play_sound("correct.mp3")
            messagebox.showinfo("Correct!", "Well done!")
        else:
            play_sound("incorrect.mp3")
            messagebox.showerror("Incorrect!", f"The correct answer was '{self.current_word}'.")
        
        self.next_question()
    
    def end_game(self):
        self.game_frame.pack_forget()
        self.restart_button.pack(pady=20)
        
        messagebox.showinfo("Game Over", f"{self.username}, your score is {self.score}/{self.total_questions}")
        self.progress[self.username] = {"difficulty": self.difficulty, "score": self.score}
        save_progress(self.progress)
    
    def restart_game(self):
        self.restart_button.pack_forget()
        self.start_game()

# Main Application
if _name_ == "_main_":
    root = tk.Tk()
    app = EnglishLearningGame(root)
    root.mainloop()