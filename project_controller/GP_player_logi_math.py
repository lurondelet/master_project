import gzip
import pickle
import sys, os

sys.path.insert(0, 'evoman')
sys.path.insert(1, 'evoman-framwork/')
from environment import Environment
from random import choice, randrange, random
import copy
# imports other libs
import numpy as np
import argparse
from GP_controller_logi_math import player_controller, enemy_controller
from GP_class import *






experiment_name = 'GP_agent_24_july_test'
if not os.path.exists(experiment_name):
    os.makedirs(experiment_name)

sys.path.append(experiment_name)


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

def export_population(population, experiment_name,enemy=False):
    if enemy:
        file = gzip.open(experiment_name + '/GP_solution_enemy', 'w', compresslevel=5)
    else:
        file = gzip.open(experiment_name + '/GP_solution', 'w', compresslevel=5)
    pickle.dump(population, file, protocol=2)
    file.close()

def load_population(experiment_name,enemy=False,display=False):
    if enemy:
        file = gzip.open(experiment_name + '/GP_solution_enemy')
    else:
        file = gzip.open(experiment_name + '/GP_solution' )
    pop = pickle.load(file, encoding='latin1')
    if display:
        print_pop(pop)
    return pop

def save_build(experiment_name,env,population,enemy_pop):
    #save each
    env.save_state()
    export_population(population, experiment_name)
    export_population(enemy_pop ,experiment_name, True)
    return "done"

def save_build_static(experiment_name,env,population):
    env.save_state()
    export_population(population, experiment_name)
    return "done"

def load_build(experiment_name):
    population = load_population(experiment_name)
    enemy_pop = load_population(experiment_name, True)
    envs = generate_envs(population, experiment_name)
    return [population, enemy_pop, envs]

def generate_envs(population,experiment_name):
    envs = []
    for i in range(population.pop_number):
        if not os.path.exists(experiment_name + '/' + str(i)):
            os.makedirs(experiment_name + '/' + str(i))

        env = Environment(experiment_name=experiment_name + '/' + str(i),
                          playermode="ai",
                          player_controller=player_controller(population.agents[i]),
                          speed="fastest",
                          enemymode="static",
                          # enemy_controller=enemy_controller(enemy_pop.agents[i]),
                          level=2
                          )
        envs.append(env)
    return envs

def generate_envs_with_enemy(population,enemy_pop,experiment_name):
    envs = []
    for i in range(population.pop_number):
        if not os.path.exists(experiment_name + '/' + str(i)):
            os.makedirs(experiment_name + '/' + str(i))

        env = Environment(experiment_name=experiment_name + '/' + str(i),
                          playermode="ai",
                          player_controller=player_controller(population.agents[i]),
                          speed="fastest",
                          # multiplemode="yes",
                          enemymode="ai",
                          enemy_controller=enemy_controller(enemy_pop.agents[i]),
                          # inputcoded="yes"
                          level=2
                          )
        envs.append(env)
    return envs

def run_experiment(population,enemy_pop,envs,experiment_name):
    for g in range(0, population.gen_number):
        for en in range(1, 9):
            # loop on the whole population
            for i in range(population.pop_number):
                # print_tree(population.agents[i].trees[0])
                envs[i].update_parameter('enemies', [en])
                if en <= 6 and envs[i].enemymode == 'static':
                    envs[i].update_parameter('enemymode', 'ai')
                #the seventh and eighth enemies features more than 4 attack  which stops the instances
                if en > 6 and envs[i].enemymode == 'ai':
                    envs[i].update_parameter('enemymode','static')
                envs[i].play()
                population.agents[i].fitness += envs[i].fitness_single() / 8
                enemy_pop.agents[i].fitness -= envs[i].fitness_single() / 8
        population.new_generation()
        enemy_pop.new_generation()
        save_build(population=population,
                   enemy_pop=enemy_pop,
                   env=envs[0],
                   experiment_name=experiment_name)

def run_experiment_static(population,envs,experiment_name):
    for g in range(0, population.gen_number):
        for en in range(1, 9):
            # loop on the whole population
            for i in range(population.pop_number):
                # print_tree(population.agents[i].trees[0])
                envs[i].update_parameter('enemies', [en])
                envs[i].play()
                population.agents[i].fitness += envs[i].fitness_single() / 8
        population.new_generation()
        save_build_static(population=population,
                   env=envs[0],
                   experiment_name=experiment_name)

