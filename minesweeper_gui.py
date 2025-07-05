import tkinter as tk
import tkinter.messagebox
import random

class Minesweeper(tk.Frame):
    def __init__(self, master, rows, cols, mines, restart_callback):
        super().__init__(master)
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.restart_callback = restart_callback
        
        self.pack()

        self.mine_map = []
        self.revealed_cells = 0
        self.flag_count = 0
        self.game_over = False
        self.first_click = True

        self.create_widgets()
        self._initialize_game_state()

    def create_widgets(self):
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(pady=5)

        self.new_game_button = tk.Button(self.top_frame, text="New Game", command=self.restart_callback)
        self.new_game_button.pack(side=tk.LEFT, padx=10)

        self.flag_counter_label = tk.Label(self.top_frame, text=f"Flags: {self.mines}", font=("Helvetica", 12))
        self.flag_counter_label.pack(side=tk.LEFT, padx=10)

        self.status_label = tk.Label(self.top_frame, text="Good Luck!", font=("Helvetica", 12))
        self.status_label.pack(side=tk.RIGHT, padx=10)

        self.game_frame = tk.Frame(self)
        self.game_frame.pack()
        
        self.buttons = []

    def setup_board_buttons(self):
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        self.buttons = [[tk.Button(self.game_frame, width=2, height=1, font=('Helvetica', 10, 'bold')) for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.cols):
                self.buttons[r][c].grid(row=r, column=c)
                self.buttons[r][c].bind('<Button-1>', lambda e, r=r, c=c: self.on_button_click(r, c, e))
                self.buttons[r][c].bind('<Button-3>', lambda e, r=r, c=c: self.on_button_click(r, c, e))

    def place_mines(self, first_r, first_c):
        self.mine_map = [['0' for _ in range(self.cols)] for _ in range(self.rows)]
        possible_mines = set((r, c) for r in range(self.rows) for c in range(self.cols))

        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= first_r + i < self.rows and 0 <= first_c + j < self.cols:
                    possible_mines.discard((first_r + i, first_c + j))

        num_mines_to_place = min(self.mines, len(possible_mines))
        mine_positions = random.sample(list(possible_mines), num_mines_to_place)

        for r, c in mine_positions:
            self.mine_map[r][c] = 'M'

        for r in range(self.rows):
            for c in range(self.cols):
                if self.mine_map[r][c] == 'M': continue
                mine_count = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= r + i < self.rows and 0 <= c + j < self.cols and self.mine_map[r + i][c + j] == 'M':
                            mine_count += 1
                self.mine_map[r][c] = str(mine_count)

    def reveal_mines(self, game_won=False):
        self.game_over = True
        for r in range(self.rows):
            for c in range(self.cols):
                if self.mine_map[r][c] == 'M':
                    if self.buttons[r][c]['text'] != '🚩':
                        bg_color = 'lightgreen' if game_won else 'red'
                        self.buttons[r][c].config(text='M', bg=bg_color, state='disabled', relief=tk.SUNKEN)
                elif self.buttons[r][c]['text'] == '🚩':
                    self.buttons[r][c].config(bg='orange', state='disabled', relief=tk.SUNKEN)

    def check_win(self):
        return self.revealed_cells == (self.rows * self.cols) - self.mines

    def _initialize_game_state(self):
        self.game_over = False
        self.revealed_cells = 0
        self.flag_count = self.mines
        self.first_click = True
        self.status_label.config(text="Good Luck!")
        self.flag_counter_label.config(text=f"Flags: {self.flag_count}")
        self.setup_board_buttons()

    def on_button_click(self, r, c, event):
        if self.game_over: return

        if event.num == 1: # Left-click
            if self.buttons[r][c]['state'] == 'disabled':
                self.chord(r, c)
            elif self.buttons[r][c]['text'] == '🚩':
                return
            else:
                if self.first_click:
                    self.place_mines(r, c)
                    self.first_click = False
                
                if self.mine_map[r][c] == 'M':
                    self.reveal_mines()
                    self.status_label.config(text="Game Over!")
                else:
                    self.reveal_cell(r, c)
        
        elif event.num == 3: # Right-click
            self.toggle_flag(r, c)

        if not self.game_over and self.check_win():
            self.status_label.config(text="You Win!")
            self.reveal_mines(game_won=True)

    def chord(self, r, c):
        if self.mine_map[r][c] == '0': return
        try: mine_count_in_cell = int(self.mine_map[r][c])
        except (ValueError, TypeError): return

        flag_count_around = sum(1 for i in range(-1, 2) for j in range(-1, 2) if 0 <= r + i < self.rows and 0 <= c + j < self.cols and self.buttons[r + i][c + j]['text'] == '🚩')
        
        if mine_count_in_cell == flag_count_around:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0: continue
                    if 0 <= r + i < self.rows and 0 <= c + j < self.cols and self.buttons[r + i][c + j]['text'] != '🚩':
                        self.reveal_cell(r + i, c + j)

    def reveal_cell(self, r, c):
        if self.buttons[r][c]['state'] == 'disabled': return

        if self.mine_map[r][c] == 'M':
            self.reveal_mines()
            self.status_label.config(text="Game Over!")
            return

        self.buttons[r][c].config(state='disabled', relief=tk.SUNKEN, bg='#d9d9d9')
        if self.mine_map[r][c] != '0':
            self.buttons[r][c].config(text=self.mine_map[r][c])
        
        self.revealed_cells += 1

        if self.mine_map[r][c] == '0':
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= r + i < self.rows and 0 <= c + j < self.cols:
                        self.reveal_cell(r + i, c + j)

    def toggle_flag(self, r, c):
        if self.game_over or self.buttons[r][c]['state'] == 'disabled': return
        
        if self.buttons[r][c]['text'] == '':
            if self.flag_count > 0:
                self.buttons[r][c].config(text='🚩', bg='yellow')
                self.flag_count -= 1
        elif self.buttons[r][c]['text'] == '🚩':
            self.buttons[r][c].config(text='', bg='SystemButtonFace')
            self.flag_count += 1
        
        self.flag_counter_label.config(text=f"Flags: {self.flag_count}")

class SettingsDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Settings")
        self.transient(master)
        self.grab_set()
        self.result = None

        self.difficulty = tk.StringVar(value="medium")

        tk.Label(self, text="Difficulty:").grid(row=0, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        tk.Radiobutton(self, text="Easy (9x9, 10 mines)", variable=self.difficulty, value="easy", command=self.toggle_custom_entries).grid(row=1, column=0, columnspan=2, sticky="w", padx=5)
        tk.Radiobutton(self, text="Medium (16x16, 40 mines)", variable=self.difficulty, value="medium", command=self.toggle_custom_entries).grid(row=2, column=0, columnspan=2, sticky="w", padx=5)
        tk.Radiobutton(self, text="Hard (16x30, 99 mines)", variable=self.difficulty, value="hard", command=self.toggle_custom_entries).grid(row=3, column=0, columnspan=2, sticky="w", padx=5)
        tk.Radiobutton(self, text="Custom", variable=self.difficulty, value="custom", command=self.toggle_custom_entries).grid(row=4, column=0, columnspan=2, sticky="w", padx=5)

        self.custom_frame = tk.Frame(self)
        self.custom_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        tk.Label(self.custom_frame, text="Rows:").grid(row=0, column=0)
        self.rows_entry = tk.Entry(self.custom_frame, width=5)
        self.rows_entry.grid(row=0, column=1)
        self.rows_entry.insert(0, "16")

        tk.Label(self.custom_frame, text="Cols:").grid(row=1, column=0)
        self.cols_entry = tk.Entry(self.custom_frame, width=5)
        self.cols_entry.grid(row=1, column=1)
        self.cols_entry.insert(0, "16")

        tk.Label(self.custom_frame, text="Mines:").grid(row=2, column=0)
        self.mines_entry = tk.Entry(self.custom_frame, width=5)
        self.mines_entry.grid(row=2, column=1)
        self.mines_entry.insert(0, "40")

        self.start_button = tk.Button(self, text="Start Game", command=self.start_game)
        self.start_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.toggle_custom_entries()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.wait_window(self)

    def toggle_custom_entries(self):
        state = 'normal' if self.difficulty.get() == "custom" else 'disabled'
        for child in self.custom_frame.winfo_children():
            if isinstance(child, tk.Entry):
                child.configure(state=state)

    def start_game(self):
        difficulty = self.difficulty.get()
        if difficulty == "easy": self.result = (9, 9, 10)
        elif difficulty == "medium": self.result = (16, 16, 40)
        elif difficulty == "hard": self.result = (16, 30, 99)
        else:
            try:
                rows, cols, mines = int(self.rows_entry.get()), int(self.cols_entry.get()), int(self.mines_entry.get())
                if not (9 <= rows <= 24 and 9 <= cols <= 30 and 10 <= mines <= (rows * cols) - 10):
                    tk.messagebox.showerror("Invalid Settings", "Check custom values.\n(Rows: 9-24, Cols: 9-30, Mines: 10 to Rows*Cols-10)")
                    return
                self.result = (rows, cols, mines)
            except ValueError:
                tk.messagebox.showerror("Invalid Input", "Please enter valid numbers.")
                return
        self.destroy()

    def on_close(self):
        self.result = None
        self.destroy()

class App:
    def __init__(self, master):
        self.master = master
        self.current_game_frame = None
        self.master.title("Minesweeper")
        self.show_settings()

    def show_settings(self):
        if self.current_game_frame:
            self.current_game_frame.destroy()

        # DO NOT HIDE THE MAIN WINDOW. This is the key change.
        # self.master.withdraw()
        settings_dialog = SettingsDialog(self.master)
        settings = settings_dialog.result

        if settings:
            # self.master.deiconify()
            self.start_game(settings)
        else:
            self.master.destroy()

    def start_game(self, settings):
        rows, cols, mines = settings
        self.current_game_frame = Minesweeper(self.master, rows, cols, mines, self.show_settings)
        
        self.master.update_idletasks()
        width = self.current_game_frame.winfo_width()
        height = self.current_game_frame.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f'{width}x{height}+{x}+{y}')

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
