"""
MiniMax Player
"""
import numpy as np

from players.AbstractPlayer import AbstractPlayer
from SearchAlgos import *
import time

#TODO: you can import more modules, if needed

class Player(AbstractPlayer):
    def __init__(self, game_time):
        AbstractPlayer.__init__(self, game_time) # keep the inheritance of the parent's (AbstractPlayer) __init__()
        #TODO: initialize more fields, if needed, and the AlphaBeta algorithm from SearchAlgos.py
        self.board = None
        self.my_pos = None
        self.rival_pos = None
        self.turn = 0
        self.searchAlgo = MiniMax(utility=self.utility, succ=self.succ, goal=self.goal)
    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, of the board.
        No output is expected.
        """
        # TODO: erase the following line and implement this function.
        self.board = board
        self.my_pos = np.full(9, -1)
        self.rival_pos = np.full(9, -1)
        self.turn = 0


    def make_move(self, time_limit):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement
        """
        #TODO: erase the following line and implement this function.
        if self.turn < 18:
            move = self._stage_1_move(time_limit)
            self.turn += 1
            return move

        else:
            move = self._stage_2_move(time_limit)
            self.turn += 1
            return move


    def set_rival_move(self, move):
        """Update your info, given the new position of the rival.
        input:
            - move: tuple, the new position of the rival.
        No output is expected
        """
        # TODO: erase the following line and implement this function.
        rival_pos, rival_soldier, my_dead_pos = move

        if self.turn < 18:
            self.board[rival_pos] = 2
            self.rival_pos[rival_soldier] = rival_pos
        else:
            rival_prev_pos = self.rival_pos[rival_soldier]
            self.board[rival_prev_pos] = 0
            self.board[rival_pos] = 2
            self.rival_pos[rival_soldier] = rival_pos
        if my_dead_pos != -1:
            self.board[my_dead_pos] = 0
            dead_soldier = int(np.where(self.my_pos == my_dead_pos)[0][0])
            self.my_pos[dead_soldier] = -2
        self.turn += 1


    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed
    def _update_player_on_board(self, next_pos, prev_pos, soldier):
        # update position and board:
        self.board[next_pos] = 1
        self.board[prev_pos] = 0
        self.my_pos[soldier] = next_pos

    def _choose_rival_cell_to_kill(self, turn_time):  # we choose a rival cell to kill
        start_time = time.time()
        rival_pos = self.get_player_position(1)
        time_divisor = len(rival_pos)
        minmax_turn_time = turn_time/time_divisor
        max_val = ALPHA_VALUE_INIT
        rival_cell = -1
        for i in rival_pos:
            state = self.State(self.board, self.my_pos, self.rival_pos, self.turn)
            state.board[i] = 0
            rival_idx = np.where(state.rivalPositions == i)[0][0]       # i added this after finishing
            state.rivalPositions[rival_idx] = -2
            d = 1
            while True:
                value, move = self.searchAlgo.search(state=state, depth=d, maximizing_player=True, start_time=start_time, turn_time=minmax_turn_time)
                if max_val < value:
                    max_val = value
                    rival_cell = i
                d += 1
                if time.time() - start_time >= 0.05*minmax_turn_time:
                    value, move = self.searchAlgo.search(state=state, depth=d, maximizing_player=True, start_time=start_time, turn_time=minmax_turn_time, last_itration=True)
                    if max_val < value:
                        max_val = value
                        rival_cell = i
                    break
        return rival_cell


    def get_player_position(self, player_id, board=None):
        """
        :param player_id: 0/1/-1
        board: the current state board
        :return:
        """
        pos = []
        size = np.array(board).size
        if size == 24:
            for i in range(24):
                if board[i] == player_id + 1:
                    pos.append(i)
        else:
            for i in range(24):
                if self.board[i] == player_id + 1:
                    pos.append(i)
        return pos

    def _make_mill_get_rival_cell(self, turn_time):
        rival_cell = self._choose_rival_cell_to_kill(turn_time)
        rival_idx = np.where(self.rival_pos == rival_cell)[0][0]
        self.rival_pos[rival_idx] = -2
        self.board[rival_cell] = 0
        return rival_cell

    def _stage_1_choose_cell_and_soldier_to_move(self, turn_time):
        # cell = int(np.where(self.board == 0)[0][0])
        # soldier_that_moved = int(np.where(self.my_pos == -1)[0][0])
        # return cell, soldier_that_moved
        start_time = time.time()
        time_divisor = self.count_index_amount_in_board(0)
        minmax_turn_time = turn_time / time_divisor
        available_pos = self.get_player_position(-1)
        max_val = ALPHA_VALUE_INIT
        soldier_that_moved = -1
        cell = None
        for i in available_pos:
            state = self.State(self.board, self.my_pos, self.rival_pos, self.turn)
            state.board[i] = 1
            #tmp_soldier_that_moved = int(np.where(state.playerPositions == -1)[0][0])
            tmp_soldier_that_moved = self.soldier_that_move(state.playerPositions, -1)
            state.playerPositions[tmp_soldier_that_moved] = i
            d = 1
            while True:
                value, move = self.searchAlgo.search(state=state, depth=d, maximizing_player=True, start_time=start_time, turn_time=minmax_turn_time)
                if max_val < value:
                    max_val = value
                    cell = i
                    soldier_that_moved = tmp_soldier_that_moved
                d += 1
                if time.time() - start_time >= 0.4 * minmax_turn_time:
                    value, move = self.searchAlgo.search(state=state, depth=d, maximizing_player=True, start_time=start_time, turn_time=minmax_turn_time, last_itration=True)
                    if max_val < value:
                        max_val = value
                        cell = i
                        soldier_that_moved = tmp_soldier_that_moved
                    break
        return cell, soldier_that_moved

    def count_index_amount_in_board(self, index):
        count = 0
        for i in range(24):
            if self.board[i] == index:
                count += 1

        return count

    def _stage_1_move(self, turn_time) -> tuple:
        cell, soldier_that_moved = self._stage_1_choose_cell_and_soldier_to_move(turn_time*0.75)
        self.my_pos[soldier_that_moved] = cell     # 75% possible that there is no mill
        self.board[cell] = 1

        rival_cell = -1 if not self.is_mill(cell) else self._make_mill_get_rival_cell(turn_time)
        return cell, soldier_that_moved, rival_cell

    def _stage_2_move(self, turn_time) -> tuple:## posiblite direction change
        start_time = time.time()
        cell, soldier_that_moved = -1, -1
        soldiers_on_board = self.get_player_position(0)
        time_divisor = len(soldiers_on_board)
        minmax_turn_time = turn_time/time_divisor
        max_val = ALPHA_VALUE_INIT
        for soldier_cell in soldiers_on_board:
            direction_list = self.directions(int(soldier_cell))
            for direction in direction_list:
                if self.board[direction] == 0:
                    state = self.State(self.board, self.my_pos, self.rival_pos, self.turn)
                    state.board[soldier_cell] = 0
                    state.board[direction] = 1
                    #tmp_soldier_that_moved = int(np.where(state.playerPositions == soldier_cell)[0][0])
                    tmp_soldier_that_moved = self.soldier_that_move(state.playerPositions, soldier_cell)
                    state.playerPositions[tmp_soldier_that_moved] = direction
                    d = 1
                    while True:
                        value, move = self.searchAlgo.search(state=state, depth=d, maximizing_player=True, start_time=start_time, turn_time=minmax_turn_time)
                        if max_val < value:
                            max_val = value
                            cell = direction
                            soldier_that_moved = tmp_soldier_that_moved
                        d += 1
                        if time.time() - start_time >= minmax_turn_time * 0.9:
                            value, move = self.searchAlgo.search(state=state, depth=d, maximizing_player=True, start_time=start_time, turn_time=minmax_turn_time, last_itration=True)
                            if max_val < value:
                                max_val = value
                                cell = direction
                                soldier_that_moved = tmp_soldier_that_moved
                            break

        self._update_player_on_board(cell, self.my_pos[soldier_that_moved], soldier_that_moved)
        rival_cell = -1 if not self.is_mill(cell) else self._make_mill_get_rival_cell(minmax_turn_time)  # Check if mill

        return cell, soldier_that_moved, rival_cell


    ########## helper functions for AlphaBeta algorithm ##########
    # TODO: add here the utility, succ, an
    def utility(self, state, maximizing_player):
        if self.goal(state):
            return 1000
        h1 = self.diff_mill_count(state.board, maximizing_player)
        h2 = self.incomplate_mill_count(state.board)
        h3 = self.remaining_soldier_count(state)
        return 3*h1 + 2*h2 + 4*h3


    def diff_mill_count(self, board, maximizing_player):
        count_1 = 0
        count_2 = 0
        player_pos = self.get_player_position(0, board)
        rival_pos = self.get_player_position(1, board)
        for i in player_pos:
            if self.check_next_mill(i, 1, board):
                count_1 += 1
        for i in rival_pos:
            if self.check_next_mill(i, 2, board):
                count_2 += 1
        if maximizing_player:
            return count_1
        return count_2

    def incomplate_mill_count(self, board):
        count_1 = 0
        count_2 = 0
        available_pos = self.get_player_position(-1, board)
        for i in available_pos:
            if self.check_next_mill(i, 1, board):
                count_1 += 1
            if self.check_next_mill(i, 2, board):
                count_2 += 1
        return count_1-count_2

    def remaining_soldier_count(self, state):
        player_count = np.count_nonzero(state.playerPositions >= 0)
        rival_count = np.count_nonzero(state.rivalPositions >= 0)
        if state.current_turn > 17:
            if rival_count < 3 or self.player_cant_move(2, state):
                return BETA_VALUE_INIT
            if player_count < 3:
                return ALPHA_VALUE_INIT
        return player_count-rival_count

    def succ(self, state, player):

        if state.current_turn < 18:
            return self.succ_phase1_player(state, player)
        else:
            return self.succ_phase2_player(state, player)

    def succ_phase1_player(self, state, player):
        available_pos = self.get_player_position(-1, state.board)
        state_succ_array = []
        for i in available_pos:
            tmp_state = self.State(state.board, state.playerPositions, state.rivalPositions, state.current_turn+1)
            tmp_state.board[i] = player
            if player == 1:
                #soldier_that_moved = int(np.where(tmp_state.playerPositions == -1)[0][0])
                soldier_that_moved = self.soldier_that_move(tmp_state.playerPositions, -1)
                tmp_state.playerPositions[soldier_that_moved] = i
            else:
                #soldier_that_moved = int(np.where(tmp_state.rivalPositions == -1)[0][0])
                soldier_that_moved = self.soldier_that_move(tmp_state.rivalPositions, -1)
                tmp_state.rivalPositions[soldier_that_moved] = i
            if self.is_mill(i, tmp_state.board):    #we need to see all possible boards with rival soldier dead
                state_succ_array += self.make_mill_get_board_without_rival(tmp_state, 3-player)
            else:
                state_succ_array.append(tmp_state)


        return state_succ_array

    def succ_phase2_player(self, state, player):
        state_succ_array = []
        soldiers_on_board = self.get_player_position(player-1, board=state.board)
        for soldier_cell in soldiers_on_board:
            direction_list = self.directions(int(soldier_cell))
            for direction in direction_list:
                if state.board[direction] == 0:
                    tmp_state = self.State(state.board, state.my_pos, state.rival_pos, state.current_turn+1)
                    tmp_state.board[soldier_cell] = 0
                    tmp_state.board[direction] = player
                    if player == 1:
                        #tmp_soldier_that_moved = int(np.where(tmp_state.playerPositions == soldier_cell)[0][0])
                        tmp_soldier_that_moved = self.soldier_that_move(tmp_state.playerPositions, soldier_cell)
                        tmp_state.playerPositions[tmp_soldier_that_moved] = direction
                    else:
                        #tmp_soldier_that_moved = int(np.where(tmp_state.rivalPositions == soldier_cell)[0][0])
                        tmp_soldier_that_moved = self.soldier_that_move(tmp_state.rivalPositions, soldier_cell)
                        tmp_state.rivalPositions[tmp_soldier_that_moved] = direction
                    if self.is_mill(direction, tmp_state.board):  # we need to see all possible boards with rival soldier dead
                        state_succ_array += self.make_mill_get_board_without_rival(tmp_state, 3 - player)
                    else:
                        state_succ_array.append(tmp_state)

        return state_succ_array




    def make_mill_get_board_without_rival(self, state, rival_player):
        rival_pos = self.get_player_position(rival_player-1, board=state.board)
        state_succ_array = []
        for i in rival_pos:
            tmp_state = self.State(state.board, state.playerPositions, state.rivalPositions, state.current_turn)
            tmp_state.board[i] = 0
            if rival_player == 1:
                #soldier_that_moved = int(np.where(tmp_state.playerPositions == i)[0][0])
                soldier_that_moved = self.soldier_that_move(tmp_state.playerPositions, i)
                tmp_state.playerPositions[soldier_that_moved] = -2
                state_succ_array.append(tmp_state)
            else:
                #soldier_that_moved = int(np.where(tmp_state.rivalPositions == i)[0][0])
                soldier_that_moved = self.soldier_that_move(tmp_state.rivalPositions, i)
                tmp_state.rivalPositions[soldier_that_moved] = -2
                state_succ_array.append(tmp_state)

        return state_succ_array


    def goal(self, state):
        if state.current_turn > 17:
            player_count = np.count_nonzero(state.playerPositions == -2)
            rival_count = np.count_nonzero(state.rivalPositions == -2)
            num_move_1 = self.player_cant_move(1, state)
            num_move_2 = self.player_cant_move(2, state)
            if rival_count > 6 or player_count > 6:
                return True
            if num_move_1 == 0 or num_move_2 == 0:
                return True
        return False

    def player_cant_move(self, player_id, state):

        player_pos = self.get_player_position(player_id, state.board)
        all_next_positions = [(player_current_pos, player_next_pos)
                              for player_current_pos in player_pos
                              for player_next_pos in self.directions(player_current_pos)]
        possible_next_positions = [pos for pos in all_next_positions if self.pos_feasible_on_board(pos[1], state.board)]
        return len(possible_next_positions)
        #count_1 = self.movable_soldiers_num(state.board, player_id)
        #return count_1

    def pos_feasible_on_board(self, pos, board):

        # on board
        on_board = (0 <= pos < 24)
        if not on_board:
            return False

        # free cell
        value_in_pos = board[pos]
        free_cell = (value_in_pos == 0)
        return free_cell

    def soldier_that_move(self, player_pos, val):
        for i in range(9):
            if player_pos[i] == val:
                return i
        return -4

    # def calc_movable_soldiers(self, board):
    #
    #     total_movable_soldiers = [0, 0]
    #     total_movable_soldiers[0] = self.movable_soldiers_num(board, 1)
    #     total_movable_soldiers[1] = self.movable_soldiers_num(board, 2)
    #
    #     if self.turn > 17:
    #         if total_movable_soldiers[1] == 0:
    #             return np.inf
    #         if total_movable_soldiers[0] == 0:
    #             return -np.inf
    #
    #     return total_movable_soldiers[0] - total_movable_soldiers[1]
    #
    # def movable_soldiers_num(self, board, player):
    #
    #     movable_soldiers = 0
    #     for i in range(24):
    #         if board[i] == player:
    #             adjacent = self.directions(i)
    #             count = 0
    #             for j in adjacent:
    #                 if board[j] == 0:
    #                     count += 1
    #                 if count != 0:
    #                     movable_soldiers += 1
    #         return movable_soldiers