import time
import random

from sample_players import BasePlayer


class CustomPlayer(BasePlayer):
    def get_action(self, state):
        """ Choose an action available in the current state

        See RandomPlayer and GreedyPlayer for examples.

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller is responsible for
        cutting off the function after the search time limit has expired.

        **********************************************************************
        NOTE: since the caller is responsible for cutting off search, calling
              get_action() from your own code will create an infinite loop!
              See (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """

        memo = dict()
        if state.ply_count < 2:
            if 57 in state.actions():
                self.queue.put(57)
            else:
                middle = set.intersection(set(state.actions()), {57, 43, 44, 45, 56, 58, 69, 70, 71})
                self.queue.put(random.choice(list(middle)))
        # if state.ply_count < 2:
        #     self.queue.put(random.choice(state.actions()))
        else:
            time_limit = 100 / 1000
            stop_time = time.perf_counter() + time_limit
            best_move = None
            depth_limit = 6
            #             while time.perf_counter() <= stop_time:
            for depth in range(1, depth_limit + 1):
                best_move = memo.setdefault(state, self.minimax(state, depth_limit, stop_time))
                if time.perf_counter() >= stop_time:
                    break
            self.queue.put(best_move)

    #         else:
    #             self.queue.put(self.minimax(state, depth=3, stop_timer=None))

    def minimax(self, state, depth, stop_time):

        def min_value(state, depth, stop_time):
            #             print(depth)
            if state.terminal_test(): return state.utility(self.player_id)

            if time.perf_counter() >= stop_time: return self.score(state)
            if depth <= 0: return self.score(state)
            value = float("inf")
            # modification of the algorithm
            if self.is_divided(state): value = self.score(state)
            for action in state.actions():
                value = min(value, max_value(state.result(action), depth - 1, stop_time))
            return value

        def max_value(state, depth, stop_time):
            #             print(depth)
            if state.terminal_test(): return state.utility(self.player_id)

            if time.perf_counter() >= stop_time: return self.score(state)
            if depth <= 0: return self.score(state)
            value = float("-inf")
            # modification of the algorithm
            if self.is_divided(state): value = self.score(state)
            for action in state.actions():
                value = max(value, min_value(state.result(action), depth - 1, stop_time))
            return value

        return max(state.actions(), key=lambda x: min_value(state.result(x), depth - 1, stop_time))

    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)

    def is_divided(self, state):
        """Checks if the move allows to split the board with more
         liberties for custom agent than the opponent."""
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        if not any(set(own_liberties).intersection(set(opp_liberties))) and len(own_liberties) > len(opp_liberties):
            return True
        return False

