# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import ModelEstimation1 as ME
import time

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
        
    def NewSampleInX(self, newX):
        for i in range(self.lenX - 1):
            self.x[i] = self.x[i + 1][:]

        self.x[self.lenX-1] = newX  # Update the first row with the new value


        
    def NewSampleInY(self, newY):
        for i in range(self.lenY - 1):
            self.y[i] = self.y[i + 1]

        self.y[self.lenY-1] = newY  # Update the first row with the new value

    
    
    def RunModel(self, u):
        """Estimating what the next n values will be"""
        
        self.model.x = self.x.copy()
        self.model.y = self.y.copy()
        
        #print("\nNew run \nWith start values as:", self.model.y, self.y)
        t = np.linspace(0, 10,10)

        
        y = np.zeros(self.n)
        
        for i in range(self.n):
            x1 = np.interp(i+10, t, self.x[:,0])
            x2 = np.interp(i+10, t, self.x[:,1])
            x3 = 0
            x4 = u[i]
            x5 = np.interp(i+10, t, self.x[:,4])
            self.xNext = np.array([x1,x2,x3,x4,x5])
            #self.xNext[3] = x4
            self.model.NewSampleInX(self.xNext)
            y[i] = self.model.Estimate()
            #print(y[i])
            
        
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
        #print(J)
    
        
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
        res = minimize(self.ObjectiveFunction, x0, method='SLSQP', bounds=b)#, constraints=[self.Constrains(u)])
        if not(res.success):
            print("Problem")
        #     res = minimize(self.ObjectiveFunction, x0, method='SLSQP', bounds=b)#, constraints=[self.Constrains(u)])
        #     if not(res.success):
        #         print("2nd try problem")
        self.U = res.x[0]
        #print(self.U)
        return res



# Main Simulation
start = 0
stop = 2*24*60
print('The simulation will last:', stop-start, 'seconds')
dt = 1
SP = 8
n = 25

time1 = int((stop - start) / dt)
DS1 = np.zeros(time1)
DS2 = np.zeros(time1)
u = np.ones(time1)
t = np.linspace(start, stop, time1)
SetPoint = np.ones(time1)

x_len = 10
x_width = 5
y_len = 10

x_init_len=[4.1, 6.2, 6, 0.3, 20]

X_init = np.array([x_init_len])
X = np.zeros((time1,x_width))
X[:,2]= 0.14

Y_init = np.ones(y_len)*8

MPC = MPC(n, SP, x_len, x_width, y_len, X_init, Y_init)

model = ME.ModellEstimation(x_len, x_width, y_len, X_init, Y_init)
model2 = ME.ModellEstimation(x_len, x_width, y_len, X_init, Y_init)

timeuse = np.zeros(time1)
u1 = 0.4

#OneRun
#res = MPC.calculate()

# for i in range(len(res.x)):
#     X_init[0][3] = res.x[i]
#     model.NewSampleInX(X_init)
#     DS[i] = model.Estimate()
#     SetPoint[i] = MPC.SP

for i in range(time1):
    if i > 500:
         MPC.SP = 8.3
         #u1 = 0.45
    start_time = time.time()  # Get current time at the start of the loop

    SetPoint[i] = MPC.SP

    res = MPC.calculate()
    #print(res.fun)
    u[i] = MPC.U
    
    X[i][0] = X_init[0][0]+0.15*np.sin(2*np.pi*1/(11*2*60)*i)
    X[i][1] = X_init[0][1]+0.28*np.sin(2*np.pi*1/(3*2*60)*i)
    X[i][3] = u[i]
    X[i][4] = X_init[0][4]+4.5*np.sin(2*np.pi*1/(1*60*24)*i)
    DS1[i]=model.Estimate()
    #DS2[i]=model.EstimateOld()
    model.NewSampleInX(X[i])
    #model2.NewSampleInX(X[i])
    
    MPC.NewSampleInX(X[i])
    MPC.NewSampleInY(DS1[i])
    
    end_time = time.time()  # Get current time at the end of the loop
    loop_time = end_time - start_time  # Calculate the time taken for this iteration
    timeuse[i] = loop_time  # Store the time taken for this iteration
    
    if(i%10 == 0):
        print(i)

#%%

label = ['QT03', 'FT01', 'FT02', 'POL', 'SED18-QI01 x2']
color = ['brown','olive', 'pink', 'purple', 'navy']

# Plotting
plt.close()
plt.figure()
plt.subplot(3, 1, 1)
#plt.plot(t, DS1, label="% Dry solids")
plt.plot(t, DS1, label="Simulated % Dry solids")
plt.plot(t, SetPoint, label="Setpoint")
plt.xlabel('Time')
plt.ylabel('Dry solids [%DS]')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(t, u, label="POLF_FT09 (u) [l/s]", color=color[3])
plt.xlabel('Time')
plt.ylabel('Flow')
plt.legend()

plt.subplot(3, 1, 3)
for i in range(2):
    plt.plot(X[:,i], label=label[i])
plt.plot(X[:,4]/2, label=label[4], color=color[4])
plt.xlabel('Time')
plt.ylabel('Dry solids [%DS], flow [l/s] and Turbidity [FTU]')
plt.legend()

# plt.subplot(3, 3, 8)
# for i in range(2,4):
#     plt.plot(X[:,i], label=label[i], color= color[i])
# plt.legend()

# plt.subplot(3, 2, 6)
# plt.plot(X[:,4], label=label[4], color=color[4])
# plt.xlabel('Time')
# plt.ylabel('Turbidity')
# plt.legend()
# plt.show()

# Plotting the histogram
plt.figure()
plt.subplot(1, 2, 1)
plt.hist(timeuse, bins=10, color='blue', alpha=0.7)
plt.xlabel('Time Usage')
plt.ylabel('Frequency')
plt.title('Time Usage Histogram')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(t, timeuse, label="time")
plt.xlabel('Time')
plt.ylabel('Time Usage')
plt.legend()
plt.show()
plt.show()
