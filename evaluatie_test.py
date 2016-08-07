import pandas as pd
import numpy as np
import aritmatic as ari
import re

_author_ = 'Harry Boer'
_project_ = 'Monte Carlo Simulation'

# De 'Width' van de output console, zodat DataFrames and Numpy arrays niet worden afgebroken
desired_width = 320
pd.set_option('display.width', desired_width)

def check_out_input_file():  # Get the shape of the dataframe
    mcframe = pd.read_excel('montecarlo-template.xlsx')
    row, coll = mcframe.shape
    return(row)

operands = r'- + * / ^'
operand_regex = re.compile(operands)
Operand_List = ['+', '-', '*', '/', '**']  # To make it possible to input floats like -0.1
Distribution_List = ['norm', 'logn', 'tria', 'uni']  # Lists are predefined; stacks are to be filled
Logical_List = ['>', '<', '<=', '>=']  #ToDo: Maak het mogelijk om logicals uit te voeren.
operation_stack = []
variable_stack = []
distribution_stack = []
distribution_parameter_stack = []

mcframe = pd.read_excel('montecarlo-template.xlsx', skiprows=[0, 1, 2, 3, 4, check_out_input_file(), check_out_input_file()-1])  #0,1,2,3,4,11,12
mcframe.set_index(['Variables'], inplace=True)  # TODO: als er een lege rij is dan gaat het fout
rows, colls = mcframe.shape
mcframe = mcframe.fillna(0)
Variable_List = mcframe.index  # maak een lijst van variabele namen zoals deze voorkomen in de input sheet

Revgrowthrate = mcframe.ix[Variable_List[0]][0]
Costgrowthrate = mcframe.ix[Variable_List[1]][0]
sgr = mcframe.ix[Variable_List[2]][0]
exyield = mcframe.ix[Variable_List[3]][0]
r = mcframe.ix[Variable_List[4]][0]
investment = mcframe.ix[Variable_List[5]][0]
N = mcframe.ix[Variable_List[6]][0]
simulations = mcframe.ix[Variable_List[7]][0]

evaluation = ari.arithmeticEval('2 ** 4')
print('De evaluatie van 2 ** 4 is',evaluation)
print('eval r * investment =', eval('-(r+1) * investment'))
print('mcframe.ix[Variable_List[4]][0] * mcframe.ix[Variable_List[5]][0] =',
      eval('(1+mcframe.ix[Variable_List[4]][0]) * mcframe.ix[Variable_List[5]][0]'))


print(mcframe)


formula_dict = {}  # dictionary to keep the formulas
value_dict = {}  # dictionary to keep the values belonging to the row of the variable

for item in range(len(Variable_List)):
    formula_dict[Variable_List[item]]=mcframe.ix[Variable_List[item]][0]

for item in range(len(Variable_List)):
    value_dict[Variable_List[item]] = mcframe.ix[Variable_List[item],1:(N+1)]  #DataFrame	df.loc[row_indexer,column_indexer]


def operation_in_string(operand_lijst, the_string):
    return (set(Operand_List).intersection(the_string.split()))

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False



    # Deze functie haalt alle variabelen, distributies en operaties uit de input file en maakt ze klaar voor gebruik!

def extract_formula():
    for i in range(6, rows):  # inspect each row for the presence of a formula
        description_or_formule = mcframe.ix[Variable_List[i]][0]  # Shows the inhoud van de kolom "Description"
        description_or_formule = str(description_or_formule)
        # print('description_or_formula:  ', description_or_formule, 'type is', type(description_or_formule))
        if operation_in_string(Operand_List, description_or_formule):
            variable = Variable_List[i]
            formule_stack = description_or_formule.split()
            print('formula_stack is', formule_stack)
            for item in range(len(formule_stack)):
                operand = formule_stack.pop(0)
                if operand in Operand_List:  # if operand_regex.findall(operand) kan niet gebruikt worden -0.1 wordt niet herkend
                    operation_stack.append(operand)  # stop de * + - ^ operations in de operation_stack
                elif operand in Variable_List or is_number(operand):
                    variable_stack.append(operand)  # stop variabele of float in variable_stack
            print('operation_stack is', operation_stack, 'en variable_stack is', variable_stack)
            # evaluate_operation(variable)

# print('De formula_dict is', formula_dict)
# print('rows is', rows, 'and collumns is', colls)
# print('(Sales + Consulting + Other) * 0.1 =',(value_dict['Sales'] + value_dict['Consulting'] + value_dict['Other']) * 0.35)
# mcframe.loc['Variable-costs'] = (value_dict['Sales'] + value_dict['Consulting'] + value_dict['Other']) * -0.1
# print(mcframe)

extract_formula()