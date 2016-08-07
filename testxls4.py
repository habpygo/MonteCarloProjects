import pandas as pd
from pandas import DataFrame
import numpy as np
import time
import re
import distribution as dist
import math
import aritmatic as ari
# import matplotlib.pyplot as plt

_author_ = 'Harry Boer'
_project_ = 'Monte Carlo Simulation'

# De 'Width' van de output console, zodat DataFrames and Numpy arrays niet worden afgebroken
desired_width = 320
pd.set_option('display.width', desired_width)
WorkDir = 'file://localhost/Users/harryboer/Data/Software-Development/Python_Programs/MonteCarlo/mc-inputdata/montecarlo-template.xlsx'

def check_out_input_file():  # Get the shape of the dataframe
    mcframe = pd.read_excel(WorkDir)
    row, coll = mcframe.shape
    return(row)


mcframe = pd.read_excel(WorkDir, skiprows=[0, 1, 2, 3, 4, check_out_input_file(), check_out_input_file()-1])  #0,1,2,3,4,11,12
mcframe.set_index(['Variables'], inplace=True)  # todo: als er een lege rij is dan gaat het fout
rows, colls = mcframe.shape
mcframe = mcframe.fillna(0)

Variable_List = mcframe.index  # maak een lijst van variabele namen zoals deze voorkomen in de input sheet
operands = r'- + * / ^'
operand_regex = re.compile(operands)
Operand_List = ['+', '-', '*', '/', '**']  # To make it possible to input floats like -0.1
Distribution_List = ['norm', 'logn', 'tria', 'uni']  # Lists are predefined; stacks are to be filled
Logical_List = ['>', '<', '<=', '>=']  #ToDo: Maak het mogelijk om logicals uit te voeren.
operation_stack = []
variable_stack = []
distribution_stack = []
distribution_parameter_stack = []


def distributions_in_string(distribution_list, the_string):
    return(set(distribution_list).intersection(the_string.split()))

def operation_in_string(operand_lijst, the_string):
    return(set(Operand_List).intersection(the_string.split()))

print(mcframe)  # Het originele frame


Revgrowthrate = mcframe.ix[Variable_List[0]][0]
Costgrowthrate = mcframe.ix[Variable_List[1]][0]
sgr = mcframe.ix[Variable_List[2]][0]
exyield = mcframe.ix[Variable_List[3]][0]
r = mcframe.ix[Variable_List[4]][0]
investment = mcframe.ix[Variable_List[5]][0]
N = mcframe.ix[Variable_List[6]][0]
simulations = mcframe.ix[Variable_List[7]][0]

print('All the devils are there!:',Revgrowthrate,Costgrowthrate,sgr,r,exyield,investment,N, simulations)

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
        if distributions_in_string(Distribution_List, description_or_formule):
            variable = Variable_List[i]
            distribution = description_or_formule.split()
            # print('distribution_stack found is', distribution)
            # print('distribution_stack[2] = ', distribution[2])
            for j in range(len(distribution)):
                operand = distribution.pop(0)
                # print('lengte distribution is', len(distribution), ' en operand', j, 'is', operand)
                if operand in Distribution_List:
                    distribution_stack.append(operand)
                elif is_number(operand):
                    distribution_parameter_stack.append(operand)
            kind, mean, stdv, c = evaluate_distribution(variable)
            # print('kind is ', kind, 'mean is', mean, 'stdv is', stdv)
            dist.Distribution(simulations, kind, mean, stdv, c)  # HIER WORDT EEN INSTANCE VAN DISTRIBUTION GECREEERD. WAT NU ;-)
        elif operation_in_string(Operand_List, description_or_formule):
            variable = Variable_List[i]
            formule_stack = description_or_formule.split()
            # print('formula_stack is', formule_stack)
            for item in range(len(formule_stack)):
                operand = formule_stack.pop(0)
                if operand in Operand_List:  # if operand_regex.findall(operand) kan niet gebruikt worden -0.1 wordt niet herkend
                    operation_stack.append(operand)  # stop de * + - ^ operations in de operation_stack
                elif operand in Variable_List or is_number(operand):
                    variable_stack.append(operand)  # stop variabele of float in variable_stack
            print('operation_stack is', operation_stack, 'en variable_stack is', variable_stack)
            evaluate_operation(variable)


