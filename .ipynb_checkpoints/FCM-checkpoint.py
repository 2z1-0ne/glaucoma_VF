import pandas as pd
import skfuzzy as fuzz
import warnings
import yaml

warnings.filterwarnings(action='ignore')

# Path_Setup ===============================================================================
with open('config.yaml') as f:
    config = yaml.safe_load(f)
    
DATA_PATH = config['TDV54_path']
PARAM_PATH = config['param54_path']

# Load_Data =================================================================================
data=pd.read_csv(DATA_PATH)
cntr=pd.read_csv(PARAM_PATH)


# model_build & calculate Fuzz coef =================================================================================
u, u0, d, jm, p, fpc = fuzz.cluster.cmeans_predict(
data.T, cntr, 2, error=0.005, maxiter=1000)

mat=pd.DataFrame(u)
    
coef=mat.T
coef.columns=['FUZZ1','FUZZ2','FUZZ3','FUZZ4','FUZZ5','FUZZ6','FUZZ7','FUZZ8','FUZZ9','FUZZ10','FUZZ11','FUZZ12','FUZZ13','FUZZ14','FUZZ15','FUZZ16'] #You can add Fuzz17... or remove Fuzz16..., as needed.

# Save_coef =================================================================================    
coef.to_csv('FCM_coef.csv', sep = ',')