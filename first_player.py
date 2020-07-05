import sys, os
sys.path.insert(0, 'evoman')
from evoman.environment import Environment
from first_controller import player_controller

# imports other libs

experiment_name = 'first_agent_demo'
if not os.path.exists(experiment_name):
    os.makedirs(experiment_name)

# initializes environment for single objective mode (specialist)  with static enemy and ai player
env = Environment(experiment_name=experiment_name,
                      playermode="ai",
                      player_controller=player_controller(),
                      speed="normal",
                      enemymode="static",
                      level=2)


# tests for each enemy
for en in range(1, 9):

    #Update the enemy
    env.update_parameter('enemies',[en])

    env.play()
