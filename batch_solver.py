import pandas as pd
import time
from solver import solve_sudoku

# Load CSV, force quizzes column to string
df = pd.read_csv("sudoku.csv", converters={'quizzes': str})

# Clean: Drop NaNs and filter only 81-digit numeric strings
df = df.dropna(subset=['quizzes'])
df = df[df['quizzes'].str.match(r'^[0-9]{81}$')]

# Stop if no valid rows
if len(df) == 0:
    raise ValueError("No valid puzzles found in the dataset.")

# Parse 81-char puzzle string to 9x9 board
def parse_puzzle(puzzle_str):
    return [[char if char != '0' else '.' for char in puzzle_str[i*9:(i+1)*9]] for i in range(9)]

# Sample 100 puzzles
sample_df = df.sample(n=min(100, len(df)), random_state=42)

# Time the solving
start_time = time.time()
for puzzle_str in sample_df['quizzes']:
    board = parse_puzzle(puzzle_str)
    solve_sudoku(board)
end_time = time.time()

# Estimate total time
total_time = end_time - start_time
avg_time_per_puzzle = total_time / len(sample_df)
estimated_total_time = avg_time_per_puzzle * len(df)

# Output
print(f"Solved {len(sample_df)} puzzles in {total_time:.2f} seconds")
print(f"Avg time per puzzle: {avg_time_per_puzzle:.4f} seconds")
print(f"Estimated time to solve all puzzles: {estimated_total_time / 60:.2f} minutes")
