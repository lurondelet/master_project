
## Installation

* Clone the repository
* Install Anaconda (https://www.anaconda.com/products/individual)
* Install all the packages listed in the `requirements.txt` file 
* run the player file (`python human_demo.py`) to see if the evoman framework runs properly
* copy paste content from project_controller into evoman_framework

## run experience


* To run new a new experience, `python GP_player_logi_math.py new_run` 
followed by `experience_name`  `population_number` `generation_number` `survivor`
* To rerun or continue an experience, `python GP_player_logi_math.py run_build` 
followed by `experience_name`
* To look at the best result of an experience, `python GP_player_logi_math.py run_best`
followed by `experience_name`

## retriving the data

*  Once the player program are ran at least once, the data will be sent to a folder with matching name.
* The population and enemy population are saved in pickle file `GP_solution` and `GP_solution_enemy`
* Environment parameters are saved in the first sub folder in the folder matching the experience name
in a form of `evoman_paramstate.txt`
* The score of the differents agents used through the population are saved in the subfolder
in form of `evoman_logs.txt` and `evoman_logs_MM:DD-HH:MM:SS.txt` to keep track 
if the  experience is ran multiple times

## Evoman framework

The evoman framework can be found in : https://github.com/karinemiras/evoman_framework

