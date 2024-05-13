# Import necessary libraries
import pandas as pd
from sklearn.decomposition import PCA
from sklearn import preprocessing as pre
import matplotlib.pyplot as plt
import numpy as np

# Load the data from CSV file
X = pd.read_csv('The CSV file to run PCA on', delimiter=';')


# Set the index to the first column
X.set_index(X.columns[0], inplace=True)

# Display the first few rows and the shape of the data
print(X.head())
print(X.shape)

# Calculate the mean, min, and max values for each column
column_names = list(X.columns.values)
mean = X.mean()
mini = X.min()
maxi = X.max()

# Scale the data to have zero mean and unit variance
for index1, row in X.iterrows():
    for name, value in row.items():
        X.at[index1, name] = (value-mean[name])/(maxi[name]-mini[name])

# Transpose the data for PCA
scaled_data = X.T

# Initialize PCA with the desired number of components
pca = PCA()
pca.fit(scaled_data)
pca_data = pca.transform(scaled_data)

# Plot the explained variance ratio for each principal component
per_var = np.round(pca.explained_variance_ratio_*100, decimals=4)
labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]

plt.bar(x=range(1, len(per_var)+1), height=per_var, tick_label=labels)
plt.ylabel('Percentage of Explained Variance [%]')
plt.xlabel('Principal Component')
plt.title('Screen Plot')
plt.show()

# Convert the PCA data to a DataFrame
pca_df = pd.DataFrame(pca_data, index=column_names, columns=labels)

# Perform PCA with a specific number of components
pca = PCA(n_components=5)
principal_components = pca.fit_transform(X)

# Convert the PCA results to a DataFrame for visualization
principal_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2', 'PC3', 'PC4', 'PC5'], index=X.index)

# Plot the score and loading plots
plt.close()
plt.figure(figsize=(15, 5))

plt.subplot(1, 2, 1)
plt.scatter(pca_df.PC1, pca_df.PC2)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('Loadings')

for sample in pca_df.index:
    plt.annotate(sample, (pca_df.PC1.loc[sample], pca_df.PC2.loc[sample]))

plt.subplot(1, 2, 2)
plt.scatter(principal_df['PC1'], principal_df['PC2'])
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('Score Plot')

for sample in principal_df.index:
    plt.annotate(sample, (principal_df.PC1.loc[sample], principal_df.PC2.loc[sample]))

plt.show()

plt.figure(figsize=(15, 5))

plt.subplot(1, 2, 1)
plt.scatter(pca_df.PC1, pca_df.PC3)
plt.xlabel('PC1')
plt.ylabel('PC3')
plt.title('Loadings')

for sample in pca_df.index:
    plt.annotate(sample, (pca_df.PC1.loc[sample], pca_df.PC3.loc[sample]))

plt.subplot(1, 2, 2)
plt.scatter(principal_df['PC1'], principal_df['PC3'])
plt.xlabel('PC1')
plt.ylabel('PC3')
plt.title('Score Plot')

for sample in principal_df.index:
    plt.annotate(sample, (principal_df.PC1.loc[sample], principal_df.PC3.loc[sample]))

plt.show()

plt.figure(figsize=(15, 5))

plt.subplot(1, 2, 1)
plt.scatter(pca_df.PC1, pca_df.PC4)
plt.xlabel('PC1')
plt.ylabel('PC4')
plt.title('Loadings')

for sample in pca_df.index:
    plt.annotate(sample, (pca_df.PC1.loc[sample], pca_df.PC4.loc[sample]))

plt.subplot(1, 2, 2)
plt.scatter(principal_df['PC2'], principal_df['PC4'])
plt.xlabel('PC2')
plt.ylabel('PC4')
plt.title('Score Plot')

for sample in principal_df.index:
    plt.annotate(sample, (principal_df.PC2.loc[sample], principal_df.PC4.loc[sample]))

plt.show()

# Print the explained variance ratio
print(pca.explained_variance_ratio_)
