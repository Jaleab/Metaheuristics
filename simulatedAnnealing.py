from numpy import exp
from numpy.random import randn
from numpy.random import rand	
from numpy.random import randint	
from numpy import seterr
import time
import random
import sys  
from copy import deepcopy

#lee los numeros de la lista input.txt
def read_input():
    f = open('input.txt',"r")
    input_numbers = []
    for line in f:
        input_numbers.append(int(line.strip('\n')))
    
    return input_numbers

#asigna numeros a grupos aleatorios
#los indices indican cuales numeros cambiar de grupo
def randomize_list(num_list, indices):
	new_list = deepcopy(num_list)

	for i in indices:
		new_list[i][1] = random.randint(1, 3)

	return new_list


# funcion objetivo
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
	return [fitness, [s1,s2,s3]]

# simulated annealing algorithm
def simulated_annealing(nums, n_iterations, temp):
	# para que numpy no tire warnings para overflow y underflow
	seterr(over="ignore",under="ignore")
	start_time = time.time()
	# crear grupos con numeros
	nums_groups = []
	for n in nums:
		nums_groups.append([n,0])
	# genera una solucion inicial y la evalua
	best = randomize_list (nums_groups, range(len(nums_groups)))
	best_eval, best_sums = objective(best)
	# solucion actual
	curr, curr_eval, curr_sums = best, best_eval, best_sums

	for i in range(n_iterations):
		# genera otra solucion vecina
		change_amount = int(abs(randn()*(len(nums)/3))) + 1
		if change_amount > len(nums):
			change_amount = len(nums)
		numbers_change = random.sample(range(len(nums)), change_amount)
		candidate = randomize_list(curr, numbers_change)
		
		# evalua solucion vecina
		candidate_eval, candidate_sums = objective(candidate)
		if candidate_eval < best_eval:
			best, best_eval, best_sums = candidate, candidate_eval, candidate_sums
			# imprime progreso
			print('Fitness at', i,'th iteration:', best_eval)
		diff = candidate_eval - curr_eval
		# calcula la temperatura actual
		t = temp / float(i + 1)
		# calcula el valor metropolis y decide si aceptar el nuevo punto
		metropolis = exp(-diff / t)
		if diff < 0 or rand() < metropolis:
			curr, curr_eval, curr_sums = candidate, candidate_eval, candidate_sums

	elapsed_time = time.time() - start_time
	return [best, best_eval, best_sums, elapsed_time]


def main():

	#lee de input.txt
	nums = read_input()
	n_iterations = 5000
	temp = 100
	# Hace el Simulated Annealing con los numeros nums
	best, score, sums, elapsed_time = simulated_annealing(nums, n_iterations, temp)
	print('----------')
	print('Elapsed time: ', elapsed_time,'s')
	print('Fitness of best solution: ', score)
	print('Subsets sums:  ', sums)
	print('Explored solutions: ', n_iterations)

if __name__ == "__main__":
	main()