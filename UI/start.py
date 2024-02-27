from Repository.board import Board
from Service.gamee import Game
from UI.ui import UI

board = Board()
game = Game(board)
ui = UI(game)
ui.start()
