library(reticulate)
library(archetypes)
library(dplyr)

setwd(getwd())


TDV = read.csv('TDV_52.csv')

memory.limit(600000)
set.seed(42)

aa = stepArchetypes(data = TDV, k = 1:20, nrep = 3,  verbose = TRUE)

a16 = bestModel(aa[[16]]) #Modify to the desired number of representative archetypes (AT).

AA_coef = predict(a16, TDV)

write.csv(parameters(a16), 'parameter_52.csv', row.names=FALSE)
write.csv(AA_coef, 'AA_coef.csv', row.names = FALSE)


