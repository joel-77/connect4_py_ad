import sys
from game_state import GameState
from player_base import PlayerBase
from input_base import Keys
from output_base import *
from util import Util

if Util.isRaspberry():
    from input_sensehat import InputSenseHat
    from output_sensehat import OutputSenseHat
else:
    print("PlayerSenseHat can only be used on a Raspberry Pi with Sense HAT.")
    sys.exit(1)


class PlayerSenseHat(PlayerBase):
    def __init__(self, player: GameToken):  # Red or Yellow player
        super().__init__(player)
        self._output = OutputSenseHat()  # use this class for Sense HAT output
        self._input = InputSenseHat()    # use this class for Sense HAT input

    def play_turn(self) -> int:
        # return desired column from user input (0..6)
        # use self._input to read keys, use self._output to draw current token position
        y = -1
        x = 3

        while True:
            self._output.draw_token(x, y, self._player)
            key = self._input.read_key()

            if key == Keys.RIGHT:
                if x < 6:
                    self._output.draw_token(x, y)
                    x += 1
            elif key == Keys.LEFT:
                if x > 0:
                    self._output.draw_token(x, y)
                    x -= 1
            elif key == Keys.ENTER:
                self._output.draw_token(x, y)
                return x

    def draw_board(self, board: list, state: GameState) -> None:
        # draw grid with tokens using self._output
        self._output.draw_grid()
        for y, val_y in enumerate(board):
            for x, val_yx in enumerate(val_y):
                self._output.draw_token(x, y, val_yx)


if __name__ == '__main__':
    # use the code below to test your implementation

    # creates an empty board
    board = [[GameToken.EMPTY for _ in range(7)] for _ in range(6)]

    # put some tokens at 'impossible' locations
    # note: board[row][column]
    board[0][0] = GameToken.RED     # top left corner
    board[0][6] = GameToken.YELLOW  # top right corner
    board[4][3] = GameToken.RED     # 2nd but last row, middle position

    p = PlayerSenseHat(GameToken.YELLOW)  # this is the yellow player ('0')

    # draw board for the player yellow using Sense HAT output
    # also tell the yellow player that it's yellow's turn
    p.draw_board(board, GameState.TURN_YELLOW)
    # you should now see the board with the 3 'impossible' tokens

    # now let's ask yellow for their turn (using Sense HAT input/output)
    pos = p.play_turn()

    # print out the position for you to check if it's correct
    print(f"Position selected: {pos}")

    row = 5  # put yellow's token in the last row
    board[row][pos] = GameToken.YELLOW  # put yellow's token on the board

    # now, after yellow has made their turn, redraw board for the *yellow*
    # player so they can see what has changed (using Sense HAT input/output)
    # also tell the *yellow* player that it's now red's turn
    p.draw_board(board, GameState.TURN_RED)