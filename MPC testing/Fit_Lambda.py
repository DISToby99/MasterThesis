import numpy as np
from scipy.optimize import curve_fit


# Define the function to fit: lambda + k * f(u)
def fit_function(u, lambda_, k, k1, k2, k3):
    u1, u2, u3 = u  # Unpack u into individual components
    return lambda_ + k * (k1 * u1 + k2 * u2 + k3 * u3)

# Extract u and lambda values from known points
u = np.array([[2.5, 5.1, 8.15],
              [2.5, 6, 12],
              [3, 5.2, 12],
              [3, 6, 8],
              [2.2, 5.3, 10],
              [2.2, 5.3, 6.75]])
lambda_values = np.array([1050, 500, 500, 0, 900, 1300])

# Fit the function to the known points
popt, _ = curve_fit(fit_function, u.T, lambda_values)

# Extract the optimal parameters
lambda_opt, k_opt, k1_opt, k2_opt, k3_opt = popt

# Print the optimized parameters
print("Optimized lambda:", lambda_opt)
print("Optimized k:", k_opt)
print("Optimized k1:", k1_opt)
print("Optimized k2:", k2_opt)
print("Optimized k3:", k3_opt)
