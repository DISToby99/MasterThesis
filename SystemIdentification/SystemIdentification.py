# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 07:59:29 2024

@author: toma
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sysidentpy.model_structure_selection import FROLS
from sysidentpy.basis_function._basis_function import Polynomial
from sysidentpy.metrics import root_relative_squared_error
from sysidentpy.utils.display_results import results
from sysidentpy.utils.plotting import plot_residues_correlation, plot_results
from sysidentpy.residues.residues_correlation import (
    compute_residues_autocorrelation,
    compute_cross_correlation,
)
import matplotlib.pyplot as plt
from sysidentpy.simulation import SimulateNARMAX
from sklearn.metrics import mean_squared_error
from sysidentpy.utils.save_load import save_model, load_model
#%%

data = pd.read_csv('Place where CSV is stored', delimiter=';')
data = data.drop(['Time'], axis=1) #, 'PHA18_SED18_QB01'  'TRS5_FT01', 'TRS5_FT02', 'FOR_QT03', 'PHA18_SED18_QB01', 'TRS5_FT02', 'FOR_QT03', 'TRS5_SI01'

# Assuming df is your original DataFrame
total_rows = len(data)
split_index = int(0.9 * total_rows)


# Select the first 90% for df_train
df_train = data.iloc[:split_index]
y_train = ((df_train.u).to_numpy()).reshape(-1, 1)
x_train = (df_train.drop(['u'], axis=1)).to_numpy()

# Select the remaining 10% 'for df_test
df_test = data.iloc[split_index:]
y_test = ((df_test.u).to_numpy()).reshape(-1, 1)
x_test = (df_test.drop(['u'], axis=1)).to_numpy()

#y_test = (y_test[:17999])
#x_test=x_test[:17999]

x_train[:,3]= x_train[:,3]*0.14
x_test[:,3]= x_test[:,3]*0.14
#x_train = x_train[:,3]*0.13*100
#x_test = x_test[:,3]*0.13*100

label = ['DS_in [%DS]', 'Q_in [l/s]', 'Q_w [l/s]', 'u [l/s]', 'f_T [FTU]', 'DS_out [%DS]']

plt.subplot(2,2,1)
plt.plot(y_train,
          label='Train data')
plt.legend()
plt.ylabel('Output [%DS]')
plt.subplot(2,2,2)
for i in range(4):
    plt.plot(x_train[:,i], label=label[i])
plt.legend()
plt.ylabel('Inputs')

plt.subplot(2,2,3)
plt.plot(y_test,
          label='Test data')
plt.legend()
plt.ylabel('Output [%DS]')
plt.xlabel('Time')
plt.subplot(2,2,4)
for i in range(4):
    plt.plot(x_test[:,i], label=label[i])

plt.legend()
plt.xlabel('Time')
plt.ylabel('Inputs')


plt.show()



#%%
#Build the model
basis_function = Polynomial(degree=3)

model = FROLS(
    order_selection=True,
    n_terms=5,
    extended_least_squares=False,
    ylag=1,
    xlag=[[1,2, 3, 4], [1,2], [1,2], [3, 4], [1,2,3], [1,2,3]],#
    info_criteria="aic",
    estimator="least_squares",
    basis_function=basis_function,
)
#%%
model.fit(X=x_train, y=y_train)

#%%

#y_test = (np.ones(10)*9).reshape(-1, 1)

yhat = model.predict(X=x_test, y=y_test[:4])
rrse = root_relative_squared_error(y_test, yhat)
print(rrse)

r = pd.DataFrame(
    results(
        model.final_model,
        model.theta,
        model.err,
        model.n_terms,
        err_precision=8,
        dtype="sci",
    ),
    columns=["Regressors", "Parameters", "ERR"],
)
print(r)
plot_results(y=y_test, yhat=yhat, n=len(yhat))
#yhat = (yhat[:3000]).flatten()

mse = mean_squared_error(yhat, y_test)  
print("The RMSE is:", mse)
ee = compute_residues_autocorrelation(y_test, yhat)
plot_residues_correlation(data=ee, title="Residues", ylabel="$e^2$")
x1e = compute_cross_correlation(y_test, yhat, x_test[:, 0])
plot_residues_correlation(data=x1e, title="Residues", ylabel="$x_1e$")


#%%
#Saving Model
save_model(model=model, file_name="C:/Users/toma/VEAS SELVKOST AS/Torbjørns Masteroppgave - General/Python debugging/SystemIdentification/CalculateTS_5in_1out_010224_2.syspy")
