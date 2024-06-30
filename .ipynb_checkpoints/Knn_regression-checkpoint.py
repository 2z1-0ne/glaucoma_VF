from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yaml

# Setup ==============================================================================
with open('config.yaml') as f:
    config = yaml.safe_load(f)

COEF_PATH = config['coeff_path']
col = config['columns']
params = config['params']

data = pd.read_csv(COEF_PATH)
X = data[col['x_col']]
Y = data[col['y_col']]
param_grid = params['knn']

# Define parameter grid for GridSearchCV  =================================================================================
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=123)

grid_search = GridSearchCV(KNeighborsRegressor(), param_grid, cv =3, n_jobs=1, verbose = 1)
grid_search.fit(X_train, Y_train)
best_params = grid_search.best_params_
print(best_params)

# Bootstrap resampling and evaluation =================================================================================
mean_squared = []
pearson = []

for i in range(30) :
    boots_sample = data.sample(n=len(data), replace=True)
    X_boots = boots_sample[col['x_col']]
    Y_boots = boots_sample[col['y_col']]

    X_train, X_test, Y_train, Y_test = train_test_split(X_boots, Y_boots, test_size=0.3)
    reg =  KNeighborsRegressor(**best_params)
    
    reg.fit(X_train, Y_train)
    y_pred = reg.predict(X_test)

    # Mean Squared Error
    mse = mean_squared_error(Y_test, y_pred)
    mean_squared.append(mse)
   
    # Pearson correlation coefficient
    corr, _ = pearsonr(Y_test.to_numpy().ravel(), y_pred)
    pearson.append(corr)

mean_squared = mean_squared.T
pearson = pearson.T

# Print mean and standard deviation of Mean Squared Error =================================================================================
print(f"MSE mean : {mean_squared.mean().to_string(index=False)}, MSE std : {mean_squared.std().to_string(index=False)} ")
#print(f"{mean_squared.mean().to_string(index=False)}±{mean_squared.std().to_string(index=False)}")

# Print mean and standard deviation of Pearson correlation coefficient =================================================================================
print(f"pearsonr coefficient mean : {pearson.mean().to_string(index=False)}, pearsonr coefficient std : {pearson.std().to_string(index=False)} ")
#print(f"{pearson.mean().to_string(index=False)}±{pearson.std().to_string(index=False)}")

# Save results to CSV files =================================================================================
mean_squared.to_csv('mean_squared_knn.csv', index=False)
pearson.to_csv('pearson_knn.csv', index=False)
