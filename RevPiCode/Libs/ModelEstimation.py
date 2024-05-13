import numpy as np

class EstimateModel():
    def __init__(self):
        # Initialize the model with predefined parameters
        self.Xlen = 10
        self.model = ModellEstimation(Xlen=self.Xlen, Xwidth=5, Ylen=10, 
                                    X_init=[0,0,0,0,0], Y_init=8)


    def StartUp5x(self, newX):
        """
        Prepare the model for estimation by providing initial data.

        Args:
        - newX (array-like): Initial data to start estimation.

        Returns:
        - None
        """
        # The model needs data 5 samples backward before starting to estimate
        for i in range(self.Xlen):
            self.model.NewSampleInX(newX)


    def Estimate(self, newX):
        """
        Estimate the target variable based on the provided data.

        Args:
        - newX (array-like): New data to perform estimation.

        Returns:
        - y (float): Estimated value.
        """
        y = self.model.Estimate()

        # Puts all the new values into the x matrix
        self.model.NewSampleInX(newX)
        # print("Estimated:", y, "when x is:", model.x)

        return y


class ModellEstimation:
    def __init__(self, Xlen, Xwidth, Ylen, X_init, Y_init):
        """
        Initialize the model estimation object.

        Args:
        - Xlen (int): Length of X matrix.
        - Xwidth (int): Width of X matrix.
        - Ylen (int): Length of Y vector.
        - X_init (array-like): Initial values for X matrix.
        - Y_init (float): Initial value for Y vector.

        Returns:
        - None
        """
        self.x = (np.ones([Xlen, Xwidth]) * X_init)
        self.y = np.ones(Ylen) * Y_init
        self.lenX = Xlen
        self.lenY = Ylen
        
    def NewSampleInX(self, newX):
        """
        Update the X matrix with a new sample.

        Args:
        - newX (array-like): New sample to be added to X matrix.

        Returns:
        - None
        """
        for i in range(self.lenX - 1):
            self.x[i] = self.x[i + 1][:]

        self.x[self.lenX-1] = newX  # Update the first row with the new value
        x = self.x

        
    def NewSampleInY(self, newY):
        """
        Update the Y vector with a new sample.

        Args:
        - newY (float): New value to be added to Y vector.

        Returns:
        - None
        """
        for i in range(self.lenY - 1):
            self.y[i] = self.y[i + 1]

        self.y[self.lenY-1] = newY  # Update the first row with the new value

        
    def Estimate(self):
        """
        Perform estimation based on current X and Y values.

        Args:
        - None

        Returns:
        - y_hat (float): Estimated value.
        """
        y = self.y
        x1 = self.x[:, 0]
        x2 = self.x[:, 1]
        x3 = self.x[:, 2]
        x4 = self.x[:, 3] * x3
        x5 = self.x[:, 4]
        k = self.lenX
        y_hat = 1.0239*y[k-1] + -1.4126E-3*x2[k-1]*x1[k-6]*y[k-1] + 1.6950E-01*x4[k-3]*x1[k-6]**2 + \
                -3.3035E-04*x5[k-10]*y[k-1]**2 + 2.7617E-04*x5[k-9]*y[k-1]**2 
        
        # self.NewSampleInY(y_hat)
        return y_hat
