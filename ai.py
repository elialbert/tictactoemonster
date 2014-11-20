from collections import defaultdict
import random
import copy
from time import sleep

class AI(object):
    def __init__(self,player,board, lookahead=True):
        self.board = board
        self.player = player
        self.lookahead=lookahead
        self.opponent = 'y' if player == 'x' else 'x'
        self.starting_moves = [(1,1),(3,1),(2,2),(1,3),(3,3)]

    def get_move(self, board):
        print "computer is thinking..."
        sleep(.5)
        self.board = board
        if not self.board.x_coords or not self.board.y_coords:
            return self.get_starting_move()
        winning, move = self.extend_chain()
        if winning:
            return move
        need_to_block = self.check_need_to_block()
        return need_to_block or move

    def get_starting_move(self):
        starting_moves = copy.copy(self.starting_moves)
        try:
            existing = self.board.coord_dict.keys()[0]
            if existing in starting_moves:
                starting_moves.remove(existing)
        except IndexError:
            pass
        return starting_moves[random.randint(0,len(starting_moves)-1)]

    def check_need_to_block(self, board=None, player=None, return_all=False):
        result_list = []
        board = board or self.board
        player = player or self.player
        opponent_coords, my_coords = self.get_coords(board=board, player=player)
        for victory_coordlist in board.victory_coordlists:
            num_found = 0
            not_found = None
            for victory_coord in victory_coordlist:
                if victory_coord in opponent_coords:
                    num_found += 1
                elif victory_coord not in board.coord_dict:
                    not_found = victory_coord
            if num_found == 2 and not_found:
                if return_all:
                    result_list.append(not_found)
                else:
                    return not_found
        if return_all:
            return result_list
        return False

    def extend_chain(self, board=None, player=None, depth=1):
        board = board or self.board
        player = player or self.player
        opponent_coords, my_coords = self.get_coords(board=board,player=player)
        available_extenders = []
        for victory_coordlist in board.victory_coordlists:
            num_found = 0
            not_found = None
            current_coord = None
            working_extender = {}
            for victory_coord in victory_coordlist:
                if victory_coord in my_coords:
                    num_found += 1
                    working_extender['current'] = victory_coord
                elif victory_coord not in board.coord_dict:
                    not_found = victory_coord
                    if working_extender.get('extension'):
                        working_extender['final'] = victory_coord
                    else:
                        working_extender['extension'] = not_found
                else: 
                    # if the opponent has already chosen one of the
                    # spots, do not consider for extension. 
                    # at least for right now.
                    working_extender = {}
            if num_found == 2 and not_found:
                return True, not_found # victory
            elif num_found == 1 and len(working_extender.keys()) == 3:
                available_extenders.append(working_extender)
        # print "found avail ext: {}".format(available_extenders)
        available = [x for x in board.all_coords if x not in board.coord_dict]
        if self.lookahead and available_extenders and depth == 1:
            lookahead_option = self.get_lookahead(player, available_extenders, depth)
            if lookahead_option:
                return False, lookahead_option
            elif not_found:
                return False, not_found

        return False, available[random.randint(0,len(available)-1)]


    def get_lookahead(self, player, available_extenders, depth):
        '''
        go over all available chain extension options and look
        ahead one move to determine if any of them force a victory
        (or allow a forced victory?)
        '''

        score_dict = {}

        for extender in available_extenders:
            for idx,extender_coord in enumerate([extender['extension'],extender['final']]):
                other_extender_coord = extender['extension'] if idx else extender['final']
                future_board = self.board.get_board_copy()
                future_board.add_coord(player, extender_coord)

                result = self.check_need_to_block(board=future_board, player=self.get_other_player(player), return_all=True)
                if len(result) > 1:
                    # print "found forced victory {}".format(extender_coord)
                    return extender_coord

                future_board.add_coord(self.get_other_player(player), other_extender_coord)
                result = self.check_need_to_block(board=future_board, player=player, return_all=True)
                if len(result) < 2:
                    # print "found safe answer: {}".format(extender_coord)
                    score_dict[extender_coord] = 5 if extender_coord not in self.starting_moves else 10
                # else:
                # print "attempting to avoid dangerous answer: {}".format(extender_coord)
        if score_dict:
            return sorted(score_dict.iteritems(),key=lambda(x):x[1], reverse=True)[0][0]

    def get_coords(self, board=None, player=None):
        board = board or self.board
        player = player or self.player
        opponent = self.get_other_player(player)
        opponent_coords = getattr(board,"{}_coords".format(opponent))
        my_coords = getattr(board,"{}_coords".format(player))
        return opponent_coords, my_coords

    def get_other_player(self, player):
        return 'x' if player == 'y' else 'y'
