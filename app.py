from flask import Flask, render_template, request
from typing import List

app = Flask(__name__)

# Sudoku Solver using recursive backtracking
def solve_sudoku(board: List[List[str]]) -> bool:
    # Helper: Check if placing a number is valid
    def is_valid(row, col, num):
        for i in range(9):
            if board[i][col] == num:  # Check column
                return False
            if board[row][i] == num:  # Check row
                return False
            # Check 3x3 box
            box_row = 3 * (row // 3) + i // 3
            box_col = 3 * (col // 3) + i % 3
            if board[box_row][box_col] == num:
                return False
        return True

    # Recursive function to fill the board
    def fill(row, col):
        if row == 9:  # Solved entire board
            return True
        if col == 9:  # End of row, go to next
            return fill(row + 1, 0)
        if board[row][col] != '.':  # Skip filled cell
            return fill(row, col + 1)

        for num in map(str, range(1, 10)):  # Try numbers 1–9
            if is_valid(row, col, num):
                board[row][col] = num
                if fill(row, col + 1):  # Recurse
                    return True
                board[row][col] = '.'  # Backtrack

        return False  # No valid number found

    return fill(0, 0)

# Flask route to show and solve the puzzle
@app.route('/', methods=['GET', 'POST'])
def index():
    board = [['' for _ in range(9)] for _ in range(9)]
    solved_cells = [[False for _ in range(9)] for _ in range(9)]
    error_message = None

    if request.method == 'POST':
        board = [
            [request.form.get(f'cell-{r}-{c}', '.') or '.' for c in range(9)]
            for r in range(9)
        ]

        # Validate user input: must be empty or digit 1–9
        for r in range(9):
            for c in range(9):
                val = board[r][c]
                if val not in [str(i) for i in range(1, 10)] and val != '.':
                    error_message = "Only digits 1–9 are allowed. Please correct the input."
                    return render_template('index.html', board=board, solved=solved_cells, error=error_message)

        # Track original filled cells
        original = [
            [cell if cell != '.' and cell != '' else '' for cell in row]
            for row in board
        ]

        # Validate Sudoku rules before solving
        def is_valid_cell(board, row, col, num):
            for i in range(9):
                if board[row][i] == num or board[i][col] == num:
                    return False
                box_row = 3 * (row // 3) + i // 3
                box_col = 3 * (col // 3) + i % 3
                if board[box_row][box_col] == num:
                    return False
            return True

        def is_valid_board(board):
            for r in range(9):
                for c in range(9):
                    num = board[r][c]
                    if num == '.' or num == '':
                        continue
                    board[r][c] = '.'  # Temporarily clear it
                    if not is_valid_cell(board, r, c, num):
                        return False
                    board[r][c] = num  # Restore it
            return True

        if not is_valid_board(board):
            error_message = "Sudoku rules violated. Check for duplicate numbers."
            return render_template('index.html', board=board, solved=solved_cells, error=error_message)

        if not solve_sudoku(board):
            error_message = "This Sudoku puzzle cannot be solved."
            return render_template('index.html', board=board, solved=solved_cells, error=error_message)

        # Mark solved cells
        for r in range(9):
            for c in range(9):
                if original[r][c] == '' and board[r][c] != '':
                    solved_cells[r][c] = True

    return render_template('index.html', board=board, solved=solved_cells, error=error_message)


if __name__ == '__main__':
    app.run(debug=True)
