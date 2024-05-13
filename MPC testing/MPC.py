# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import ModelEstimation1 as ME  # Importing a module named ModelEstimation1 as ME
import time

# MPC Controller Class
class MPC:
    def __init__(self, n_, SP_, Xlen, Xwidth, Ylen, X_init, Y_init):
        """Initialize MPC Controller."""
        self.model = ME.ModellEstimation(Xlen, Xwidth, Ylen, X_init, Y_init)  # Initialize a model for estimation
        self.lenX = Xlen
        self.lenY = Ylen
        self.x = self.model.x
        self.y = (np.ones(Ylen)*Y_init)
        self.xNext = (np.ones(Xwidth)*X_init[0])
        self.Xlen = Xlen-1
        self.u = np.zeros(n_)
        self.n = n_
        self.SP = SP_
        self.U = 0.1
        self.P = 6998  # Control parameter
        self.Q = 16  # Control parameter
        self.R = 1  # Control parameter
        self.J = 0  # Objective function value
        self.min = 0  # Minimum value
        self.NewLim = False  # Flag for new limit
        self.CalculetedMax = 1  # Calculated maximum value
        
    def NewSampleInX(self, newX):
        """Update the values of X with a new sample."""
        for i in range(self.lenX - 1):
            self.x[i] = self.x[i + 1][:]

        self.x[self.lenX-1] = newX  # Update the first row with the new value
        
    def NewSampleInY(self, newY):
        """Update the values of Y with a new sample."""
        for i in range(self.lenY - 1):
            self.y[i] = self.y[i + 1]

        self.y[self.lenY-1] = newY  # Update the first row with the new value
    
    def RunModel(self, u):
        """Estimate the next n values."""
        self.model.x = self.x.copy()
        self.model.y = self.y.copy()
        t = np.linspace(0, 10, 10)  # Define time points
        
        # Define the indices for checking differences
        indices = [0, 1, 3, 4, 5, 6, 7, 8, 9]
        # Define the expected difference
        expected_diff = 0.5
        # Compute the differences for the specified indices
        diff = self.x[indices, 1] - np.roll(self.x[indices, 1], -1)
        
        y = np.zeros(self.n)
        
        for i in range(self.n):
            x1 = np.interp(i+10, t, self.x[:,0])
            if not np.allclose(diff, expected_diff):
                x2 = self.x[9,1]
            else:
                x2 = np.interp(i+10, t, self.x[:,1])
            x3 = np.interp(i+10, t, self.x[:,2])
            x4 = u[i]
            x5 = np.interp(i+10, t, self.x[:,4])
            self.xNext = np.array([x1,x2,x3,x4,x5])
            self.model.NewSampleInX(self.xNext)
            y[i] = self.model.Estimate()  # Estimate next value
        
        return y
    
    def ObjectiveFunction(self, u):
        """Objective function for MPC optimization."""
        #Making a vector for the setpoint
        ref = np.ones(self.n) * self.SP
        
        #Estimating
        y = self.RunModel(u)
        
        #Finding the error
        e = ref - y
        #Setting the previous used u into u
        u = np.insert(u, 0, self.U)
        #Finding the change in u
        deltaU = u[:self.n] - u[1:]
        
        lam = max(6247.25+ 6.71 * (-121.25 * self.x[9,0] + \
                                -87.54 * self.x[9,1] + \
                                -3.51 * self.x[9,4]),0)
        
        #Calculating objective function
        self.J = (e.T * self.Q @ e) + (deltaU.T * self.P @ deltaU) + (u.T * self.R @ u) \
            + np.maximum(0, 0.15 - u.T) * lam @ np.maximum(0, 0.15 - u)

        return self.J
    
    def Constraints(self, u):
        """Define constraints for optimization."""
        def MinChangeU(u):
            z = np.insert(u, 0, self.U)
            deltaU = np.diff(z)  # Calculate differences between consecutive elements of u
            return deltaU - 0.001  # Constraint: deltaU >= 0.05
        
        def MaxChangeU(u):
            z = np.insert(u, 0, self.U)
            deltaU = np.diff(z)  # Calculate differences between consecutive elements of u
            return 1 - deltaU  # Constraint: deltaU <= 0.05
    
        min_constraint = {'type': 'ineq', 'fun': MinChangeU}
        #max_constraint = {'type': 'ineq', 'fun': MaxChangeU}
        
        return [min_constraint]#, max_constraint]
    
    def calculate(self):
        """Perform optimization and update control input."""
        b = np.zeros((self.n, 2))
        
        delatQ = self.x[9,1]-self.x[8,1]
        if delatQ>0.9:
            self.NewLim = True
            self.CalculetedMax = min(self.U*2,1)
        if self.min >= 40 and self.NewLim:
            self.min = 0
            self.NewLim = False
        elif self.NewLim:
            self.min += 1          
        
        for i in range(self.n):
            if self.NewLim:
                b[i][0] = 0.05
                b[i][1] = self.CalculetedMax
            else:
                b[i][0] = 0.05
                b[i][1] = 1
        
        x0 = self.u
        res = minimize(self.ObjectiveFunction, x0, method='SLSQP', bounds=b)#, constraints=self.Constraints(x0))
        if not(res.success):
            print("Problem")
        self.U = res.x[0]  # Update control input
        return res

# Main Simulation
start = 0
stop = 2*24*60  # Simulation duration
print('The simulation will last:', stop-start, 'minutes')
dt = 1
SP = 8.2  # Setpoint
n = 60  # Number of samples

time1 = int((stop - start) / dt)
DS1 = np.zeros(time1)
DS2 = np.zeros(time1)
u = np.ones(time1)
t = np.linspace
