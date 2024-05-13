# Import necessary libraries
import numpy as np
from sysidentpy.model_structure_selection import FROLS
from sysidentpy.utils.save_load import save_model, load_model
import pandas as pd
import time
import matplotlib.pyplot as plt

# Read data from a CSV file
data = pd.read_csv('Place where CSV is stored', delimiter=';')

# Drop the 'Time' column from the data
data = data.drop(['Time'], axis=1)

# Extract features (Allx) and target (Ally) data
Allx = (data.drop(['QB01'], axis=1)).to_numpy()[:18000, :]
Ally = (data['QB01']).to_numpy().reshape(-1, 1)[:18000]

# Modify one of the features (Adding the DS of polymer)
Allx[:, 3] = Allx[:, 3] * 0.14

# Define a class for model estimation
class ModellEstimation:
    def __init__(self, Xlen, Xwidth, Ylen, X_init, Y_init):
        # Initialize state variables
        self.x = X_init
        self.y = Y_init
        self.lenX = Xlen
        self.lenY = Ylen
    
    # Method to update the state with a new sample in X
    def NewSampleInX(self, newX):
        for i in range(self.lenX - 1):
            self.x[i] = self.x[i + 1].copy()
        self.x[self.lenX - 1] = newX
    
    # Method to update the state with a new sample in Y
    def NewSampleInY(self, newY):
        for i in range(self.lenY - 1):
            self.y[i] = self.y[i + 1].copy()
        self.y[self.lenY - 1] = newY
        
    # Method to estimate the next value
    def Estimate(self):
        # Perform a specific estimation
        # ...
        self.NewSampleInY(y_hat)  # Update the state with the estimated value
        return y_hat
    
    # Method to try a model prediction
    def TryModel(self, model):
        # Perform model prediction
        # ...
        self.NewSampleInY(y_hat)  # Update the state with the predicted value
        return y_hat
    
    # Other estimation methods...
    
# Initialize model estimation object
Model = ModellEstimation(x_len, x_width, y_len, x, y)

# Iterate through the data points for prediction
for j in range(len(all_y) - 3):
    x = Allx[i]  # Select the features for prediction
    Model.NewSampleInX(x)  # Update the state with the new features
    y = Model.LaplaceModel2()  # Perform a specific model estimation
    all_y[j] = y  # Store the predicted value
    i = i + 1  # Move to the next data point

# Read additional data for comparison or visualization
data = pd.read_csv('C:/Users/toma/VEAS SELVKOST AS/Torbjørns Masteroppgave - General/Python debugging/PCA/InterpolationAllData.csv', delimiter=';')

# Plot the comparison between the predicted and actual values
data.plot(x="Time", subplots=True)
plt.legend()
plt.show()

# Plotting comparison with lab results
df = pd.read_csv('C:/Users/toma/VEAS SELVKOST AS/Torbjørns Masteroppgave - General/Prøvetaking/Labresultater.csv', delimiter=';')
df['Time'] = pd.to_datetime(df['Time'], format='%d.%m.%Y %H:%M')
data['Time'] = pd.to_datetime(data['Time'], format='%d.%m.%Y %H:%M')

plt.plot(data['Time'], data['QB01_hat'], color='red', label='Estimated')
plt.scatter(df['Time'], df['DS_out'], label='Sample analyzed at Laboratory')
plt.xlabel('Time')
plt.ylabel('%DS')
plt.legend()
plt.show()
