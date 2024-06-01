""" Play all of our agents against eachother in a tournament """

import sys

sys.path.append("./simulations")
sys.path.append("./agents")       # allows importing of modules in agents folder
sys.path.append("./agents")       # allows importing of modules in agents folder

from basic_agent import BasicAgent
from random_agent import RandomAgent
from mcts_agent import MCTSAgent
from mixed_agent import MixedAgent

from game import Game

from sim_helpers  import data_to_rows, create_csv_files


def resistance_tournament(agents, num_sims, data_outpath):
    '''
    run num_sims games against the agents in agents
    '''

    print("Beginning Tournament...")

    if len(agents) < 5:
        raise ValueError("Must be atleast 5 agents in the tournament")


    for i in range(num_sims):
        game = Game(agents)
        game.play()
        print(f"{i+1}/{num_sims}")

    for agent in agents:
        data = {
        "win_ratios" : agent.win_ratios,
        "spy_ratios" : agent.spy_win_ratios,
        "res_ratios" : agent.resistance_win_ratios
        }

        create_csv_files(data_to_rows(data, num_sims), data_outpath, agent.name)

        print(f"...{agent.name} agent data exported\n", "-" * 80, sep="")
