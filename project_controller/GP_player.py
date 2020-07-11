import sys, os
sys.path.insert(0, 'evoman')
from environment import Environment
from  random import choice,randrange,random
import copy
# imports other libs
import numpy as np
from GP_controller import player_controller

experiment_name = 'GP_agent_demo'
if not os.path.exists(experiment_name):
    os.makedirs(experiment_name)


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

    def mutation(self):
        rng = random.random()
        inputs = [i for i in range(1, 21)]
        if rng < 0.9:
            node = generate_random_tree(2)
        elif 0.8 < rng <= 0.9:
            node = random.choics(inputs)

    def crossover(self, node):
        node2 = copy.deepcopy(node)
        self.data = node2.data
        self.leftchild = node2.leftchild
        self.rightchild = node2.rightchild

def print_tree(node ,i = 0):
    # print('node data is ', node.data)
    array_lvl2 = []
    array=[node.data]
    print(i*'    ', 'LVL ', i)
    print(i * '    ', array)
    if node.leftchild is not None :
        array_lvl2 += [print_tree(node.leftchild , i+1)]
    if node.rightchild is not None :
        array_lvl2 += [print_tree(node.rightchild , i+1)]
    array += array_lvl2

def copytree(tree):
    newtree = Node()
    newtree.data = tree.data
    if tree.rightchild != None:
        newtree.rightchild = copytree(tree.rightchild)
    if tree.leftchild != None:
        newtree.leftchild = copytree(tree.lefthchild)
    return newtree

def generate_random_tree(depth,operator='math',proba=25):
    #node pool
    #the first set of operators "bool" requires to take the inputs as logical condition : ex if input is triggered (input !=0) then do X
    if operator=="bool":
        and_node = Node('&&')
        or_node = Node('||')
        xor_node = Node('^')
        nodes = [and_node, or_node, xor_node]
    #the inputs are in form of integer which means that they can be compared to each other and to numerical number
    #with math operator we can check inputs value by comparing them to number or each other.
    else :
        sup_node = Node('>')
        inf_node = Node('<')
        infeq_node = Node('<=')
        supeq_node = Node('>=')
        eq_node = Node ('=')
        dif_node = Node('!=')
        #tresh1_node = Node('sigma')
        nodes = [sup_node,inf_node,infeq_node,supeq_node,eq_node,dif_node]#,tresh1_node]
        numerical_nodes = [-100,-50,0,50,100]
    inputs =[i for i in range(1,21)]
    #add the input as ints which will serve as index to take from the real inputs array taken from the sensors.
    node2copy = choice(nodes)
    parent_node = copy.deepcopy(node2copy)
    p1,p2=randrange(0,100),randrange(0,100)
    #probability to have arbitrary number comparaison in the tree
    if depth-1==0:
        if p1 > proba:
            parent_node.leftchild = Node(choice(inputs))
        else :
            parent_node.leftchild = Node(choice(numerical_nodes))
        if p2 > proba:
            parent_node.rightchild = Node(choice(numerical_nodes))
        else :
            parent_node.rightchild = Node(choice(inputs))
    else:
        parent_node.rightchild = generate_random_tree(depth - 1)
        parent_node.leftchild = generate_random_tree(depth - 1)
    return parent_node

def generation(population):
    newgeneration= Population(population)
    return newgeneration

class Agent(Node):
    def __init__(self,playerorenemy,fitness=0):
        if playerorenemy == True:
            self.trees = [generate_random_tree(4),
                   generate_random_tree(4),
                   generate_random_tree(4),
                   generate_random_tree(4),
                   generate_random_tree(4)]
        else:
            self.trees=[generate_random_tree(4),
                   generate_random_tree(4),
                   generate_random_tree(4),
                   generate_random_tree(4)]
        self.fitness=fitness

    def toArray(self):
        return np.array([self.trees,self.fitness])

    def get_fitness(self):
        return self.fitness
    def set_fitness(self,new_fitness):
        self.fitness=new_fitness

class Population:
    def __init__(self,
                 pop_number=5,
                 survivor=0.2,
                 player=True,
                 gen_number=2,
                 max_depth=1000,
                 max_split=500
                 #,pop=[]
                 ):
        #number of entity in the pop
        self.pop_number = pop_number
        #number of surviving entity each epoch
        self.survivor = survivor
        #boolean to change how th tree is parsed/treated
        self.player = player
        #generation number to look how time the algorithm ran
        self.gen_number = gen_number
        #max depth and max width of the tree to stop it from going overboar
        self.max_depth = max_depth
        self.max_split = max_split
        #array stocking the agents trees
        self.agents=np.array([])
        for i in range(pop_number):
            newagent = Agent(playerorenemy=self.player)
            # self.agents = self.agents.append(newagent.toArray())
            # self.agents = self.agents.append(newagent)
            self.agents = np.append(self.agents, newagent)
    #
    # def champion(self):
    #     self.agents *= -1
    #     self.agents = -self.agents[self.agents[:, 1].argsort()]
    #     return(self.agents[:self.pop_number//self.survivor])


population = Population()
envs=[]
#for each agent an environment needs to be created to run an instance of the game
for i in range(population.pop_number):
    env = Environment(experiment_name=experiment_name,
                      #playermode="ai",
                      player_controller=player_controller(population.agents[i]),
                      speed="fastest",
                    # multiplemode="yes",
                      enemymode="static",
                      # inputcoded="yes"
                      level=2
                      )
    envs.append(env)

# loop to fight each enemies
for g in range(1,population.gen_number):
    for en in range(1, 9):
        # loop on the whole population
        for i in range(population.pop_number):
            envs[i].update_parameter('enemies', [en])
            #print_tree(population.agents[i].trees[0])
            #print(pars_tree(population.agents[i].trees[1]))
            envs[i].play()
            #print(envs[i].fitness_single())
            population.agents[i].fitness=envs[i].fitness_single()
            # print('\n saved ' + str(en) + ' \n')
    #population.gen_number += 1
    #new gen : calculate champion, reset fitness, reproduce with mutation and crossover





