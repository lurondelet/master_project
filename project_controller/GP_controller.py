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
            print(pars_tree(self.agent.trees[i]))
            if pars_tree(self.agent.trees[i]):
                keys[i] = 1
            else:
                keys[i] = 0

        print([left, right, jump, shoot, release])
        return keys


class enemy_controller(Controller):
    def __init__(self, agent):
        self.agent = agent

    def control(self, inputs, Controller, population):
        attack1, attack2, attack3, attack4 = 0, 0, 0, 0
        keys = [attack1, attack2, attack3, attack4]
        for i in range(len(self.agent)):
            if pars_tree(self.agent.trees[i]):
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
    if node.leftchild is None or node.rightchild is None:
        print(type(node.data)is None)
            # result=0
            # if node.data == '<':
            #     # print('leftchild : \'',node.leftchild.data,'\' INFERIOR ,rightchild : \'',node.rightchild.data,'\'' )
            #     result= pars_tree(node.leftchild) < pars_tree_bool(node.rightchild)
            # if node.data == '>':
            #     # print('leftchild : \'',node.leftchild.data,'\' SUPERIOR rightchild : \'',node.rightchild.data,'\'' )
            #     result= pars_tree(node.leftchild) > pars_tree_bool(node.rightchild)
            # if node.data == '<=':
            #     # print('leftchild : \'',node.leftchild.data,'\' INF,EQUAL rightchild : \'',node.rightchild.data,'\'' )
            #     result = pars_tree(node.leftchild) <= pars_tree_bool(node.rightchild)
            # if node.data == '>=':
            #     # print('leftchild : \'',node.leftchild.data,'\' SUP,EQUAL rightchild : \'',node.rightchild.data,'\'' )
            #     result = pars_tree(node.leftchild) >= pars_tree_bool(node.rightchild)
            # if node.data == '=':
            #     # print('leftchild : \'',node.leftchild.data,'\' EQUAL rightchild : \'',node.rightchild.data,'\'' )
            #     result = pars_tree(node.leftchild) == pars_tree(node.rightchild)
            # if node.data == '!=':
            #     # print('leftchild : \'',node.leftchild.data,'\' INEQUAL rightchild : \'',node.rightchild.data ,'\'')
            #     result = pars_tree(node.leftchild) != pars_tree(node.rightchild)
            #
            # node.data =  result
            # print('CHANGED')

        print('data is',node.data)
        return node.data
    else:
        print('----------NEW ETAPE----------')
        print(node.leftchild.data, ',', node.data, ',', node.rightchild.data)
        # print(type(node.leftchild.data), ',', type(node.data), ',', type(node.rightchild.data))
        print('PARAMETRE DE BASE')
        print(node.data)
        print(node.leftchild.data)
        print(node.rightchild.data)
        if node.data == '<':
            # print('leftchild : \'',node.leftchild.data,'\' INFERIOR ,rightchild : \'',node.rightchild.data,'\'' )
            node.data=pars_tree(node.leftchild) < pars_tree_bool(node.rightchild)
            return pars_tree(node.leftchild) < pars_tree_bool(node.rightchild)
        if node.data == '>':
            # print('leftchild : \'',node.leftchild.data,'\' SUPERIOR rightchild : \'',node.rightchild.data,'\'' )
            node.data=pars_tree(node.leftchild) > pars_tree_bool(node.rightchild)
            return pars_tree(node.leftchild) > pars_tree_bool(node.rightchild)
        if node.data == '<=':
            # print('leftchild : \'',node.leftchild.data,'\' INF,EQUAL rightchild : \'',node.rightchild.data,'\'' )
            node.data=pars_tree(node.leftchild) <= pars_tree_bool(node.rightchild)
            return pars_tree(node.leftchild) <= pars_tree_bool(node.rightchild)
        if node.data == '>=':
            # print('leftchild : \'',node.leftchild.data,'\' SUP,EQUAL rightchild : \'',node.rightchild.data,'\'' )
            node.data=pars_tree(node.leftchild) >= pars_tree_bool(node.rightchild)
            return pars_tree(node.leftchild) >= pars_tree_bool(node.rightchild)
        if node.data == '=':
            # print('leftchild : \'',node.leftchild.data,'\' EQUAL rightchild : \'',node.rightchild.data,'\'' )
            node.data=pars_tree(node.leftchild) == pars_tree_bool(node.rightchild)
            return pars_tree(node.leftchild) == pars_tree(node.rightchild)
        if node.data == '!=':
            # print('leftchild : \'',node.leftchild.data,'\' INEQUAL rightchild : \'',node.rightchild.data ,'\'')
            node.data=pars_tree(node.leftchild) != pars_tree_bool(node.rightchild)
            return pars_tree(node.leftchild) != pars_tree(node.rightchild)
