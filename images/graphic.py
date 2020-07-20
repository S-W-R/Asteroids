from PyQt5.QtGui import QImage
from enum import *


class GraphicInfo:
    def __init__(self, scale_coefficient: float, sprite: QImage):
        self._sprite = sprite
        self._scale_coefficient = scale_coefficient

    @property
    def sprite(self) -> QImage:
        return self._sprite

    @property
    def scale_coefficient(self) -> float:
        return self._scale_coefficient


class Graphic(Enum):
    S_BATTLESHIP = GraphicInfo(1.3, QImage("./images/ships/battleshipW.png"))
    S_EMPIRE_FIGHTER = GraphicInfo(1, QImage("./images/ships/fighterY.png"))
    P_BLUE_LASER_1 = GraphicInfo(2,
                                 QImage("./images/projectiles/bluelaser1.png"))
    P_RED_LASER_1 = GraphicInfo(2,
                                QImage("./images/projectiles/redlaser1.png"))
    P_YELLOW_LASER_2 = GraphicInfo(1.5, QImage(
        "./images/projectiles/yellowlaser2.png"))
    A_METAL1 = GraphicInfo(1.1, QImage("./images/asteroids/metal1.png"))
