# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import ModelEstimation as ME



class StartMPC:
    def __init__(self):
        _SP = 8
        n = 20
        x_len = 10
        x_width = 5
        y_len = 10

        x_init_len=[4, 6, 0.14, 0.1, 20]

        X_init = np.array([x_init_len])

        Y_init = np.ones(y_len)*7

        self.MPC = MPC(n, _SP, x_len, x_width, y_len, X_init, Y_init)

    def RunMPC(self, _x, _y, _SP):
            self.MPC.SP = _SP

            self.MPC.x = _x.copy()
            self.MPC.y = _y.copy()
            self.MPC.xNext = _x[3]  

            res = self.MPC.calculate()

            u = self.MPC.U
            return res.x[0], res.success

# MPC Controller Class
class MPC:
    def __init__(self, n_, SP_, Xlen, Xwidth, Ylen, X_init, Y_init):
        """Initialize MPC Controller."""
        self.model = ME.ModellEstimation(Xlen, Xwidth, Ylen, X_init, Y_init)
        self.lenX = Xlen
        self.lenY = Ylen
        self.x = self.model.x
        self.y = (np.ones(Ylen)*Y_init)
        self.xNext = (np.ones(Xwidth)*X_init[0])
        self.Xlen = Xlen-1
        self.u = np.zeros(n_)
        self.n = n_
        self.SP = SP_
        self.U = 0.4
        self.P = 33
        self.Q = 16
        self.R = 1
        self.J = 0

    
    
    def RunModel(self, u):
        """Estimating what the next n values will be"""
        
        self.model.x = self.x.copy()
        self.model.y = self.y.copy()

        t = np.linspace(0, 10,10)

        y = np.zeros(self.n)
        
        for i in range(self.n):
            x1 = np.interp(i+10, t, self.x[:,0])
            x2 = np.interp(i+10, t, self.x[:,1])
            x3 = self.xNext[2]
            x4 = u[i]
            x5 = np.interp(i+10, t, self.x[:,4])
            self.xNext = np.array([x1,x2,x3,x4,x5])
            self.model.x[self.Xlen][3] = u[i]
            self.model.NewSampleInX(self.xNext)
            y[i] = self.model.Estimate()
            
        
        return y
    

    # Objective function for optimization
    def ObjectiveFunction(self, u):
        """Objective function for MPC optimization."""

        ref = np.ones(self.n) * self.SP
        y = self.RunModel(u)
        
        e = ref - y
        u = np.insert(u, 0, self.U)
        deltaU = u[:self.n] - u[1:]
        
        self.J = (e.T * self.Q).dot(e) + (deltaU.T * self.P).dot(deltaU) + (u.T * self.R).dot(u)

    
        
        return self.J
    
    # Bounds for optimization
    def Constrains(self, u):
        """Define constrains for optimization."""
       
        def MinChangeU(u):
            u = np.insert(u, 0, self.U)
            deltaU = u[:self.n] - u[1:]
            
            return deltaU - 1  # Example constraint: u[i] - u[i-1] >= 1.0
        
        cons = {'type': 'ineq', 'fun': MinChangeU}
        return cons
        
        
    
    # Optimization calculation
    def calculate(self):
        """Perform optimization and update control input."""
        b = np.zeros((self.n, 2))
        
        for i in range(self.n):
            b[i][0] = 0
            b[i][1] = 1
        
        x0 = self.u
        res = minimize(self.ObjectiveFunction, x0, method='SLSQP', bounds=b)
        self.U = res.x[0]

        return res