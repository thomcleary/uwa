""" Classes to generate game tree for the resistance """

from enum import Enum
from itertools import combinations



class RoundState(Enum):
    """ State that a given round can be in """
    ROOT_PROPOSE = 0
    PROPOSE      = 1
    MISSION      = 2


class GameState:
    """ Class that represents the state of the game, with parent and child states """

    mission_sizes = {
            5:[2,3,2,3,3], \
            6:[2,3,4,3,4], \
            7:[2,3,3,4,4], \
            8:[3,4,4,5,5], \
            9:[3,4,4,5,5], \
            10:[3,4,4,5,5]
            }

    spy_count = {5:2, 6:2, 7:3, 8:3, 9:3, 10:4} 
    

    def __init__(self, 
        num_players,     round_num,   round_state, 
        round_leader,    round_team,  votes_held, 
        missions_failed, parent=None, is_spy=True, 
    ):

        # MCTS simulation counts
        self.num_wins = 1
        self.num_sims = 2

        # information about the current round
        self.round_num    = round_num
        self.round_state  = round_state
        self.round_leader = round_leader
        self.round_team   = round_team # 'proposed' team if mission state is PROPOSE
        self.votes_held   = votes_held

        # information about the state of the game as a whole
        self.num_players     = num_players
        self.agent_is_spy    = is_spy
        self.missions_failed = missions_failed
        self.missions_passed = self.round_num - 1 - missions_failed

        self.children = []
        self.expanded = False
        self.parent   = parent

    
    def __repr__(self):
        return ("GameState \n- RoundNum: {}\n- RoundState - {}\n" + \
                "- RoundLeader: {}\n- RoundTeam: {}\n- VotesHeld: {}\n" + \
                "- MissionsFailed: {}\n- MissionsPassed: {}\n- NumChildren: {}\n" + \
                "- DeepestSimmedChild: {}\n-TotalSims: {}\n-TotalSimWins: {}\n"
        ).format(
            self.round_num, self.round_state, self.round_leader, self.round_team, self.votes_held,
            self.missions_failed, self.missions_passed, len(self.children),
            self.num_sims, self.num_wins
        )


    def is_terminal(self):
        """ return True if this GameState is a 'game over' state, else False """
        return self.missions_failed >= 3 or self.missions_passed >= 3


    def is_root(self):
        """ return True if this is the root node of the game tree, else false """
        return self.parent == None


    def has_children(self):
        """ return True if this node has children, else false """
        return len(self.children) > 0


    def expand(self):
        """ add this states children to self.children """
        if self.is_terminal() or self.expanded:
            self.expanded = True
            return

        self.expanded = True

        if self.round_state == RoundState.ROOT_PROPOSE:
            self.expand_root_propose()

        elif self.round_state == RoundState.PROPOSE:
            self.expand_propose()

        else: # self.round_state == RoundState.MISSION
            self.expand_mission()


    def expand_root_propose(self):
        """ children of root need to be all combinations of teams agent can propose """
        # Child for each possible team that could be proposed next
        team_combos = list(combinations(
            list(range(self.num_players)), 
            GameState.mission_sizes[self.num_players][self.round_num-1]
        ))

        for combo in team_combos:
            self.children.append(GameState(
                self.num_players,     self.round_num, RoundState.PROPOSE,
                self.round_leader,    combo,          self.votes_held,
                self.missions_failed, parent=self, is_spy=self.agent_is_spy
            ))

    
    def expand_propose(self):
        """ expand the state treating the current round as being in the PROPOSE state """
        votes_held = self.votes_held + 1

        # Proposal passed
        # ---------------------------------------------------------------------
        # single child if vote passes: RoundState -> MISSION
        self.children.append(GameState(
            self.num_players,     self.round_num,  RoundState.MISSION,
            self.round_leader,    self.round_team, votes_held,
            self.missions_failed, parent=self, is_spy=self.agent_is_spy
        ))


        # Proposal failed
        # ---------------------------------------------------------------------
        next_leader      = (self.round_leader + 1) % self.num_players
        next_round       = self.round_num
        mission_failures = self.missions_failed

        # DO NOT GENERATE CHILD FOR VOTE FAILING FIFTH ROUND - ASSUME NO ONE WOULD DO THAT

        # Only generate another round of proposal children if they have been less than 5 voting rounds
        if not (self.missions_failed == 2 and self.votes_held == 4):
            team_combos = list(combinations(
                list(range(self.num_players)), 
                GameState.mission_sizes[self.num_players][self.round_num-1]
            ))

            for combo in team_combos:
                self.children.append(GameState(
                    self.num_players, next_round, RoundState.PROPOSE,
                    next_leader,      combo,      votes_held,
                    mission_failures, parent=self, is_spy=self.agent_is_spy
                ))
        

    def expand_mission(self):
        """ expand the state treating the current round as being in the MISSION state """
        # If a fail or pass does not result in a loss for either side, then we have 2 * number of team combinations
        # child nodes, same combination twice for each outcome
        # If a fail / pass results in a win for a side then we only need 1 child for that side
        # eg, mission failed and spies win then 1 child for mission failed, many for mission passed.

        fail_expanded    = False
        success_expanded = False
        votes_held = 0

        next_round  = self.round_num + 1
        next_leader = (self.round_leader + 1) % self.num_players


        # Create terminal states if missions failed/passed == 2
        if self.missions_failed == 2:
            self.children.append(GameState(
                self.num_players,         next_round, RoundState.PROPOSE,
                next_leader,              [],         votes_held,
                self.missions_failed + 1, parent=self, is_spy=self.agent_is_spy
            ))

            fail_expanded = True


        if self.missions_passed == 2:
            self.children.append(GameState(
                self.num_players,     next_round, RoundState.PROPOSE,
                next_leader,          [],         votes_held,
                self.missions_failed, parent=self, is_spy=self.agent_is_spy
            ))

            success_expanded = True


        # if we have not created both terminal states
        if not fail_expanded or not success_expanded:
            team_combos = list(combinations(
                list(range(self.num_players)), 
                GameState.mission_sizes[self.num_players][self.round_num-1]
            ))

            for combo in team_combos:
                if not success_expanded:
                    self.children.append(GameState(
                        self.num_players,     next_round, RoundState.PROPOSE,
                        next_leader,          combo,      votes_held,
                        self.missions_failed, parent=self, is_spy=self.agent_is_spy
                    ))

                if not fail_expanded:
                    self.children.append(GameState(
                        self.num_players,         next_round, RoundState.PROPOSE,
                        next_leader,              combo,      votes_held,
                        self.missions_failed + 1, parent=self, is_spy=self.agent_is_spy
                    ))

