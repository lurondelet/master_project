##GP based agent
from controller import Controller
from  random import *
import numpy as np
import copy

#from evoman_framework.GP_player import print_tree


class player_controller(Controller):
    def __init__(self, agent):
        self.agent = agent
    # population generation
    # population variation
    # crossover : tree1, tree2, node1, node2.
    # mutation with random element.
    # reproduction: taking the X tree  and copy paste.



    def control(self,  inputs, Controller):

        #print(self.agent.fitness)
        left,  right, jump, shoot, release = 0, 0, 0, 0, 0
        keys = [left, right, jump, shoot, release]
        for i in range(len(self.agent.trees)):
            # print(pars_tree(self.agent.trees[i]))
            refresh_inputs(self.agent.trees[i], inputs)
            if pars_tree(self.agent.trees[i]):
                keys[i] = 1
            else:
                keys[i] = 0

        # print([left, right, jump, shoot, release])
        return keys


class enemy_controller(Controller):
    def __init__(self, agent):
        self.agent = agent

    def control(self, inputs, Controller, population):
        attack1, attack2, attack3, attack4 = 0, 0, 0, 0
        keys = [attack1, attack2, attack3, attack4]
        for i in range(len(self.agent)):
            refresh_inputs(self.agent.trees[i], inputs)
            if pars_tree(self.agent.trees[i]):
                keys[i] = 1
            else:
                keys[i] = 0
        return keys

def print_tree(node ,i = 0):
    # print('node data is ', node.data)
    array_lvl2 = []
    array=[node.data]
    print(i*'    ', 'LVL ', i)
    print(i * '    ', array)
    if node.leftchild is not None :
        array_lvl2 += [print_tree(node.leftchild, i+1)]
    if node.rightchild is not None :
        array_lvl2 += [print_tree(node.rightchild, i+1)]
    array += array_lvl2

def refresh_inputs(node, inputs):
    # print_tree(node)
    if (node.leftchild == None or node.rightchild == None) :
        if 1 < node.data < 20:
            node.data = inputs[node.data]
    else:
        refresh_inputs(node.leftchild, inputs)
        refresh_inputs(node.rightchild, inputs)



##boolean expression
def pars_tree_bool(node):
    #recursion end condition
    if node.leftchild == None or node.rightchild == None:
        return node.data
    else:
        #and node
        if node.data == "&&":
            return pars_tree_bool(node.leftchild) and pars_tree_bool(node.rightchild)
        #or node
        if node.data == "||":
            return pars_tree_bool(node.leftchild) or pars_tree_bool(node.rightchild)
        #Xor node
        if node.data == "^":
            return pars_tree_bool(node.leftchild) ^ pars_tree_bool(node.rightchild)
        #right to left implication
        if node.data == "=>":
            return not pars_tree_bool(node.leftchild) or pars_tree_bool(node.rightchild)
        #left to right implication
        if node.data == "<=":
            return pars_tree_bool(node.leftchild) or not pars_tree_bool(node.rightchild)
        #equivalence
        if node.data == "<=>":
            return (not pars_tree_bool(node.leftchild) or pars_tree_bool(node.rightchild)) and (pars_tree_bool(node.leftchild) or not pars_tree_bool(node.rightchild))

##mathematical expression operator < > <  = !=
def pars_tree(node):
    if node.leftchild is None or node.rightchild is None:
        return node.data
    else:
        if node.data == '<':
            return pars_tree(node.leftchild) < pars_tree(node.rightchild)
        if node.data == '>':
            return pars_tree(node.leftchild) > pars_tree(node.rightchild)
        if node.data == '<=':
            return pars_tree(node.leftchild) <= pars_tree(node.rightchild)
        if node.data == '>=':
            return pars_tree(node.leftchild) >= pars_tree(node.rightchild)
        if node.data == '=':
            return pars_tree(node.leftchild) == pars_tree(node.rightchild)
        if node.data == '!=':
            return pars_tree(node.leftchild) != pars_tree(node.rightchild)
