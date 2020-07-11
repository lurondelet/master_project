# imports framework
import sys, os
sys.path.insert(0, 'evoman')
sys.path.append('evoman_framework')
sys.path.append('evoman_framework/evoman')
sys.path.append('project_controller')
from environment import Environment
from project_controller.first_controller import player_controller
from datetime import datetime

experiment_name = 'dummy_custom_demo'
#file_aux = open(experiment_name + '/evoman_logs.txt', 'w')
now=datetime.now()
#print to log with date
file_tocopy = experiment_name + '/evoman_logs.txt'
file_aux2= experiment_name + '/evoman_logs_'+now.strftime("%m:%d-%H:%M:%S")+'.txt'

#file_aux2 = open(experiment_name + '/evoman_logs2.txt', 'w')
#find a way to convert text from log to str to copy the logs
#file_aux2.write(file_aux_copy)

print(file_tocopy)

with open(file_tocopy) as f:
    lines = f.readlines()
    lines = [l for l in lines if "ROW" in l]
    with open(file_aux2, "w") as f1:
        f1.writelines(lines)

if not os.path.exists(experiment_name):
    os.makedirs(experiment_name)

# initializes environment with ai player using random controller, playing against static enemy
#env = Environment(experiment_name=experiment_name)
env = Environment(experiment_name=experiment_name,
                      playermode="ai",
                      player_controller=player_controller(),
                      speed="fastest",
                      enemymode="static",
                    #inputcoded="yes"
                        level=2
                  )


for en in range (1,9):
    # Update the enemy
    env.update_parameter('enemies', [en])

    #sol = np.loadtxt('masterproject/demo_' + str(en) + '.txt')
    print('\n saved ' + str(en) + ' \n')
    env.play()





