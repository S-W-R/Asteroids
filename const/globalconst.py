from enum import *


@unique
class MoveCommands(Enum):
    move_forward = auto()
    move_left = auto()
    move_right = auto()
    move_backward = auto()
    rotate_left = auto()
    rotate_right = auto()


@unique
class Factions(Enum):
    player = auto()
    asteroids = auto()
    pirates = auto()
    empire = auto()
    aliens = auto()


@unique
class GameObjectTypes(Enum):
    asteroid = auto(),
    ship = auto(),
    projectile = auto(),

@unique
class States(Enum):
    playing = auto(),
    paused = auto(),
    win = auto(),
    lose = auto()
