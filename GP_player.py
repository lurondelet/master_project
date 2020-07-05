import sys, os
sys.path.insert(0, 'evoman')
from environment import Environment
from GP_controller import player_controller

# imports other libs
import numpy as np

experiment_name = 'GP_agent_demo_1'
if not os.path.exists(experiment_name):
    os.makedirs(experiment_name)