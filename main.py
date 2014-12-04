import draw
import ai
import copy

class Board(object):
    def __init__(self):
        self.x_coords = [] # list of (x,y) tuples
        self.y_coords = []
        self.coord_dict = {}
        self.translated_coord_dict = {}
        self.victory_coordlists = [[(1,1),(2,1),(3,1)],[(1,2),(2,2),(3,2)],[(1,3),(2,3),(3,3)],[(1,1),(1,2),(1,3)],[(2,1),(2,2),(2,3)],[(3,1),(3,2),(3,3)],[(1,1),(2,2),(3,3)],[(1,3),(2,2),(3,1)]]
        self.all_coords = [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(3,3)]

    def add_coord(self, player, coord):
        getattr(self, "{}_coords".format(player)).append(coord)
        self.coord_dict[coord] = player
        coord = self.translate_coord(coord)
        self.translated_coord_dict[coord] = player

    def translate_coord(self, coord):
        x = (coord[0] - 1) * 3 + coord[0]
        y = (coord[1] - 1) * 3 + 1 
        return (x,y)

    def get_board_copy(self):
        new_board = Board()
        for board_prop in ['x_coords','y_coords','coord_dict','translated_coord_dict']: 
            setattr(new_board, board_prop, copy.copy(getattr(self, board_prop)))
        return new_board

class TicTacToeGame(object):
    def __init__(self, params, fast_mode=False):
        self.params = params
        self.fast_mode = fast_mode
        self.board = Board()
        self.setup_players(self.params)

        self.drawer = draw.TicTacToeDraw(self.board)
        self.drawer.construct_and_print_board()
        self.player = 'x'

    def setup_players(self, params):
        self.x_ai = None
        self.y_ai = None
        if params[0] == 'y':
            self.x_ai = ai.AI('x',self.board, lookahead=False, fast_mode=self.fast_mode)
        if params[1] == 'y':
            self.y_ai = ai.AI('y',self.board, lookahead=True, fast_mode=self.fast_mode)

    def switch_player(self):
        if self.player == 'x':
            self.player = 'y'
        else:
            self.player = 'x'

    def run_turn(self):
        print "to move: player {}".format(self.player)
        player_ai = getattr(self, "{}_ai".format(self.player))
        if player_ai:
            incoming_coords = player_ai.get_move(self.board)
        else:
            incoming_coords = self.get_human_input()
        self.board.add_coord(self.player, incoming_coords)
        self.drawer.construct_and_print_board(self.board)
        end_game = self.check_end_game()
        if end_game:
            self.end_game(end_game)
            return end_game
        self.switch_player()

    def get_human_input(self):
        coords = input("please input move coords (x,y): ")
        if coords in self.board.coord_dict:
            print "that move is already taken!"
            return self.get_human_input()
        if type(coords) != tuple:
            print "please input coords like: (2,3)"
            return self.get_human_input()
        while coords[0] not in [1,2,3] or coords[1] not in [1,2,3]:
            print "those coords are not allowed! please choose two values from 1 to 3 like (2,3)"
            return self.get_human_input()
        return coords

    def check_end_game(self):
        for player in ['x', 'y']:
            player_coords = getattr(self.board, "{}_coords".format(player))
            for victory_coords in self.board.victory_coordlists:
                found = True
                for victory_coord in victory_coords:
                    if victory_coord not in player_coords:
                        found = False
                        break
                if found:
                    return player
        if len(self.board.coord_dict) == 9:
            return "nobody"

    def end_game(self, winner):
        print "Game over: {} wins".format(winner)

def start_game(params=None, return_winner=False, fast_mode=False):
    if not params:
        params = get_params()
    game = TicTacToeGame(params, fast_mode=fast_mode)
    while True:
        game_over = game.run_turn()
        if game_over:
            if return_winner:
                return game_over
            break

def get_params():
    p1_ai = raw_input("player one easy computer? (y,n): ")
    p2_ai = raw_input("player two hard computer? (y,n): ")
    return p1_ai,p2_ai

if __name__ == "__main__":
    start_game()
