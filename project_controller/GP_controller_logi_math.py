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

    def control(self, inputs, Controller):
        attack1, attack2, attack3, attack4 = 0, 0, 0, 0
        keys = [attack1, attack2, attack3, attack4]
        for i in range(len(self.agent.trees)):
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
    if (node.leftchild == None and node.rightchild == None) :
        if 1 < node.data < 20:
            node.data = inputs[node.data]
    else:
        if node.leftchild != None:
            refresh_inputs(node.leftchild, inputs)
        if node.rightchild!= None:
            refresh_inputs(node.rightchild, inputs)


##mathematical expression operator < > <  = != + logical
def pars_tree(node):
    if node.leftchild is None or node.rightchild is None:
        return node.data
    else:
        #inf node
        if node.data == '<':
            return pars_tree(node.leftchild) < pars_tree(node.rightchild)
        #superior node
        if node.data == '>':
            return pars_tree(node.leftchild) > pars_tree(node.rightchild)
        #inf  or equal node
        if node.data == '<=':
            return pars_tree(node.leftchild) <= pars_tree(node.rightchild)
        #sup or equal node
        if node.data == '>=':
            return pars_tree(node.leftchild) >= pars_tree(node.rightchild)
        #equal node
        if node.data == '=':
            return pars_tree(node.leftchild) == pars_tree(node.rightchild)
        #not equal node
        if node.data == '!=':
            return pars_tree(node.leftchild) != pars_tree(node.rightchild)
        #and node
        if node.data == "&&":
            return pars_tree(node.leftchild) and pars_tree(node.rightchild)
        #or node
        if node.data == "||":
            return pars_tree(node.leftchild) or pars_tree(node.rightchild)
        #Xor node
        if node.data == "^":
            return pars_tree(node.leftchild) or pars_tree(node.rightchild)
        #right to left implication
        if node.data == "=>":
            return not pars_tree(node.leftchild) or pars_tree(node.rightchild)
        #left to right implication
        if node.data == "<=":
            return pars_tree(node.leftchild) or not pars_tree(node.rightchild)
        #equivalence
        if node.data == "<=>":
            return (not pars_tree(node.leftchild) or pars_tree(node.rightchild)) and (pars_tree(node.leftchild) or not pars_tree(node.rightchild))

