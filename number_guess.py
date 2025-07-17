import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import json
import os

class NumberGuessingGameGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎯 Ultimate Number Guessing Game")
        self.root.geometry("600x700")
        self.root.configure(bg='#1a1a1a')
        self.root.resizable(False, False)
        
        # Game variables
        self.secret_number = 0
        self.attempts = 0
        self.max_attempts = 7
        self.start_time = 0
        self.score = 0
        self.high_score = self.load_high_score()
        self.min_range = 1
        self.max_range = 100
        self.game_active = False
        
        self.setup_gui()
        self.show_main_menu()
    
    def load_high_score(self):
        """Load high score from file"""
        try:
            with open('high_score.json', 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0)
        except:
            return 0
    
    def save_high_score(self):
        """Save high score to file"""
        try:
            with open('high_score.json', 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except:
            pass
    
    def setup_gui(self):
        """Setup the main GUI components"""
        # Title Frame
        title_frame = tk.Frame(self.root, bg='#1a1a1a')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(title_frame, text="🎯 ULTIMATE NUMBER GUESSING GAME", 
                              font=('Arial', 20, 'bold'), fg='#ff8c00', bg='#1a1a1a')
        title_label.pack()
        
        # High Score Display
        self.high_score_label = tk.Label(title_frame, text=f"🏆 High Score: {self.high_score}", 
                                        font=('Arial', 12, 'bold'), fg='#ffff00', bg='#1a1a1a')
        self.high_score_label.pack(pady=5)
        
        # Main Content Frame
        self.main_frame = tk.Frame(self.root, bg='#1a1a1a')
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Game Info Frame
        self.info_frame = tk.Frame(self.main_frame, bg='#2d2d2d', relief='raised', bd=2)
        self.info_frame.pack(fill='x', pady=10)
        
        # Status Labels
        self.status_label = tk.Label(self.info_frame, text="Welcome! Choose difficulty to start", 
                                   font=('Arial', 12, 'bold'), fg='#00ff00', bg='#2d2d2d')
        self.status_label.pack(pady=5)
        
        self.attempts_label = tk.Label(self.info_frame, text="", 
                                     font=('Arial', 10), fg='#ffffff', bg='#2d2d2d')
        self.attempts_label.pack()
        
        # Difficulty Frame
        diff_frame = tk.Frame(self.main_frame, bg='#1a1a1a')
        diff_frame.pack(pady=10)
        
        tk.Label(diff_frame, text="🎚️ Choose Difficulty:", 
                font=('Arial', 12, 'bold'), fg='#ff8c00', bg='#1a1a1a').pack()
        
        # Difficulty Buttons
        button_frame = tk.Frame(diff_frame, bg='#1a1a1a')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Easy\n(1-50, 10 attempts)", 
                 font=('Arial', 10, 'bold'), bg='#00cc00', fg='white', 
                 width=15, height=2, command=lambda: self.start_game(1, 50, 10)).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="Medium\n(1-100, 7 attempts)", 
                 font=('Arial', 10, 'bold'), bg='#ff8c00', fg='white', 
                 width=15, height=2, command=lambda: self.start_game(1, 100, 7)).pack(side='left', padx=5)
        
        tk.Button(button_frame, text="Hard\n(1-200, 5 attempts)", 
                 font=('Arial', 10, 'bold'), bg='#cc0000', fg='white', 
                 width=15, height=2, command=lambda: self.start_game(1, 200, 5)).pack(side='left', padx=5)
        
        # Game Input Frame
        self.input_frame = tk.Frame(self.main_frame, bg='#1a1a1a')
        self.input_frame.pack(pady=20)
        
        tk.Label(self.input_frame, text="👉 Enter your guess:", 
                font=('Arial', 12, 'bold'), fg='#ffffff', bg='#1a1a1a').pack()
        
        # Input and Button Frame
        input_button_frame = tk.Frame(self.input_frame, bg='#1a1a1a')
        input_button_frame.pack(pady=10)
        
        self.guess_entry = tk.Entry(input_button_frame, font=('Arial', 14, 'bold'), 
                                   width=10, justify='center', bg='#2d2d2d', fg='white', 
                                   insertbackground='white')
        self.guess_entry.pack(side='left', padx=5)
        self.guess_entry.bind('<Return>', lambda event: self.submit_guess())
        
        self.submit_btn = tk.Button(input_button_frame, text="Submit Guess", 
                                   font=('Arial', 12, 'bold'), bg='#ff8c00', fg='white', 
                                   command=self.submit_guess)
        self.submit_btn.pack(side='left', padx=5)
        
        # Hint Frame
        self.hint_frame = tk.Frame(self.main_frame, bg='#2d2d2d', relief='raised', bd=2)
        self.hint_frame.pack(fill='x', pady=10)
        
        self.hint_label = tk.Label(self.hint_frame, text="", 
                                  font=('Arial', 14, 'bold'), fg='#ffff00', bg='#2d2d2d')
        self.hint_label.pack(pady=10)
        
        # History Frame
        self.history_frame = tk.Frame(self.main_frame, bg='#1a1a1a')
        self.history_frame.pack(fill='both', expand=True, pady=10)
        
        tk.Label(self.history_frame, text="📊 Guess History:", 
                font=('Arial', 12, 'bold'), fg='#ff8c00', bg='#1a1a1a').pack()
        
        # History Listbox with Scrollbar
        history_container = tk.Frame(self.history_frame, bg='#1a1a1a')
        history_container.pack(fill='both', expand=True, pady=5)
        
        scrollbar = tk.Scrollbar(history_container)
        scrollbar.pack(side='right', fill='y')
        
        self.history_listbox = tk.Listbox(history_container, yscrollcommand=scrollbar.set, 
                                         font=('Arial', 10), bg='#2d2d2d', fg='white', 
                                         selectbackground='#ff8c00', height=8)
        self.history_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Control Buttons
        control_frame = tk.Frame(self.main_frame, bg='#1a1a1a')
        control_frame.pack(pady=10)
        
        tk.Button(control_frame, text="🎮 New Game", 
                 font=('Arial', 12, 'bold'), bg='#00cc00', fg='white', 
                 command=self.show_main_menu).pack(side='left', padx=5)
        
        tk.Button(control_frame, text="📊 Show Stats", 
                 font=('Arial', 12, 'bold'), bg='#0066cc', fg='white', 
                 command=self.show_stats).pack(side='left', padx=5)
        
        tk.Button(control_frame, text="❌ Exit", 
                 font=('Arial', 12, 'bold'), bg='#cc0000', fg='white', 
                 command=self.root.quit).pack(side='left', padx=5)
        
        # Initially disable input
        self.toggle_input(False)
    
    def show_main_menu(self):
        """Reset to main menu state"""
        self.game_active = False
        self.toggle_input(False)
        self.status_label.config(text="Welcome! Choose difficulty to start", fg='#00ff00')
        self.attempts_label.config(text="")
        self.hint_label.config(text="")
        self.history_listbox.delete(0, tk.END)
        self.guess_entry.delete(0, tk.END)
    
    def toggle_input(self, enabled):
        """Enable/disable input components"""
        state = 'normal' if enabled else 'disabled'
        self.guess_entry.config(state=state)
        self.submit_btn.config(state=state)
    
    def start_game(self, min_range, max_range, max_attempts):
        """Start a new game with given parameters"""
        self.min_range = min_range
        self.max_range = max_range
        self.max_attempts = max_attempts
        self.secret_number = random.randint(min_range, max_range)
        self.attempts = 0
        self.start_time = time.time()
        self.game_active = True
        
        # Clear previous game data
        self.history_listbox.delete(0, tk.END)
        self.guess_entry.delete(0, tk.END)
        
        # Update UI
        self.status_label.config(text=f"🚀 Game Started! Guess number between {min_range}-{max_range}", 
                               fg='#00ff00')
        self.attempts_label.config(text=f"🎯 Attempts: 0/{max_attempts}")
        self.hint_label.config(text="Good luck! 🍀")
        
        # Enable input
        self.toggle_input(True)
        self.guess_entry.focus()
    
    def submit_guess(self):
        """Process user's guess"""
        if not self.game_active:
            return
        
        try:
            guess = int(self.guess_entry.get())
            
            # Validate range
            if not (self.min_range <= guess <= self.max_range):
                messagebox.showerror("Invalid Input", 
                                   f"Please enter a number between {self.min_range} and {self.max_range}!")
                return
            
            self.attempts += 1
            self.guess_entry.delete(0, tk.END)
            
            # Add to history
            self.history_listbox.insert(tk.END, f"Attempt {self.attempts}: {guess}")
            self.history_listbox.see(tk.END)
            
            # Update attempts display
            remaining = self.max_attempts - self.attempts
            self.attempts_label.config(text=f"🎯 Attempts: {self.attempts}/{self.max_attempts}")
            
            if guess == self.secret_number:
                self.win_game()
            elif guess < self.secret_number:
                self.give_hint("🔼 Too LOW! Try a HIGHER number.", guess)
            else:
                self.give_hint("🔽 Too HIGH! Try a LOWER number.", guess)
            
            # Check if game over
            if self.attempts >= self.max_attempts and guess != self.secret_number:
                self.lose_game()
        
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number!")
    
    def give_hint(self, direction_hint, guess):
        """Provide smart hints based on guess"""
        diff = abs(guess - self.secret_number)
        
        if diff <= 5:
            hint = f"{direction_hint}\n🔥 You're VERY close!"
        elif diff <= 15:
            hint = f"{direction_hint}\n♨️ Getting warmer!"
        elif diff <= 30:
            hint = f"{direction_hint}\n🌡️ You're in the right area!"
        else:
            hint = f"{direction_hint}\n🧊 You're quite far!"
        
        self.hint_label.config(text=hint, fg='#ffff00')
        
        # Add hint to history
        self.history_listbox.insert(tk.END, f"   → {hint.replace(chr(10), ' ')}")
        self.history_listbox.see(tk.END)
    
    def win_game(self):
        """Handle game win"""
        self.game_active = False
        self.toggle_input(False)
        
        end_time = time.time()
        time_taken = round(end_time - self.start_time, 2)
        self.score = self.calculate_score()
        
        # Update high score
        new_high_score = False
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            self.high_score_label.config(text=f"🏆 High Score: {self.high_score}")
            new_high_score = True
        
        # Victory message
        message = f"🎉 CONGRATULATIONS! YOU WON! 🎉\n\n"
        message += f"✅ The number was: {self.secret_number}\n"
        message += f"🎯 Attempts used: {self.attempts}/{self.max_attempts}\n"
        message += f"⏱️ Time taken: {time_taken} seconds\n"
        message += f"💯 Your Score: {self.score}\n\n"
        
        if new_high_score:
            message += "🌟 NEW HIGH SCORE! 🌟\n"
        
        message += "🎊 You're a guessing genius! 🎊"
        
        self.hint_label.config(text="🎉 YOU WON! 🎉", fg='#00ff00')
        self.status_label.config(text="🏆 VICTORY! 🏆", fg='#00ff00')
        
        messagebox.showinfo("Victory!", message)
    
    def lose_game(self):
        """Handle game loss"""
        self.game_active = False
        self.toggle_input(False)
        
        message = f"😞 GAME OVER! 😞\n\n"
        message += f"🎯 The number was: {self.secret_number}\n"
        message += f"🎲 You used all {self.max_attempts} attempts!\n"
        message += f"🎮 Better luck next time!"
        
        self.hint_label.config(text="😞 GAME OVER! 😞", fg='#ff0000')
        self.status_label.config(text="💥 GAME OVER! 💥", fg='#ff0000')
        
        messagebox.showinfo("Game Over", message)
    
    def calculate_score(self):
        """Calculate score based on performance"""
        base_score = 1000
        difficulty_multiplier = (self.max_range - self.min_range) // 50
        attempt_penalty = (self.attempts - 1) * 50
        time_taken = time.time() - self.start_time
        time_bonus = max(0, 300 - int(time_taken))
        
        score = (base_score * difficulty_multiplier) - attempt_penalty + time_bonus
        return max(score, 100)
    
    def show_stats(self):
        """Show game statistics"""
        stats = f"📊 GAME STATISTICS 📊\n\n"
        stats += f"🏆 High Score: {self.high_score}\n"
        stats += f"🎯 Current Game Status: {'Active' if self.game_active else 'Inactive'}\n"
        
        if self.game_active:
            stats += f"🎲 Secret Number Range: {self.min_range}-{self.max_range}\n"
            stats += f"🎯 Attempts Used: {self.attempts}/{self.max_attempts}\n"
            time_elapsed = round(time.time() - self.start_time, 2)
            stats += f"⏱️ Time Elapsed: {time_elapsed} seconds\n"
        
        messagebox.showinfo("Statistics", stats)
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

# Run the game
if __name__ == "__main__":
    game = NumberGuessingGameGUI()
    game.run()