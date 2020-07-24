import gzip
import pickle
import sys, os

sys.path.insert(0, 'evoman')
from environment import Environment
from random import choice, randrange, random
import copy
# imports other libs
import numpy as np
from GP_controller import player_controller, enemy_controller

experiment_name = 'GP_agent_24_july_test'
if not os.path.exists(experiment_name):
    os.makedirs(experiment_name)

sys.path.append(experiment_name)


# ##------------------------------------------------------- class starts

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

def mutation(node):
    rng = random()
    inputs = [i for i in range(1, 21)]
    if rng <= 0.5:
        add_sub_tree_leaf(node, generate_random_tree(3))
    else:
        node = choice(inputs)

def add_sub_tree_leaf(node,subtree):
    rng = randrange(2)
    if node.leftchild is not None and rng:
        add_sub_tree_leaf(node.leftchild, subtree)
    if node.rightchild is not None and not rng:
        add_sub_tree_leaf(node.leftchild, subtree)
    if node.leftchild is None and node.rightchild is None :
        node.data = generate_random_tree(1).data
        if rng:
            node.leftchild=subtree
        else:
            node.rightchild=subtree

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


# def copytree(tree):
#     newtree = Node()
#     newtree.data = tree.data
#     if tree.rightchild != None:
#         newtree.rightchild = copytree(tree.rightchild)
#     if tree.leftchild != None:
#         newtree.leftchild = copytree(tree.lefthchild)
#     return newtree


def generate_random_tree(depth, operator='math', proba=25):
    # node pool
    # the first set of operators "bool" requires to take the inputs as logical condition :
    # ex if input is triggered (input !=0) then do X
    if operator == "bool":
        and_node = Node('&&')
        or_node = Node('||')
        xor_node = Node('^')
        imp_rl = Node('=>')
        imp_lr = Node('<=')
        equi = Node("<=>")
        nodes = [and_node, or_node, xor_node, imp_lr, imp_rl, equi]
    # the inputs are in form of integer which means that they can be compared to each other and to numerical number
    # with math operator we can check inputs value by comparing them to number or each other.
    else:
        sup_node = Node('>')
        inf_node = Node('<')
        infeq_node = Node('<=')
        supeq_node = Node('>=')
        eq_node = Node('=')
        dif_node = Node('!=')
        # tresh1_node = Node('sigma')
        nodes = [sup_node, inf_node, infeq_node, supeq_node, eq_node, dif_node]  # ,tresh1_node]
    numerical_nodes = [-100, -50, 0, 50, 100]
    inputs = [i for i in range(1, 21)]
    # add the input as ints which will serve as index to take from the real inputs array taken from the sensors.
    node2copy = choice(nodes)
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
    else:
        parent_node.rightchild = generate_random_tree(depth - 1)
        parent_node.leftchild = generate_random_tree(depth - 1)
    return parent_node


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
                self.agents[i].fitness=0
            else:
                self.agents[i].fitness=100

    def new_generation(self, proba_mutation=30):
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
            else:
                new_generation[self.survivor + i].inter_crossover(new_generation[i])
        # print("NEW GENERATION : ===========================",len(new_generation))
        self.fitness_reset()
        self.agents = new_generation


# def triFusion(T):
#     # entrée ː un tableau T
#     # sortie ː une permutation triée de T
#     # fonction  triFusion(T[1, …, n])
#     # si  n ≤ 1
#     if len(T) <= 1:
#         #     renvoyer  T
#         return T
#     # sinon
#     else:
#         q = len(T) // 2
#         #     renvoyer  fusion(triFusion(T[1, …, n / 2]), triFusion(T[n / 2 + 1, …, n]))
#         return fuse(triFusion(T[:q]), triFusion(T[q:]))
#
#
# def fuse(A, B):
#     # entrée ː deux tableaux triés  A et  B
#     # sortie: un  tableau  trié   qui  contient exactement   les éléments  des  tableaux A    et   B
#     # fonction    fusion(A[1, …, a], B[1, …, b])
#     # si    A   est  le   tableau    vide
#     # print('LEN A', len(A), 'LEN B', len(B))
#     if len(A) == 0:
#         #     renvoyer     B
#         return B
#     # si B est le tableau vide
#     if len(B) == 0:
#         #     renvoyer A
#         return A
#     # si A[1] ≤ B[1]
#     # print("ITERATION ---------------------------------")
#     #
#     # print("len A =", len(A))
#     # print("A =", A)
#     # print("len B  =", len(B))
#     # print("B =", B)
#     # print("A0 =", A[0])
#     # print("B0 =", B[0])
#     if A[0].fitness <= B[0].fitness:
#         # print('LEN A[:1]', len(A[1:]), 'LEN B', len(B))
#         #     renvoyer    A[1] ⊕ fusion(A[2, …, a], B)
#         return [A[0]] + fuse(A[1:], B)
#     # sinon
#     else:
#         #     renvoyer B[1] ⊕ fusion(A, B[2, …, b])
#         # print('LEN A[:1]', len(A), 'LEN B', len(B[1:]))
#         return [B[0]] + fuse(A, B[1:])

