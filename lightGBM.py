from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from scipy.stats import pearsonr
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

import warnings
import pandas as pd
import numpy as np
import lightgbm as lgb
import yaml

warnings.filterwarnings("ignore")
# Setup ==============================================================================
with open('config.yaml') as f:
    config = yaml.safe_load(f)

COEF_PATH = config['coeff_path']
col = config['columns']
params = config['lgbm']

data = pd.read_csv(COEF_PATH)
X = data[col['x_col']]
Y = data[col['y_col']]
param_grid = params['knn']

# Define parameter grid for GridSearchCV  =================================================================================
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=123)

grid_search = GridSearchCV(lgb.LGBMRegressor(), params, cv =3, n_jobs=1, scoring='neg_mean_squared_error')
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
    
    X_train, X_test, Y_train, Y_test = train_test_split(X_boots, Y_boots, test_size=0.3, random_state=123)
    lgbm = lgb.LGBMRegressor(learning_rate= 0.01,**best_params, seed = 4324)


    lgbm.fit(X_train, Y_train)
    y_pred = lgbm.predict(X_test)
    
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

print(f"pearsonr coefficient mean : {pearson.mean().to_string(index=False)}, pearsonr coefficient std : {pearson.std().to_string(index=False)} ")
#print(f"{pearson.mean().to_string(index=False)}±{pearson.std().to_string(index=False)}")

# Save results to CSV files =================================================================================
mean_squared.to_csv('mean_squared_randomforest.csv', index=False)
pearson.to_csv('pearson_randomforest.csv', index=False)

# Plot the results for visualization ==============================================================================
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.hist(mean_squared['MSE'], bins=10, edgecolor='k')
plt.title('Mean Squared Error Distribution')
plt.xlabel('MSE')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
plt.hist(pearson['Pearson'], bins=10, edgecolor='k')
plt.title('Pearson Correlation Coefficient Distribution')
plt.xlabel('Pearson r')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()