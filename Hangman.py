import tkinter as tk
from tkinter import messagebox
import random

# --------------------------
# Global Variables
# --------------------------
words = []
word = ""
guessed_letters = []
attempts = 6
hint_limit = 0
hints_used = 0

root = None
word_label = None
letter_entry = None
attempts_label = None
hints_label = None
canvas = None

# --------------------------
# Start Window
# --------------------------
def start_window():
    global root
    root = tk.Tk()
    root.title("Hangman Game")
    root.geometry("400x500")
    root.configure(bg="#FFDD99")

    tk.Label(root, text="HANGMAN", font=("Impact", 40, "bold"), bg="#FFDD99", fg="#2E86AB").pack(pady=50)

    tk.Button(root, text="Start Game", font=("Comic Sans MS", 18, "bold"), command=start_difficulty,
              bg="#28B463", fg="white", bd=5, relief="raised", width=12).pack(pady=10)

    tk.Button(root, text="Exit", font=("Comic Sans MS", 16, "bold"), command=root.destroy,
              bg="#C0392B", fg="white", bd=5, relief="raised", width=10).pack(pady=10)

    root.mainloop()

# --------------------------
# Difficulty Selection Window
# --------------------------
def start_difficulty():
    root.destroy()
    diff_window = tk.Tk()
    diff_window.title("Choose Difficulty")
    diff_window.geometry("400x500")
    diff_window.configure(bg="#FAD7A0")

    tk.Label(diff_window, text="Select Difficulty Level", font=("Comic Sans MS", 20, "bold"), bg="#FAD7A0", fg="#5D6D7E").pack(pady=25)

    def set_difficulty(level):
        global words
        filename = f"{level}.txt"
        try:
            with open(filename, "r") as file:
                words.clear()
                words.extend([line.strip().lower() for line in file.readlines()])
        except FileNotFoundError:
            messagebox.showerror("Error", f"{filename} not found!")
            diff_window.destroy()
            return

        if not words:
            messagebox.showerror("Error", f"{filename} is empty!")
            return

        diff_window.destroy()
        start_game()

    tk.Button(diff_window, text="Easy", width=20, font=("Comic Sans MS", 16, "bold"),
              bg="#F7DC6F", fg="black", command=lambda: set_difficulty("easy")).pack(pady=8)
    tk.Button(diff_window, text="Medium", width=20, font=("Comic Sans MS", 16, "bold"),
              bg="#F5B041", fg="black", command=lambda: set_difficulty("medium")).pack(pady=8)
    tk.Button(diff_window, text="Hard", width=20, font=("Comic Sans MS", 16, "bold"),
              bg="#EC7063", fg="white", command=lambda: set_difficulty("hard")).pack(pady=8)

    tk.Button(diff_window, text="Main Menu", font=("Comic Sans MS", 14, "bold"),
              bg="#5DADE2", fg="white", command=lambda: [diff_window.destroy(), start_window()]).pack(pady=12)

    diff_window.mainloop()

