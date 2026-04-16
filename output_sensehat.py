from sense_hat import SenseHat
from game_token import GameToken
from output_base import OutputBase

class OutputSenseHat(OutputBase):
    # Farbdefinitionen (R, G, B)
    COLOR_GRID = (0, 0, 255)    # Blau
    COLOR_RED = (255, 0, 0)     # Rot
    COLOR_YELLOW = (255, 255, 0) # Gelb
    COLOR_EMPTY = (0, 0, 0)      # Schwarz / Aus
    
    # Das Spielfeld startet laut Grafik bei y=2 auf der Matrix
    BOARD_Y_OFFSET = 2

    def __init__(self):
        self.sense = SenseHat()
        self.sense.clear()

    def draw_grid(self) -> None:
        """
        Zeichnet das blaue Spielfeld auf die Matrix.
        Das Board ist 7 Spalten breit und 6 Zeilen hoch.
        """
        # Wir füllen den Bereich von x=0-6 und y=2-7 blau
        for x in range(7):
            for y in range(self.BOARD_Y_OFFSET, 8):
                self.sense.set_pixel(x, y, self.COLOR_GRID)

    def draw_token(self, x: int, y: int, token: GameToken = GameToken.EMPTY) -> None:
        """
        Setzt einen Spielstein an die angegebene Koordinate.
        x: 0-6 (Spalte)
        y: 0-5 (Reihe von oben nach unten)
        """
        # Umrechnung der Spiel-Koordinate in Matrix-Koordinate
        matrix_x = x
        matrix_y = y + self.BOARD_Y_OFFSET

        # Farbwahl basierend auf dem Token-Typ
        if token == GameToken.RED:
            color = self.COLOR_RED
        elif token == GameToken.YELLOW:
            color = self.COLOR_YELLOW
        else:
            # Falls das Feld leer sein soll, setzen wir es zurück auf die Grid-Farbe
            # oder Schwarz, je nachdem ob es Teil des Boards ist
            color = self.COLOR_GRID if y >= 0 else self.COLOR_EMPTY

        # Pixel auf der Matrix setzen
        if 0 <= matrix_x < 8 and 0 <= matrix_y < 8:
            self.sense.set_pixel(matrix_x, matrix_y, color)

if __name__ == '__main__':
    # Test-Code
    import time
    
    os = OutputSenseHat()
    os.draw_grid()
    
    # Test-Steine setzen
    os.draw_token(0, 5, GameToken.YELLOW) # Unten Links
    os.draw_token(1, 5, GameToken.RED)    # Daneben
    os.draw_token(3, 0, GameToken.YELLOW) # Oben Mitte
    
    time.sleep(2)
    print("SenseHat Test abgeschlossen.")