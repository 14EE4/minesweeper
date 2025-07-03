import tkinter as tk
import random

class Minesweeper:
    def __init__(self, master, rows, cols, mines):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.first_click = True

        self.master.title("Minesweeper")
        self.master.resizable(False, False)
        self.create_widgets()
        self.new_game()
        self.master.update_idletasks()
        self.master.geometry('')

    def create_widgets(self):
        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack()

        self.new_game_button = tk.Button(self.top_frame, text="New Game", command=self.new_game)
        self.new_game_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.flag_counter_label = tk.Label(self.top_frame, text=f"Flags: {self.mines}")
        self.flag_counter_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.status_label = tk.Label(self.top_frame, text="Good Luck!")
        self.status_label.pack(side=tk.RIGHT, padx=5, pady=5)

        self.frame = tk.Frame(self.master)
        self.frame.pack()
        
        self.buttons = [] # Initialize buttons list here, populate in new_game

    def setup_board_buttons(self):
        # Clear existing buttons
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        self.buttons = [[tk.Button(self.frame, width=2, height=1) for c in range(self.cols)] for r in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                self.buttons[r][c].grid(row=r, column=c)
                self.buttons[r][c].bind('<Button-1>', lambda e, r=r, c=c: self.on_button_click(r, c, e))
                self.buttons[r][c].bind('<Button-3>', lambda e, r=r, c=c: self.on_button_click(r, c, e))

    def place_mines(self, first_r, first_c):
        safe_cells = set()
        for r in range(self.rows):
            for c in range(self.cols):
                safe_cells.add((r, c))

        # Remove the first clicked cell and its neighbors from safe_cells
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= first_r + i < self.rows and 0 <= first_c + j < self.cols:
                    safe_cells.discard((first_r + i, first_c + j))

        mine_positions = random.sample(list(safe_cells), self.mines)

        for r, c in mine_positions:
            self.mine_map[r][c] = 'M'

        # Calculate numbers for non-mine cells
        for r in range(self.rows):
            for c in range(self.cols):
                if self.mine_map[r][c] == 'M':
                    continue
                
                mine_count = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= r + i < self.rows and 0 <= c + j < self.cols and self.mine_map[r + i][c + j] == 'M':
                            mine_count += 1
                self.mine_map[r][c] = str(mine_count)

    def reveal_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.mine_map[r][c] == 'M':
                    self.buttons[r][c].config(text='M', bg='red')

    def check_win(self):
        return self.revealed_cells == (self.rows * self.cols) - self.mines

    def update_buttons(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.buttons[r][c].config(text='', state='normal', relief=tk.RAISED, bg='SystemButtonFace')
                self.buttons[r][c].bind('<Button-1>', lambda e, r=r, c=c: self.on_button_click(r, c, e))
                self.buttons[r][c].bind('<Button-3>', lambda e, r=r, c=c: self.on_button_click(r, c, e))

    def new_game(self):
        self.game_over = False
        self.revealed_cells = 0
        self.flag_count = self.mines
        self.first_click = True # Reset for new game
        self.status_label.config(text="Good Luck!")
        self.flag_counter_label.config(text=f"Flags: {self.flag_count}")
        
        # Re-create the mine_map based on current rows/cols
        self.mine_map = [['0' for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Setup board buttons for new dimensions
        self.setup_board_buttons()

        # Mines are placed after the first click
        self.update_buttons()

    def on_button_click(self, r, c, event):
        if self.game_over:
            return

        if event.num == 1:  # Left click
            if self.buttons[r][c]['text'] == '🚩': # Don't open flagged cells
                return

            if self.first_click:
                self.place_mines(r, c)
                self.first_click = False

            if self.mine_map[r][c] == 'M':
                self.reveal_mines()
                self.status_label.config(text="Game Over!")
                self.game_over = True
            else:
                self.reveal_cell(r, c)
                if self.check_win():
                    self.status_label.config(text="You Win!")
                    self.game_over = True

            # Chord functionality: if a numbered cell is clicked and it's already revealed
            # and the number of surrounding flags matches the cell's number, open surrounding unflagged cells.
            if self.buttons[r][c]['state'] == 'disabled' and self.mine_map[r][c] != '0':
                self.chord(r, c)

        elif event.num == 3:  # Right click
            self.toggle_flag(r, c)

    def chord(self, r, c):
        # This chord function is now called only when a revealed numbered cell is left-clicked
        mine_count = int(self.mine_map[r][c])
        flag_count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= r + i < self.rows and 0 <= c + j < self.cols:
                    if self.buttons[r + i][c + j]['text'] == '🚩':
                        flag_count += 1
        
        if mine_count == flag_count:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= r + i < self.rows and 0 <= c + j < self.cols:
                        if self.buttons[r + i][c + j]['text'] != '🚩':
                            self.reveal_cell(r + i, c + j)

    def reveal_cell(self, r, c):
        if self.buttons[r][c]['state'] == 'disabled':
            return

        self.buttons[r][c].config(text=self.mine_map[r][c] if self.mine_map[r][c] != '0' else '', state='disabled', relief=tk.SUNKEN)
        self.revealed_cells += 1

        if self.mine_map[r][c] == '0':
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= r + i < self.rows and 0 <= c + j < self.cols:
                        self.reveal_cell(r + i, c + j)

    def toggle_flag(self, r, c):
        if self.game_over or self.buttons[r][c]['state'] == 'disabled':
            return
        
        if self.buttons[r][c]['text'] == '':
            if self.flag_count > 0:
                self.buttons[r][c].config(text='🚩', bg='yellow')
                self.flag_count -= 1
        elif self.buttons[r][c]['text'] == '🚩':
            self.buttons[r][c].config(text='', bg='SystemButtonFace')
            self.flag_count += 1
        
        self.flag_counter_label.config(text=f"Flags: {self.flag_count}")

if __name__ == '__main__':
    root = tk.Tk()
    # Default values for rows, cols, mines
    rows, cols, mines = 15, 15, 30 
    game = Minesweeper(root, rows, cols, mines)
    root.mainloop()