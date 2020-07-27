import gzip
import pickle
import sys, os
from random import choice, randrange, random
import copy
# imports other libs
import numpy as np

## class ------------------------------------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class Node:
    def __init__(self, data):
        self.data = data
        self.leftchild = None
        self.rightchild = None

    def print_tree(self):
        if self.leftchild:
            self.leftchild.print_tree()
        print(self.data)
        if self.rightchild:
            self.rightchild.print_tree()

    # def mutation(self):
    #     rng = random()
    #     inputs = [i for i in range(1, 21)]
    #     if rng <= 0.1:
    #         add_sub_tree_leaf(self, generate_random_tree(3))
    #     else:
    #         node = choice(inputs)

    def crossover(self, node):
        node2 = copy.deepcopy(node)
        self.data = node2.data
        self.leftchild = node2.leftchild
        self.rightchild = node2.rightchild


class Agent(Node):
    def __init__(self, playerorenemy=True, fitness=0):
        if playerorenemy:
            self.trees = np.array([generate_random_tree(4),
                                   generate_random_tree(4),
                                   generate_random_tree(4),
                                   generate_random_tree(4),
                                   generate_random_tree(4)])
        else:
            self.trees = np.array([generate_random_tree(4),
                                   generate_random_tree(4),
                                   generate_random_tree(4),
                                   generate_random_tree(4)])
        self.fitness = fitness
        self.player = playerorenemy

    def toArray(self):
        return np.array([self.trees, self.fitness])

    def get_fitness(self):
        return self.fitness

    def set_fitness(self, new_fitness):
        self.fitness = new_fitness

    def mutate(self):
        for i in range(len(self.trees)):
            mutation(self.trees[i])

    def rdm_crossover(self):
        for i in range(len(self.trees)):
            rng = randrange(0, len(self.trees))
            # print("RNG", rng)
            # print("CHOSEN", self.trees[rng])
            self.trees[i].crossover(self.trees[rng])

    def inter_crossover(self,agent):
        for i in range(len(self.trees)):
            rng = randrange(0, len(self.trees))
            # print("RNG", rng)
            # print("CHOSEN", self.trees[rng])
            self.trees[i].crossover(agent.trees[rng])

    def __lt__(self, agent):
        return self.fitness < agent.fitness

    def __neg__(self):
        self.fitness *= -1


class Population:
    def __init__(self,
                 pop_number=5,
                 survivor=1,
                 player=True,
                 gen_number=2,
                 max_depth=1000,
                 max_split=500
                 # ,pop=[]
                 ):
        # number of entity in the pop
        self.pop_number = pop_number
        # number of surviving entity each epoch
        self.survivor = survivor
        # boolean to change how th tree is parsed/treated
        self.player = player
        # generation number to look how time the algorithm ran
        self.gen_number = gen_number
        # max depth and max width of the tree to stop it from going overboar
        self.max_depth = max_depth
        self.max_split = max_split
        # array stocking the agents trees
        self.agents = np.array([])
        for i in range(pop_number):
            newagent = Agent(playerorenemy=self.player)
            # self.agents = self.agents.append(newagent.toArray())
            # self.agents = self.agents.append(newagent)
            self.agents = np.append(self.agents, newagent)

    def agenttoarray(self):
        for i in range(len(self.agents)):
            self.agents[i] = self.agents[i].toArray()

    def __neg__(self):
        for i in range(len(self.agents)):
            self.agents[i] *= -1

    def __add__(self, pop):
        self.agents=np.append(self.agents,pop.agents)
        self.pop_number+=pop.pop_number

    # sort function on agents.----------------
    # def champion(self):
    # print("OBJECT FORM",self.agents[0].fitness)
    # self.agenttoarray()
    # print("ARRAY FORM", self.agents.ndim)
    # # for i in self.agents:
    # #     i.toArray()
    # self.agents *= -1
    # self.agents = -self.agents[self.agents[:, 1].argsort()]
    # return self.agents[:self.pop_number//self.survivor]
    def champion(self):
        # fusion sort based on the second element of the agents object of the population
        # for i in range (len(self.agents)):
        #     print(self.agents[i].fitness)
        # print(self.agents)
        # triFusion(self.agents)
        -self.agents
        self.agents.sort()
        -self.agents
        # print(self.agents)
        # return 'done'

    def enemy_champion(self):
        self.agents.sort()

    def fitness_reset(self):
        for i in range(self.pop_number):
            if self.agents[i].player:
                self.agents[i].fitness = 0
            else:
                self.agents[i].fitness = 100

    def new_generation(self, proba_mutation=10):
        # #fitness sort
        # self.agenttoarray()
        # # print(self.agents)
        # self.agents *= -1
        # self.agents = -self.agents[self.agents[:, 1].argsort()]
        # self.agents[:self.pop_number//self.survivor]
        # champions
        if self.player:
            self.champion()
        else:
            self.enemy_champion()
        loop_changed = self.pop_number // self.survivor
        leftover = self.pop_number % self.survivor
        # print("loop changed", loop_changed, "           leftover", leftover)
        new_generation = np.array([])
        # print("new generation",new_generation)

        if loop_changed >= 1:
            # print(loop_changed)
            for i in range(loop_changed):
                # print("looped---------------------------------------------------------", loop_changed)
                survivor_copy = np.array(copy.deepcopy(self.agents[:self.survivor]))
                # print("survivor", survivor_copy)
                new_generation = np.append(new_generation, survivor_copy)
                # print("IN LOOP                              ", new_generation)

        # print("NEW GENERATION in loop : ===========================",len(new_generation))
        if leftover > 0:
            new_generation = np.append(new_generation, copy.deepcopy(self.agents[:leftover]))
            # print("leftoooooooooooooooooover--------------------------------------", leftover)
        rng = randrange(0, 100)

        # print("NEW GENERATION b4mute : ===========================",len(new_generation))
        for i in range(self.pop_number - self.survivor):
            if 0 < rng < proba_mutation:
                new_generation[self.survivor + i].mutate()
            elif proba_mutation <= rng < 2*proba_mutation:
                # print('SLLLLLLLLLLLICE',self.survivor+i)
                new_generation[self.survivor + i].rdm_crossover()
            elif 2*proba_mutation <= rng < 3*proba_mutation:
                new_generation[self.survivor + i].inter_crossover(new_generation[i])
        # print("NEW GENERATION : ===========================",len(new_generation))

        self.fitness_reset()
        self.agents = new_generation
        fail_safe(self)



