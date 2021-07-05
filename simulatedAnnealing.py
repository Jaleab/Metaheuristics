from numpy import asarray
from numpy import exp
from numpy.random import randn
from numpy.random import rand	
from numpy.random import randint	
from numpy.random import seed
import random

def randomize_list(num_list, indices):
    for i in indices:
        num_list[i][1] = random.randint(1, 3)


# objective function
def objective(num_list):
    s1 = 0
    s2 = 0
    s3 = 0

    for i in num_list:
        if num_list[i][0] == 1:
            suma1 += key
        if num_list[i][0] == 2:
            suma2 += key
        if num_list[i][0] == 3:
            suma3 += key

    fitness = (s1 - s2)^2 + (s1 - s3)^2 + (s2 - s3)^2
    return fitness

# simulated annealing algorithm


def simulated_annealing(objective, bounds, n_iterations, step_size, temp):
	# generate an initial point
	best = randomize_list (l, range(len(l)))
	# evaluate the initial point
	best_eval = objective(best)
	# current working solution
	curr, curr_eval = best, best_eval
	# run the algorithm
	for i in range(n_iterations):
		# take a step
		#TODO hacer nueva solucion con array.copy()
		candidate = curr + randn(len(bounds)) * step_size
		# evaluate candidate point
		candidate_eval = objective(candidate)
		# check for new best solution
		if candidate_eval < best_eval:
			# store new best point
			best, best_eval = candidate, candidate_eval
			# report progress
			print('>%d f(%s) = %.5f' % (i, best, best_eval))
		# difference between candidate and current point evaluation
		diff = candidate_eval - curr_eval
		# calculate temperature for current epoch
		t = temp / float(i + 1)
		# calculate metropolis acceptance criterion
		metropolis = exp(-diff / t)
		# check if we should keep the new point
		if diff < 0 or rand() < metropolis:
			# store the new current point
			curr, curr_eval = candidate, candidate_eval
	return [best, best_eval]

# seed the pseudorandom number generator
# seed(1)
# define range for input
# bounds = asarray([[-5.0, 5.0]])
# define the total iterations
# n_iterations = 1000
# define the maximum step size
# step_size = 0.1
# initial temperature
# temp = 10
# perform the simulated annealing search
# best, score = simulated_annealing(objective, bounds, n_iterations, step_size, temp)
# print('Done!')
# print('f(%s) = %f' % (best, score))

l = [[1,0],[1,0],[1,0],[1,0],[1,0],[1,0],[1,0],[1,0],[1,0]]
print(l)
randomize_list (l, range(len(l)))
print(l)