def new_run(experiment_name,total_pop,generation,survivor):
    #generate the population for the player
    population = Population(
        pop_number=total_pop,
        survivor=survivor,
        gen_number=generation)
    #generate the population for the enemy
    enemy_pop = Population(
        pop_number=total_pop,
        survivor=survivor,
        gen_number=generation,
        player=False)
    # for each agent an environment needs to be created to run an instance of the game
    envs = generate_envs_with_enemy(population, enemy_pop, experiment_name)
    # loop to fight each enemies
    run_experiment(population, enemy_pop, envs, experiment_name)

def new_run_static(experiment_name,total_pop,generation,survivor):
    #generate the population for the player
    population = Population(
        pop_number=total_pop,
        survivor=survivor,
        gen_number=generation)
    #generate the population for the enemy
    # enemy_pop = Population(
    #     pop_number=total_pop,
    #     survivor=survivor,
    #     gen_number=generation,
    #     player=False)
    # for each agent an environment needs to be created to run an instance of the game
    envs = generate_envs(population, experiment_name)
    # loop to fight each enemies
    run_experiment(population, envs, experiment_name)

def run_build(experiment_name):
    [population, enemy_pop, envs] = load_build(experiment_name)
    # print_pop(population)
    run_experiment(population, enemy_pop, envs, experiment_name)

def print_pop(population):
    for i in range(len(population.agents)):
        for j in range(len(population.agents[0].trees)):
            print_tree(population.agents[i].trees[j])
            print("---------------------------------------",i,"-----------------------")

def run_best(experiment_name):
    [population, enemy_pop, envs] = load_build(experiment_name)
    new_pop= Population(
        pop_number=population.survivor,
        survivor=1,
        gen_number=2)
    new_pop.agents=np.array(copy.deepcopy(population.agents[:population.survivor]))
    new_envs=generate_envs(new_pop,'gpXY')
    for en in range(1, 9):
        for i in range(new_pop.pop_number):
            # new_envs[i].update_parameter('enemymode','static')
            new_envs[i].update_parameter('enemies', [en])
            new_envs[i].play()


def correct_tree(node):
    if node.leftchild is not None and node.rightchild is None:
        return False
    elif node.leftchild is None and node.rightchild is not None:
        return False
    elif node.leftchild is None and node.rightchild is None:
        return True
    else:
        if correct_tree(node.leftchild) == False or correct_tree(node.rightchild) == False:
            return False
        else:
            return True


# ------------------------------------------------------#

# new_run('test_load', 1,1, 1)
# pop = load_population('test_load',False,False)
# # print_tree(pop.agents[2].trees[0])
# print(correct_tree(pop.agents[2].trees[0]))
# print('loading behavior --------------------------------------------------')
# # print_tree(pop.agents[2].trees[1])
# print(correct_tree(pop.agents[2].trees[1]))
# print('loading behavior --------------------------------------------------')
# # print_tree(pop.agents[2].trees[2])
# print(correct_tree(pop.agents[2].trees[2]))
# print('loading behavior --------------------------------------------------')
# # print_tree(pop.agents[2].trees[3])
# print(correct_tree(pop.agents[2].trees[3]))
# print('loading behavior --------------------------------------------------')
# # print_tree(pop.agents[2].trees[4])
# print(correct_tree(pop.agents[2].trees[4]))
# print('loading behavior --------------------------------------------------')
# new_run('test_load', 1,1, 1)
# print('loading behavior --------------------------------------------------')
# run_best('gpX')

# working
parser = argparse.ArgumentParser()

parser.add_argument("function",
                    nargs="?",
                    choices=['new_run',"new_run_static", 'run_build', 'run_best'],
                    default='new_run',
                    )
args, sub_args = parser.parse_known_args()

if args.function == "new_run":
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str, help='name of the experience')
    parser.add_argument('tp', type=int, default=10, help='number of agents')
    parser.add_argument('gen', type=int, default=10, help='number of gene')
    parser.add_argument('s', type=int, default=5, help='number of surviving agent')
    args = parser.parse_args(sub_args)
    new_run(args.name, args.tp, args.gen,args.s)

elif args.function == "run_build":
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str, help='name of the experience')
    args = parser.parse_args(sub_args)
    run_build(args.name)

elif args.function == "run_best":
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str, help='name of the experience')
    args = parser.parse_args(sub_args)
    run_best(args.name)

elif args.function == "new_run_static":
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str, help='name of the experience')
    parser.add_argument('tp', type=int, default=10, help='number of agents')
    parser.add_argument('gen', type=int, default=10, help='number of gene')
    parser.add_argument('s', type=int, default=5, help='number of surviving agent')
    args = parser.parse_args(sub_args)
    new_run_static(args.name, args.tp, args.gen,args.s)
