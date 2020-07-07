##GP based agent
from controller import Controller
from sensors import sensors
from  random import *
import copy

class player_Controller(Controller):
    def __init__(self,pop_number=25,survivor=50 , fitness_number=1 , gen_number=30 , max_depth = 1000 , max_split = 500):
        self.pop_number=pop_number
        ###parameters
        #number of pop; survivor number(fraction).
        self.survivor=survivor
        #pop=[]
        #fitness function number.
        self.fitness_number=fitness_number
        #number of generation until stop.
        self.gen_number = gen_number
        #max depth and max split. for optimisation purpose.
        self.max_depth = max_depth
        self.max_split=max_split
    #####population generation



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
        if node.data == '=':
            return pars_tree(node.leftchild) == pars_tree(node.rightchild)
        if node.data == '!=':
            return pars_tree(node.leftchild) != pars_tree(node.rightchild)