def export_tree(node, expertience_name):
    return True
# ------------------------------------------------------#




# total_pop = 100
# generation = 50
# survivor = 10
#
# population = Population(
#     pop_number=total_pop,
#     survivor=survivor,
#     gen_number=generation)
# # for i in range (len(a.trees)):
# #     print_tree(a.trees[i])
#
# print_tree(population.agents[0].trees[0])
# print("SAVING----------------------------------------------------------------")
# #save------------------------------
# file = gzip.open(experiment_name + '/evoman_solstate', 'w', compresslevel=5)
# pickle.dump(population, file, protocol=2)
# file.close()
# print("CHANGING--------------------------------------------------------------")
# population.agents[0].mutate()
# print_tree(population.agents[0].trees[0])
# print("LOADING--------------------------------------------------------------")
# file = gzip.open(experiment_name + '/evoman_solstate')
# pop2 = pickle.load(file, encoding='latin1')
# # for i in range (len(b.trees)):
# #     print_tree(b.trees[i])
# print_tree(pop2.agents[0].trees[0])
# print("CHANGING FILE--------------------------------------------------------")
# file = gzip.open(experiment_name + '/evoman_solstate', 'w', compresslevel=5)
# pickle.dump(population, file, protocol=2)
# file.close()
# print("LOADING2 -------------------------------------------------------------")
# file = gzip.open(experiment_name + '/evoman_solstate')
# pop3 = pickle.load(file, encoding='latin1')
# print_tree(pop3.agents[0].trees[0])

# ##---------------------------------------------------------program
#param
total_pop = 100
generation = 50
survivor = 10

population = Population(
    pop_number=total_pop,
    survivor=survivor,
    gen_number=generation)
envs = []
enemy_pop = Population(
    pop_number=total_pop,
    survivor=survivor,
    gen_number=generation,
    player=False)
# for each agent an environment needs to be created to run an instance of the game
for i in range(population.pop_number):
    if not os.path.exists(experiment_name + '/' + str(i)):
        os.makedirs(experiment_name + '/' + str(i))

    env = Environment(experiment_name=experiment_name + '/' + str(i),
                      # playermode="ai",
                      player_controller=player_controller(population.agents[i]),
                      speed="fastest",
                      # multiplemode="yes",
                      enemymode="ai",
                      # enemy_controller=enemy_controller(enemy_pop.agents[i]),
                      # inputcoded="yes"
                      level=2
                      )
    envs.append(env)

# loop to fight each enemies
for g in range(0, population.gen_number):
    for en in range(1, 9):
        # loop on the whole population
        for i in range(population.pop_number):
            print_tree(population.agents[i].trees[0])
            envs[i].update_parameter('enemies', [en])
            envs[i].play()
            population.agents[i].fitness += envs[i].fitness_single() / 8
            enemy_pop.agents[i].fitness -= envs[i].fitness_single()/8
    population.new_generation()
    enemy_pop.new_generation()
    # print("LEN AGENTS AFTER NEW GEN",len(population.agents))
    print_tree(population.agents[0].trees[0])
    print("NEW GENERATION --------------------------------------------------------------")
    print(g* ' ',g)
            # print('\n saved ' + str(en) + ' \n')
    # population.gen_number += 1
    # population.new_generation()
    # new gen : calculate champion, reset fitness, reproduce with mutation and crossover

# end------------------------------------------------------
