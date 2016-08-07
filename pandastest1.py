import pandas as pd
import numpy as np

# De 'Width' van de output console, zodat DataFrames and Numpy arrays niet worden afgebroken
desired_width = 320
pd.set_option('display.width', desired_width)

# df = pd.read_excel("excel-comp-data.xlsx")
# # print(df)
#
# df['total'] = df['Jan'] + df['Feb'] + df['Mar']
# # print(df)
#
# sum_row = df[['Jan', 'Feb', 'Mar', 'total']].sum()
# df_sum = pd.DataFrame(data=sum_row).T
# df_sum = df_sum.reindex(columns = df.columns)
# df_final = df.append(df_sum,ignore_index=True)
# print(df_final)

df = pd.read_excel("montecarlo-template2.xlsx", skiprows=[0, 1, 2, 3, 4, 11, 12])
df = df.fillna(0)
print(df)


operation_stack = ['Sales', '+', 'Consulting', '+', 'Other', '*', 0.35]


def evaluate(list):
    if operation_stack:  # Python way of testing whether the list is empty or not. Empty lists can't be popped ;-)
        operand = operation_stack.pop(0)
        evaluate_operation(operand)
        print('de operand is', operand, 'en de operation_stack is nu', operation_stack)
        evaluate(operation_stack)  # apply recursion here


def evaluate_operation(op):
    # print(op)
    pass


evaluate(operation_stack)
