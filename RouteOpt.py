import random
from NodeSimulation import Node
import matplotlib.pyplot as plt
random.seed(123)

# Graph Points
cost = []
time = []
fitness = []

# Inputs
POPULATION_SIZE = 20
NUM_TYPE_NODES = 3
NUM_MAN = 2
NUM_WHO = 3
NUM_RET = 2

manufacturer = []
manufacturer.append(Node(30, 25))
manufacturer.append(Node(10, 40))

wholesaler = []
wholesaler.append(Node(10, 50))
wholesaler.append(Node(50, 65))
wholesaler.append(Node(27, 55))

retailer = []
retailer.append(Node(50, 76))
retailer.append(Node(25, 89))

# In hundreds
production_cost = [54, 76]
man_to_who_cost = [
    [10, 45, 72],
    [21, 54, 37]
]
who_to_ret_cost = [
    [26, 54],
    [34, 56],
    [12, 39]
]

# In hours
production_time = [24, 32]
# TODO Calculate from node coordinates
man_to_who_time = [
    [12, 16, 14],
    [15, 13, 11],
    [14, 10, 17]
]
who_to_ret_time = [
    [5, 9],
    [4, 6],
    [8, 2]
]


# Functions for GA

def get_chromosome():
    chromosome = []
    chromosome.append(random.randint(0, NUM_MAN-1))
    chromosome.append(random.randint(0, NUM_WHO-1))
    chromosome.append(random.randint(0, NUM_RET-1))
    return chromosome

def cal_fitness(individual):
    chromosome = individual.chromosome
    cost = 0
    cost += production_cost[chromosome[0]]
    cost += man_to_who_cost[chromosome[0]][chromosome[1]]
    cost += who_to_ret_cost[chromosome[1]][chromosome[2]]
    individual.cost = cost

    time = 0
    time += production_time[chromosome[0]]
    time += man_to_who_time[chromosome[0]][chromosome[1]]
    time += who_to_ret_time[chromosome[1]][chromosome[2]]
    individual.time = time

    cap = 0
    if (manufacturer[chromosome[0]].number_of_goods + 1 <= manufacturer[chromosome[0]].capacity):
        cap += 1
    if (wholesaler[chromosome[1]].number_of_goods + 1 <= wholesaler[chromosome[1]].capacity):
        cap += 1
    if (retailer[chromosome[2]].number_of_goods + 1 <= retailer[chromosome[2]].capacity):
        cap += 1
    
    return float(1000 * cap /(1+cost+time))

class Individual:
    def __init__(self, chromosome=None):
        if chromosome is None:
            self.chromosome = get_chromosome()
        else :
            self.chromosome = chromosome
        self.fitness = cal_fitness(self)
    # Operator overloading to sort according to fitness
    def __lt__(self, other):
        return self.fitness>other.fitness

def generate_initial_population():
    population = []
    i = 0
    while (i < POPULATION_SIZE):
        population.append(Individual())
        i += 1
    return population

pop = generate_initial_population()
for i in pop:
    print(i.chromosome)

def crossover (parent1, parent2):
    child_chromosome = []
    for i in range(NUM_TYPE_NODES):
        prob = random.randint(0,100)
        if (prob < 49):
            # Take gene from parent 1
            child_chromosome.append(parent1.chromosome[i])
        elif (prob <= 98):
            # Take gene from parent 2
            child_chromosome.append(parent2.chromosome[i])
        else :
            # Perform mutation
            if (i==0):
                child_chromosome.append(random.randint(0,NUM_MAN-1))
            elif (i==1):
                child_chromosome.append(random.randint(0, NUM_WHO-1))
            else:
                child_chromosome.append(random.randint(0, NUM_RET-1))
    return Individual(chromosome = child_chromosome)

def find_population_fitness(population):
    sum_fitness = 0
    sum_time = 0
    sum_cost = 0
    for i in population:
        sum_fitness += i.fitness
        sum_time += i.time
        sum_cost += i.cost
    new_avg_fitness = float(sum_fitness/POPULATION_SIZE)
    fitness.append(new_avg_fitness)
    time.append(float(sum_time/POPULATION_SIZE))
    cost.append(float(sum_cost/POPULATION_SIZE))
    return new_avg_fitness

# Main Function

def run_ga():
    generation = 0
    population = generate_initial_population()
    population.sort()
    pvs_avg_fitness = 0
    new_avg_fitness = find_population_fitness(population)
    fitness.append(new_avg_fitness)
    print("Generation: 0" + " Fitness: " + str(new_avg_fitness))
    while (abs(new_avg_fitness - pvs_avg_fitness) > 0.001):          
        new_generation = []
        
        # Elitism, i.e, 10% of fittest population sent to next gen
        size = int(0.1 * POPULATION_SIZE)
        for i in range(size):
            new_generation.append(population[i])
        # Rest 90% formed by mating amongst the fittest 50%
        size = int(0.9 * POPULATION_SIZE)
        for i in range(size):
            r = random.randint(0,POPULATION_SIZE/2)
            parent1 = population[r]
            r = random.randint(0,POPULATION_SIZE/2)
            parent2 = population[r]
            new_generation.append(crossover(parent1, parent2))
        population = new_generation
        pvs_avg_fitness = new_avg_fitness
        population.sort()
        new_avg_fitness = find_population_fitness(population)
        generation += 1
        print("Generation: " + str(generation) + " Fitness: " + str(new_avg_fitness))
    print("Solution chromosome: ")
    print(population[0].chromosome)
    plot1 = plt.figure(1)
    plt.plot(fitness)
    plt.xlabel('Generation') 
    plt.ylabel('Fitness')  
    plt.title('Graph Showing Fitness Of the Solution Over Different Generations') 
    plot2 = plt.figure(2)
    plt.plot(cost)
    plt.xlabel('Generation') 
    plt.ylabel('Cost')  
    plt.title('Graph Showing the Cost Of Transportation Over Different Generations') 
    plot3 = plt.figure(3)
    plt.plot(time)
    plt.xlabel('Generation') 
    plt.ylabel('Time')  
    plt.title('Graph Showing the Time Needed For Transportation Over Different Generations') 
    plt.show()

run_ga()