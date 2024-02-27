from texttable import Texttable


class Board:
    def __init__(self):
        """
        Create the Connect4 board: a matrix of 6 rows and 7 columns
        """
        self.board = [[' ' for _ in range(7)] for _ in range(6)]

    def get_position(self, row, column):
        """
        Get the symbol from the position (row, column) of the board
        :param row:
        :param column:
        :return: R, B, ' '
        """
        return self.board[row][column]

    def move(self, col: str, symbol):
        """
        Represent a move on the board
        :raise ValueError if the move is outside the board, if the column is full,the col is not an integer
        or the symbol is invalid
        :param col: The column that we want to place the symbol at
        :param symbol: R (red), B (blue)
        :return: The row where the move was made (to check for win)
        """
        if symbol not in ['R', 'B']:
            raise ValueError("Invalid symbol")
        if col.isdigit():
            col = int(col)
            if col > 6:
                raise ValueError("Move outside the board")
            if self.board[0][col] != ' ':
                raise ValueError("The column is full, you can not make a move there")
        else:
            raise ValueError("The column has to be a digit")

        i = 5
        while i >= 0:
            # look for the first empty cell
            if self.board[i][col] == ' ':
                self.board[i][col] = symbol  # make the move
                return i
            i -= 1

    def __str__(self):
        """
        Return the board string representation
        :return: String form of board
        """
        table = Texttable()
        for row in range(0, 6):
            table.add_row(self.board[row])
        return table.draw()
