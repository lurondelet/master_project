import gzip
import pickle
import sys, os
from random import choice, randrange, random
import copy
# imports other libs
import numpy as np

## class ------------------------------------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
            rng_mutation = randrange(0, 100)
            if rng_mutation > 60:
                mutation(self.trees[i])

    def rdm_crossover(self):
        for i in range(len(self.trees)):
            rng_crossover = randrange(0, 100)
            if rng_crossover > 60:
                rng = randrange(0, len(self.trees))
                # print("RNG", rng)
                # print("CHOSEN", self.trees[rng])
                self.trees[i].crossover(self.trees[rng])

    def inter_crossover(self, agent):
        for i in range(len(self.trees)):
            #change the behavior of 2t rees out of 5
            rng_changing_tree = randrange(0,100)
            if rng_changing_tree<40:
                depth_parent_1 = find_depth(self.trees[i])
                depth_parent_2 = find_depth(agent.trees[i])

                rng = randrange(1, 1+depth_parent_2//3)
                agent2 = copy.deepcopy(find_depth_tree(agent.trees[i], 0, depth_parent_1-rng))
                rng_changed = randrange(0,3)
                find_depth_tree(self.trees[i],0,find_depth(self.trees[i])-rng_changed)

    def __lt__(self, agent):
        return self.fitness < agent.fitness

    def __gt__(self, agent):
        return self.fitness > agent.fitness

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

    def __add__(self, pop):
        self.agents=np.append(self.agents,pop.agents)
        self.pop_number+=pop.pop_number

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
                self.agents[i].fitness = 0
            else:
                self.agents[i].fitness = 100

    def new_generation(self, proba_mutation=33):
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
            elif 2*proba_mutation <= rng < 3*proba_mutation:
                new_generation[self.survivor + i].inter_crossover(new_generation[i])
        # print("NEW GENERATION : ===========================",len(new_generation))

        self.agents = new_generation
        self.fitness_reset()
        fail_safe(self)

    def generation(self,proba=1):
        if proba:
            proba=self.survivor
        if self.player:
            self.champion()
        else:
            self.enemy_champion()
        #copy pop_number-survivor to new gene
        generation = np.array(copy.deepcopy(self.agents))
        survivor_copy = np.array(copy.deepcopy(self.agents[:self.survivor]))
        #tournament for crossover:
        for it in range(self.survivor):
            #select the 2 parents
            agent_to_cross = tournament_selection(self.agents, 2)
            agent = copy.deepcopy(agent_to_cross[0])
            agent.inter_crossover(agent_to_cross[1])
            agent.fitness = (agent_to_cross[0].fitness+agent_to_cross[1].fitness)/2
            #rng for mutation
            rng = randrange(0, 100)
            #mutation of the children
            if rng < proba:
                agent.mutate()
            generation = np.append(generation, agent)
        #select 100 agent with tournament for new generation
        new_gen = np.array(tournament_selection(generation, self.pop_number))
        gen = np.append(new_gen[self.survivor:], survivor_copy)

        self.agents = gen
        self.fitness_reset()
        fail_safe(self)

    def survivor_cut(self):
        new_population = Population(
            pop_number=self.survivor,
            survivor=1,
            gen_number=self.gen_number
        )
        new_population.agents = np.array(copy.deepcopy(self.agents[:self.survivor]))
        return new_population

## class end --------------------------------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

## function ---------------------------------------- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def mutation(node):
    rng = random()
    inputs = [i for i in range(1, 21)]
    if rng <= 0.5:
        add_sub_tree_leaf(node, generate_random_tree(3))
    else:
        node = choice(inputs)


def add_sub_tree_leaf(node,subtree):
    rng = randrange(2)
    # print_tree(node)
    if node.leftchild is not None and rng:
        add_sub_tree_leaf(node.leftchild, subtree)
    if node.rightchild is not None and not rng:
        add_sub_tree_leaf(node.rightchild, subtree)
    if node.leftchild is None and node.rightchild is None :
        node.data = generate_random_tree(1).data
        if rng:
            node.leftchild = subtree
        else:
            node.rightchild = subtree


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


def generate_random_tree(depth, operator='math', proba=25):
    # node pool
    # the first set of operators "bool" requires to take the inputs as logical condition :
    # pool of logical operator
    and_node = Node('&&')
    or_node = Node('||')
    xor_node = Node('^')
    imp_rl = Node('=>')
    imp_lr = Node('<=')
    equi = Node("<=>")
    nodes_logi = [and_node, or_node, xor_node, imp_lr, imp_rl, equi]
    # pool of mathematical operator
    sup_node = Node('>')
    inf_node = Node('<')
    infeq_node = Node('<=')
    supeq_node = Node('>=')
    eq_node = Node('=')
    dif_node = Node('!=')
    nodes_math = [sup_node, inf_node, infeq_node, supeq_node, eq_node, dif_node]  # ,tresh1_node]
    #pool of numerical value for the leaves node
    numerical_nodes = [-100, -50, 0, 50, 100]
    inputs = [i for i in range(1, 21)]
    #copy of the random node
    pool = nodes_math+nodes_logi
    node2copy = choice(pool)
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

    #mathematical comparaison
    elif depth - 2 == 0:
        parent_node.data = choice(nodes_math).data
        parent_node.rightchild = generate_random_tree(depth - 1)
        parent_node.leftchild = generate_random_tree(depth - 1)
    else:
        parent_node.rightchild = generate_random_tree(depth - 1)
        parent_node.leftchild = generate_random_tree(depth - 1)
    return parent_node


def correct_tree(node):
    if node.leftchild is not None and node.rightchild is None:
        node.rightchild = generate_random_tree(2)
        return False
    elif node.leftchild is None and node.rightchild is not None:
        node.leftchild = generate_random_tree(2)
        return False
    elif node.leftchild is None and node.rightchild is None:
        return True
    else:
        if correct_tree(node.leftchild) == False or correct_tree(node.rightchild) == False:
            return False
        else:
            return True


def fail_safe(population):
    for i in range(len(population.agents)):
        for j in range(len(population.agents[i].trees)):
            correct_tree(population.agents[i].trees[j])


def tournament_selection(agents, number, p=1):
    selected = []
    selected_index=[]
    #generate reference array
    agentindex = [i for i in range(len(agents))]

    #compute the ideal cluster used for the
    if len(agents)//10 > 3:
        cluster = len(agents)//10
    else:
        cluster = 2

    #loop of tournament
    for it in range(number):

        # probability array
        proba_array = []
        for i in range(len(agents)):
            proba_array += [len(agents)-i for j in range(i)]

        #remove already selected agent
        for s in range(len(selected_index)):
            proba_array = list(filter(lambda a: a != selected_index[s], proba_array))

        #generate tournament array
        tournament_array = []
        # print('proba_array--------------')
        # print(proba_array)
        for i in range(cluster):
            #select a random element to add to the cluster
            index = choice(proba_array)
            tournament_array.append(index)
        #convert index to agent
        # print('cluster-------------')
        tournament_array_agent = []
        # print(tournament_array)
        for n in range(len(tournament_array)):
            tournament_array_agent += [copy.deepcopy(agents[tournament_array[n]])]
        #sort the tree to be able to select the best
        tournament_array.sort()

        tournament_array_agent.sort(reverse=True)
        # tournament_array_agent.sort(reverse=True)
        #append the winner to the selected array
        selected.append(tournament_array_agent[0])
        #adds the selected index to the index to be sure not to be able to pick it up again
        selected_index.append(tournament_array[0])
    # print('selected index --------------------------')
    # print(selected_index)
    # print('selected ---------------------------------------------nique')
    # print(selected)
    return selected

def load_population(experiment_name, enemy=False, display=False):

    if enemy:
        file = gzip.open(experiment_name +'/GP_solution_enemy')
    else:
        file = gzip.open(experiment_name + '/GP_solution' )
    pop = pickle.load(file, encoding='latin1')
    print('pop_number--------------------', pop.pop_number)
    print('survivor-----------', pop.survivor)
    print('gen-----------', pop.gen_number)
    if display:
        check_pop(pop)
    return pop

def print_pop(population):
    for i in range(population.survivor):
        for j in range(len(population.agents[0].trees)):
            print_tree(population.agents[i].trees[j])
            print("---------------------------------------", i, "-----------------------")

def check_pop(population):
    print_tree(population.agents[0].trees[0])
    print_tree(population.agents[1].trees[0])


def print_agent(agent):
    print(agent.fitness)

def find_depth_tree(node,i=0,goal=0):
    rng = randrange(0,2)
    if i == goal or (node.leftchild is None and node.rightchild is None):
        return node
    if node.leftchild is not None and rng:
        return find_depth_tree(node.leftchild, i + 1, goal)
    if node.rightchild is not None and rng == False :
        return find_depth_tree(node.rightchild, i + 1, goal)

def find_depth(node,i=0):
    if node.leftchild is None and node.rightchild is None:
        return i
    if node.leftchild is not None:
        return find_depth(node.leftchild, i + 1)
    if node.rightchild is not None:
        return find_depth(node.rightchild, i + 1)

# pop = load_population('GP_PLAYER_TEST_co')
# ar = tournament_selection(pop.agents,10,1)
# print(len(ar))

# a = Agent()
# for i in range(100):
#     a.mutate()
# print_tree(a.trees[0])
# print(find_depth(a.trees[0]))
# print('test1')
# print_tree(find_depth_tree(a.trees[0],0,1))
# print('test2')
# print_tree(find_depth_tree(a.trees[0],0,2))
# print('test3')
# print_tree(find_depth_tree(a.trees[0],0,3))


# a=Population(10,2,True,2)
# a.generation()
# for i in range(len(a.agents)):
#     a.agents[i].fitness=randrange(100)
#     print(a.agents[i].fitness)
# a.champion()
# print('-------------------------')
# for i in range(len(a.agents)):
#     print('--')
#     print(a.agents[i].fitness)
#     a.fitness_reset()
#     print(a.agents[i].fitness)
#     print('---')