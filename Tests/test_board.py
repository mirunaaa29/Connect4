import unittest

from Repository.board import Board


class test_board(unittest.TestCase):
    def test_board1(self):
        board = Board()
        board.move("2", "R")
        self.assertEqual(board.get_position(5, 2), "R")
        try:
            board.move("move", "R")
            assert False
        except ValueError:
            assert True
        try:
            board.move("2", "br")
            assert False
        except ValueError:
            assert True

    def test_board2(self):
        board = Board()
        board.move("3", "B")
        self.assertEqual(board.get_position(5, 3), "B")
        board.move("3", "R")
        self.assertEqual(board.get_position(4, 3), "R")
        try:
            board.move("wrong input", "R")
            assert False
        except ValueError:
            assert True
        try:
            board.move("10", "B")
            assert False
        except ValueError:
            assert True
            