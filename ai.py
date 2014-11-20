import random
import copy
from time import sleep

class AI(object):
    def __init__(self,player,board):
        self.board = board
        self.player = player
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

    def check_need_to_block(self):
        opponent_coords = self.board.x_coords
        my_coords = self.board.y_coords
        for victory_coordlist in self.board.victory_coordlists:
            num_found = 0
            not_found = None
            for victory_coord in victory_coordlist:
                if victory_coord in opponent_coords:
                    num_found += 1
                elif victory_coord not in self.board.coord_dict:
                    not_found = victory_coord
            if num_found == 2 and not_found:
                return not_found
        return False

    def extend_chain(self):
        my_coords = self.board.y_coords
        opponent_coords = self.board.x_coords
        for victory_coordlist in self.board.victory_coordlists:
            num_found = 0
            not_found = None
            for victory_coord in victory_coordlist:
                if victory_coord in my_coords:
                    num_found += 1
                elif victory_coord not in self.board.coord_dict:
                    not_found = victory_coord
            if num_found == 2 and not_found:
                return True, not_found # victory
        if not not_found:
            available = [x for x in self.board.all_coords if x not in self.board.coord_dict]
            return False, available[random.randint(0,len(available)-1)]
        return False, not_found
