# Import necessary libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read data from a CSV file
data = pd.read_csv('Place where CSV is stored', delimiter=';')

# Define time intervals and corresponding initial values for TS0
start = 0
stop = 16
t0 = np.arange(stop - start + 1) + start
TS0 = np.ones(len(t0)) * 9
TS0[0] = 9

# Iterate through the data to calculate TS0 values
for previous_index, row in data.iterrows():
    if 0 < previous_index < stop + 1:
        change = row['DS_in'] / forige['DS_in'] - 0.01
        TS0[previous_index] = TS0[previous_index] * (change)
    forige = row

# Define time intervals and calculate TS1 and TS2
start = 17
stop = 38
t1 = np.arange(stop - start + 1) + start

start = 39
stop = 45
t2 = np.arange(stop - start + 1) + start

TS1 = 0.0042 * t1 ** 2 - 0.3736 * t1 + 12.598
TS2 = -0.1319 * t2 ** 2 + 11.652 * t2 - 248.28

# Define time intervals and initialize TS3
start = 46
stop = 299
t3 = np.arange(stop - start + 1) + start
TS3 = np.zeros(len(t3)) + 9.02

# Iterate through the data to calculate TS3 values based on previous samples
previous_samples = [None] * 3

for previous_index, row in data.iterrows():
    if previous_index > start:
        if all(sample is not None for sample in previous_samples):
            # Calculate changes and update TS3 values
            change1 = row['Q_in'] / previous_samples[0]['Q_in']
            change4 = row['Q_w'] / previous_samples[0]['Q_w']
            change1 = change1 - change4
            change2 = row['DS_in'] / previous_samples[0]['DS_in'] - 1
            change3 = row['f_T'] / previous_samples[0]['f_T']
            change3 = (1 - change3) if change3 > 1 else abs(1 - change3)
            change = (change1 / 5 + 1 * change3 / 8 + change2 / 9) + 1
            TS3[previous_index - start] = TS3[previous_index - start] * change
        else:
            TS3[previous_index - start] = TS3[previous_index - start - 1]

    # Update the previous samples
    previous_samples.pop(0)
    previous_samples.append(row)

# Combine TS values and time intervals
TS = np.concatenate((TS0, TS1, TS2, TS3))
t = np.concatenate((t0, t1, t2, t3))

# Plot data
axes = data.plot(x="Time", subplots=True)
labels = ['[%DS]', '[l/s]', '[l/s]', '[l/s]', '[FTU]', '[%DS]']

# Set labels for each y-axis
for i, ax in enumerate(axes):
    ax.set_ylabel(labels[i])

plt.legend()

# Additional data processing and visualization
# (Omitted for brevity)

# Save merged data to a CSV file
merged.to_csv('Path to save merged data', index=False, sep=';')
