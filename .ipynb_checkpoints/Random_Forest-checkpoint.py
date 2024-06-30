from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from scipy.stats import pearsonr
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

import pandas as pd
import numpy as np
import yaml

# Setup ==============================================================================

data = pd.read_csv('./2_more_coef.csv')
data = data[['AA_coef_1','AA_coef_2','AA_coef_3','AA_coef_4','AA_coef_5','AA_coef_6','AA_coef_7','AA_coef_8','AA_coef_9','AA_coef_10','AA_coef_11','AA_coef_12','AA_coef_13','AA_coef_14','AA_coef_15','AA_coef_16','AA_coef_17','AA_coef_18','AA_coef_19','AA_coef_20','MD']]
X = data[['AA_coef_1','AA_coef_2','AA_coef_3','AA_coef_4','AA_coef_5','AA_coef_6','AA_coef_7','AA_coef_8','AA_coef_9','AA_coef_10','AA_coef_11','AA_coef_12','AA_coef_13','AA_coef_14','AA_coef_15','AA_coef_16','AA_coef_17','AA_coef_18','AA_coef_19','AA_coef_20']]
Y = data[['MD']]

params = {
    'n_estimators' : [10,50, 100],
    'min_samples_split' : [8, 16, 20],
    'min_samples_leaf' : [8, 12],
    #'max_features' : [],
    'max_depth' : [6, 8],
    #'max_leaf_nodes' : [],
     
}

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=123)

grid_search = GridSearchCV(RandomForestRegressor(), params, cv =3, n_jobs=1, verbose = 0)

grid_search.fit(X_train, Y_train)

best_params = grid_search.best_params_
rf = RandomForestRegressor(**best_params, n_jobs=1, verbose = 0, random_state=4324)
rf.fit(X_train, Y_train)
y_pred = rf.predict(X_test)

# Mean Squared Error 
mse = mean_squared_error(Y_test.to_numpy().ravel(), y_pred)
print("Mean Squared Error:", mse)


# Pearson correlation coefficient
corr, _ = pearsonr(Y_test.to_numpy().ravel(), y_pred)
print("Pearson correlation coefficient:", corr)

mean_squared = pd.DataFrame()
pearson = pd.DataFrame()

for i in range(30) :

    boots_sample = data.sample(n=len(data), replace=False)
    X_boots = boots_sample[['AA_coef_1','AA_coef_2','AA_coef_3','AA_coef_4','AA_coef_5','AA_coef_6','AA_coef_7','AA_coef_8','AA_coef_9','AA_coef_10','AA_coef_11','AA_coef_12','AA_coef_13','AA_coef_14','AA_coef_15','AA_coef_16','AA_coef_17','AA_coef_18','AA_coef_19','AA_coef_20']]
    Y_boots = boots_sample[['MD']]
    X_train, X_test, Y_train, Y_test = train_test_split(X_boots, Y_boots, test_size=0.3, random_state=123)
    rf=RandomForestRegressor(**best_params, n_jobs=1, verbose = 0, random_state=4324)

    rf.fit(X_train, Y_train)
    y_pred = rf.predict(X_test)

    # R-squared 
    r2 = r2_score(Y_test, y_pred)
    print("R-squared:", r2)

    # Mean Squared Error 
    mse = mean_squared_error(Y_test, y_pred)
    mean_squared[i] = [mse]

    # Pearson correlation coefficient
    corr, _ = pearsonr(Y_test.to_numpy().ravel(), y_pred)
    pearson[i] = [corr]

mean_squared = mean_squared.T
pearson = pearson.T

print(f"MSE mean : {mean_squared.mean().to_string(index=False)}, MSE std : {mean_squared.std().to_string(index=False)} ")
print(f"{mean_squared.mean().to_string(index=False)}±{mean_squared.std().to_string(index=False)}")

print(f"pearsonr coefficient mean : {pearson.mean().to_string(index=False)}, pearsonr coefficient std : {pearson.std().to_string(index=False)} ")
print(f"{pearson.mean().to_string(index=False)}±{pearson.std().to_string(index=False)}")

mean_squared.to_csv('mean_squared_randomforest.csv', index=False)
pearson.to_csv('pearson_randomforest.csv', index=False)



