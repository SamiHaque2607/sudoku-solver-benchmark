# solver.py

from typing import List

def solve_sudoku(board: List[List[str]]) -> bool:
    def is_valid(row, col, num):
        for i in range(9):
            if board[i][col] == num or board[row][i] == num:
                return False
            box_row = 3 * (row // 3) + i // 3
            box_col = 3 * (col // 3) + i % 3
            if board[box_row][box_col] == num:
                return False
        return True

    def fill(row, col):
        if row == 9:
            return True
        if col == 9:
            return fill(row + 1, 0)
        if board[row][col] != '.':
            return fill(row, col + 1)

        for num in map(str, range(1, 10)):
            if is_valid(row, col, num):
                board[row][col] = num
                if fill(row, col + 1):
                    return True
                board[row][col] = '.'

        return False

    return fill(0, 0)