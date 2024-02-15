# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 09:10:12 2024

@author: toma
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv('C:/Users/toma/VEAS SELVKOST AS/Torbjørns Masteroppgave - General/Interpolation/SprangresponsData.csv', delimiter=';')

start = 0
stopp = 16
t0 = np.arange(stopp-start+1)+start
TS0 = np.ones(len(t0))*9
TS0[0] = 9
forige = 0
for index, row in data.iterrows():
    if index < stopp+1 and index > 0:
        change = row['FOR_QT03'] / forige['FOR_QT03'] -0.01
        TS0[index]= TS0[index]*(change)
        #print(change-0.01)
    forige = row
        
    

start = 17
stopp = 38
t1 = np.arange(stopp-start+1)+start

start = 39
stopp = 45
t2 = np.arange(stopp-start+1)+start

TS1 = 0.0042*t1**2 - 0.3736*t1 + 12.598
TS2 = -0.1319*t2**2 + 11.652*t2 - 248.28


start = 46
stopp = 299
t3 = np.arange(stopp - start + 1) + start
TS3 = np.zeros(len(t3))+9.02
#TS3[0] = 9
previous_samples = [None] * 3  # Store the previous three samples


for index, row in data.iterrows():
    if index > start:
        if all(sample is not None for sample in previous_samples):  # Check if all elements are not None
            change1 = (row['TRS5_FT01']) / (previous_samples[0]['TRS5_FT01'])
            change4 = (row['TRS5_FT02']) / (previous_samples[0]['TRS5_FT02'])
            change1 = change1-change4
            change2 = row['FOR_QT03'] / previous_samples[0]['FOR_QT03']
            change2 = change2 - 1
            change3 = row['PHA18_SED18_QB01'] / previous_samples[0]['PHA18_SED18_QB01']
            
            if change3>1:
                change3 = (1-change3)
            else:
                change3 = abs(1-change3)
            TS3[index - start] = TS3[index - start] * change
            change = (change1/5+1*change3/8+change2/9)+1
            print(change)
        else:
            TS3[index - start] = TS3[index - start]  # Set to the previous value if not enough previous samples

    # Update the previous samples
    previous_samples.pop(0)  # Remove the oldest previous sample
    previous_samples.append(row)  # Add the current row as the newest previous sample

# Now TS3 contains the calculated TS values using the previous three samples with a 3-sample time delay

TS = np.concatenate((TS0, TS1, TS2, TS3))
t = np.concatenate((t0, t1, t2, t3))

DB1 = (data.TRS5_FT01/data.TRS5_FT01+1)*data.FOR_QT03+1
df2 = pd.DataFrame(DB1, columns=['QB02'])

df = pd.DataFrame(TS, columns=['QB01'])

data = pd.concat([data, df], axis=1)
data = data.drop(['TRS5_RV01'], axis=1)

data.plot(x="Time",
             subplots=True)
plt.legend()
\

#%%
#Legg til data fra 03.01.24 til laging av modell
ds = pd.read_csv('C:/Users/toma/VEAS SELVKOST AS/Torbjørns Masteroppgave - General/Interpolation/LavTsInn_HøyUt.csv', delimiter=';')


start = 1
stopp = 370
t = np.arange(stopp - start + 1) + start
TS = 0.0005*t+9.1695
previous_samples = [None] * 3  # Store the previous three samples
change = 1

for index, row in ds.iterrows():
    if index > start:
        if all(sample is not None for sample in previous_samples):  # Check if all elements are not None
            change1 = (row['TRS5_FT01']) / (previous_samples[0]['TRS5_FT01'])
            change4 = (row['TRS5_FT02']) / (previous_samples[0]['TRS5_FT02'])
            change1 = change1-change4
            change2 = row['FOR_QT03'] / previous_samples[0]['FOR_QT03']
            change2 = change2 - 1
            
            TS[index - start] = min(TS[index - start] * change,9.5)
            change = (change1/8+change2/9)+1
            #print(change)
        else:
            TS[index - start] = TS[index - start - 1]  # Set to the previous value if not enough previous samples

    # Update the previous samples
    previous_samples.pop(0)  # Remove the oldest previous sample
    previous_samples.append(row)  # Add the current row as the newest previous sample

df = pd.DataFrame(TS, columns=['QB01'])

ds1 = pd.concat([ds, df], axis=1)


# Perform the merge
# merged = pd.concat([ds, data], axis=0)

# merged.plot(x="Time", 
#           subplots=True)
# plt.legend()

#%%
#Legg til data fra 03.01.24 til laging av modell
ds = pd.read_csv('C:/Users/toma/VEAS SELVKOST AS/Torbjørns Masteroppgave - General/Interpolation/LavTsUt.csv', delimiter=';')


start = 1
stopp = 653
t = np.arange(stopp - start + 1) + start
TS = 0.0003*t+7.0597
previous_samples = [None] * 3  # Store the previous three samples
change = 1

for index, row in ds.iterrows():
    if index > start:
        if all(sample is not None for sample in previous_samples):  # Check if all elements are not None
            change1 = (row['TRS5_FT01']) / (previous_samples[0]['TRS5_FT01'])
            change4 = (row['TRS5_FT02']) / (previous_samples[0]['TRS5_FT02'])
            change1 = change1-change4
            change2 = row['FOR_QT03'] / previous_samples[0]['FOR_QT03']
            change2 = change2 - 1
            
            TS[index - start] = min(TS[index - start] * change,9.5)
            change = (change1/20+change2/15)+1
            #print(change)
        else:
            TS[index - start] = TS[index - start - 1]  # Set to the previous value if not enough previous samples

    # Update the previous samples
    previous_samples.pop(0)  # Remove the oldest previous sample
    previous_samples.append(row)  # Add the current row as the newest previous sample
    

for i in range(31):
    TS[i]= 9.33*t[i]**-0.082
    TS[652-30+i]=0.4587*np.log(t[i])+7.33
    


df = pd.DataFrame(TS, columns=['QB01'])

ds2 = pd.concat([ds, df], axis=1)

# ds2.plot(x='Time',
#         subplots=True)


# Perform the merge
merged = pd.concat([ds1, ds2, data], axis=0)

merged = merged.drop(['TRS5_RV01'], axis=1)

merged.plot(x="Time", 
          subplots=True)
plt.legend()



#%%
#Save data

merged.to_csv('C:/Users/toma/VEAS SELVKOST AS/Torbjørns Masteroppgave - General/Interpolation/SprangresponsData_mTS.csv', index=False, sep=';')  # Set index=False if you don't want to save row indices