import sys, os
sys.path.insert(0, 'evoman')
from environment import Environment
from GP_controller import player_controller
from  random import *
import copy
# imports other libs
import numpy as np

experiment_name = 'GP_agent_demo_1'
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
        inputs =[i for i in range(1,21)]
        if (rng < 0.9):
            node = generate_random_tree(2)
        elif (rng > 0.8 and rng <= 0.9):
            node = random.choics(inputs)

    def crossover(self,node):
        node2=copy.deepcopy(node)
        self.data=node2.data
        self.leftchild=node2.leftchild
        self.rightchild=node2.rightchild

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

    parent_node = copy.deepcopy(random.choices(nodes))
    p1,p2=randrange(0,100),randrange(0,100)
    #probability to have arbitrary number comparaison in the tree
    if depth-1==0:
        if p1 < proba:
            parent_node.leftchild = Node(random.choices(inputs))
        else :
            parent_node.leftchild = Node(random.choice(numerical_nodes))
        if p2 < proba:
            parent_node.rightchild = Node(random.choice(numerical_nodes))
        else :
            parent_node.rightchild = Node(random.choices(inputs))
    else:
        parent_node.rightchild = generate_random_tree(depth - 1)
        parent_node.leftchild = generate_random_tree(depth - 1)
    return parent_node

class agent(Node):
    def __init__(self,playerorenemy):
        if playerorenemy == True:
            self.trees=[generate_random_tree(4),
                   generate_random_tree(4),
                   generate_random_tree(4),
                   generate_random_tree(4),
                   generate_random_tree(4),
                   generate_random_tree(4)]
        else:
            self.trees=[generate_random_tree(4),
                   generate_random_tree(4),
                   generate_random_tree(4),
                   generate_random_tree(4)]
        self.fitness=0


class Population:
    def __init__(self,
                 pop_number=25,
                 survivor=50,
                 fitness_number=1,
                 gen_number=30,
                 max_depth=1000,
                 max_split=500
                 #,pop=[]
                 ):
        self.pop_number = pop_number
        self.survivor = survivor
        self.fitness_number = fitness_number
        self.gen_number = gen_number
        self.max_depth = max_depth
        self.max_split = max_split
        #self.pop = pop


    # import fitness function from the given problem


agents = Population()
envs=[]
for i in range(agents.pop_number):
    env=Environment(experiment_name=experiment_name,
                      playermode="ai",
                      player_controller=player_controller(),
                      speed="fastest",
                      enemymode="static",
                      # inputcoded="yes"
                      level=2
                      )
    envs.append(env)

# initializes environment with ai player using random controller, playing against static enemy
#env = Environment(experiment_name=experiment_name)



for en in range (1,9):
    # Update the enemy
    for i in range(agents.pop_number):
        envs[i].update_parameter('enemies', [en])
        #calcul de la fitness ici : avec l'environement
        envs[i].play()
        agents[i]=envs.fitness_single()
        print('\n saved ' + str(en) + ' \n')



