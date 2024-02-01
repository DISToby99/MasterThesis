# Import necessary libraries
import pandas as pd
from sklearn.decomposition import PCA
from sklearn import preprocessing as pre
import matplotlib.pyplot as plt
import numpy as np

# Load the data from CSV file
X = pd.read_csv('C:/Users/toma/VEAS SELVKOST AS/Torbjørns Masteroppgave - General/Prøvetaking/Labresultater.csv', delimiter=';')
#X = pd.read_csv('C:/Users/toma/VEAS SELVKOST AS/Torbjørns Masteroppgave - General/Python debugging/PCA/Interpolation.csv', delimiter=';')


X.set_index(X.columns[0], inplace=True)




print(X.head())
print(X.shape)

column_names = list(X.columns.values)
index = list(X.index.values)

mean = X.mean()
mini = X.min()
maxi = X.max()

for index1, row in X.iterrows():
    for name, value in row.items():
        X.at[index1, name] = (value-mean[name])/(maxi[name]-mini[name])

        
scaled_data = X.T
#scaled_data = pre.scale(X.T)


#%%


# Initialize PCA with the desired number of components
pca = PCA()
pca.fit(scaled_data)
pca_data = pca.transform(scaled_data)

#plotting
per_var = np.round(pca.explained_variance_ratio_*100, decimals=4)
labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]

plt.bar(x=range(1, len(per_var)+1), height=per_var, tick_label = labels)
plt.ylabel('Precentage of Explained Variance')
plt.xlabel('Prinicpal Component')
plt.title('Screen Plot')
plt.show()

#%%
pca_df = pd.DataFrame(pca_data, index=column_names, columns=labels)

# Initialize PCA with the desired number of components
pca = PCA(n_components=5)  # You can change the number of components as needed

# Perform PCA
principal_components = pca.fit_transform(X)

# Convert to DataFrame for visualization or further analysis
principal_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2', 'PC3', 'PC4', 'PC5'], index=index)

plt.close()
plt.figure()
plt.subplot(1,2,1)
plt.scatter(pca_df.PC1, pca_df.PC2)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('Loadings')

for sample in pca_df.index:
    plt.annotate(sample, (pca_df.PC1.loc[sample], pca_df.PC2.loc[sample]))

plt.subplot(1,2,2)
# If you just want to see the transformed data:
plt.scatter(principal_df['PC1'], principal_df['PC2'])
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('Score plot')
for sample in principal_df.index:
    plt.annotate(sample, (principal_df.PC1.loc[sample], principal_df.PC2.loc[sample]))
plt.show()

plt.figure()  
plt.subplot(1,2,1)
plt.scatter(pca_df.PC1, pca_df.PC3)
plt.xlabel('PC1')
plt.ylabel('PC3')
plt.title('Loadings')

for sample in pca_df.index:
    plt.annotate(sample, (pca_df.PC1.loc[sample], pca_df.PC3.loc[sample]))

plt.subplot(1,2,2)
# If you just want to see the transformed data:
plt.scatter(principal_df['PC1'], principal_df['PC3'])
plt.xlabel('PC1')
plt.ylabel('PC3')
plt.title('Score plot')
for sample in principal_df.index:
    plt.annotate(sample, (principal_df.PC1.loc[sample], principal_df.PC3.loc[sample]))


plt.figure()
plt.subplot(1,2,1)
plt.scatter(pca_df.PC1, pca_df.PC4)
plt.xlabel('PC1')
plt.ylabel('PC4')
plt.title('Loadings')

for sample in pca_df.index:
    plt.annotate(sample, (pca_df.PC1.loc[sample], pca_df.PC4.loc[sample]))

plt.subplot(1,2,2)
# If you just want to see the transformed data:
plt.scatter(principal_df['PC1'], principal_df['PC4'])
plt.xlabel('PC1')
plt.ylabel('PC4')
plt.title('Score plot')
for sample in principal_df.index:
    plt.annotate(sample, (principal_df.PC1.loc[sample], principal_df.PC4.loc[sample]))
    
plt.show()
# You can also inspect the explained variance ratio
print(pca.explained_variance_ratio_)

