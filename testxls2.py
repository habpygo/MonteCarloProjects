from pandas import DataFrame
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import re
import stringevaluator as streval
_author_ = 'Harry Boer'
_project_ = 'Monte Carlo Simulation'



# De 'Width' van de output console, zodat DataFrames and Numpy arrays niet worden afgebroken
desired_width = 320
pd.set_option('display.width', desired_width)

mcframe = pd.read_excel('montecarlo-template.xlsx', skiprows=[0, 1, 2, 3, 4, 17, 18])
mcframe.set_index(['Variables'], inplace=True)
rows, colls = mcframe.shape
mcframe = mcframe.fillna(0)

Variable_List = mcframe.index

operands = r'[-+*/^]'
operand_regex = re.compile(operands)
variable = []
variable_dict = {}
list_x = []
operand_list = []
number_list = []

def how_many_formulas():
    no_of_formulas = 0
    for i in range(rows - 1):
        waarde = mcframe.ix[Variable_List[i]][0]
        waarde = str(waarde)
        if operand_regex.findall(waarde):
            no_of_formulas += 1
    return(no_of_formulas)

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

# print(mcframe)  # show de DataFrame
# print('-------------------------------------\n')

def catch_variables(deWaarde):
    print('deWaarde is', deWaarde)
    for k in range(2, colls):
        variable.append(mcframe.ix[deWaarde][k])  # Hier wordt de index opgepikt en de bijbehorende waarden in de kolommen
    variable_dict[deWaarde] = variable            # in list_x gestopt/gekopieerd
    list_x.append(variable_dict[deWaarde].copy())
    variable_dict.clear()
    variable.clear()
    print('list is', list_x)
    return(list_x)  # Nu de functie aanroepen om iets met de list te doen

def add_result_to_numpyarray(a_list):
    pass
    # return(arr)

def evaluate(a_list):
    arr = np.array(a_list)
    # print(arr, '\n','type is', type(arr))
    if number_list:
        getal = number_list.pop(0)
        operand = operand_list.pop(0)
        if operand == '*':
            arr2 = arr * float(getal)
            # print('Vanuit evaluate(a_list):\n',arr2)  # doe iets nuttigs
            # mcframe.replace()
            print(mcframe)
        elif operand == '+':
            arr2 = arr + float(getal)
            print(arr2)
        elif operand == '-':
            arr2 = arr - float(getal)
            print(arr2)
        elif operand == '/':
            arr2 = arr / float(getal)
            print(arr2)

def interim_evaluate(interim_list):
    arr_interim = np.array(interim_list)
    # print('Vanuit de def interim_evaluate: arr_interim is \n', arr_interim, 'operand_list is', operand_list, 'number_list is:', number_list)
    for i in range(len(operand_list)):
        operand1 = operand_list.pop(0)
        if operand1 == '+':
            voorlopig = arr_interim.sum(0)
            # print('arr_interim.sum is', voorlopig, 'voorlopig is', type(voorlopig))


def extract_formula():
    for i in range(rows - 1):  # inspect each row for the presence of a formula
        operand_list.clear()  # clean out the operand list for new row inspection
        formule = mcframe.ix[Variable_List[i]][0]  # Variable_List = mcframe.index
        print('De formule is ', formule, 'en het type is', type(formule))
        formule = str(formule)
        if operand_regex.findall(formule):  # Gaat alleen de if loop in als er een formule is gevonden. Dus constanten slaat hij over
            gesplitste_formule = formule.split()
            print('**************************************************** \n')
            print('gesplitste_formule is ', gesplitste_formule, 'en het type is', type(gesplitste_formule))
            for j in range(len(gesplitste_formule)):  # bijvoorbeeld: len(Sales * 0.35) is drie
                # print('j =',j)
                formule_item = gesplitste_formule[j]
                if formule_item in Variable_List:
                    The_List = catch_variables(formule_item)  # vang de waarden bijbehorende de index variabele in een list
                    print('formule_item is', formule_item)
                    print('en bijbehorende reeks is \n', mcframe.ix[formule_item])
                elif is_number(formule_item):
                    number_list.append(formule_item)
                elif operand_regex.findall(formule_item):
                    operand_list.append(formule_item)
                elif formule_item == ')':  # Hier is de interim Break
                    interim_evaluate(The_List)  # Hier moet de berekening uitgevoerd worden (Sales + Consulting + Other)
            evaluate(The_List)
            The_List.clear()  # Hier is de Break; alle lists worden ge-cleared
            number_list.clear()
            operand_list.clear()

extract_formula()

