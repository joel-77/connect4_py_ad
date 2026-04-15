from input_base import InputBase
from input_base import Keys
from enum import Enum

import time

from sense_hat import SenseHat

sense = SenseHat()

class InputConsole(InputBase):
    """
    Input handler for Sensehat applications using Joystick input.

    Do not modify this class. 
    """

    # def key_pressed(self) -> bool:
    #     """
    #     Check if a key has been pressed.

    #     Returns:
    #         bool: True if a key is pressed, False otherwise.
    #     """
    #     if os.name == 'nt':
    #         return msvcrt.kbhit()
    #     else:
    #         dr, dw, de = select([sys.stdin], [], [], 0)
    #         return dr != []
    #         # return keyboard.read_event().event_type == keyboard.KEY_DOWN

    def read_key(self) -> Enum:
        """
        Read a key from the Sensehat and return its corresponding key code
        (i.e., the enumeration member of the Keys enum, as defined in input_base.py).

        Returns:
            The key code corresponding to the pressed key.
        """
        key = None
        while not key:
            events = sense.stick.get_events()
            for event in events:
                if event.action == "released": continue # ignore release events
                # print(f"Event {event.direction} {event.action}, at {event.timestamp}")
                key = event.direction
                break
            if not key: time.sleep(0.1)

        if key == "up":
            return Keys.UP
        elif key == "down":
            return Keys.DOWN
        elif key == "left":
            return Keys.LEFT
        elif key == "right":
            return Keys.RIGHT
        elif key == "middle":
            return Keys.ENTER
        # No ESC!
        return Keys.UNKNOWN

 

if __name__ == '__main__':
    print("Use this class to read the joystick input. Let's try it out:")
    print("Press any direction, ENTER (middle) to exit.")
    c = InputConsole()
    while True:
        key = c.read_key()
        print(f"Taste: {key}, Type: {type(key)}")
        if key == Keys.ENTER:
            print("You pressed Enter!")
            break
