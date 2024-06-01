# CITS3001 AI Project

## Students
Thomas Cleary (21704985)  
Chauntelle Bonser (22706693)


# Project File Structure
## ./agents
Contains all agents mentioned in report (and supporting code).
- random_agent.py -> *randomAgent*
- basic_agent.py -> *basicAgent*
- mcts_agent.py -> *randomMCTSAgent* **and** *basicMCTSAgent* (sim_type parameter of class constructor used to call different simulation function)
- mixed_agent.py -> *mixedAgent*

It also contains supporting code for the MCTS agents
- game_tree.py -> classes to define a current game state and methods to expand its children etc.
- mcts.py -> functions to run a MCTS on the game tree of The Resistance

sim_agent.py is a modified version of agent.py that was provided. It is used as the abstract class for which all agents are subclassed.  
(it has been modified to allow for tracking of win ratios of agents)

## ./resistance
Contains the code provided to use to start the project.

## ./simulations
Contains the code to run the simulations relevant to the validation part of the report.
### ./simulations/data
Is where sim.py dumps all the performance data it creates
### ./simulations/data/OPPONENT_TYPE
OPPONENT_TYPE is the directory that refers to the type of opponent you run sim.py with
- random
- basic
- tournament


# To Run Simulations
NOTE: Our scripts use sys.path().append() to add the other directories to the system path. **All scripts must be run from the top level directory**  
eg. Current directory must be top project folder, then run  
`$ python simulations/sim.py NUM_SIMS TEST_AGENT_TYPE OPPONENT_TYPE `

## sim.py
Is used to collect all of our testing / validation data found in ./simulations/data/   
It will dump the csv data into the appropriate folder, dependant on the opponents that you choose.

To get a help message on what arguments need to be given to the script run   
`$ python simulations/sim.py -h`

sim.py takes 3 positional arguments  
1. number of simulations
2. the agents you wish to test
3. the opponents you wish to test them against

For example the data for **randomAgent** playing against **randomAgents** for 1 million sims was done by running sim.py as:  
`$ python simulations/sim.py 1000000 random random`

## The full list of commands we used to get our data is as follows:
`$ python simulations/sim.py 1000000 random random`  
`$ python simulations/sim.py 1000000 random basic`  
`$ python simulations/sim.py 1000000 basic random`  
`$ python simulations/sim.py 1000000 basic basic`  
`$ python simulations/sim.py 5000 randomMCTS random`  
`$ python simulations/sim.py 5000 randomMCTS basic`  
`$ python simulations/sim.py 5000 basicMCTS random`  
`$ python simulations/sim.py 5000 basicMCTS basic`  
`$ python simulations/sim.py 5000 all tournament`  


# NOTE: IF YOU ONLY WISH TO VALIDATE THAT OUR AGENTS RUN WITHOUT CRASHING RUN THIS COMMAND
` $ python simulations/sim.py 1 all random`

This will run each type of agent once against 4 other **randomAgent** players  
NOTE: This will overwrite any exists data found in ./simulations/data/opponents-random

