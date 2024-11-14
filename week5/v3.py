import pandas as pd
import re


def extract_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    times = []
    # Regular expression to match the elapsed time in the format "MM:SS.SS"
    pattern = re.compile(r'\d+:\d+\.\d+')

    for line in lines:
        match = pattern.search(line)
        if match:
            # Extract the elapsed time
            elapsed_time = match.group(0)
            # Convert elapsed time to seconds
            minutes, seconds = map(float, elapsed_time.split(':'))
            total_seconds = minutes * 60 + seconds
            times.append(total_seconds)
    
    # Create a DataFrame with sequential worker IDs and the extracted times
    df = pd.DataFrame({'Workers': range(len(times)), 'Time': times})
    print(df)
    return df

if __name__ == '__main__':
    # Extract data from the results.csv file
    filepath = '/homes/zhe/Desktop/programming/p5/week5/results.csv'
    data_frame = extract_data(filepath)
   