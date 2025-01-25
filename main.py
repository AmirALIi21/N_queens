import tkinter as tk
from tkinter import messagebox
import random

class NQueensGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("N-Queens Solver")
        
        # Configuration frame
        self.config_frame = tk.Frame(self.root)
        self.config_frame.pack(pady=10)
        
        tk.Label(self.config_frame, text="Board Size:").pack(side=tk.LEFT)
        self.board_size_var = tk.StringVar(value="8")
        tk.Entry(self.config_frame, textvariable=self.board_size_var, width=5).pack(side=tk.LEFT, padx=5)
        
        tk.Label(self.config_frame, text="Number of Queens:").pack(side=tk.LEFT, padx=5)
        self.num_queens_var = tk.StringVar(value="4")
        tk.Entry(self.config_frame, textvariable=self.num_queens_var, width=5).pack(side=tk.LEFT)
        
        tk.Button(self.config_frame, text="Solve", command=self.solve).pack(side=tk.LEFT, padx=10)
        
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack(padx=10, pady=10)
        
        self.colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'magenta', 'yellow']
        self.root.mainloop()

    def is_safe(self, board, row, col, n):
        # Check row
        for j in range(n):
            if board[row][j] != -1:
                return False
                
        # Check column
        for i in range(n):
            if board[i][col] != -1:
                return False
                
        # Check diagonals
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] != -1:
                return False
        for i, j in zip(range(row, n, 1), range(col, -1, -1)):
            if board[i][j] != -1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, n, 1)):
            if board[i][j] != -1:
                return False
        for i, j in zip(range(row, n, 1), range(col, n, 1)):
            if board[i][j] != -1:
                return False
                
        return True

    def solve_n_queens_util(self, board, queens_left, n, queen_num):
        if queens_left == 0:
            return True
            
        for row in range(n):
            for col in range(n):
                if self.is_safe(board, row, col, n):
                    board[row][col] = queen_num
                    if self.solve_n_queens_util(board, queens_left - 1, n, queen_num + 1):
                        return True
                    board[row][col] = -1
                    
        return False

    def draw_board(self, board_size, board, queen_positions):
        self.canvas.delete("all")
        cell_size = min(480 // board_size, 480 // board_size)
        offset = 10
        
        # Draw the chess board
        for i in range(board_size):
            for j in range(board_size):
                x1 = offset + j * cell_size
                y1 = offset + i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                color = "white" if (i + j) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        
        # Draw threat zones and queens
        for queen_num, (row, col) in enumerate(queen_positions):
            color = self.colors[queen_num % len(self.colors)]
            
            # Draw horizontal and vertical lines (semi-transparent)
            for i in range(board_size):
                # Horizontal
                x1 = offset + 0
                y1 = offset + row * cell_size + cell_size // 2
                x2 = offset + board_size * cell_size
                y2 = y1
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2, dash=(4, 4))
                
                # Vertical
                x1 = offset + col * cell_size + cell_size // 2
                y1 = offset + 0
                x2 = x1
                y2 = offset + board_size * cell_size
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2, dash=(4, 4))
            
            # Draw diagonals
            for i in range(-board_size, board_size):
                if 0 <= row + i < board_size and 0 <= col + i < board_size:
                    x1 = offset + (col + i) * cell_size + cell_size // 2
                    y1 = offset + (row + i) * cell_size + cell_size // 2
                    x2 = x1
                    y2 = y1
                    self.canvas.create_line(x1, y1, x2, y2, fill=color, width=4)
                    
                if 0 <= row + i < board_size and 0 <= col - i < board_size:
                    x1 = offset + (col - i) * cell_size + cell_size // 2
                    y1 = offset + (row + i) * cell_size + cell_size // 2
                    x2 = x1
                    y2 = y1
                    self.canvas.create_line(x1, y1, x2, y2, fill=color, width=4)
            
            # Draw queen
            queen_x = offset + col * cell_size + cell_size // 2
            queen_y = offset + row * cell_size + cell_size // 2
            queen_size = cell_size // 3
            self.canvas.create_oval(queen_x - queen_size, queen_y - queen_size,
                                  queen_x + queen_size, queen_y + queen_size,
                                  fill=color, outline="black", width=2)

    def solve(self):
        try:
            n = int(self.board_size_var.get())
            num_queens = int(self.num_queens_var.get())
            
            if n < 1 or num_queens < 1:
                messagebox.showerror("Error", "Board size and number of queens must be positive")
                return
                
            if num_queens > n * n:
                messagebox.showerror("Error", "Too many queens for the board size")
                return
                
            board = [[-1 for _ in range(n)] for _ in range(n)]
            
            if self.solve_n_queens_util(board, num_queens, n, 0):
                queen_positions = []
                for i in range(n):
                    for j in range(n):
                        if board[i][j] != -1:
                            queen_positions.append((i, j))
                self.draw_board(n, board, queen_positions)
            else:
                messagebox.showinfo("No Solution", 
                    f"No solution exists for {num_queens} queens on a {n}x{n} board")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

if __name__ == "__main__":
    NQueensGUI()