#TODO:  FUNCTION CAN NOT HANDLE EVEN NUMBER OF OPERATIONS THUS: * + + is ok. + + or + + + * NOT
def evaluate_operation(x):
    first_popped_variable = variable_stack.pop(0)
    popped_operation = operation_stack.pop(0)
    second_popped_variable = variable_stack.pop(0)
    if first_popped_variable and second_popped_variable in Variable_List:  # Case 1: beiden zijn variabelen
        # print('Case 1: x =',x)
        if popped_operation == '+':
            mcframe.loc[x] = mcframe.loc[first_popped_variable] + mcframe.loc[second_popped_variable]
        elif popped_operation == '-':
            mcframe.loc[x] = mcframe.loc[first_popped_variable] - mcframe.loc[second_popped_variable]
        elif popped_operation == '*':
            mcframe.loc[x] = mcframe.loc[first_popped_variable] * mcframe.loc[second_popped_variable]
        elif popped_operation == '/':
            mcframe.loc[x] = mcframe.loc[first_popped_variable] / mcframe.loc[second_popped_variable]
    elif first_popped_variable in Variable_List and is_number(second_popped_variable):  # Case 2: Eerste is een variabele, tweede is een getal
        # print('Case 2: x =', x)
        if popped_operation == '+':
            mcframe.loc[x] = mcframe.loc[first_popped_variable] + float(second_popped_variable)
        elif popped_operation == '-':
            mcframe.loc[x] = mcframe.loc[first_popped_variable] - float(second_popped_variable)
        elif popped_operation == '*':
            mcframe.loc[x] = mcframe.loc[first_popped_variable] * float(second_popped_variable)
        elif popped_operation == '/':
            mcframe.loc[x] = mcframe.loc[first_popped_variable] / float(second_popped_variable)
    elif is_number(first_popped_variable) and second_popped_variable in Variable_List:  # Case 3: Eerste is een getal, tweede een variabele
        # print('Case 3: x =', x)
        if popped_operation == '+':
            mcframe.loc[x] = mcframe.loc[second_popped_variable] + float(first_popped_variable)
        elif popped_operation == '-':
            mcframe.loc[x] = mcframe.loc[second_popped_variable] - float(first_popped_variable)
        elif popped_operation == '*':
            mcframe.loc[x] = mcframe.loc[second_popped_variable] * float(first_popped_variable)
        elif popped_operation == '/':
            mcframe.loc[x] = mcframe.loc[second_popped_variable] / float(first_popped_variable)
    if variable_stack and operation_stack:  # Als er nog wat in de stacks zit, evalueer het
        first_popped_variable = variable_stack.pop(0)
        popped_operation = operation_stack.pop(0)
        if first_popped_variable in Variable_List:
            if popped_operation == '+':
                mcframe.loc[x] += mcframe.loc[first_popped_variable]
            elif popped_operation == '-':
                mcframe.loc[x] -= mcframe.loc[first_popped_variable]
            elif popped_operation == '*':
                mcframe.loc[x] *= mcframe.loc[first_popped_variable]
            elif popped_operation == '/':
                mcframe.loc[x] /= mcframe.loc[first_popped_variable]
        elif is_number(first_popped_variable):
            if popped_operation == '+':
                mcframe.loc[x] += first_popped_variable
            elif popped_operation == '-':
                mcframe.loc[x] -= first_popped_variable
            elif popped_operation == '*':
                mcframe.loc[x] *= first_popped_variable
            elif popped_operation == '/':
                mcframe.loc[x] /= first_popped_variable
    if variable_stack and operation_stack:
        first_popped_variable = variable_stack.pop(0)
        popped_operation = operation_stack.pop(0)
        # print('Case 5: x =', x)
        # print('first_popped_variable is', first_popped_variable)
        # print('popped_operation is', popped_operation)
        if first_popped_variable in Variable_List:
            if popped_operation == '+':
                mcframe.loc[x] += mcframe.loc[first_popped_variable]
            elif popped_operation == '-':
                mcframe.loc[x] -= mcframe.loc[first_popped_variable]
            elif popped_operation == '*':
                mcframe.loc[x] *= mcframe.loc[first_popped_variable]
            elif popped_operation == '/':
                mcframe.loc[x] /= mcframe.loc[first_popped_variable]
        elif is_number(first_popped_variable):
            if popped_operation == '+':
                mcframe.loc[x] += float(first_popped_variable)
            elif popped_operation == '-':
                mcframe.loc[x] -= float(first_popped_variable)
            elif popped_operation == '*':
                mcframe.loc[x] *= float(first_popped_variable)
            elif popped_operation == '/':
                mcframe.loc[x] /= float(first_popped_variable)



def evaluate_distribution(y):
    distribution = distribution_stack.pop(0)
    mean = distribution_parameter_stack.pop(0)
    stdv = distribution_parameter_stack.pop(0)
    if distribution_parameter_stack:
        c = distribution_parameter_stack.pop(0)
        return(distribution, mean, stdv, c)
    else:
        return(distribution, mean, stdv, None)



extract_formula()  # Haal eerst de formules boven water

print(mcframe)  # Het berekende frame

profit=mcframe.ix[:, 1:].sum(axis=0) # Sum over all rows, but skip first column
exit_price = (profit[N-1]*(1+sgr))/exyield
print('EXIT PRICE is:', exit_price)
profit[7] = exit_price

irr = round(np.irr(profit), 4)
print('The IRR is', irr * 100, "%")
print('number of rows:', rows, 'number of colls:', colls)
print('Date of run is:',time.strftime("%d/%m/%Y"))
print('Time of run is:',time.strftime("%H:%M:%S"))

evaluation = ari.arithmeticEval('2 ** 4')
print('Het evaluatie totaal is',evaluation)


