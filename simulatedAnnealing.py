from numpy import asarray
from numpy import exp
from numpy.random import randn
from numpy.random import rand	
from numpy.random import randint	
from numpy.random import seed
from numpy.random import standard_normal
import time
import random
import sys  
from copy import deepcopy

def read_input():
    f = open('input.txt',"r")
    input_numbers = []
    for line in f:
        input_numbers.append(int(line.strip('\n')))
    
    return input_numbers


def randomize_list(num_list, indices):
	new_list = deepcopy(num_list)

	for i in indices:
		new_list[i][1] = random.randint(1, 3)

	return new_list


# objective function
def objective(num_list):
	s1 = 0
	s2 = 0
	s3 = 0
	
	for i in num_list:
		if i[1] == 1:
			s1 += i[0]
		if i[1] == 2:
			s2 += i[0]
		if i[1] == 3:
			s3 += i[0]

	fitness = (s1 - s2)**2 + (s1 - s3)**2 + (s2 - s3)**2
	return fitness

# simulated annealing algorithm


def simulated_annealing(nums, n_iterations, step_size, temp):
	start_time = time.time()
	#crear grupos con numeros
	nums_groups = []
	for n in nums:
		nums_groups.append([n,0])
	# generate an initial point
	best = randomize_list (nums_groups, range(len(nums_groups)))
	# evaluate the initial point
	best_eval = objective(best)
	# current working solution
	curr, curr_eval = best, best_eval
	# run the algorithm
	for i in range(n_iterations):
		# take a step
		change_amount = int(abs(randn()*(len(nums)/3))) + 1
		if change_amount > len(nums):
			change_amount = len(nums)
		numbers_change = random.sample(range(len(nums)), change_amount)
		candidate = randomize_list(curr, numbers_change)
		# evaluate candidate point
		candidate_eval = objective(candidate)
		# check for new best solution
		if candidate_eval < best_eval:
			# store new best point
			best, best_eval = candidate, candidate_eval
			# report progress
			print('> iter %d: fitness %.5f' % (i, best_eval))
		# difference between candidate and current point evaluation
		diff = candidate_eval - curr_eval
		# calculate temperature for current epoch
		t = temp / float(i + 1)
		# calculate metropolis acceptance criterion
		metropolis = 0
		try: 
			metropolis = exp(-diff / t)
		except OverflowError as e:
			metropolis = sys.maxint
		# check if we should keep the new point
		if diff < 0 or rand() < metropolis:
			# store the new current point
			curr, curr_eval = candidate, candidate_eval

	elapsed_time = time.time() - start_time
	return [best, best_eval, elapsed_time]

#read from input
nums = read_input()
# define the total iterations
n_iterations = 1000
# define the maximum step size
step_size = 0.1
# initial temperature
temp = 10
# perform the simulated annealing search
best, score, elapsed_time = simulated_annealing(nums, n_iterations, step_size, temp)
print('----------')
print('Elapsed time: ', elapsed_time)
print('Best fitness: ', score)
print('Number of iterations: ', n_iterations)
# print('f(%s) = %f' % (best, score))
