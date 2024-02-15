import numpy as np

class ModellEstimation:
    def __init__(self, Xlen, Xwidth, Ylen, X_init, Y_init):
        self.x = (np.ones([Xlen, Xwidth])*X_init)
        self.y = np.ones(Ylen)*Y_init
        self.lenX = Xlen
        self.lenY = Ylen
        
    def NewSampleInX(self, newX):
        for i in range(self.lenX - 1):
            self.x[i] = self.x[i + 1][:]

        self.x[self.lenX-1] = newX  # Update the first row with the new value
        x = self.x

        
    def NewSampleInY(self, newY):
        for i in range(self.lenY - 1):
            self.y[i] = self.y[i + 1]

        self.y[self.lenY-1] = newY  # Update the first row with the new value
        y = self.y

        
    def Estimate(self):
        y = self.y
        x1 = self.x[:,0]
        x2 = self.x[:,1]
        x3 = self.x[:,2]
        x4 = self.x[:,3]*0.14
        x5 = self.x[:,4]
        k=10
        y_hat = 1.0239*y[k-1] + -1.4126E-3*x2[k-1]*x1[k-6]*y[k-1] + 1.6950E-01*x4[k-4]*x1[k-6]**2 + \
                -3.3035E-04*x5[k-10]*y[k-1]**2 + 2.7617E-04*x5[k-10]*y[k-1]**2 
        
        self.NewSampleInY(y_hat)
        return y_hat
    
    def EstimateOld(self):
        y = self.y
        x1 = self.x[:,0]
        x2 = self.x[:,1]
        x3 = self.x[:,2]
        x4 = self.x[:,3]*0.14
        x5 = self.x[:,4]
        k=6
        y_hat = 1.0239*y[k-1] + -1.4126E-3*x2[k-1]*x1[k-4]*y[k-1] + 1.6950E-01*x4[k-4]*x1[k-1]**2 + \
                -3.3035E-04*x5[k-2]*y[k-1]**2 + 2.7617E-04*x5[k-2]*y[k-1]**2 
        
        self.NewSampleInY(y_hat)
        return y_hat

        