from game_token import GameToken
from game_state import GameState
from drop_state import DropState
from player_base import PlayerBase
from game_logic_base import GameLogicBase 
from util import Util

class Coordinator:
    """
    The Coordinator mediates between one or two player objects (subclasses
    of PlayerBase) and the game logic (a subclass of GameLogicBase). The
    easiest case is a local game of two players, e.g., 2 objects of
    PlayerConsole and a GameLogicLocal object.
    """

    def __init__(self, game_logic: GameLogicBase, player_red: PlayerBase, player_yellow: PlayerBase):
        """
        Create a Coordinator that mediates between the game_logic and the
        players player_red and player_yellow, which are passed as arguments. 
        """
        
        self._game_logic = game_logic  # either GameLogicLocal or GameLogicClient
        self._player_red = player_red
        self._player_yellow = player_yellow


    def run(self):

        # play game until won or draw
        while (True):

            # - get game state from logic
            state = self._game_logic.get_state()
            
            # - if game over: end game
            if state in [GameState.WON_RED, GameState.WON_YELLOW, GameState.DRAW]:
                # Draw the final board state
                player = self._player_red if state != GameState.WON_YELLOW else self._player_yellow
                player.draw_board(self._game_logic.get_board(), state)
                break
                
            # - get board from logic
            board = self._game_logic.get_board()
            
            # Identify current player based on state
            if state == GameState.TURN_RED:
                current_player = self._player_red
            elif state == GameState.TURN_YELLOW:
                current_player = self._player_yellow
            else:
                break
                
            # - draw the board for the current player
            current_player.draw_board(board, state)
            
            # - ask the current player for their turn
            column = current_player.play_turn()
            
            # - tell the game logic to execute that move
            self._game_logic.drop_token(current_player.get_player(), column)


# start a local game
if __name__ == '__main__':
    print("Welcome to Connect 4")

    from game_logic_local import GameLogicLocal

    # print(f"Util is Rapsberry Pi: {Util.isRaspberry()}")

    if Util.isRaspberry():
        from player_sensehat import PlayerSenseHat
    else:
        from player_console import PlayerConsole

    # create the appropriate player and game logic objects
    game_logic = GameLogicLocal()

    if Util.isRaspberry():
        player_red = PlayerSenseHat(GameToken.RED)
        player_yellow = PlayerSenseHat(GameToken.YELLOW)
    else:
        player_red = PlayerConsole(GameToken.RED)
        player_yellow = PlayerConsole(GameToken.YELLOW)
 

    coordinator = Coordinator(game_logic, player_red, player_yellow)
    coordinator.run() # start game
