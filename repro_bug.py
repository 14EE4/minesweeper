import tkinter as tk
from minesweeper_gui import Minesweeper

class MockMaster(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw() # Hide window

def test_flag_overwrite():
    root = MockMaster()
    
    # Create fixed board 3x3
    # M 1 0
    # 1 1 0
    # 0 0 0
    # (0,0) is mine. 
    # (0,2), (1,2), (2,0)..(2,2) are 0s.
    
    game = Minesweeper(root, 3, 3, 1, lambda: None)
    
    # Manually set mine map to be deterministic
    # We override place_mines or just set data directly after init
    game.mine_map = [
        ['M', '1', '0'],
        ['1', '1', '0'],
        ['0', '0', '0']
    ]
    # Set buttons to match
    game.buttons[0][0].config(state='normal')
    
    # User validates logic:
    # 1. Flag (0, 1) which is safe '1'. (User mistake or strategy)
    game.toggle_flag(0, 1)
    
    print(f"Cell (0,1) text after flag: '{game.buttons[0][1]['text']}'")
    assert game.buttons[0][1]['text'] == '🚩'
    
    # 2. Click (2, 2) which is '0'. Should expand.
    # Expansion should reach (0, 1) because it's neighbor of (0, 2) '0'.
    # If bug exists, (0, 1) flag will be cleared and revealed as '1'.
    
    print("Clicking (2,2) [Zero cell]...")
    game.reveal_cell(2, 2)
    
    print(f"Cell (0,1) text after expansion: '{game.buttons[0][1]['text']}'")
    print(f"Cell (0,1) state after expansion: '{game.buttons[0][1]['state']}'")
    
    if game.buttons[0][1]['text'] != '🚩':
        print("BUG REPRODUCED: Flag was overwritten!")
    else:
        print("Bug not reproduced: Flag preserved.")

    root.destroy()

if __name__ == "__main__":
    test_flag_overwrite()
