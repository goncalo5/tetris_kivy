import time
import unittest
import main
from settings import *

class TestGame(unittest.TestCase):

    def setUp(self):
        pass

    def test_add_new_piece(self):
        print("\nadd_new_piece()")
        game = main.Game()
        old_pieces = game.pieces.copy()
        print(old_pieces)
        game.add_new_piece()
        new_pieces = game.pieces
        self.assertEqual(len(old_pieces) + 1, len(new_pieces))

    def test_update(self):
        game = main.Game()
        game.size = [1000, 1000]
        x, y = (500, 500)
        game.piece.pos = x, y
        game.vel = 100
        game.update(1)
        y -= game.vel
        self.assertEqual(game.piece.pos, [x, y])
        game.keys.add("right")
        game.update(1)
        x += TILESIZE
        y -= game.vel
        self.assertEqual(game.piece.pos, [x, y])
        game.keys.remove("right")
        game.keys.add("left")
        game.update(1)
        x -= TILESIZE
        y -= game.vel
        self.assertEqual(game.piece.pos, [x, y])
        game.keys = set()
        game.piece.y = 0
        game.update(1)
        self.assertEqual(game.pieces[-2].pos, [x, 0])

    def test__on_keyboard_down(self):
        game = main.Game()
        game._on_keyboard_down(None, None, 79, None, None)
        self.assertEqual(game.keys, {"right"})
        game._on_keyboard_down(None, None, 79, None, None)
        self.assertEqual(game.keys, {"right"})
        game._on_keyboard_down(None, None, 80, None, None)
        self.assertEqual(game.keys, {"right", "left"})
        game._on_keyboard_down(None, None, 80, None, None)
        self.assertEqual(game.keys, {"right", "left"})

    def test__on_keyboard_up(self):
        game = main.Game()
        game.keys.add("right")
        game._on_keyboard_up(None, None, 79, None, None)
        self.assertEqual(game.keys, set())
        game._on_keyboard_up(None, None, 79, None, None)
        self.assertEqual(game.keys, set())
        game.keys.add("right")
        game.keys.add("left")
        game._on_keyboard_up(None, None, 79, None, None)
        self.assertEqual(game.keys, {"left"})
        game._on_keyboard_up(None, None, 80, None, None)
        self.assertEqual(game.keys, set())

    def test_check_collisions(self):
        game = main.Game()
        game.size = [1000, 1000]
        game.n_tiles = 4
        game.tilesize = 250
        game.piece.y = 10
        game.check_collisions()
        # vertical collisions:
        self.assertEqual(game.piece.y, game.piece.y)
        game.piece.y = -10
        game.check_collisions()
        self.assertEqual(game.piece.y, game.height)
        self.assertEqual(game.pieces[-2].y, 0)
        # horizontal collisions:
        game.piece.pos = 0, 10
        game.check_collisions()
        self.assertEqual(game.piece.pos, game.piece.pos)
        game.piece.pos = -10, 10
        game.check_collisions()
        self.assertEqual(game.piece.pos, [0, 10])
        # piece-piece collisions:
        game.pieces = []
        piece = main.Piece(pos=(500, 0))
        game.pieces.append(piece)
        game.piece = main.Piece(pos=(500, 500))
        game.check_collisions()
        self.assertEqual(game.piece.y, 500)
        game.pieces = []
        piece = main.Piece(pos=(500, 0))
        game.pieces.append(piece)
        game.piece = main.Piece(pos=(500, 1))
        game.pieces.append(game.piece)
        game.check_collisions()
        self.assertEqual(game.pieces[-2].y, game.piece.height)
        piece_size = (200, 200)
        piece = main.Piece(pos=[600.0, 0], size=piece_size)
        game.piece = main.Piece(pos=[800.0, 100.52930300000013], size=piece_size)
        game.pieces = [piece, game.piece]
        game.check_collisions()
        self.assertEqual(game.piece.pos, [800.0, 100.52930300000013])
        game.size = [2000, 1400]
        piece_size = (200, 200)
        piece = main.Piece(pos=[1000.0, 0], size=piece_size)
        game.piece = main.Piece(pos=[1000.0, 150.94461800000005], size=piece_size)
        game.pieces = [piece, game.piece]
        print("\n\n\n")
        print([piece.pos for piece in game.pieces])
        game.check_collisions()
        print("\n\n\n")
        self.assertEqual(game.pieces[-2].pos, [1000.0, 200])

    def test_calc_borders(self):
        game = main.Game()
        game.size = [1000, 1000]
        game.n_tiles = 4
        game.tilesize = 200
        self.assertEqual(game.calc_borders(), [100, 900])
        game.size = [1000, 1000]
        game.n_tiles = 4
        game.tilesize = 250
        self.assertEqual(game.calc_borders(), [0, 1000])
        game.size = [1000, 1000]
        game.n_tiles = 5
        game.tilesize = 200
        self.assertEqual(game.calc_borders(), [0, 1000])
        game.size = [100, 100]
        with self.assertRaises(Exception):
            game.calc_borders()


if __name__ == '__main__':
    unittest.main()