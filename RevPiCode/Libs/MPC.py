# Importing necessary libraries
import numpy as np
from scipy.optimize import minimize
import ModelEstimation as ME

class StartMPC:
    def __init__(self):
        """Initialize the MPC controller."""
        _SP = 8  # Setpoint
        n = 35  # Horizon length
        x_len = 10  # Length of X matrix
        x_width = 5  # Width of X matrix
        y_len = 10  # Length of Y vector
        x_init_len = [4, 6, 0.14, 0.1, 20]  # Initial values for X matrix
        
        X_init = np.array([x_init_len])  # Initial X matrix
        Y_init = np.ones(y_len) * 7  # Initial Y vector
        
        # Initialize MPC controller
        self.MPC = MPC(n, _SP, x_len, x_width, y_len, X_init, Y_init)

    def RunMPC(self, _x, _y, _SP):
        """
        Run the MPC controller.

        Args:
        - _x (array-like): Current state vector.
        - _y (array-like): Current output vector.
        - _SP (float): Setpoint value.

        Returns:
        - float: Optimized control input.
        - bool: Success flag of the optimization.
        """
        # Update setpoint
        self.MPC.SP = _SP

        # Copy current state and output vectors
        self.MPC.x = _x.copy()
        self.MPC.y = _y.copy()
        self.MPC.xNext = _x[3]  

        # Perform MPC calculation
        res = self.MPC.calculate()

        # Extract control input and optimization success flag
        u = self.MPC.U
        return res.x[0], res.success

class MPC:
    def __init__(self, n_, SP_, Xlen, Xwidth, Ylen, X_init, Y_init):
        """Initialize MPC Controller."""
        # Initialize model estimation
        self.model = ME.ModellEstimation(Xlen, Xwidth, Ylen, X_init, Y_init)
        self.lenX = Xlen
        self.lenY = Ylen
        self.x = self.model.x
        self.y = (np.ones(Ylen) * Y_init)
        self.xNext = (np.ones(Xwidth) * X_init[0])
        self.Xlen = Xlen - 1
        self.u = np.zeros(n_)
        self.n = n_
        self.SP = SP_
        self.U = 0.2
        self.P = 10000  # Weight for input rate-of-change penalty
        self.Q = 16  # Weight for output error penalty
        self.R = 1  # Weight for input penalty
        self.J = 0  # Objective function value

    def RunModel(self, u):
        """Estimate the next n output values."""
        # Copy current state and output vectors
        self.model.x = self.x.copy()
        self.model.y = self.y.copy()

        # Initialize time vector
        t = np.linspace(0, 10, 10)

        # Initialize exponential difference threshold
        exp_diff = 1

        # Calculate difference between consecutive x values
        diff = self.x[0:10, 1] - np.roll(self.x[0:10, 1], -1)

        # Initialize output vector
        y = np.zeros(self.n)

        # Iterate over the horizon length
        for i in range(self.n):
            # Interpolate x values
            x1 = np.interp(i + 10, t, self.x[:, 0])
            if not np.any(np.abs(diff) > exp_diff):
                x2 = np.interp(i + 10, t, self.x[:, 1])
            else:
                x2 = self.x[9, 1]
            x3 = self.xNext[2]
            x4 = u[i]
            x5 = np.interp(i + 10, t, self.x[:, 4])

            # Update next x value and perform estimation
            self.xNext = np.array([x1, x2, x3, x4, x5])
            self.model.x[self.Xlen][3] = u[i]
            self.model.NewSampleInX(self.xNext)
            y[i] = self.model.Estimate()

        return y

    def ObjectiveFunction(self, u):
        """Calculate objective function for MPC optimization."""
        # Define reference vector
        ref = np.ones(self.n) * self.SP

        # Estimate output values
        y = self.RunModel(u)
        
        # Calculate error
        e = ref - y

        # Compute input rate-of-change
        u = np.insert(u, 0, self.U)
        deltaU = u[:self.n] - u[1:]

        # Define exponential difference threshold
        exp_diff = 1

        # Calculate difference between consecutive x values
        diff = self.x[0:10, 1] - np.roll(self.x[0:10, 1], -1)

        # Update penalty weights based on difference threshold
        if not np.any(np.abs(diff) > exp_diff):
            self.P = 11998
        else:
            self.P = 556

        # Calculate objective function value
        self.J = (e.T @ self.Q @ e) + (deltaU.T @ self.P @ deltaU) + (u.T @ self.R @ u) \
            + np.maximum(0, 0.15 - u.T) * lam @ np.maximum(0, 0.15 - u)

        return self.J

    def Constrains(self, u):
        """Define constraints for optimization."""
        # Define minimum change in control input
        def MinChangeU(u):
            u = np.insert(u, 0, self.U)
            deltaU = u[:self.n] - u[1:]
            return deltaU - 1
        
        # Define inequality constraint
        cons = {'type': 'ineq', 'fun': MinChangeU}
        return cons

    def calculate(self):
        """Perform optimization and update control input."""
        # Initialize bounds for optimization
        b = np.zeros((self.n, 2))
        
        # Define bounds
        for i in range(self.n):
            b[i][0] = 0.05
            b[i][1] = 1
        
        # Initialize optimization parameters
        x0 = self.u
        
        # Perform optimization using Sequential Least Squares Programming (SLSQP) method
        res = minimize(self.ObjectiveFunction, x0, method='SLSQP', bounds=b)

        # Update control input
        self.U = res.x[0]

        return res
