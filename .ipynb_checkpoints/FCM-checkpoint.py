import pandas as pd
import skfuzzy as fuzz

# Path_Setup ===============================================================================
TDV_DATA_PATH = "./TDV_54.csv" 
AA_PARAMETER_PATH = "./parameter_54.csv" 

# Load_Data =================================================================================
data=pd.read_csv(TDV_DATA_PATH)
cntr=pd.read_csv(AA_PARAMETER_PATH)


# model_build & calculate Fuzz coef =================================================================================
u, u0, d, jm, p, fpc = fuzz.cluster.cmeans_predict(
data.T, cntr, 2, error=0.005, maxiter=1000)

mat=pd.DataFrame(u)
    
coef=mat.T
coef.columns=['FUZZ1','FUZZ2','FUZZ3','FUZZ4','FUZZ5','FUZZ6','FUZZ7','FUZZ8','FUZZ9','FUZZ10','FUZZ11','FUZZ12','FUZZ13','FUZZ14','FUZZ15','FUZZ16']

# Save_coef =================================================================================    
coef.to_csv('FCM_coef.csv', sep = ',')