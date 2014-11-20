import random
import copy

class AI(object):
    def __init__(self,player,board):
        self.board = board
        self.player = player
        self.starting_moves = [(1,1),(3,1),(2,2),(1,3),(3,3)]

    def get_move(self, board):
        self.board = board
        if not self.x_coords or not self.y_coords:
            return self.get_starting_move()
        move = self.check_need_to_block()
        if not move:
            move = self.extend_chain()

    def get_starting_move(self):
        starting_moves = copy.copy(self.starting_moves)
        try:
            existing = self.board.coord_dict.keys()[0]
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
                if victory_coord in opponent_coords and victory_coord not in my_coords:
                    num_found += 1
                elif victory_coord not in self.board.coord_dict:
                    not_found = victory_coord
            if num_found == 2:
                return not_found
        return False

    def extend_chain(self):
        my_coords = self.board.y_coords
        opponent_coords = self.board.x_coords
        for victory_coordlist in self.board.victory_coordlists:
            num_found = 0
            not_found = None
            for victory_coord in victory_coordlist:
                if victory_coord in my_coords and victory_coord not in opponent_coords:
                    num_found += 1
                elif victory_coord not in self.board.coord_dict:
                    not_found = victory_coord
            if num_found == 2:
                return not_found # victory
        if not not_found:
            available = [x for x in self.board.all_coords if x not in self.board.coord_dict]
            return available[random.randint(0,len(available)-1)]
        return not_found
