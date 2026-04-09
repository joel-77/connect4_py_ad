from game_token import GameToken
from game_state import GameState
from drop_state import DropState
from game_logic_base import GameLogicBase


class GameLogicLocal(GameLogicBase):
    ROWS = 6
    COLS = 7

    def __init__(self):
        # initialize an empty board and set starting player to RED
        self._board = [[GameToken.EMPTY for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self._state = GameState.TURN_RED


    def get_state(self) -> GameState:
        # returns the current GameState
        return self._state


    def drop_token(self, player: GameToken, column: int) -> DropState:
        # returns a DropState (DROP_OK, COLUMN_INVALID, COLUMN_FULL, WRONG_PLAYER)
        if not (column >= 0 and column <= self.COLS - 1):
            return DropState.COLUMN_INVALID

        # check it's the correct player's turn
        if (self._state == GameState.TURN_RED and player != GameToken.RED) or \
           (self._state == GameState.TURN_YELLOW and player != GameToken.YELLOW):
            return DropState.WRONG_PLAYER

        # check if the column is full (top row occupied)
        if self._board[0][column] != GameToken.EMPTY:
            return DropState.COLUMN_FULL

        # find lowest empty row in the column and place the token
        for row in range(self.ROWS - 1,-1,-1):
            if self._board[row][column] == GameToken.EMPTY:
                self._board[row][column] = player

                # check if the current player has won
                if self._check_winner(player):
                    if player == GameToken.RED:
                        self._state = GameState.WON_RED
                    else:
                        self._state = GameState.WON_YELLOW
                # check for a draw (board completely full)
                elif self._is_board_full():
                    self._state = GameState.DRAW
                else:
                    # switch turn
                    if self._state == GameState.TURN_RED:
                        self._state = GameState.TURN_YELLOW
                    else:
                        self._state = GameState.TURN_RED
                return DropState.DROP_OK

        # fallback (shouldn't be reached because of COLUMN_FULL check)
        return DropState.COLUMN_FULL


    def _check_winner(self, player: GameToken) -> bool:
        """Check if the given player has 4 tokens in a row (horizontal, vertical, or diagonal)."""
        # horizontal
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                if (self._board[row][col] == player and
                    self._board[row][col+1] == player and
                    self._board[row][col+2] == player and
                    self._board[row][col+3] == player):
                    return True

        # vertical
        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                if (self._board[row][col] == player and
                    self._board[row+1][col] == player and
                    self._board[row+2][col] == player and
                    self._board[row+3][col] == player):
                    return True

        # diagonal (top-left to bottom-right)
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                if (self._board[row][col] == player and
                    self._board[row+1][col+1] == player and
                    self._board[row+2][col+2] == player and
                    self._board[row+3][col+3] == player):
                    return True

        # diagonal (bottom-left to top-right)
        for row in range(3, self.ROWS):
            for col in range(self.COLS - 3):
                if (self._board[row][col] == player and
                    self._board[row-1][col+1] == player and
                    self._board[row-2][col+2] == player and
                    self._board[row-3][col+3] == player):
                    return True

        return False


    def _is_board_full(self) -> bool:
        """Check if every cell on the board is occupied."""
        for col in range(self.COLS):
            if self._board[0][col] == GameToken.EMPTY:
                return False
        return True