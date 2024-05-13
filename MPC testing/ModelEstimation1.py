import numpy as np

class ModellEstimation:
    def __init__(self, Xlen, Xwidth, Ylen, X_init, Y_init):
        # Initialize the model with initial values for X and Y
        self.x = (np.ones([Xlen, Xwidth])*X_init)
        self.y = np.ones(Ylen)*Y_init
        self.lenX = Xlen
        self.lenY = Ylen
        
    def NewSampleInX(self, newX):
        # Update the values of X with a new sample
        for i in range(self.lenX - 1):
            self.x[i] = self.x[i + 1][:]
        self.x[self.lenX-1] = newX  # Update the first row with the new value
        
    def NewSampleInY(self, newY):
        # Update the values of Y with a new sample
        for i in range(self.lenY - 1):
            self.y[i] = self.y[i + 1]
        self.y[self.lenY-1] = newY  # Update the first row with the new value
        
    def Estimate(self):
        # Perform estimation based on the current values of X and Y
        y = self.y
        x1 = self.x[:,0]
        x2 = self.x[:,1]
        x3 = self.x[:,2]
        x4 = self.x[:,3]*0.14
        x5 = self.x[:,4]
        k=10
        y_hat = 1.0239*y[k-1] + -1.4126E-3*x2[k-1]*x1[k-5]*y[k-1] + 1.6950E-01*x4[k-4]*x1[k-5]**2 + \
                -3.3035E-04*x5[k-9]*y[k-1]**2 + 2.7617E-04*x5[k-10]*y[k-1]**2 
        
        # Update Y with the estimated value
        self.NewSampleInY(y_hat)
        return y_hat
    
    def EstimateOld(self):
        # Perform an alternative estimation based on the current values of X and Y
        y = self.y
        x1 = self.x[:,0]
        x2 = self.x[:,1]
        x3 = self.x[:,2]
        x4 = self.x[:,3]*0.14
        x5 = self.x[:,4]
        k=10
        y_hat = 1.0239*y[k-1] + -1.4126E-3*x2[k-1]*x1[k-4]*y[k-1] + 1.6950E-01*x4[k-3]*x1[k-1]**2 + \
                -3.3035E-04*x5[k-1]*y[k-1]**2 + 2.7617E-04*x5[k-2]*y[k-1]**2 
        
        # Update Y with the estimated value
        self.NewSampleInY(y_hat)
        return y_hat

    def LaplaceModel(self):
        # Perform estimation using a Laplace model based on the current values of X and Y
        y = self.y
        x1 = self.x[:,0]
        x2 = self.x[:,1]
        x3 = self.x[:,2]
        x4 = self.x[:,3]*0.14
        x5 = self.x[:,4]
        k=10
        
        # Model parameters
        tau = 68201174.810846
        k1 = 27.59008722368786
        k2 = 1.411641696178872
        k3 = 0.019655581687325695
        k4 = 0.5122622877351493
        k5 = -0.08198366078302685
        
        # Estimate using the Laplace model equation
        y_hat = -1/tau * y[k-1] + k1 * x4[k-4] + k2 * x1[k-4] + k3 * x2[k-1] + k4 * x3[k-1] + k5 * x5[k-9]
        
        # Return the estimated value
        return y_hat
