# glaucoma_VF                                  
This study is based on a hybrid artificial intelligence technique that combines archetypal analysis (AA) and fuzzy c-means (FCM) clustering. The objective is to minimize the projection loss that occurs when visual field tests are analyzed solely using archetypal analysis. By doing so, the method aims to analyze and classify visual field tests without any loss of information.

## Data
* TDV values of patients with glaucoma or suspected glaucoma. (We used data from 132,938 patients.)
  When conducting the analysis, two sets are required:
  - one with 52 columns *(1)* and another with 54 columns *(2)*. 
  - The set with 52 columns involves removing blind spot areas from the 54-column TDV dataset. 
 
## Prerequisites
* python 3.6
* R studio 4.1.1

## Archetype Analysis
1. download the 'Archetype.R' file from GitHub.
2. Modify the code with the desired analysis file name.
   - Reference: The file for analysis should be formatted as follows: N X 52 ---- *(1)*
     The blind spot TDV needs to be removed. 
                    TDV1 TDV2 ... TDV54
         patient1
         patient2
            ...
         patient N
3. You will obtain parameter file and AA coefficient file.

## Fuzzy C-means
1. download the 'FCM.py' file from GitHub.
2. Add blind spots to columns 26 and 35 of the TDV file used in Archetype.R. 
   Fill these columns with a value of 0.
   - Reference: The file for analysis should be formatted as follows: N X 54 ----- *(2)
     The blind spot TDV needs to be removed.
                    TDV1 TDV2 ... TDV54
         patient1
         patient2
            ...
         patient N
3. Modify the path of 'TDV54_path' in the 'config.yaml' file.
