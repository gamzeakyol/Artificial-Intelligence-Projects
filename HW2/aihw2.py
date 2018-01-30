# Furkan Ozcelik 150140128

from simpleai.search import CspProblem
import numpy as np
import matplotlib.pyplot as plt
import cv2

def convert_pixels(result):
    r, c = 10, 10
    pixelboard = np.zeros((r, c))
    for i in range(10):
        for j in range(10):
            pixelboard[i,j] = result[(i,j)]
    return pixelboard

filename = "example_input.txt"
file = open(filename,"r")



# Row constraints
line = file.readline()
r = int(line)
rc_raw = []
for i in range(r):
    line = file.readline()
    line = line.split(" ")
    line = [int(x) for x in line]
    rc_raw.append(line)
row_lens = [len(x) for x in rc_raw]
row_con_len = max(row_lens)


global row_constraints
row_constraints= np.zeros((r,row_con_len))
for i in range(r):
    for j in range(row_lens[i]):
        row_constraints[i,j] = rc_raw[i][j]


# Column constraints
line = file.readline()
c = int(line)
cc_raw = []
for i in range(r):
    line = file.readline()
    line = line.split(" ")
    line = [int(x) for x in line]
    cc_raw.append(line)
col_lens = [len(x) for x in cc_raw]
col_con_len = max(col_lens)


global col_constraints
col_constraints= np.zeros((c,col_con_len))
for i in range(c):
    for j in range(col_lens[i]):
        col_constraints[i,j] = cc_raw[i][j]


variables = tuple((x,y) for x in range(r) for y in range(c))


domains = {}
for x in range(r):
    for y in range(c):
        domains[(x,y)] = [0,1]

def const_row(variables,values):
    row_state = np.zeros(row_con_len)
    global row_constraints
    row_num = variables[0][0]
    row_const = row_constraints[row_num]
    i = 0
    count = 0
    block_num = 0
    while i<10:
        if values[i] == 0:
            if count !=0:
                if block_num >= row_con_len:
                    return False
                row_state[block_num] = count
                block_num = block_num + 1
                count = 0
        else:
            count = count + 1
            if i == 9:
                if block_num >= row_con_len:
                    return False
                row_state[block_num] = count
        i = i+1
    satisfied = True
    for i in range(row_con_len):
        if(row_state[i] != row_constraints[row_num,i]):
            satisfied = False
    return satisfied


def const_col(variables,values):
    col_state = np.zeros(col_con_len)
    global col_constraints
    col_num = variables[0][1]
    i = 0
    count = 0
    block_num = 0
    while i < 10:
        if values[i] == 0:
            if count != 0:
                if block_num >= col_con_len:
                    return False
                col_state[block_num] = count
                block_num = block_num + 1
                count = 0
        else:
            count = count + 1
            if i == 9:
                if block_num >= col_con_len:
                    return False
                col_state[block_num] = count
        i = i + 1
    satisfied = True
    for i in range(col_con_len):
        if (col_state[i] != col_constraints[col_num, i]):
            satisfied = False
    return satisfied


constraints = []

for i in range(r):
    rows = tuple((i, x) for x in range(c))
    constraints.append((rows,const_row))

for i in range(c):
    cols = tuple((x, i) for x in range(r))
    constraints.append((cols,const_col))


from simpleai.search import backtrack, MOST_CONSTRAINED_VARIABLE, LEAST_CONSTRAINING_VALUE
from simpleai.search import convert_to_binary

variables, domains, constraints = convert_to_binary(variables, domains, constraints)

my_problem = CspProblem(variables, domains, constraints)
result = backtrack(my_problem,variable_heuristic= MOST_CONSTRAINED_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)
result = convert_pixels(result)
result[result==0] = 255
result[result==1] = 0

plt.imshow(result,cmap='gray',interpolation='nearest')
plt.show()


