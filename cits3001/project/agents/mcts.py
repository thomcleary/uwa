"""
MCTS of the Resistance Game tree (GameState class in game_tree.py)

Uses UCT (Upper confidence bound 1 applied to trees)

mcts() function found at bottom of file
"""

import copy
import math
import random
import time

from game_tree import GameState
from game_tree import RoundState


def uct(node):
    """ return the uct value of node """
    c = math.sqrt(2)

    exploitation = node.num_wins / node.num_sims

    exploration  = c * math.sqrt(math.log(node.parent.num_sims) / node.num_sims)

    return exploitation + exploration


def get_highest_uct_node(parent_node):
    """ return the child of parent node with the highest uct, random if multiple """
    # Pick the child of the current node with highest
    highest_uct_nodes = [] 
    highest_uct       = 0

    for child in parent_node.children:
        child_uct = uct(child)

        if child_uct > highest_uct:
            highest_uct_nodes = [child]
            highest_uct       = child_uct

        elif child_uct == highest_uct:
            highest_uct_nodes.append(child)

    return random.choice(highest_uct_nodes)


def get_terminal_result(terminal_node):
    """
    Return the terminal result of this node depending on agent role
    """
    if terminal_node.missions_failed >= 3:
        if terminal_node.agent_is_spy:
            return 1
        else:
            return 0

    if terminal_node.missions_passed >= 3:
        if terminal_node.agent_is_spy:
            return 0
        else:
            return 1


def random_simulate(leaf_node):
    """
    Simulate LIKE RANDOM AGENT from a child of this leaf_node.
    If leaf_node is a terminal state, return the result of the game
    """
    if leaf_node.is_terminal():
        return (get_terminal_result(leaf_node), leaf_node)

    return (random.choice([0, 1]), random.choice(leaf_node.children))



def is_spy(opponent, agent, num_spys):
    """ return if agent thinks voter is a spy """
    if agent.is_spy():
        return opponent in agent.spy_list

    else:
        fail_counts_copy = copy.deepcopy(agent.fail_counts)
        spy_list_guess = []

        for _ in range(num_spys):
            most_suspicious = fail_counts_copy.index(max(fail_counts_copy))
            spy_list_guess.append(most_suspicious)
            fail_counts_copy.pop(most_suspicious)

        return opponent in spy_list_guess


def simulate_vote(propose_state, agent):
    """ return how basic agents would vote on a proposed team """
    votes_for = 0
    votes_against = 0

    votes_held = propose_state.votes_held + 1

    # if this is the last vote always return FOR
    if votes_held == 5:
        return True # For

    for voting_agent in range(propose_state.num_players):
        
        if is_spy(voting_agent, agent, propose_state.spy_count[propose_state.num_players]):
            # if spy is on the mission vote for, else against
            if len(set(get_spy_list(propose_state, agent, voting_agent)) & set(propose_state.round_team)) > 0:
                votes_for += 1
            else:
                votes_against += 1

        else:
            # vote FOR is the team average of past failures is less than the overall average
            # else against
            team_fails = 0
            for player in propose_state.round_team:
                team_fails += agent.fail_counts[player]
            
            team_average = team_fails / len(propose_state.round_team)
            overall_average = sum(agent.fail_counts) / len(agent.fail_counts)

            if team_average < overall_average:
                votes_for += 1
            else:
                votes_against += 1

    if votes_for > votes_against:
        return True
    else:
        return False


def get_spy_list(sim_state, agent, requesting_agent):
    """ 
    if agent is spy and requester is spy return true spy list
    if agent is not spy return list of spys agent thinks is spies
    """
    if agent.is_spy():
        if requesting_agent in agent.spy_list:
            return agent.spy_list

    else:
        spy_list = []
        fail_counts = copy.deepcopy(agent.fail_counts)
        while len(spy_list) < sim_state.spy_count[sim_state.num_players]:
            spy = fail_counts.index(max(fail_counts))
            if spy not in spy_list:
                spy_list.append(spy)
            fail_counts[spy] = -math.inf

        return spy_list



def choose_team(sim_state, agent, next_leader):
    """ return a team proposal that agent thinks next_leader would propose """
    team = []
    team_size = sim_state.mission_sizes[sim_state.num_players][sim_state.round_num-1]
    fail_counts = copy.deepcopy(agent.fail_counts)

    if is_spy(next_leader, agent, sim_state.spy_count[sim_state.num_players]):
        spy_hide = random.random() < 0.5
        # if resistance is at 2 mission successes, or 1 fail away from losing, or not hiding
        # always propose appropriate amount of spies
        if sim_state.missions_passed == 2 or sim_state.missions_failed == 2 or not spy_hide:
            while len(team) < agent.fails_required[agent.number_of_players][agent.current_round-1]:
                spy = random.choice(get_spy_list(sim_state, agent, next_leader))
                if spy not in team:
                    team.append(spy)

    # fill team with players involved in least number of failures
    while len(team) < team_size:
        agent = fail_counts.index(min(fail_counts))
        if agent not in team:
            team.append(agent)
        fail_counts[agent] = math.inf

    return team


def simulate_mission(sim_state, agent):
    """ simulate if agent thinks mission would be betrayed """

    num_spies_on_mission = 0
    for opponent in sim_state.round_team:
        if is_spy(opponent, agent, sim_state.spy_count[sim_state.num_players]):
            num_spies_on_mission += 1

    for opponent in sim_state.round_team:
        if is_spy(opponent, agent, sim_state.spy_count[sim_state.num_players]):
            if sim_state.round_num == 5 or sim_state.missions_failed == 2:
                return True
            else:
                fail_rate = 0.75 / num_spies_on_mission
                return random.random() < fail_rate

    return False # not betrayed


