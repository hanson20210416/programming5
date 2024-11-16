import re
import pandas as pd
import matplotlib.pyplot as plt

def extract_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    times = []
    # Regular expression to match the relevant lines
    pattern = re.compile(r'(\d+\.\d+)(user\s+\d+\.\d+system\s+)(\d+:\d+.\d+)')
    for line in lines:
        match = pattern.search(line)
        if match:
            # Extract the elapsed time
            elapsed_time = match.group(3)
            # Convert elapsed time to seconds
            minutes, seconds = map(float, elapsed_time.split(':'))
            total_seconds = minutes * 60 + seconds
            times.append(total_seconds)
    df = pd.DataFrame({'Workers': range(len(times)), 'Time': times})
    print(df)
    return df

def plot_data(df):
    # Plot 1: Workers vs Time
    plt.figure(figsize=(10, 5))
    plt.plot(df['Workers'], df['Time'], marker='o', label='Time vs Workers')
    plt.title('Performance: Workers vs Time')
    plt.xlabel('Number of Workers')
    plt.ylabel('Time (seconds)')
    plt.grid()
    plt.legend()
    plt.savefig('workers_vs_time.png')
    plt.show()

if __name__ == '__main__':
    # Extract data from the results.csv file
    filepath = '/homes/zhe/Desktop/programming/p5/week2/results.csv'
    data_frame = extract_data(filepath)
    # Plot the extracted data
    plot_data(data_frame)