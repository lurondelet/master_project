##GP based agent
from controller import Controller
from sensors import sensors
from  random import *
import copy

class Ma_Player_Controller:
    ###parameters
    #number of pop; survivor number(fraction).
    pop_number = 25
    survivor = 50
    pop=[]
    #fitness function number.
    fitness_number = 1
    #number of generation until stop.
    gen_number = 30
    #max depth and max split. for optimisation purpose.
    max_depth = 1000
    max_split = 500

    #####population generation
    ###first generation:
    #tree generation :
    for i in range(0, pop_number):
        pop[i]=[generate_random_tree(4),generate_random_tree(4),generate_random_tree(4),generate_random_tree(4)]

    ###loop on pop


    #####fitness function
    for i in range(0,pop_number):



    #####population variation.
    ###crossover : tree1, tree2, node1, node2.
    ###mutation with random element.
    ###reproduction: taking the X tree  and copy paste.



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

    def mutate(self):
        rng = random.random()
        inputs = sensors
        if (rng < 0.9):
            node = generate_random_tree(2)
        elif (rng > 0.8 and rng <= 0.9):
            node = random.choics(inputs)
    def crossovered(self,node):
        node2=copy.deepcopy(node)
        self.data=node2.data
        self.leftchild=node2.leftchild
        self.rightchild=node2.rightchild

def generate_random_tree(depth):
    #random  pool
    and_node = Node('&&')
    or_node = Node('||')
    xor_node = Node('^')
    nodes = [and_node, or_node, xor_node]
    inputs = sensors

    parent_node = copy.deepcopy(random.choices(nodes))

    if(depth-1==0):
        parent_node.leftchild = Node(random.choices(inputs))
        parent_node.rightchild = Node(random.choices(inputs))
    else:
        parent_node.rightchild = generate_random_tree(depth - 1)
        parent_node.leftchild = generate_random_tree(depth - 1)
    return(parent_node)

def pars_tree(node):
    if(node.leftchild==None or node.rightchild==None):
        return node.data
    else:
        if node.data == "&&":
            return pars_tree(node.leftchild) and pars_tree(node.rightchild)
        if node.data == "||":
            return pars_tree(node.leftchild) or pars_tree(node.rightchild)
        if node.data == "^":
            return pars_tree(node.leftchild) ^ pars_tree(node.rightchild)