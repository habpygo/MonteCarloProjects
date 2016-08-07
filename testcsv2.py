_author_ = 'Harry Boer'
_project_ = 'Monte Carlo Simulation'

from pandas import DataFrame, read_csv
import pandas as pd
import numpy as np
import re
import stringevaluator as streval


# De 'Width' van de output console, zodat DataFrames and Numpy arrays niet worden afgebroken
desired_width = 320
pd.set_option('display.width', desired_width)

mcframe = pd.read_excel('montecarlo-template2.xlsx',skiprows=[0,1,2,3])


rows, colls = mcframe.shape

mcnparray = np.asarray(mcframe)

# Index and Columns are integers
column_index = np.arange(colls)
mcframe.columns = [column_index]

mcframe = mcframe.fillna(0)

def no_of_years():
    row1, col2 = np.where(mcnparray == "N")
    return int(np.asscalar(mcnparray[row1, col2 + 1])),row1

Aantal_Jaren, rij = no_of_years()

print("De waarde is", Aantal_Jaren, "en de waarde in row is", rij)


def growth_rate():
    """
    :rtype: object
    """
    row1, col2 = np.where(mcnparray == "Growth Rate")
    return float(np.asscalar(mcnparray[row1, col2 + 1]))

Growth = growth_rate()

operands = r'[-+*/^]'
regex = re.compile(operands)
distributions = "norm" #, 'logn', 'trian', 'uni'] MAAK VIER APPARTE STRINGS EN TEST EEN VOOR EEN.
regdist = re.compile("norm")


def find_MonteCarlo_Distributions():
    for i in range(rows - 1):
        distributie = mcframe.loc[i][1]
        distributie = str(distributie)
        if regdist.findall(distributie):
            print("Something is happening at row", i)


def find_formula():
    for i in range(rows - 1):
        waarde = mcframe.loc[i][1]
        waarde = str(waarde)
        if regex.findall(waarde):
            De_rij = i
            print("Het rijnummers waar een operator gevonden is: ", De_rij)

find_formula() #
find_MonteCarlo_Distributions() #




#print(mcframe)
#for i in range(rows - 1):
#    for j in range(colls - 1):
#        mcframe.loc[i,j+1]=mcframe.iloc[i][j+1]*(1 + Growth)


print(mcframe, '\n \n')
profit=mcframe.ix[:, 2:].sum(axis=0) # Sum over all rows, but skip first two columns
print(profit)

irr = round(np.irr(profit), 4)
print('The irr is', irr * 100, "%")

stve = streval.NumericStringParser()
result = stve.eval('2^4')
print(result)