## class end --------------------------------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

## function ---------------------------------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def mutation(node):
    rng = random()
    inputs = [i for i in range(1, 21)]
    if rng <= 0.5:
        add_sub_tree_leaf(node, generate_random_tree(3))
    else:
        node = choice(inputs)

def add_sub_tree_leaf(node,subtree):
    rng = randrange(2)
    # print_tree(node)
    if node.leftchild is not None and rng:
        add_sub_tree_leaf(node.leftchild, subtree)
    if node.rightchild is not None and not rng:
        add_sub_tree_leaf(node.rightchild, subtree)
    if node.leftchild is None and node.rightchild is None :
        node.data = generate_random_tree(1).data
        if rng:
            node.leftchild = subtree
        else:
            node.rightchild = subtree

def print_tree(node, i=0):
    # print('node data is ', node.data)
    array_lvl2 = []
    array = [node.data]
    print(i * '    ', 'LVL ', i)
    print(i * '    ', array)
    if node.leftchild is not None:
        array_lvl2 += [print_tree(node.leftchild, i + 1)]
    if node.rightchild is not None:
        array_lvl2 += [print_tree(node.rightchild, i + 1)]
    array += array_lvl2

def generate_random_tree(depth, operator='math', proba=25):
    # node pool
    # the first set of operators "bool" requires to take the inputs as logical condition :
    # pool of logical operator
    and_node = Node('&&')
    or_node = Node('||')
    xor_node = Node('^')
    imp_rl = Node('=>')
    imp_lr = Node('<=')
    equi = Node("<=>")
    nodes_logi = [and_node, or_node, xor_node, imp_lr, imp_rl, equi]
    # pool of mathematical operator
    sup_node = Node('>')
    inf_node = Node('<')
    infeq_node = Node('<=')
    supeq_node = Node('>=')
    eq_node = Node('=')
    dif_node = Node('!=')
    nodes_math = [sup_node, inf_node, infeq_node, supeq_node, eq_node, dif_node]  # ,tresh1_node]
    #pool of numerical value for the leaves node
    numerical_nodes = [-100, -50, 0, 50, 100]
    inputs = [i for i in range(1, 21)]
    #copy of the random node
    pool = nodes_math+nodes_logi
    node2copy = choice(pool)
    parent_node = copy.deepcopy(node2copy)
    p1, p2 = randrange(0, 100), randrange(0, 100)

    # probability to have arbitrary number comparaison in the tree
    if depth - 1 == 0:
        if p1 > proba:
            parent_node.leftchild = Node(choice(inputs))
        else:
            parent_node.leftchild = Node(choice(numerical_nodes))
        if p2 > proba:
            parent_node.rightchild = Node(choice(numerical_nodes))
        else:
            parent_node.rightchild = Node(choice(inputs))

    #mathematical comparaison
    elif depth - 2 == 0:
        parent_node.data = choice(nodes_math).data
        parent_node.rightchild = generate_random_tree(depth - 1)
        parent_node.leftchild = generate_random_tree(depth - 1)
    else:
        parent_node.rightchild = generate_random_tree(depth - 1)
        parent_node.leftchild = generate_random_tree(depth - 1)
    return parent_node



def correct_tree(node):
    if node.leftchild is not None and node.rightchild is None:
        node.rightchild = generate_random_tree(2)
        return False
    elif node.leftchild is None and node.rightchild is not None:
        node.leftchild = generate_random_tree(2)
        return False
    elif node.leftchild is None and node.rightchild is None:
        return True
    else:
        if correct_tree(node.leftchild) == False or correct_tree(node.rightchild) == False:
            return False
        else:
            return True


def fail_safe(population):
    for i in range(len(population.agents)):
        for j in range(len(population.agents[i].trees)):
            correct_tree(population.agents[i].trees[j])

def export_population(population, experiment_name):
    file = gzip.open(experiment_name + '/GP_solution', 'w', compresslevel=5)
    pickle.dump(population, file, protocol=2)
    file.close()


def load_population(experiment_name):
    file = gzip.open(experiment_name + '/GP_solution')
    pop = pickle.load(file, encoding='latin1')
    return pop

# a = Agent()
# for i in range(100):
#     a.mutate()
# print_tree(a.trees[0])


