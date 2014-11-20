

class TicTacToeDraw(object):
    def __init__(self, board):
        self.board = board

    def construct_and_print_board(self, board = None):
        if board:
            self.board = board
        board_lines = self.construct_board()
        self.print_board(board_lines)

    def print_board(self, board_lines):
        print "board: "
        print "----------------\n\n"
        
        for line in board_lines:
            print line

        print "\n\n----------------\n\n"

    def construct_board(self):
        lines = []
        for line_number in range(9):
            lines.append(self.construct_line(line_number))
        return lines
            
    def construct_line(self, line_number):
        line_string = ''
        for col_number in range(11):
            if col_number in [3,7]:
                line_string += '|'
            else:
                if line_number in [0,1,3,4,6,7,8]:
                    line_string += self.get_entry(line_number, col_number)
                elif line_number in [2,5]:
                    line_string += '_'
        return line_string
                
    def get_entry(self, line_number, col_number):
        val = self.board.coord_dict.get((col_number, line_number),' ')
        return val
