"""Search Algos: MiniMax, AlphaBeta
"""
#TODO: you can import more modules, if needed
#TODO: update ALPHA_VALUE_INIT, BETA_VALUE_INIT in utils
import time
import numpy as np
ALPHA_VALUE_INIT = -np.inf
BETA_VALUE_INIT = np.inf # !!!!!

class SearchAlgos:
    def __init__(self, utility, succ, perform_move=None, goal=None):
        """The constructor for all the search algos.
        You can code these functions as you like to, 
        and use them in MiniMax and AlphaBeta algos as learned in class
        :param utility: The utility function.
        :param succ: The succesor function.
        :param perform_move: The perform move function.
        :param goal: function that check if you are in a goal state.
        """
        self.utility = utility
        self.succ = succ
        self.perform_move = perform_move
        self.goal = goal

    def search(self, state, depth, maximizing_player, start_time, turn_time, last_itration=False):
        pass


class MiniMax(SearchAlgos):

    def search(self, state, depth, maximizing_player, start_time, turn_time, last_itration = False):
        """Start the MiniMax algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """

        if self.goal(state) or depth == 0 or (time.time()-start_time > 0.92*turn_time and state.current_turn <= 17):
            return self.utility(state,maximizing_player), state.direction
        player = 2 if maximizing_player else 1
        children = self.succ(state, player)
        if last_itration and depth == 1:
            child_util = {child:self.utility(child, maximizing_player) for child in children}
            tmp_children = [k[0] for k in sorted(child_util.items(), key=lambda item: item[1])]
            children = tmp_children
        if maximizing_player:
            currMax = -np.inf
            currV = None
            for c in children:
                v = self.search(c, depth - 1, False, start_time, turn_time, last_itration)
                if v[0] > currMax:
                    currMax = v[0]
                    currV = v
            return currV
        else:
            currMin = np.inf
            currV = None
            for c in children:
                v = self.search(c, depth - 1, False, start_time, turn_time, last_itration)
                if v[0] < currMin:
                    currMin = v[0]
                    currV = v
            return currV



class AlphaBeta(SearchAlgos):

    def search(self, state, depth, maximizing_player, alpha=ALPHA_VALUE_INIT, beta=BETA_VALUE_INIT):
        """Start the AlphaBeta algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :param alpha: alpha value
        :param: beta: beta value
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        #TODO: erase the following line and implement this function.
        raise NotImplementedError
