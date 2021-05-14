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

    def greedymax(self, state, depth):

        def greedy_score(state):
            own_loc = state.locs[self.player_id]
            own_liberties = state.liberties(own_loc)
            return len(own_liberties)

        def greedy_choice(state):
            if state.terminal_test():
                return state.utility(self.player_id)
            choice = max(state.actions(), key=lambda x: greedy_score(state.result(x)))
            return max_value(choice, depth-1)

        def max_score(state):
            own_loc = state.locs[self.player_id]
            opp_loc = state.locs[1 - self.player_id]
            own_liberties = state.liberties(own_loc)
            opp_liberties = state.liberties(opp_loc)
            return len(own_liberties) - len(opp_liberties)

        def max_value(state, depth):
            if state.terminal_test():
                value = state.utility(self.player_id)
                return value
            depth -= 1
            if depth <= 0:
                return max_score(state)
            v = float("-inf")
            for a in state.actions():
                v = max(v, greedy_choice(state.result(a)))
            return v

        return max(state.actions(), key=lambda x: max_value(state.result(x), depth -1))

    def minimax_decision(self, state, depth):
        best_score = float("-inf")
        best_move = None
        for a in state.actions():
            # call has been updated with a depth limit
            v = self.greedymax(state, depth - 1)
            if v > best_score:
                best_score = v
                best_move = a
        return best_move

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
        import random
        if state.ply_count < 2:
            if 57 in state.actions():
                self.queue.put(57)
            else:
                middle = set.intersection(set(state.actions()), {57, 43, 44, 45, 56, 58, 69, 70, 71})
                self.queue.put(random.choice(list(middle)))
        else:
            '''__________Time management___________'''
            time_limit = 148 / 1000
            timer_ends = time.perf_counter() + time_limit
            best_move = None
            depth_limit = 4
            while True:
                # print("I play")
                if time.perf_counter() <= timer_ends:
                    self.queue.put(best_move)
                # self.queue.put(random.choice(state.actions()))
                for depth in range(1, depth_limit + 1):
                    best_move = self.greedymax(state, depth_limit)
                self.queue.put(best_move)

    # max calls greedy on RESULTS of each possible action in that STATE, then calls max
    # on each possible action in the state greedy chooses.

    def is_divided(self, state):
        pass
        if state.liberties():
            pass
