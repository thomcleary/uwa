""" An agent that plays the game randomly.

Subclassed from SimAgent class (which is modified super class provided in resistance/agent.py)
"""

import random

from sim_agent import SimAgent


class RandomAgent(SimAgent):
    '''A sample implementation of a random agent in the game The Resistance'''

    def __init__(self, name='Rando', tester=False):
        '''
        Initialises the agent.
        Nothing to do here.
        '''
        super().__init__(name=name, tester=tester)
        

    def new_game(self, number_of_players, player_number, spy_list):
        '''
        initialises the game, informing the agent of the
        number_of_players, 
        the player_number (an id number for the agent in the game),
        and a list of agent indexes which are the spies, if the agent is a spy, or empty otherwise
        '''
        self.number_of_players = number_of_players
        self.player_number = player_number
        self.spy_list = spy_list


    def is_spy(self):
        '''
        returns True iff the agent is a spy
        '''
        return self.player_number in self.spy_list


    def propose_mission(self, team_size, betrayals_required=1):
        '''
        expects a team_size list of distinct agents with id between 0 (inclusive) and number_of_players (exclusive)
        to be returned.
        betrayals_required are the number of betrayals required for the mission to fail.
        '''
        team = []
        while len(team) < team_size:
            agent = random.randrange(self.number_of_players)
            if agent not in team:
                team.append(agent)
        return team


    def vote(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission.
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.
        '''
        return random.random() < 0.5


    def vote_outcome(self, mission, proposer, votes):
        '''
        mission is a list of agents to be sent on a mission.
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        votes is a dictionary mapping player indexes to Booleans (True if they voted for the mission, False otherwise).
        No return value is required or expected.
        '''
        # nothing to do here
        pass


    def betray(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission.
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The method should return True if this agent chooses to betray the mission, and False otherwise.
        By default, spies will betray 30% of the time.
        '''
        if self.is_spy():
            return random.random() < 0.5


    def mission_outcome(self, mission, proposer, betrayals, mission_success):
        '''
        mission is a list of agents to be sent on a mission.
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        betrayals is the number of people on the mission who betrayed the mission,
        and mission_success is True if there were not enough betrayals to cause the mission to fail, False otherwise.
        It is not expected or required for this function to return anything.
        '''
        # nothing to do here
        pass


    def round_outcome(self, rounds_complete, missions_failed):
        '''
        basic informative function, where the parameters indicate:
        rounds_complete, the number of rounds (0-5) that have been completed
        missions_failed, the numbe of missions (0-3) that have failed.
        '''
        # nothing to do here
        pass


    def game_outcome(self, resistance_wins, spies):
        '''
        basic informative function, where the parameters indicate:
        spies_win, True iff the spies caused 3+ missions to fail
        spies, a list of the player indexes for the spies.
        '''
        if not self.tester:
            return


        if self.is_spy():
            self.num_spy_games += 1

            if not resistance_wins:
                self.spy_wins += 1


        else:
            self.num_resistance_games += 1

            if resistance_wins:
                self.resistance_wins += 1


        self.update_win_ratios()
    

    def update_win_ratios(self):
        '''
        update the win ratios of the agent depending on if they are a spy or resistance member
        '''
        if self.is_spy():
            self.spy_win_ratios.append(round(
                self.spy_wins / self.num_spy_games,
                5
            ))

        else:
            self.resistance_win_ratios.append(round(
                (self.resistance_wins / self.num_resistance_games),
                5
            ))

        self.win_ratios.append(round(
            (self.spy_wins + self.resistance_wins) /
            (self.num_spy_games + self.num_resistance_games),
            5
        ))
