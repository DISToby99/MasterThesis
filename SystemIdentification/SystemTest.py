# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 15:27:54 2024

@author: toma
"""

import numpy as np
from sysidentpy.model_structure_selection import FROLS
from sysidentpy.utils.save_load import save_model, load_model
import pandas as pd
import time
import matplotlib.pyplot as plt

model=load_model(file_name="C:/Users/toma/VEAS SELVKOST AS/Torbjørns Masteroppgave - General/Python debugging/SystemIdentification/CalculateTS_5in_1out_010224_2.syspy")

data = pd.read_csv('C:/Users/toma/VEAS SELVKOST AS/Torbjørns Masteroppgave - General/Python debugging/PCA/InterpolationAllData.csv', delimiter=';')
#data = pd.read_csv('C:/Users/toma/VEAS SELVKOST AS/Torbjørns Masteroppgave - General/Interpolation/SprangresponsData_mTS.csv', delimiter=';')

data = data.drop(['Time'], axis=1)
Allx = (data.drop(['QB01'], axis=1)).to_numpy()
Ally = ((data.QB01).to_numpy()).reshape(-1, 1)
Allx[:,3]=Allx[:,3]*0.14

class ModellEstimation:
    def __init__(self, Xlen, Xwidth, Ylen, X_init, Y_init):
        self.x = X_init #(np.ones([Xlen, Xwidth])*X_init)
        self.y = Y_init #(np.ones(Ylen)*Y_init) #Y_init #
        self.lenX = Xlen
        self.lenY = Ylen
        
    def NewSampleInX(self, newX):
        for i in range(self.lenX - 1):
            self.x[i] = self.x[i + 1].copy()

        self.x[self.lenX-1] = newX  # Update the first row with the new value
        x = self.x
        #print(x)
        #return x
        
    def NewSampleInY(self, newY):
        for i in range(self.lenY - 1):
            self.y[i] = self.y[i + 1].copy()

        self.y[self.lenY-1] = newY  # Update the first row with the new value
        y = self.y
        #self.y = newY
        #print(newY)
        #print(self.y)
        
    def Estimate(self):
        y = self.y
        x1 = self.x[:,0]
        x2 = self.x[:,1]
        x3 = self.x[:,2]
        x4 = self.x[:,3]
        # x5 = self.x[:,4]
        # x6 = self.x[:,5]
        # x7 = self.x[:,6]
        # x8 = self.x[:,7]
        # x9 = self.x[:,8]
        # x10 = self.x[:,9]
        # x11 = self.x[:,10]
        k=4
        y_hat = 1.1222*y[k-1] + 8.3490*x4[k-1]*x1[k-1] + -3.3717 *x4[k-2]*x1[k-1] + \
                -7.7931E-02*x3[k-2]*x1[k-2] + 2.5890E-02*x3[k-2]**2 + \
                -2.4945E-02*x2[k-2]*y[k-1]
        
        # y_hat=max(y_hat,5)
        # y_hat=min(y_hat,11)
        self.NewSampleInY(y_hat)
        return y_hat
    
    def TryModel(self, model):
        y = (self.y).reshape(-1, 1)
        x = self.x
        y_hat = model.predict(X = x, y = y)
        #print(y_hat)
        self.NewSampleInY(min(max(y_hat[[4]],x[0,3]),12))
        #print(y_hat[[4]])
        return max(y_hat[[4]],x[0,3])
        
        

x_len = 5
x_width = 4
y_len = 4

#The initial values of x: FOR_QT03, TRS5_FT01, TRS5_FT02, POLF_FT09 (U), PHA18-SED18-QB01
x = Allx[:x_len] #np.array([4,6.6,6,0.48*0.13*100])

y = np.array([9, 9, 9, 9.1])
all_y = np.zeros(len(Allx))

#yhat = model.predict(X=Allx, y=Ally[:4])  


Model = ModellEstimation(x_len, x_width, y_len, x, y)
i = 3
# yhat = Model.TryModel(model)
#print(yhat)
for j in range(len(all_y)-3):
    x = Allx[i]
    Model.NewSampleInX(x)
    y = Model.TryModel(model)
    #y = Model.Estimate()
    #print(x)
    
    #print("Next Estimate is:", y, "and X is:", x)
    all_y[j] = y
    i=i+1
    #time.sleep(1)
    
#x = Model.NewSampleInX([1,1,1,1,1])

#%%       

# plt.plot(Ally, label="True value")
# plt.plot(all_y, label="Predicted")
# plt.legend()
# plt.show()

#data = pd.read_csv('C:/Users/toma/VEAS SELVKOST AS/Torbjørns Masteroppgave - General/Interpolation/SprangresponsData_mTS.csv', delimiter=';')
data = pd.read_csv('C:/Users/toma/VEAS SELVKOST AS/Torbjørns Masteroppgave - General/Python debugging/PCA/InterpolationAllData.csv', delimiter=';')

df = pd.DataFrame(all_y, columns=['QB01_hat'])

data = pd.concat([data, df], axis=1)

data.plot(x="Time", 
          #y=['QB01','QB01_hat'],
          subplots=True)
plt.legend()



#%%
#Testing if lab results is correct for the model

# Assuming 'df_points' is your DataFrame with points and 'df_trend' is your DataFrame with the trend
#df = pd.read_csv('C:/Users/toma/VEAS SELVKOST AS/Torbjørns Masteroppgave - General/Interpolation/SprangresponsData_mTS.csv', delimiter=';')
df = pd.read_csv('C:/Users/toma/VEAS SELVKOST AS/Torbjørns Masteroppgave - General/Prøvetaking/Labresultater.csv', delimiter=';')
df['Time'] = pd.to_datetime(df['Time'], format='%d.%m.%Y %H:%M')


data['Time'] = pd.to_datetime(data['Time'], format='%d.%m.%Y %H:%M')
# Plot trend line from another DataFrame
plt.plot(data['Time'], data['QB01_hat'], color='red', label='Estimated')

# Plot scatter plot of points
plt.scatter(df['Time'], df['QB01'], label='Sample analyesed at Labratory')

# Add labels and legend
plt.xlabel('Time')
plt.ylabel('%DS')
plt.legend()

# Show plot
plt.show()
        