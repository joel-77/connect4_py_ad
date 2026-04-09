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
                # switch turn
                if self._state == GameState.TURN_RED:
                    self._state = GameState.TURN_YELLOW
                else:
                    self._state = GameState.TURN_RED
                return DropState.DROP_OK

        # fallback (shouldn't be reached because of COLUMN_FULL check)
        return DropState.COLUMN_FULL