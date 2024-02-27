import unittest

from Repository.board import Board
from Service.gamee import Game


class test_game(unittest.TestCase):
    def test_game1(self):
        board = Board()
        game = Game(board)
        game.human_move("2")
        self.assertEqual(game.board.get_position(5, 2), "R")
        # test if the board is full
        self.assertEqual(game.check_if_full(), False)
        game.human_move("2")
        game.human_move("2")
        row = game.human_move("2")
        # test check win
        self.assertEqual(game.check_for_win("R"), True)

    def test_game2(self):
        board = Board()
        game = Game(board)
        game.human_move("3")
        self.assertEqual(game.board.get_position(5, 3), "R")
        # test if the board is full
        self.assertEqual(game.check_if_full(), False)
        game.human_move("3")
        game.human_move("3")
        row = game.human_move("3")
        # test check win
        self.assertEqual(game.check_for_win("R"), True)
