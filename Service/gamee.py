import copy
import math
import random

from Repository.board import Board


class Game:
    def __init__(self, board: Board):
        self.board = board

    def __str__(self):
        return str(self.board)

    def human_move(self, col):
        """
        Record human's move on the board
        The human plays with R (from red)
        :param col: The col where the human wants to move
        :return: None
        """
        return self.board.move(col, "R")

    def check_for_win(self, symbol):
        """
        Check if the game is won
        :return: True if the game is won, False if not
        """
        # check for horizontal win
        for c in range(7 - 3):
            for r in range(6):
                if self.board.board[r][c] == symbol and self.board.board[r][c + 1] == symbol \
                        and self.board.board[r][c + 2] == symbol and self.board.board[r][c + 3] == symbol:
                    return True

        # check for vertical win
        for c in range(7):
            for r in range(6 - 3):
                if self.board.board[r][c] == symbol and self.board.board[r + 1][c] == symbol \
                        and self.board.board[r + 2][c] == symbol and self.board.board[r + 3][c] == symbol:
                    return True

        # check for diagonal win ( top-right to bottom-left)
        for c in range(7 - 3):
            for r in range(6 - 3):
                if self.board.board[r][c] == symbol and self.board.board[r + 1][c + 1] == symbol \
                        and self.board.board[r + 2][c + 2] == symbol and self.board.board[r + 3][c + 3] == symbol:
                    return True

        # # check for diagonal win ( top-right to bottom-left)
        for c in range(7 - 3):
            for r in range(3, 6):
                if self.board.board[r][c] == symbol and self.board.board[r - 1][c + 1] == symbol and \
                        self.board.board[r - 2][c + 2] == symbol and self.board.board[r - 3][c + 3] == symbol:
                    return True
        return False

    def check_if_full(self):
        """
        Check if the board game is full
        :return: True if the board is full, and False if not
        """
        for i in range(7):
            if self.board.get_position(0, i) == ' ':
                return False
        return True

    # AI - USING MINIMAX ALGORITHM

    def score_window(self, window: list, symbol: str):
        """
        Give score to a portion of 4 symbols
        :param window: List of 4 elements from the board
        :param symbol: "B", "R"
        :return: The score that the window obtained
        """
        score = 0
        count = 0
        empty = 0
        opp_symbol = 0
        for element in window:
            if element == symbol:
                count += 1
            elif element == ' ':
                empty += 1
            else:
                opp_symbol += 1
        # if we find a winning possibility to give maxim score
        if count == 4:
            score += 100
        elif count == 3 and empty == 1:  # 3 same color on the row
            score += 5
        elif count == 2 and empty == 2:
            score += 2

        if opp_symbol == 3 and empty == 1:
            score -= 4

        return score

    def score(self, symbol: str):
        """
        Score the board based on how good the scenario is
        :param symbol: "R" or "B"
        :return: The score of the board
        """

        score = 0
        # Score center column - the centerpieces have more opportunities (make diagonal easier)
        center_array = [self.board.board[i][3] for i in range(6)]
        center_count = 0
        for element in center_array:
            if element == symbol:
                center_count += 1
        score += center_count * 3

        # Score horizontal
        for r in range(6):
            # Create a list for every row of the board
            row_array = [str(i) for i in self.board.board[r]]
            for c in range(7 - 3):
                # partition every row by 4
                window = row_array[c:c + 4]
                score += self.score_window(window, symbol)
        # Score vertical
        for c in range(7):
            # Create a list for every column
            col_array = [self.board.board[i][c] for i in range(6)]
            for r in range(6 - 3):
                window = col_array[r:r + 4]
                score += self.score_window(window, symbol)
        # Score bottom-left, top-right diagonal
        for r in range(6 - 3):
            for c in range(7 - 3):
                window = [self.board.board[r + i][c + i] for i in range(4)]
                score += self.score_window(window, symbol)
        # Score bottom-right, top-left diagonal
        for r in range(6 - 3):
            for c in range(7 - 3):
                window = [self.board.board[r + 3 - i][c + i] for i in range(4)]
                score += self.score_window(window, symbol)

        return score

    def is_terminal(self):
        """
        Check if the game is finished: a player won/ the board is full
        :return: True if the game is finished
        """
        return self.check_for_win("R") or self.check_for_win("B") or self.check_if_full()

    def minimax(self, depth, maximizingPlayer):
        """
        Make the next move by evaluating the score of the board using depth-first-search. The AI wants to maximize his
        score, while the human player wants to minimize it
        :param depth: The depth of the game tree ( how many rounds the AI should play ahead )
        :param maximizingPlayer: True - if it is AI's turn, False - human turn
        :return: A tuple consisting of where the AI should move, and the best score
        """
        valid_positions = self.get_valid_positions()
        is_terminal = self.is_terminal()
        if depth == 0 or is_terminal:
            # check witch terminal case we have
            if is_terminal:
                # if we have the possibility to win return a high score
                if self.check_for_win("B"):
                    return None, 100000000
                elif self.check_for_win("R"):  # else return a small score
                    return None, -100000000
                else:  # Game over
                    return None, 0
            else:  # Depth is zero
                return None, self.score("B")
        if maximizingPlayer:  # if it's the AI's turn
            score = - math.inf  # we start with the smallest score
            best_col = 0
            for col in valid_positions:
                b_copy = copy.deepcopy(self)
                b_copy.board.move(str(col), "B")
                new_score = b_copy.minimax(depth-1, False)[1]  # get the score from the tuple
                if new_score > score:
                    score = new_score
                    best_col = col
            return best_col, score
        else:  # minimizing player
            score = math.inf  # we start with the highest score
            best_col = 0
            for col in valid_positions:
                b_copy = copy.deepcopy(self)
                b_copy.board.move(str(col), "R")
                new_score = b_copy.minimax(depth - 1, True)[1]
                if new_score < score:
                    score = new_score
                    best_col = col
            return best_col, score

    # find all the columns where we can make a move
    def get_valid_positions(self):
        """
        Find all the valid columns where a move can be made
        :return: List with the index of the valid columns
        """
        valid_positions = []
        for col in range(7):
            if self.board.get_position(0, col) == ' ':
                valid_positions.append(col)
        return valid_positions

    # pick best move that AI makes
    def pick_best_move(self):
        """
        Pick best move that AI should make
        :return: the column where the AI should move
        """
        valid_locations = self.get_valid_positions()
        best_score = -100
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            # make a deep copy (so that the initial board does not change) of the game
            # to see on witch position we make the best score
            temp_board = copy.deepcopy(self)
            temp_board.board.move(str(col), "B")
            # calculate its score and update best score
            score = temp_board.score("B")
            if score > best_score:
                best_score = score
                best_col = col

        return best_col
