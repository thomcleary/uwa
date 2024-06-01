""" Run simulations of the game

With user specified:
Number of sims
Type of players
Type of opponents

Dumps all data into relevant opponent data folder
eg ./data/opponents-random for random opponents
"""

import argparse
import sys

sys.path.append("./simulations")
sys.path.append("./agents")       # allows importing of modules in agents folder
sys.path.append("./agents")       # allows importing of modules in agents folder

from basic_agent import BasicAgent
from random_agent import RandomAgent
from mcts_agent import MCTSAgent
from mixed_agent import MixedAgent

from sim_helpers  import simulate_resistance_games
from tournament import resistance_tournament



def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "num_sims",
        help="Number of simulations per tester agent to run",
        type=int
    )
    parser.add_argument(
        "testers",
        help="Type of agents you want to test",
        choices= ["random", "basic", "randomMCTS", "basicMCTS", "mixed", "reflex", "mcts", "all"],
        type=str
    )
    parser.add_argument(
        "opponents",
        help="Opponent type for simulations",
        choices = ["random", "basic", "tournament"],
        type=str
    )
    args = parser.parse_args()

    testers = get_testers(args.testers)

    if args.opponents != "tournament":
        data_outpath = f"./simulations/data/opponents-{args.opponents}/"
        simulate_resistance_games(
            testers, 
            args.num_sims, 
            data_outpath=data_outpath, 
            opponent_type=args.opponents
        )

    else:
        data_outpath = f"./simulations/data/tournament/"
        resistance_tournament(
            testers,
            args.num_sims,
            data_outpath
        )


def get_testers(tester_arg):
    """ return a list of agents for which performance will be tracked """
    testers = []

    if tester_arg in ["random", "reflex", "all"]:
        testers.append(RandomAgent(name="random", tester=True))

    if tester_arg in ["basic", "reflex", "all"]:
        testers.append(BasicAgent(name="basic", tester=True))

    if tester_arg in ["randomMCTS", "mcts", "all"]:
        testers.append(MCTSAgent(name="randomMCTS", sim_type="random", tester=True))

    if tester_arg in ["basicMCTS", "mcts", "all"]:
        testers.append(MCTSAgent(name="basicMCTS", sim_type="basic", tester=True))

    if tester_arg in ["mixed", "all"]:
        testers.append(MixedAgent(name="mixed", sim_type="random", tester=True))

    return testers


if __name__ == "__main__":
    main()