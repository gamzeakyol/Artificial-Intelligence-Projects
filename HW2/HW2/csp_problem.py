from simpleai.search import CspProblem
from simpleai.search import backtrack, MOST_CONSTRAINED_VARIABLE, LEAST_CONSTRAINING_VALUE
from simpleai.search import convert_to_binary


row_constraints = []
column_constraints = []
row_number = 0
column_number = 0

#File operations, reading column and row constraints from a file
file = open("example_input.txt", "r")

row_number_str = file.readline()
row_number = int(row_number_str)

for r in range(row_number):
    numbers = file.readline()
    numbers = numbers.split(" ")
    row_const = [int(n) for n in numbers]
    row_constraints.append(row_const)

column_number_str = file.readline()
column_number = int(column_number_str)

for r in range(column_number):
    numbers = file.readline()
    numbers = numbers.split(" ")
    column_const = [int(n) for n in numbers]
    column_constraints.append(column_const)

file.close()

# Define variables and domains:
# Every cell in the grid is a variable
# 0 and 1s (black and white) are domains for these variables
variables = tuple((i, j) for i in range(0, row_number) for j in (0, column_number))
print variables

domains = {}
for i in range(0, row_number):
    for j in range(0, column_number):
        domains[(i, j)] = [0, 1]
print domains

# Define row and column constraints
#Define row constraint
def const_row(variables, values):
    global row_constraints
    global row_number
    global column_number

    row_index = variables[0][0]
    #print row_index
    row = row_constraints[row_index]
    curr_tuple = tuple(row)
    element_num = len(curr_tuple)
    counter_for_black = [element_num]
    counter_for_white = 0
    j = 0
    flag = False
    checker_flag = False

    for i in range(0, column_number):
        if values[i] == 1:
            counter_for_black[j] = counter_for_black[j] + 1
            flag = True

        elif values[i] == 0:
            if flag == 1:
                j = j + 1
                flag = False
            counter_for_white = counter_for_white + 1

    for k in range(0, element_num):
        if counter_for_black[k] == curr_tuple[k]:
            checker_flag = True
        else:
            checker_flag = False
            return checker_flag
    return checker_flag

#Define column constraint
def const_column(variables, values):
    global column_constraints
    global row_number
    global column_number

    column_index = variables[0][1]
    column = column_constraints[column_index]
    curr_tuple = tuple(column)
    element_num = len(curr_tuple)
    counter_for_black = [element_num]
    counter_for_white = 0
    j = 0
    flag = False
    checker_flag = False
    print element_num
    
    for i in range(0, row_number):
        if values[i] == 1:
            counter_for_black[j] = counter_for_black[j] + 1
            flag = True

        elif values[i] == 0:
            if flag == 1:
                j = j + 1
                flag = False
            counter_for_white = counter_for_white + 1

    for k in range(0, element_num):
        if counter_for_black[k] == curr_tuple[k]:
            checker_flag = True
        else:
            checker_flag = False
            return checker_flag
    return checker_flag

constraints = []
for i in range(0, row_number):
    row = tuple((i, j) for j in range(0, column_number))
    constraints.append((row, const_row))
for j in range(0, column_number):
    column = tuple((j, i) for j in range(0, row_number))
    constraints.append((column, const_column))

#constraints = [(variables[i][j], const_row), (variables[i][j], const_column),]

variables, domains, constraints = convert_to_binary(variables, domains, constraints)

#Define Constraint Satisfaction Problem with variables, domains and constraints
my_problem = CspProblem(variables, domains, constraints)
#Solve CSP with backtrack algorithm
result = backtrack(my_problem, variable_heuristic= MOST_CONSTRAINED_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)

print result

for i in range(row_number):
    for j in range(column_number):
        print result
    print '\n'
