# This file is part of the DGTCentaur Mods open source software
# ( https://github.com/Alistair-Crompton/DGTCentaurMods )
#
# DGTCentaur Mods is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# DGTCentaur Mods is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see
#
# https://github.com/Alistair-Crompton/DGTCentaurMods/blob/master/LICENSE.md
#
# This and any other notices must remain intact and unaltered in any
# distribution, modification, variant, or derivative of this software.

from DGTCentaurMods.classes.Plugin import Plugin, Centaur
from DGTCentaurMods.consts import Enums, fonts

import chess, random

QUESTIONS_COUNT:int = 20

# The plugin must inherits of the Plugin class.
# Filename must match the class name.
class Squiz(Plugin):

    # Constructor for initialization stuff
    # The id is the name of the plugin/class
    def __init__(self, id:str):
        super().__init__(id)

        self.initialize()

    # Initialization function,
    # invoked on each new game.
    def initialize(self):
        self._started:bool = False
        self._qindex:int = 0
        self._bonus:int = QUESTIONS_COUNT*3

    # Game ends.
    def game_over(self):

        Centaur.clear_screen()

        Centaur.print("GAME", row=2, font=fonts.DIGITAL_FONT)
        Centaur.print("OVER", row=4, font=fonts.DIGITAL_FONT)
        
        Centaur.print("SCORE", row=7)

        score = int(self._bonus * 100 / (QUESTIONS_COUNT*3))

        Centaur.print('%'+str(score), font=fonts.DIGITAL_FONT)

        Centaur.print("Press PLAY", row=11)
        Centaur.print("To retry!")

        self.initialize()

    # Generate a new question,
    # choosing a random square then displaying it.
    def generate_question(self):

        # Next question...
        self._qindex += 1

        # Do we reach the limit?
        if self._qindex == QUESTIONS_COUNT+1:
            self.game_over()
            return

        Centaur.clear_screen()

        # We create a random square.
        # The square_name function needs a number from 0 to 63.
        self._random_square = chess.square_name(random.randint(0,63))

        Centaur.print("Question", row=2)
        Centaur.print(str(self._qindex), font=fonts.DIGITAL_FONT)

        Centaur.print("Please place", row=5)
        Centaur.print("a piece on")
        Centaur.print()
        Centaur.print(self._random_square, font=fonts.DIGITAL_FONT)

    # This function is automatically invoked when
    # the user launches the plugin.
    def start(self):
        super().start()

        Centaur.clear_screen()
        Centaur.print("SQUIZ", font=fonts.DIGITAL_FONT, row=2)
        Centaur.print("Push PLAY", row=5)
        Centaur.print("to")
        Centaur.print("start")
        Centaur.print("the game!")

    # This function is (automatically) invoked when
    # the user stops the plugin
    def stop(self):

        # Back to the main menu.
        super().stop()

    # This function is automatically invoked each
    # time the player press a key.
    # Except the BACK key which is handled by the engine.
    def key_callback(self, key:Enums.Btn):

        if key == Enums.Btn.PLAY and not self._started:
            Centaur.sound(Enums.Sound.COMPUTER_MOVE)

            self._started = True
            
            self.generate_question()

        # If the user press HELP,
        # we display the correct square.
        if key == Enums.Btn.HELP and self._started:
            Centaur.sound(Enums.Sound.TAKEBACK_MOVE)
            Centaur.flash(self._random_square)

    # This function is automatically invoked each
    # time the player moves a piece.
    def field_callback(self,
                square:str,
                field_action:Enums.PieceAction,
                web_move:bool):
        
        if not self._started:
            return
        
        # We care only when the user drop a piece.
        if field_action == Enums.PieceAction.PLACE:

            Centaur.flash(square)

            # Correct answer?
            if self._random_square == square:
                Centaur.sound(Enums.Sound.CORRECT_MOVE)

                # Next question...
                self.generate_question()

            else:
                Centaur.sound(Enums.Sound.WRONG_MOVE)
                Centaur.print("WRONG!", row=11)

                # Wrong answer, we decrease the bonus.
                self._bonus -= 1

                if self._bonus == 0:
                    self.game_over()