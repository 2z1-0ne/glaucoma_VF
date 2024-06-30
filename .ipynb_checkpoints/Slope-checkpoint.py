import pandas as pd
import numpy as np
import argparse
import subprocess
import os
import seaborn as sns
import skfuzzy as fuzz
import warnings
from tqdm import tqdm
from statsmodels.formula.api import ols

# calculate_days ==============================================================================
def Make_interval(df):
    data = pd.DataFrame({'PID':df['PID'], 'Eye':df['Eye'], 'Exam Date':df['Exam Date']})
    data['Exam Date'] = pd.to_datetime(data['Exam Date'])
    data['interval'] = data['Exam Date'].diff()
   
    
    id = data.drop_duplicates(subset=['PID','Eye']).index
    data.loc[id, 'interval'] = '0'
    
    data['interval'] = data['interval'].apply(lambda x:str(x).split('d')[0])
    data['interval'] = data['interval'].astype('float')
    data['interval'] = data['interval'].astype('int')
    
    data['interval'] = data['interval']/365
    
    return data

# calculate slope ==============================================================================
def Make_slope(df, id, flag):
    result = pd.DataFrame()
    FCM = pd.DataFrame()
    PVAL = pd.DataFrame()
    
    df.set_index(['PID', 'Eye'], inplace = True)
    
    if((flag == 'MD') or (flag == 'VFI')):
        col_length = 1
        
    elif((flag == 'FUZZ') or (flag == 'AA')):
        col_length = 16
        
    #elif(flag == 'TDV'):
    #    col_length = 52
        
    for x in tqdm(range(col_length)):
        coef = []
        p_value = []
        Y_temp = df.iloc[:, 2 + x]
        for i in tqdm(range(len(id))):
            X_data = df.loc[id[i]]['interval'].cumsum().values
            Y_data = Y_temp.loc[id[i]].values
            
            Input_data = pd.DataFrame({'interval': X_data, 'Y':Y_data})
            Ols_md = ols('Y~interval', data = Input_data).fit()
            coef.append(Ols_md.params['interval'])
            p_value.append(Ols_md.pvalues['interval'])
        
        coef = pd.Series(coef)
        p_value = pd.Series(p_value).fillna(0)
        
        coef.index = id
        p_value.index = id
        
        colname_slope = flag + str(x+1) + '_slope'
        colname_pvalue = flag + str(x+1) + '_pvalue'
        
        tempFCM = pd.DataFrame({colname_slope:coef})
        tempPVAL = pd.DataFrame({colname_pvalue:p_value})

        FCM = pd.concat((FCM, tempFCM), axis = 1)
        PVAL = pd.concat((PVAL, tempPVAL), axis = 1)

    result = pd.concat((FCM, PVAL), axis = 1)
    return result 

# patients with more than 5 test  ==============================================================================
dataset = pd.read_csv('5_more_.csv')

FUZZ_coef = dataset.filter(regex = 'FCM_')
AA_coef = dataset.filter(regex = 'AA_')
MD = dataset.filter(regex = 'MD')
VFI = dataset.filter(regex = 'VFI')

Pid_Eye_data_interval = Make_interval(dataset)
id = Pid_Eye_data_interval.set_index(['PID', 'Eye']).index.drop_duplicates()

Pid_Eye_data_fuzz = pd.concat((Pid_Eye_data_interval, FUZZ_coef), axis = 1)
Pid_Eye_data_AA = pd.concat((Pid_Eye_data_interval, AA_coef), axis = 1)
Pid_Eye_data_MD = pd.concat((Pid_Eye_data_interval, MD), axis = 1)
Pid_Eye_data_VFI = pd.concat((Pid_Eye_data_interval, VFI), axis = 1)

# Check for potential errors ==============================================================================
check_1 = Pid_Eye_data_MD['interval'] < 0 
check_2 = Pid_Eye_data_fuzz['interval'] < 0 
check_3 = Pid_Eye_data_AA['interval'] < 0 
check_4 = Pid_Eye_data_VFI['interval'] < 0 

check_1.any(), check_2.any(), check_3.any() ,check_4.any()

# using slope function ==============================================================================
Slope_Pval_FUZZ = Make_slope(Pid_Eye_data_fuzz, id, 'FUZZ')
Slope_Pval_AA = Make_slope(Pid_Eye_data_AA, id, 'AA')
Slope_Pval_MD = Make_slope(Pid_Eye_data_MD, id, 'MD')
Slope_Pval_VFI = Make_slope(Pid_Eye_data_VFI, id, 'VFI')

# reset_index ==============================================================================
Slope_Pval_FUZZ.reset_index(inplace=True)
Slope_Pval_AA.reset_index(inplace=True)
Slope_Pval_MD.reset_index(inplace=True)
Slope_Pval_VFI.reset_index(inplace=True)

# save_slope ==============================================================================
test = pd.merge(dataset, Slope_Pval_AA, how = 'inner')
test.to_csv('AA_slope.csv',index=False)

test_2 = pd.merge(dataset, Slope_Pval_FUZZ)
test_2.to_csv('FCM_slope.csv',index=False)

test_3 = pd.merge(dataset, Slope_Pval_MD)
test_3.to_csv('MD_slope.csv',index=False)

test_4 = pd.merge(dataset, Slope_Pval_VFI)
test_4.to_csv('VFI_slope.csv',index=False)