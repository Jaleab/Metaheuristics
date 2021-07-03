import random
import math    # cos() for Rastrigin
import copy    # array-copying convenience
import sys     # max float
from datetime import datetime

total_numbers = 10000
quantity_subsets = 3

# Fill the dictionary input_numbers with the numbers from the input
def read_input():
    f = open('input.txt',"r")
    input_numbers = []
    for line in f:
        input_numbers.append(int(line.strip('\n')))
    
    return input_numbers

# Suma de cuadrados de sus diferencias: f(s1, s2, s3) = (s1 - s2)^2 + (s1 - s3)^2 + (s2 - s3)^2.
def calculate_fitness(matrix, input):
    sum_subsets = [0, 0, 0]
    row_amount = len(matrix)
    fitness_array = [0] * row_amount
    index = [0] * row_amount
    for i in range(len(matrix)):
        index[i] = i
        for j in range(len(matrix[0])):
            sum_subsets[matrix[i][j]] += input[j]

        # result = (pow((sum_subsets[0]-sum_subsets[2]), 2) + pow((sum_subsets[0]-sum_subsets[2]), 2) + pow((sum_subsets[1]-sum_subsets[2]), 2))
        fitness_array[i] = (pow((sum_subsets[0]-sum_subsets[2]), 2) + pow((sum_subsets[0]-sum_subsets[2]), 2) + pow((sum_subsets[1]-sum_subsets[2]), 2))

    index = [x for _,x in sorted(zip(fitness_array,index))]

    return fitness_array, index

def create_matrix(population):
    matrix = []
    for i in range(population):
        a = []
        for x in range(10000):
            a.append(random.randint(0,2))
        matrix.append(a)
    return matrix

    # for i in range(len(index)):
    #     pivot = random.random()
    #     if pivot <= 0.1:
    #         print("Bad")
    #     elif pivot <=0.3:
    #         print("Mdium")
    #     else:
    #         print("Good")
# The distribution is based on results : 10% bad, 20% mediumm, 60% good
def crossover(index, genomes, new_genomes):
    
    # print()
    
    index_del_1 = int(random.random() * len(index))
    genome_index_1 = index.pop(index_del_1)

    index_del_2 = int(random.random() * len(index))
    genome_index_2 = index.pop(index_del_2)

    start = random.randint(0,4999)
    end = random.randint(5000,9999)

    parent_1 = genomes[genome_index_1]
    parent_2 = genomes[genome_index_2]

    # genomes.pop(index_del_1)
    # genomes.pop(index_del_2)

    offspring_1 = parent_1[:start] +parent_2[start:end]+ parent_1[end:]
    offspring_2 = parent_2[:start] +parent_1[start:end]+ parent_2[end:]

    new_genomes.append(offspring_1)
    new_genomes.append(offspring_2)

    return index, genomes, new_genomes


def mutation(genomes):
    for i in range(len(genomes)):
        position = random.randint(0,9999)
        pivot = random.randint(1,2)
        change = (genomes[i][position] + pivot) % 3
        genomes[i][position] = change

def main():
    input = read_input()

    population = 60
    iterations = 40

    genomes = create_matrix(population)
    unsort_result = []
    index = []
    #Sorted ascending way index[0] = lower, index[n] = upper
    start_time = datetime.now()
    for l in range (iterations):
        unsort_result, index = calculate_fitness(genomes, input)
        save_index = index.copy()
        new_genomes = []
        genomes_iterations = math.floor(population // 2)
        for i in range(genomes_iterations):
            index, genomes, new_genomes = crossover(index, genomes, new_genomes)
        genomes = new_genomes.copy()

        mutation(genomes)
    finish_time = datetime.now()
    elapsed = finish_time - start_time

    print("Elapsed time :",  elapsed.total_seconds())
    print ("Better fitness :", unsort_result[save_index[9]])
    # print (genomes[save_index[9]])
    print("Population size :", population)
    print("Number of iterations :", iterations)
if __name__ == "__main__":
    main()
 
# population_size = 5
# max_iter = 10
 
# print("Setting population size = " + str(population_size))
# print("Setting max_iter = " + str(max_iter))
# print("\nStarting Genetic algorithm\n")

# best_fitness, best_subset = genetic(max_iter, population_size, 1000000, -1000000, quantity_subsets)
 
# print("Genetic algorithm completed\n")
# print("\nBest solution found:")
# print("Subsets of the solution", best_subset)
# print("fitness of best solution =", best_fitness)
 

