from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import gamewindow
from gamestate import *

if __name__ == "__main__":
    game_state_test = GameState(
        physic=Physic(minimum_speed=0.000005),
        collider=Collider(),
        size=Vector(1500, 900))
    App = QApplication(sys.argv)
    window = gamewindow.GameWindow(game_state_test)
    sys.exit(App.exec())
