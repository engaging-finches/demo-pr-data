import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('test.csv', header=None)
output_folder = './graphs/'
os.makedirs(output_folder, exist_ok=True)

pr_number = df.iloc[:, 0]
created_at = pd.to_datetime(df.iloc[1:, 3].reset_index(drop=True))
closed_at = pd.to_datetime(df.iloc[1:, 5].reset_index(drop=True))
time_diffs = []

# calculates time difference in minutes
def calculate_time_difference(row):
    try:
        return (closed_at.iloc[row] - created_at.iloc[row]).total_seconds() / 60
    except (TypeError, IndexError):
        # Handle NaN values or invalid indices
        return None

# Populate time_diffs list with valid values
for i in range(len(created_at)):
    time_diff = calculate_time_difference(i)
    if time_diff is not None:
        time_diffs.append(time_diff)

valid_time_diffs = [td for td in time_diffs if not np.isnan(td)] #filters out nan values
timestamps_every_10_minutes = np.arange(0, max(valid_time_diffs), 10) #generates y values in 10 minute intervals

plt.plot(pr_number.iloc[1:], time_diffs, marker='o', linestyle='-', color='b')
plt.yticks(timestamps_every_10_minutes)
plt.xlabel('PR Number')
plt.ylabel('Time Difference (minutes)')
plt.title('PR Duration in Repository')
plt.grid(True)
plt.ylim(top=300)
plt.ylim(bottom=0)

# Save the plot to the 'graphs' directory
output_file_path = os.path.join(output_folder, 'pr_duration_plot.png')
plt.savefig(output_file_path)

print(f"Graph saved at '{output_file_path}'")