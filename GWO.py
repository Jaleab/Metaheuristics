# python implementation of Grey wolf optimization (GWO)
# minimizing rastrigin and sphere function
 
 
import random
import math    # cos() for Rastrigin
import copy    # array-copying convenience
import sys     # max float
 
def read_input():
    f = open('input.txt',"r")
    numbers = []

    for line in f:
        numbers.append(int(line.strip('\n')))
    #print(numbers)

# Suma de cuadrados de sus diferencias: f(s1, s2, s3) = (s1 - s2)^2 + (s1 - s3)^2 + (s2 - s3)^2.
def fitness_sum_squares(numbers_subsets):
    fitness_value = 0.0
    sum_subsets = [0, 0, 0]
    for i in range(len(sum_subsets)):
        for number in numbers_subsets[i]:
            sum_subsets[i] += number
    fitness_value += pow((sum_subsets[0]-sum_subsets[2]), 2) + pow((sum_subsets[0]-sum_subsets[2]), 2) + pow((sum_subsets[1]-sum_subsets[2]), 2)
    print(fitness_value)
    return fitness_value

read_input()

numbers = [[4],[4],[4]]
fitness_sum_squares(numbers)