""" Helper functions for simulation scripts """

import sys

sys.path.append("./resistance")   # allows importing of modules in resistance package
sys.path.append("./agents")       # allows importing of modules in agents folder

from basic_agent import BasicAgent
from random_agent import RandomAgent
from game import Game



def simulate_resistance_games(testers, num_sims, data_outpath, opponent_type="random"):
    '''
    Simulate num_sims games as a SPY and RESISTANCE player for test_agent
    Write the spy/resistance win ratios of test_agent over time to a csv file
    '''

    print("-" * 80)

    for tester in testers:

        print(f"Testing {tester.name} agent...")

        num_players = 5

        for i in range(num_sims):
            if num_players == 0:
                num_players += 5

            play_game(tester, num_players, opponent_type=opponent_type)
            num_players = ((num_players + 1) % 11)

            print(f"{i}/{num_sims}")

        data = {
        "win_ratios" : tester.win_ratios,
        "spy_ratios" : tester.spy_win_ratios,
        "res_ratios" : tester.resistance_win_ratios
        }

        create_csv_files(data_to_rows(data, num_sims), data_outpath, tester.name)

        print(f"...{tester.name} agent finished\n", "-" * 80, sep="")


def play_game(test_agent, num_players=5, opponent_type="random"):
    ''' run a game of the resistance with specified number of players '''
    players = [test_agent]

    for i in range(1, num_players):

        if opponent_type == "random":
            players.append(RandomAgent(name="opp_agent{}".format(i)))

        elif opponent_type == "basic":
            players.append(BasicAgent(name="opp_agent{}".format(i)))

        else:
            raise ValueError(f"{opponent_type} is an invalid opponent type for play_game()")

    game = Game(players)
    game.play()


def create_csv_files(data, data_outpath, agent_name):
    rows_spy, rows_resistance, rows_overall = data

    outfile_spy = data_outpath + f"{agent_name}-spy.csv"
    outfile_resistance = data_outpath + f"{agent_name}-resistance.csv"
    outfile_overall = data_outpath + f"{agent_name}-overall.csv"

    rows_to_csv(rows_spy, outfile_spy)
    rows_to_csv(rows_resistance, outfile_resistance)
    rows_to_csv(rows_overall, outfile_overall)


def rows_to_csv(rows, outfile_path):
    ''' write the data in rows to a csv file '''
    with open(outfile_path, "w") as csv_file:
        for row in rows:
            row = ",".join(row) + "\n"
            csv_file.write(row)


def data_to_rows(sim_data, num_sims):
    ''' 
    Transform sim_data dict into rows (list of lists)
    In the form: [num_players, games_played, spy_win_ratio, resistance_win_ratio, win_ratio]
    '''

    rows_spy = [
        ["games_played",
         "spy_win_ratio"]
    ]

    rows_resistance = [
        ["games_played",
         "res_win_ratio"]
    ]

    rows_overall = [
        ["games_played",
         "win_ratio"]
    ]


    for games_played in range(len(sim_data["spy_ratios"])):
        rows_spy.append([
            str(games_played + 1),
            str(sim_data["spy_ratios"][games_played])
        ])

    for games_played in range(len(sim_data["res_ratios"])):
        rows_resistance.append([
            str(games_played + 1),
            str(sim_data["res_ratios"][games_played])
        ])

    games_played = 0
    while games_played < len(sim_data["win_ratios"]):
        rows_overall.append([
            str(games_played + 1),
            str(sim_data["win_ratios"][games_played])
        ])
        games_played += 1

    return (rows_spy, rows_resistance, rows_overall)