# glaucoma_VF                                  
This study is based on a hybrid artificial intelligence technique that combines archetypal analysis (AA) and fuzzy c-means (FCM) clustering. The objective is to minimize the projection loss that occurs when visual field tests are analyzed solely using archetypal analysis. By doing so, the method aims to analyze and classify visual field tests without any loss of information.

## Data
* TDV values of patients with glaucoma or suspected glaucoma. (We used data from 132,938 patients.)
  When conducting the analysis, two sets are required:
  - one with 52 columns and another with 54 columns.
  - The set with 52 columns involves removing blind spot areas from the 54-column TDV dataset.
 
## Prerequisites
* python 3.6
* R studio 4.1.1

## Archetype Analysis
1. download the Archetype.R file from GitHub
2. Modify the code with the desired analysis file name.
   - Reference: The file for analysis should be formatted as follows: N X 52
     
                    TDV1 TDV2 ... TDV54
         patient1
         patient2
            ...
         patient N

