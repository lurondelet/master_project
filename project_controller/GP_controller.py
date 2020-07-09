##GP based agent
from controller import Controller
from  random import *
import numpy as np
import copy

class player_controller(Controller):
    def __init__(self, agent):
        self.agent = agent
    #  population generation
    # population variation
    # crossover : tree1, tree2, node1, node2.
    # mutation with random element.
    # reproduction: taking the X tree  and copy paste.

    def controls(self,  inputs, Controller, population):

        left,  right, jump, shoot, release = 0, 0, 0, 0, 0
        keys = [left, right, jump, shoot, release]
        for i in range(len(self.agent)):
            if pars_tree(self.agent.trees[i]) > 0.5:
                keys[i] = 1
            else:
                keys[i] = 0
        return keys
class enemy_controller(Controller):
    def __init__(self, agent):
        self.agent = agent

    def controls(self, inputs, Controller, population):
        attack1, attack2, attack3, attack4 = 0, 0, 0, 0
        keys = [attack1, attack2, attack3, attack4]
        for i in range(len(self.agent)):
            if pars_tree(self.agent.trees[i]) > 0.5:
                keys[i] = 1
            else:
                keys[i] = 0
        return keys



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
