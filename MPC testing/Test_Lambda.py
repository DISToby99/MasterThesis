# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Define the fitting function: lambda + k * f(u)
def fitting_function(u, lambda_, k, k1, k2, k3):
    u1, u2, u3 = u  # Unpack u into individual components
    return lambda_ + k * (k1 * u1**4 + k2 * u2**4 + k3 * u3**4)

# Extract the optimal parameters (these values were found earlier)
lambda_opt =  6056.186618556514
k_opt =  -0.10094769454241467
k1_opt = 415.3967200502689
k2_opt = 21.623006044089664
k3_opt = 0.20265703139675303

# Generate time points
time = np.linspace(0, 10, 1000)

# Generate waveforms for u1, u2, u3
u1_wave = 2.6 * np.ones(len(time))  # * np.sin(2 * np.pi * 0.2 * time) + 2.5
u2_wave = 6.43 * np.ones(len(time))  # * np.sin(2 * np.pi * 0.1 * time) + 5.75
u3_wave = 15 * np.ones(len(time))  # * np.sin(2 * np.pi * 0.15 * time) + 10

# Evaluate the fitting function at each time point
lambda_wave = fitting_function([u1_wave, u2_wave, u3_wave], lambda_opt, k_opt, k1_opt, k2_opt, k3_opt)

# Set up subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 8))

# Plot lambda over time
axs[0].plot(time, lambda_wave, label='Lambda', color='blue')
axs[0].set_xlabel('Time')
axs[0].set_ylabel('Lambda')
axs[0].set_title('Lambda over time with oscillating u1, u2, and u3')
axs[0].grid(True)

# Plot u1, u2, and u3 over time
axs[1].plot(time, u1_wave, label='u1', color='red')
axs[1].plot(time, u2_wave, label='u2', color='green')
axs[1].plot(time, u3_wave, label='u3', color='purple')
axs[1].set_xlabel('Time')
axs[1].set_ylabel('Value')
axs[1].set_title('u1, u2, and u3 over time')
axs[1].legend()
axs[1].grid(True)

plt.tight_layout()
plt.show()
