##GP based agent
from controller import Controller
from sensors import sensors
from  random import *
import copy

class player_Controller(Controller):
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
        #a tree for  each action to decide.
        pop[i]=[generate_random_tree(4),generate_random_tree(4),generate_random_tree(4),generate_random_tree(4),generate_random_tree(4)]

    ###loop on pop


    #####fitness function
    for i in range(0,pop_number):
        #import fitness function from the given problem


    #####population variation.
    ###crossover : tree1, tree2, node1, node2.
    ###mutation with random element.
    ###reproduction: taking the X tree  and copy paste.

    def controls(self,inputs,Controller):
        left,right,jump,shoot,release=0,0,0,0,0
        return [left, right, jump, shoot, release]

class enemy_controller(Controller):
    def controls(self,inputs,Controller):
        attack1,attack2,attack3,attack4=0,0,0,0
        return [attack1, attack2, attack3, attack4]



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
        inputs = sensors
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
        tresh1_node = Node('sigma')
        nodes = [sup_node,inf_node,infeq_node,supeq_node,eq_node,dif_node,tresh1_node]
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



##mathematical expression operator < > <

##boolean expression
def pars_tree_bool(node):
    if node.leftchild == None or node.rightchild == None:
        return node.data
    else:
        if node.data == "&&":
            return pars_tree_bool(node.leftchild) and pars_tree_bool(node.rightchild)
        if node.data == "||":
            return pars_tree_bool(node.leftchild) or pars_tree_bool(node.rightchild)
        if node.data == "^":
            return pars_tree_bool(node.leftchild) ^ pars_tree_bool(node.rightchild)

def pars_tree(node):
    if node.leftchild == None or node.rightchild == None:
        return node.data
    else:
        #go for a switch case  here
        if node.data == '<':
            return pars_tree(node.leftchild) < pars_tree_bool(node.rightchild)
        if node.data == '>':
            return pars_tree(node.leftchild) > pars_tree_bool(node.rightchild)
        if node.data == '<=':
            return pars_tree(node.leftchild) <= pars_tree_bool(node.rightchild)
        if node.data == '>=':
            return pars_tree(node.leftchild) >= pars_tree_bool(node.rightchild)
