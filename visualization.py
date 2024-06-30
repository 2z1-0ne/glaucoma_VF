import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import skfuzzy as fuzz
import warnings
import yaml

warnings.filterwarnings(action='ignore')

# Setup ==============================================================================
with open('config.yaml') as f:
    config = yaml.safe_load(f)
    
DATA_PATH = config['TDV54_path']
COEF_PATH = config['FCM_coef']
PARAM_PATH = config['param54_path']

data = pd.read_csv(DATA_PATH) 
coef = pd.read_csv(COEF_PATH)
cntr = pd.read_csv(PARAM_PATH)
params=cntr

# ==============================================================================
mask=np.zeros((8,9))

mask[0,3] = 1
mask[0,4] = 1
mask[0,5] = 1
mask[0,6] = 1


mask[1,2] = 1
mask[1,3] = 1
mask[1,4] = 1
mask[1,5] = 1
mask[1,6] = 1
mask[1,7] = 1

mask[2,1]= 1
mask[2,2]= 1
mask[2,3]= 1
mask[2,4]= 1
mask[2,5]= 1
mask[2,6]= 1
mask[2,7]= 1
mask[2,8]= 1


mask[3,0]= 1
mask[3,1]= 1
mask[3,2]= 1
mask[3,3]= 1
mask[3,4]= 1
mask[3,5]= 1
mask[3,6]= 1

mask[3,8]= 1


mask[4,0]= 1
mask[4,1]= 1
mask[4,2]= 1
mask[4,3]= 1
mask[4,4]= 1
mask[4,5]= 1
mask[4,6]= 1

mask[4,8]= 1


mask[5,1]= 1
mask[5,2]= 1
mask[5,3]= 1
mask[5,4]= 1
mask[5,5]= 1
mask[5,6]= 1
mask[5,7]= 1
mask[5,8]= 1



mask[6,2]= 1
mask[6,3]= 1
mask[6,4]= 1
mask[6,5]= 1
mask[6,6]= 1
mask[6,7]= 1



mask[7,3]= 1
mask[7,4]= 1
mask[7,5]= 1
mask[7,6]= 1


def my(a):
    for i in range(len(a)):
        if a[i]==0:
            a[i]=1
        else:
            a[i]=0
    return a

# ==============================================================================
mask=np.apply_along_axis(my,1,mask)

def get_eye(values):
    
    arr=np.zeros((8,9))


   
    arr[0,3] =  values[0]
    arr[0,4] =  values[1]
    arr[0,5] =  values[2]
    arr[0,6] =  values[3]


    arr[1,2] =  values[4]
    arr[1,3] =  values[5]
    arr[1,4] =  values[6]
    arr[1,5] =  values[7]
    arr[1,6] =  values[8]
    arr[1,7] =  values[9]

    arr[2,1] =  values[10]
    arr[2,2] =  values[11]
    arr[2,3] =  values[12]
    arr[2,4] =  values[13]
    arr[2,5] =  values[14]
    arr[2,6] =  values[15]
    arr[2,7] =  values[16]
    arr[2,8] =  values[17]


    arr[3,0] =  values[18]
    arr[3,1] =  values[19]
    arr[3,2] =  values[20]
    arr[3,3] =  values[21]
    arr[3,4] =  values[22]
    arr[3,5] =  values[23]
    arr[3,6] =  values[24]

    arr[3,8] =  values[26]


    arr[4,0] =  values[27]
    arr[4,1] =  values[28]
    arr[4,2] =  values[29]
    arr[4,3] =  values[30]
    arr[4,4] =  values[31]
    arr[4,5] =  values[32]
    arr[4,6] =  values[33]

    arr[4,8] =  values[35]


    arr[5,1] =  values[36]
    arr[5,2] =  values[37]
    arr[5,3] =  values[38]
    arr[5,4] =  values[39]
    arr[5,5] =  values[40]
    arr[5,6] =  values[41]
    arr[5,7] =  values[42]
    arr[5,8] =  values[43]



    arr[6,2] =  values[44]
    arr[6,3] =  values[45]
    arr[6,4] =  values[46]
    arr[6,5] =  values[47]
    arr[6,6] =  values[48]
    arr[6,7] =  values[49]



    arr[7,3] =  values[50]
    arr[7,4] =  values[51]
    arr[7,5] =  values[52]
    arr[7,6] =  values[53]

    return arr
    
# ==============================================================================
def decomposition(coef_df,data,k):
    coef2=coef_df.loc[k]
    data2=data.loc[k]
    coef2=coef2.reset_index(drop=True)
    data2=data2.reset_index(drop=True)

    fig = plt.figure(figsize=(24,9))
    print(coef2)

    for n in range(1,17):
        plt.subplot(3,8,1)
        sns.heatmap(get_eye(data2),mask=mask,vmin=-30, vmax=30, cmap='RdBu',square=True,cbar=False)
        plt.title('Original VF')
        plt.xticks([])
        plt.yticks([])
        plt.subplot(3, 8, n+8)
        sns.heatmap(get_eye(params.iloc[coef2.sort_values(ascending=False)[:16].index[n-1]]), mask=mask, vmin=-30, vmax=30, cmap='RdBu',square=True,cbar=False)
        plt.title('Archetype'+str(coef2.sort_values(ascending=False)[:16].index[n-1]+1)+'('+str(np.round(coef2.sort_values(ascending=False)[:16].values[n-1]*100,1))+'%)')
        plt.xticks([])
        plt.yticks([])   
    tasknumber = "test" + str(k) + ".png"
    fig.savefig(tasknumber)

# ==============================================================================
for i in range(1, 2634, 1):
    decomposition(coef,data,i) 