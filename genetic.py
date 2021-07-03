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
            # sum_subsets[matrix[i][j]] += random.randint(0,10)
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

def parent(amount):
    pivot = random.random()
    if pivot <= 0.1:
        start = 0
        end = int(0.1 * amount)
    elif pivot <=0.3:
        start = int(0.1 * amount)
        end = int(0.3 * amount)
    else:
        start = int(0.3 * amount)
        end = amount
    return random.randint(start,end) 
# The distribution is based on results : 10% bad, 20% mediumm, 60% good
def crossover(index, genomes, new_genomes):
    
    # print()
    
    index_del_1 = parent(len(index)-1)
    genome_index_1 = index.pop(index_del_1)

    index_del_2 = parent(len(index)-1)
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

def individual_fitness(genomes, input ):
    sum_subsets = [0, 0, 0]
    row_amount = len(genomes)
    for j in range(row_amount):
        sum_subsets[genomes[j]] += input[j]
    return sum_subsets

def main():
    input = read_input()

    population = 20
    iterations = 40

    genomes = create_matrix(population)
    unsort_result = []
    index = []

    fitness_log = []
    genome_log = []

    count_10 = 0
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
        count_10 += 1
        if count_10 == 10:
            fitness_log.append(unsort_result[save_index[population -1]])
            genome_log.append(genomes[save_index[population -1]])
            count_10 = 0 
              
    finish_time = datetime.now()
    elapsed = finish_time - start_time

    print("Elapsed time :",  elapsed.total_seconds())
    print ("Best fitness :", unsort_result[save_index[population -1]])
    print("Population size :", population)
    print("Number of iterations :", iterations)

    for i in range(len(fitness_log)):
        subset_sum = individual_fitness(genome_log[i], input)
        print()
        print("Fitness at ",(i+1)*10,"th iteration :", fitness_log[i])
        print("Individuals sums")
        print("\tS1 ", subset_sum[0])
        print("\tS2 ", subset_sum[1])
        print("\tS3 ", subset_sum[2])


if __name__ == "__main__":
    main()
 
 
