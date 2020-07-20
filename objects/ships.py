from __future__ import annotations
import math
from objects.spells import *
from images.graphic import *

if TYPE_CHECKING:
    from controller.controller import *
    from objects.gameaction import *
    from typing import List
    from images.graphic import *
    from gamestate import *


class Battleship(GameObject):
    PHYSIC_CONSTANTS = PhysicConstants(mass=60, turn_rate=0.03,
                                       max_speed=5,
                                       speed_lose_coefficient=0.01,
                                       physic_radius=30,
                                       forward_force=5, backward_force=1,
                                       side_force=1)
    COLLISION_INFO = CollisionInfo(input_damage=0,
                                   output_damage=20,
                                   ignore_damage=False,
                                   ignored_types=set())
    BASE_CONTROLLER = EmptyController
    MAX_TIME_OF_LIFE = math.inf
    HEALTH_MAX = 500
    HEALTH_REGEN_RATE = 0.05
    ENERGY_MAX = 300
    ENERGY_REGEN_RATE = 0.5

    def _init_spells(self) -> List[Spell]:
        return [AttackLaserRed(self, self._game_state),
                AttackLaserYellow2(self, self._game_state)]

    @property
    def get_graphic_info(self) -> GraphicInfo:
        return Graphic.S_BATTLESHIP.value

    @property
    def death_action(self) -> GameAction:
        return EmptyAction(self._game_state)

    @property
    def object_type(self) -> GameObjectTypes:
        return GameObjectTypes.ship

    @property
    def collision_info(self) -> CollisionInfo:
        return self.COLLISION_INFO


class ImperialFighter(GameObject):
    PHYSIC_CONSTANTS = PhysicConstants(mass=10, turn_rate=0.03,
                                       max_speed=7,
                                       speed_lose_coefficient=0.01,
                                       physic_radius=12,
                                       forward_force=1, backward_force=1,
                                       side_force=1)
    COLLISION_INFO = CollisionInfo(input_damage=0,
                                   output_damage=20,
                                   ignore_damage=False,
                                   ignored_types={GameObjectTypes.ship,
                                                  GameObjectTypes.asteroid})
    BASE_CONTROLLER = EmptyController
    MAX_TIME_OF_LIFE = math.inf
    HEALTH_MAX = 50
    HEALTH_REGEN_RATE = 0.01
    ENERGY_MAX = 100
    ENERGY_REGEN_RATE = 10

    def _init_spells(self) -> List[Spell]:
        return [AttackLaserBlue(self, self._game_state)]

    @property
    def get_graphic_info(self) -> GraphicInfo:
        return Graphic.S_EMPIRE_FIGHTER.value

    @property
    def object_type(self) -> GameObjectTypes:
        return GameObjectTypes.ship

    @property
    def death_action(self) -> GameAction:
        return EmptyAction(self._game_state)

    @property
    def collision_info(self) -> CollisionInfo:
        return self.COLLISION_INFO