def basic_simulate(leaf_node, agent):
    """
    Simulate LIKE BASIC AGENT from a child of this leaf_node
    If leaf_node is terminal state, return the game result
    """

    # Choose child of leaf node
    if leaf_node.is_terminal():
        return (get_terminal_result(leaf_node), leaf_node)

    child_node = random.choice(leaf_node.children)

    # sim_state = copy.deepcopy(child_node)
    # using this copy includes parents and slows down simulation by factor of 10 

    sim_state = GameState(
        child_node.num_players, child_node.round_num, child_node.round_state,
        child_node.round_leader, child_node.round_team, child_node.votes_held,
        child_node.missions_failed, is_spy=child_node.agent_is_spy
    )

    # SIMULATE AS IF PLAYING LIKE BASIC AGENT
    while not sim_state.is_terminal():

        # OUR AGENT MUST PROPOSE A MISSION (Same logic as basic agent)
        if sim_state.round_state == RoundState.ROOT_PROPOSE:
            team = choose_team(sim_state, agent, sim_state.round_leader)

            sim_state = GameState(
                sim_state.num_players, sim_state.round_num, RoundState.PROPOSE,
                sim_state.round_leader, team, sim_state.votes_held,
                sim_state.missions_failed, is_spy=sim_state.agent_is_spy
            )


        elif sim_state.round_state == RoundState.PROPOSE:
            vote_pass = simulate_vote(sim_state, agent)

            if vote_pass:
                sim_state = GameState(
                    sim_state.num_players, sim_state.round_num, RoundState.MISSION,
                    sim_state.round_leader, sim_state.round_team, sim_state.votes_held,
                    sim_state.missions_failed, is_spy=sim_state.agent_is_spy
                )
            else:
                next_leader = (sim_state.round_leader + 1) % sim_state.num_players
                team = choose_team(sim_state, agent, next_leader)

                sim_state = GameState(
                    sim_state.num_players, sim_state.round_num, RoundState.MISSION,
                    next_leader, sim_state.round_team, sim_state.votes_held+1,
                    sim_state.missions_failed, is_spy=sim_state.agent_is_spy
                )

        else: # sim_state.round_state == RoundState.MISSION:
            mission_betrayed = simulate_mission(sim_state, agent)

            next_leader = (sim_state.round_leader + 1) % sim_state.num_players

            if mission_betrayed:
                sim_state.missions_failed += 1

            sim_state = GameState(
                sim_state.num_players, sim_state.round_num+1, RoundState.ROOT_PROPOSE,
                next_leader, [], 0,
                sim_state.missions_failed, is_spy=sim_state.agent_is_spy
            )
            
    return (get_terminal_result(sim_state), child_node)


def backpropogate(result, child_node):
    """ add the result of simulation to the child node and its parents """
    if child_node is None:
        return

    child_node.num_wins += result
    child_node.num_sims += 1

    backpropogate(result, child_node.parent)


def get_best_move(root, best_child):
    """ return the best move that the agent can make based off of moving from root -> best_child state"""
    # need to return best team to propose
    if root.round_state == RoundState.ROOT_PROPOSE:
        move = best_child.round_team

    # need to return whether to vote for or against
    if root.round_state == RoundState.PROPOSE:
        if best_child.round_state == RoundState.MISSION:
            move = True # FOR
        else: # round_state is PROPOSE again
            move = False # AGAINST

    # need to return whether to betray the mission or not
    # if best child has more failures then we betray the mission
    if root.round_state == RoundState.MISSION:
        if best_child.missions_failed > root.missions_failed: 
            move = True # Betray
        else:
            move = False # Do Not Betray


    return move


def mcts(root, agent, time_limit=1, sim_limit=1000, sim_type="random"):
    """
    Perform MCTS for num_simulations starting with current_game_state as
    the root node of the game tree
    ---------------------------------------------------------------------------
    1. Select
    2. Expand (If selected leaf is not terminal)
    3. Simulate (If selected leaf is not terminal)
    4. Backpropogate
    """
    if root.is_terminal():
        raise ValueError("Root cannot be a terminal game state.")

    start_time = time.time()
    num_sims = 0

    # to add a time limit to the search change while loop to
    # while time.time() - start_time < time_limit and num_sims < sim_limit
    
    while num_sims < sim_limit:
        # 1. Select Leaf Node
        chosen_node = root

        while chosen_node.has_children():
            chosen_node = get_highest_uct_node(chosen_node)

        # 2. Expand leaf node (method will not do anything if terminal)
        chosen_node.expand()

        # 3. Simulate from a child of leaf node
        # (if leaf is terminal will return result of game
        if sim_type == "random":    
            result, child_node = random_simulate(chosen_node)
        elif sim_type == "basic":
            result, child_node = basic_simulate(chosen_node, agent)
        else:
            raise ValueError("{} is an unsupported sim_type".format(sim_type))

        # 4. Backpropogate the result of the simulation
        backpropogate(result, child_node)

        num_sims += 1

    # Return child of root GameState with highest UCT after num_simulations
    chosen_node = get_highest_uct_node(root)
    
    # Can deduce the move to make by
    # Comparing RoundState of root and this child node
    return get_best_move(root, chosen_node)
