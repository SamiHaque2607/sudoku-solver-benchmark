import matplotlib.pyplot as plt

try:
    with open("cpp_time.txt", "r") as f:
        cpp_time = float(f.read().strip())
except FileNotFoundError:
    print("cpp_time.txt not found. Please run the C++ solver first.")
    cpp_time = None

python_time = 810  # seconds (13.5 minutes)

if cpp_time is not None:
    languages = ['Python', 'C++']
    times = [python_time, cpp_time]

    plt.figure(figsize=(6, 5))
    bars = plt.bar(languages, times, width=0.4, color=['#4C72B0', '#55A868'])

    for bar, time in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 20,
                 f"{time:.1f}s",
                 ha='center',
                 va='bottom',
                 fontsize=11,
                 fontweight='medium')

    plt.title('Performance Comparison: Python vs C++\n(Sudoku Solver – 1M Puzzles)', fontsize=14, pad=20)
    plt.ylabel('Time (seconds)', fontsize=12)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)

    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.box(False)
    plt.tight_layout()
    plt.show()