# --------------------------
# Game Window
# --------------------------
def start_game():
    global word, guessed_letters, attempts, hint_limit, hints_used
    global root, word_label, letter_entry, attempts_label, hints_label, canvas

    word = random.choice(words)
    guessed_letters = []
    attempts = 6
    hints_used = 0

    length = len(word)
    if 3 <= length <= 5:
        hint_limit = 1
    elif 6 <= length <= 9:
        hint_limit = 2
    else:
        hint_limit = 3

    root = tk.Tk()
    root.title("Hangman Game")
    root.geometry("450x700")
    root.configure(bg="#FAD7A0")

    canvas = tk.Canvas(root, width=250, height=300, bg="#FCF3CF")
    canvas.pack(pady=20)
    draw_base()

    word_label = tk.Label(root, text="_ " * len(word), font=("Arial Rounded MT Bold", 24), bg="#FAD7A0", fg="#2E4053")
    word_label.pack(pady=20)
    update_word_display()

    letter_entry = tk.Entry(root, bg="white", font=("Arial", 16, "bold"), bd=4, relief="ridge")
    letter_entry.pack(pady=12)
    letter_entry.focus()

    btn_frame = tk.Frame(root, bg="#FAD7A0")
    btn_frame.pack(pady=15)

    tk.Button(btn_frame, text="Guess", font=("Comic Sans MS", 14, "bold"),
              command=guess_letter, bg="#5DADE2", fg="white", width=8).pack(side="left", padx=10)

    tk.Button(btn_frame, text="Hint", font=("Comic Sans MS", 14, "bold"),
              command=use_hint, bg="#F39C12", fg="white", width=8).pack(side="left", padx=10)

    attempts_label = tk.Label(root, text=f"Attempts left: {attempts}",
                              font=("Arial Rounded MT Bold", 14), bg="#FAD7A0", fg="#C0392B")
    attempts_label.pack(pady=6)

    hints_label = tk.Label(root, text=f"Total Hints: {hint_limit}",
                           font=("Arial Rounded MT Bold", 14), bg="#FAD7A0", fg="#7D3C98")
    hints_label.pack(pady=6)

    menu_frame = tk.Frame(root, bg="#FAD7A0")
    menu_frame.pack(pady=15)

    tk.Button(menu_frame, text="Main Menu", font=("Comic Sans MS", 14, "bold"),
              bg="#5DADE2", fg="white", command=lambda: [root.destroy(), start_window()]).pack(side="left", padx=12)

    tk.Button(menu_frame, text="Exit", font=("Comic Sans MS", 14, "bold"),
              bg="#C0392B", fg="white", command=root.destroy).pack(side="left", padx=12)

    root.mainloop()

# --------------------------
# Draw Hangman
# --------------------------
def draw_base():
    canvas.delete("all")
    canvas.create_line(20, 230, 230, 230, width=3)
    canvas.create_line(50, 230, 50, 20, width=3)
    canvas.create_line(50, 20, 180, 20, width=3)
    canvas.create_line(180, 20, 180, 40, width=3)

def draw_hangman(wrong):
    if wrong >= 1:
        canvas.create_oval(160, 40, 200, 80, width=3)
    if wrong >= 2:
        canvas.create_line(180, 80, 180, 140, width=3)
    if wrong >= 3:
        canvas.create_line(180, 90, 150, 120, width=3)
    if wrong >= 4:
        canvas.create_line(180, 90, 210, 120, width=3)
    if wrong >= 5:
        canvas.create_line(180, 140, 150, 180, width=3)
    if wrong >= 6:
        canvas.create_line(180, 140, 210, 180, width=3)

# --------------------------
# Game Logic
# --------------------------
def update_word_display():
    display_word = ""
    for letter in word:
        display_word += letter + " " if letter in guessed_letters else "_ "
    word_label.config(text=display_word.strip())

def guess_letter():
    global attempts
    letter = letter_entry.get().lower().strip()
    letter_entry.delete(0, tk.END)

    if len(letter) != 1 or not letter.isalpha():
        messagebox.showwarning("Invalid Input", "Please enter ONE alphabet letter.")
        return

    if letter in guessed_letters:
        messagebox.showinfo("Hangman", "You already guessed that letter!")
        return

    guessed_letters.append(letter)

    if letter not in word:
        attempts -= 1
        attempts_label.config(text=f"Attempts left: {attempts}")
        draw_hangman(6 - attempts)

    update_word_display()
    check_game_over()

def use_hint():
    global hints_used

    if hints_used >= hint_limit:
        messagebox.showinfo("Hint", "No hints remaining!")
        return

    remaining = [l for l in word if l not in guessed_letters]
    if not remaining:
        messagebox.showinfo("Hint", "No letters left to reveal!")
        return

    guessed_letters.append(random.choice(remaining))
    hints_used += 1
    hints_label.config(text=f"Total Hints : {hint_limit - hints_used}")

    update_word_display()
    check_game_over()

def check_game_over():
    if all(l in guessed_letters for l in word):
        play_again_popup("Congratulations! You won! 🎉")
    elif attempts <= 0:
        draw_hangman(6)
        play_again_popup(f"You lost! The word was '{word}' 😢")

def play_again_popup(message):
    global root
    answer = messagebox.askyesno("Game Over", message + "\nDo you want to play again?")
    root.destroy()
    if answer:
        start_window()
    else:
        exit()

# --------------------------
# Start Program
# --------------------------
start_window()
