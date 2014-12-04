import main
import draw
import ai
from collections import defaultdict

class TestBoard():
    def test_add_coord(self):
        b=main.Board()
        b.add_coord('x',(1,1))
        assert(len(b.coord_dict) == 1)
        assert(b.coord_dict.values()[0] == 'x')

    def test_translate_coord(self):
        b=main.Board()
        t=b.translate_coord((2,2))
        assert(t==(5,4))

    def test_get_board_copy(self):
        b=main.Board()
        b.add_coord('x',(1,1))
        b2=b.get_board_copy()
        b2.add_coord('y',(1,2))
        assert(len(b.coord_dict) == 1)
        assert(len(b2.coord_dict) == 2)

class TestGame():
    # tests the AI at a high level. 
    # Y should win more often because it has lookahead mode enabled.
    def test_full(self):
        counts = defaultdict(int)
        for i in range(500):
            winner = main.start_game(params=('y','y'), return_winner=True, fast_mode=True)
            counts[winner] += 1
        assert(counts['y'] > counts['x'])
            
