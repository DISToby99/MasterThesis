# Import necessary libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# Read data from a CSV file
data = pd.read_csv('Place where CSV is stored', delimiter=';')

# Define the model function
def model(t, tau1, tau2, theta, k1, k2):
    return (y_data - u1_data) / tau1 + k1 * u4_data + (u2_data - u3_data) / tau2 + k2 * u5_data

# Extract data from the DataFrame
t_data = data['Time']
y_data = data['DS_out']
u1_data = data['DS_in']
u2_data = data['Q_in']
u3_data = data['Q_w']
u4_data = data['u'] * 0.14  # Assuming some modification on 'u'
u5_data = data['f_T']

# Perform curve fitting
popt, pcov = curve_fit(model, t_data, y_data)

# Extract estimated parameter values
tau1_estimert, tau2_estimert, theta_estimert, k1_estimert, k2_estimert = popt

print("Estimated values:")
print("Tau1:", tau1_estimert)
print("Tau2:", tau2_estimert)
print("Theta:", theta_estimert)
print("k1:", k1_estimert)
print("k2:", k2_estimert)

# Plot the estimated model against the actual data
plt.plot(t_data, y_data, 'b-', label='Actual data')
plt.plot(t_data, model(t_data, *popt), 'r--', label='Estimated model')
plt.xlabel('Time')
plt.ylabel('Response')
plt.legend()
plt.show()
