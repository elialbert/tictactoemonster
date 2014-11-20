import draw
import ai

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



class TicTacToeGame(object):
    def __init__(self):
        self.board = Board()
        self.ai = ai.AI('y',self.board)
        self.drawer = draw.TicTacToeDraw(self.board)
        self.drawer.construct_and_print_board()
        self.player = 'x'

    def switch_player(self):
        if self.player == 'x':
            self.player = 'y'
        else:
            self.player = 'x'

    def run_turn(self):
        print "to move: player {}".format(self.player)
        if self.player == 'y':
            incoming_coords = self.ai.get_move(self.board)
        else:
            incoming_coords = input("please input move coords (x,y): ")
        self.board.add_coord(self.player, incoming_coords)
        self.drawer.construct_and_print_board(self.board)
        victory = self.check_victory()
        if victory:
            self.end_game(victory)
            return True
        self.switch_player()

    def check_victory(self):
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

    def end_game(self, winner):
        print "Game over: {} wins".format(winner)

def start_game():
    game = TicTacToeGame()
    while True:
        game_over = game.run_turn()
        if game_over:
            break

if __name__ == "__main__":
    start_game()
