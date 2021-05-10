import time

from sample_players import BasePlayer
# from alpha_beta import *


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

    import time
    time_limit = 148 / 1000


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
        # timer_ends = time.perf_counter() + time_limit
        # best_move = None
        best_score = float('-inf')
        value = float('-inf')

        for action in state.actions():
            result = state.result(action)
            self.max_value(result)
            if best_score <= value:
                best_score = value
                best_move = action

        self.queue.put(best_move)


    def greedy_choice(self, state):
        if state.terminal_test():
            return state.utility(self.player_id)
        return max(state.actions(), key=lambda x: self.greedy_score(state.result(x)))

    # max calls greedy on RESULTS of each possible action in that STATE, then calls max
    # on each possible action in the state greedy chooses.
    def max_value(self, state):
        global value
        global time_limit
        if state.terminal_test():
            value = state.utility(self.player_id)
            return
        value = self.max_score(state)
        if time.perf_counter() >= timer_ends:

            return

        opp_move = self.greedy_choice(state)
        result = state.result(opp_move)
        for action in result.actions():
            value = max(value, self.max_value(action))

    def max_score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)


    def greedy_score(self, state):
        own_loc = state.locs[self.player_id]
        own_liberties = state.liberties(own_loc)
        return len(own_liberties)

    def is_divided(self, state):
        pass
        if state.liberties():
            pass
