from sample_players import BasePlayer
from alpfa_beta import *


class CustomPlayer(BasePlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """

    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)
        '''__________Time management___________'''
        import time
        time_limit = 148 / 1000
        timer_ends = time.perf_counter() + time_limit
        best_move = None
        best_score = int('-inf')

        while time.perf_counter() <= finish:
            best_move = self.max_value(state)

        self.queue.put(best_move)

    # max calls greedy on RESULTS of each possible action in that STATE, then calls max
    # on each possible action in the state greedy choses.
    def max_value(self, state):
        if state.terminal_test():
            return state.utility(self.player_id)

        opp_move = state.result(self.greedy(state))
        best_move = max(max_value(action) for action in opp_move.actions)

        # return action with highest score

        # search for a node where opponent has lots of liberties,
        # but i can cut him later in one go.

    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)

    def greedy(self, state):
        if state.terminal_test():
            return state.utility(self.player_id)
        return max(state.actions(), key=lambda x: self.greedy_score(state.result(x)))

    def greedy_score(self, state):
        own_loc = state.locs[self.player_id]
        own_liberties = state.liberties(own_loc)
        return len(own_liberties)
