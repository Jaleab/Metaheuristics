# Ejecucion con python3 ./GWO.py
import random
import math   
import copy    # array-copying convenience
import sys     # max float
import time

total_numbers = 10000     # Amount of numbers in input.txt
quantity_subsets = 3
keys = list(range(total_numbers))           # Keys for the dictionary {index(key):number(value)}
input_numbers = dict(zip(keys, (0 for _ in keys)))

# Fill the dictionary input_numbers with the numbers from the input
def read_input():
    f = open('input.txt',"r")
    index = 0
    for line in f:
        input_numbers[index] = int(line.strip('\n'))
        index += 1

# Populate the subsets of one individual. The size of the subsets and each subset's number are random.
def fill_subsets(numbers_subsets):
    residue = total_numbers 
    indexes_of_available_numbers = keys.copy()
    quantity_of_subsets = len(numbers_subsets)
    for i in range(quantity_of_subsets):
        numbers_in_subset = random.randint(0,residue) if i != 2 else residue                # Amount of numbers in subset i
        residue = residue - numbers_in_subset        # Amount of numbers not assigned to a subset
        for j in range(numbers_in_subset):
            random_index = random.choice(indexes_of_available_numbers)
            numbers_subsets[i].append(random_index)
            indexes_of_available_numbers.remove(random_index)


# Sum of squareed differences : f(s1, s2, s3) = (s1 - s2)^2 + (s1 - s3)^2 + (s2 - s3)^2.
def fitness_sum_squares(numbers_subsets):
    fitness_value = 0.0
    sum_subsets = [0, 0, 0]
    for i in range(len(sum_subsets)): 
        for number in numbers_subsets[i]:
            sum_subsets[i] += input_numbers[number]
    fitness_value += pow((sum_subsets[0]-sum_subsets[1]), 2) + pow((sum_subsets[0]-sum_subsets[2]), 2) + pow((sum_subsets[1]-sum_subsets[2]), 2)
    return fitness_value

# wolf class
class wolf:
  def __init__(self, fitness, quantity_subsets, maxx, minx):
    self.rnd = random.Random()
    self.position = [0.0 for i in range(quantity_subsets)]
    self.numbers_subsets = [[] for i in range(quantity_subsets)]
 
    fill_subsets(self.numbers_subsets)
    
    for i in range(quantity_subsets):
      self.position[i] = ((maxx - minx) * self.rnd.random() + minx)
 
    self.fitness = fitness(self.numbers_subsets) # curr fitness
 
 # Grey Wolf Optimization (GWO)
def gwo(fitness, max_iter, population_size, quantity_subsets, maxx, minx):
    rnd = random.Random()
    number_of_solutions = 0
 
    # Create n random wolves
    population = [ wolf(fitness_sum_squares, quantity_subsets, maxx, minx) for i in range(population_size)]
    number_of_solutions += population_size
 
    # On the basis of fitness values of wolves
    # sort the population in asc order
    population = sorted(population, key = lambda temp: temp.fitness)
 
    # best 3 solutions will be called as
    # alpha, beta and gama
    alpha_wolf, beta_wolf, gamma_wolf = copy.copy(population[: 3])
 
 
    # main loop of gwo
    Iter = 1
    while Iter <= max_iter:
 
        # after every 10 iterations
        # print iteration number and best fitness value so far
        if Iter % 10 == 0 and Iter > 1:
            print("Iter = " + str(Iter) + " best fitness = %.3f" % alpha_wolf.fitness)
        
        # linearly decreased from 2 to 0
        a = 2*(1 - Iter/max_iter)
 
        # updating each population member with the help of best three members
        for i in range(population_size):
            A1, A2, A3 = a * (2 * rnd.random() - 1), a * (
              2 * rnd.random() - 1), a * (2 * rnd.random() - 1)
            C1, C2, C3 = 2 * rnd.random(), 2*rnd.random(), 2*rnd.random()
 
            X1 = [0.0 for i in range(quantity_subsets)]
            X2 = [0.0 for i in range(quantity_subsets)]
            X3 = [0.0 for i in range(quantity_subsets)]
            Xnew = [0.0 for i in range(quantity_subsets)]
            for j in range(quantity_subsets):
                X1[j] = alpha_wolf.position[j] - A1 * abs(
                  C1 - alpha_wolf.position[j] - population[i].position[j])
                X2[j] = beta_wolf.position[j] - A2 * abs(
                  C2 -  beta_wolf.position[j] - population[i].position[j])
                X3[j] = gamma_wolf.position[j] - A3 * abs(
                  C3 - gamma_wolf.position[j] - population[i].position[j])
                Xnew[j]+= X1[j] + X2[j] + X3[j]
             
            for j in range(quantity_subsets):
                Xnew[j]/=3.0

            x_subsets = [[],[],[]] 
            fill_subsets(x_subsets)
            number_of_solutions += 1

            # fitness calculation of new solution
            fnew = fitness(x_subsets)
 
            # greedy selection
            if fnew < population[i].fitness:
                population[i].position = Xnew
                population[i].fitness = fnew 
                population[i].numbers_subsets = x_subsets
                 
        # On the basis of fitness values of wolves
        # sort the population in asc order
        population = sorted(population, key = lambda temp: temp.fitness)
 
        # best 3 solutions will be called as
        # alpha, beta and gama
        alpha_wolf, beta_wolf, gamma_wolf = copy.copy(population[: 3])
         
        Iter+= 1
    # end-while
 
    # returning the best solution
    return alpha_wolf.fitness, alpha_wolf.numbers_subsets, number_of_solutions
           
#----------------------------

read_input()

repetitions = 5
for i in range(repetitions):
    print("\nBegin grey wolf optimization on sum of squares function\n")
    fitness = fitness_sum_squares 
    
    print("Goal is to minimize sum of squares's function")
    
    population_size = 100
    max_iter = 50

    print("Setting population size = " + str(population_size))
    print("Setting max_iter = " + str(max_iter))
    print("\nStarting GWO algorithm\n")
    
    t0 = time.time()
    best_fitness, best_subset, number_of_solutions = gwo(fitness, max_iter, population_size, quantity_subsets, 4994213664, 1664737888)
    t1 = time.time()
    total_time = t1-t0
    
    print("\nGWO completed\n")
    print("\nBest solution found:")
    print("Subsets of the solution", best_subset)
    print("Fitness of best solution =", best_fitness)
    sum_subsets = [0,0,0]
    for i in range(len(best_subset)): 
            for number in best_subset[i]:
                sum_subsets[i] += input_numbers[number]
          
    print("Subsets sums: ", sum_subsets)
    print("Execution time: ", total_time)
    print("Explored solutions: ", number_of_solutions) 
    print("\nEnd GWO for sub of squares\n")