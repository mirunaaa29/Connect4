from Service.gamee import Game


class UI:
    def __init__(self, game: Game):
        self.game = game

    def start(self):
        humans_turn = True
        print(str(self.game))
        while True:  # While the game is not finished
            if humans_turn:
                human_move = input("Input the column where you want to move(0<= column <=6) You play with R: ")
                try:
                    # make a move
                    self.game.human_move(human_move)
                    # print the board after every move
                    print(str(self.game))
                    won = 0
                    if self.game.check_for_win("R"):
                        print(" YOU WON! ◝(ᵔᵕᵔ)◜")
                        won = 1
                        return
                    if self.game.check_if_full() and won == 0:
                        print(" DRAW ")
                        return
                    humans_turn = not humans_turn
                except ValueError as ve:
                    print(ve)
            else:
                col, minimax_score = self.game.minimax(4, True)
                self.game.board.move(str(col), "B")
                print(str(self.game))
                won = 0
                if self.game.check_for_win("B"):
                    print(" COMPUTER WON! ")
                    won = 1
                    return
                if self.game.check_if_full() and won == 0:
                    print(" DRAW ")
                    return
                humans_turn = not humans_turn

