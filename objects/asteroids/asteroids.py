from __future__ import annotations
import math

from objects.asteroids.asteroids_action import *
from objects.spells import *
from images.graphic import *
import random

if TYPE_CHECKING:
    from controller.controller import *
    from objects.gameaction import *
    from typing import List, Callable
    from images.graphic import *
    from gamestate import *
    from objects.asteroids.asteroids_action import *


class Asteroid(GameObject):
    PHYSIC_CONSTANTS = PhysicConstants(mass=100, turn_rate=0.03,
                                       max_speed=5,
                                       speed_lose_coefficient=0,
                                       physic_radius=10,
                                       forward_force=5, backward_force=1,
                                       side_force=1)
    COLLISION_INFO = CollisionInfo(input_damage=0,
                                   output_damage=20,
                                   ignore_damage=False,
                                   ignored_types={GameObjectTypes.asteroid})
    BASE_CONTROLLER = EmptyController
    MAX_TIME_OF_LIFE = math.inf
    HEALTH_MAX = 1
    HEALTH_REGEN_RATE = 0
    ENERGY_MAX = 0
    ENERGY_REGEN_RATE = 0

    def _init_spells(self) -> List[Spell]:
        return []

    @property
    def get_graphic_info(self) -> GraphicInfo:
        return Graphic.A_METAL1.value

    @property
    def death_action(self) -> GameAction:
        return EmptyAction(self._game_state)

    @property
    def object_type(self) -> GameObjectTypes:
        return GameObjectTypes.asteroid

    @property
    def collision_info(self) -> CollisionInfo:
        return self.COLLISION_INFO


class Asteroid4(Asteroid):
    PHYSIC_CONSTANTS = PhysicConstants(mass=100, turn_rate=0,
                                       max_speed=2,
                                       speed_lose_coefficient=0,
                                       physic_radius=45,
                                       forward_force=5, backward_force=1,
                                       side_force=1)
    COLLISION_INFO = CollisionInfo(input_damage=0,
                                   output_damage=20,
                                   ignore_damage=False,
                                   ignored_types={GameObjectTypes.asteroid})
    HEALTH_MAX = 500
    HEALTH_REGEN_RATE = 0

    @property
    def death_action(self) -> GameAction:
        return SpawnAsteroid3(self, self._game_state, 2)


class Asteroid3(Asteroid):
    PHYSIC_CONSTANTS = PhysicConstants(mass=100, turn_rate=0,
                                       max_speed=2.5,
                                       speed_lose_coefficient=0,
                                       physic_radius=35,
                                       forward_force=5, backward_force=1,
                                       side_force=1)
    COLLISION_INFO = CollisionInfo(input_damage=0,
                                   output_damage=20,
                                   ignore_damage=False,
                                   ignored_types={GameObjectTypes.asteroid})
    HEALTH_MAX = 350
    HEALTH_REGEN_RATE = 0

    @property
    def death_action(self) -> GameAction:
        return SpawnAsteroid2(self, self._game_state, 3)


class SpawnAsteroid3(SpawnAsteroid):
    ASTEROID_CONSTRUCTOR = Asteroid3


class Asteroid2(Asteroid):
    PHYSIC_CONSTANTS = PhysicConstants(mass=100, turn_rate=0,
                                       max_speed=3,
                                       speed_lose_coefficient=0,
                                       physic_radius=28,
                                       forward_force=5, backward_force=1,
                                       side_force=1)
    COLLISION_INFO = CollisionInfo(input_damage=0,
                                   output_damage=20,
                                   ignore_damage=False,
                                   ignored_types={GameObjectTypes.asteroid})
    HEALTH_MAX = 150
    HEALTH_REGEN_RATE = 0

    @property
    def death_action(self) -> GameAction:
        return SpawnAsteroid1(self, self._game_state, 4)


class SpawnAsteroid2(SpawnAsteroid):
    ASTEROID_CONSTRUCTOR = Asteroid2


class Asteroid1(Asteroid):
    PHYSIC_CONSTANTS = PhysicConstants(mass=100, turn_rate=0,
                                       max_speed=4,
                                       speed_lose_coefficient=0,
                                       physic_radius=10,
                                       forward_force=5, backward_force=1,
                                       side_force=1)
    COLLISION_INFO = CollisionInfo(input_damage=0,
                                   output_damage=10,
                                   ignore_damage=False,
                                   ignored_types={GameObjectTypes.asteroid})
    HEALTH_MAX = 20
    HEALTH_REGEN_RATE = 0

    @property
    def death_action(self) -> GameAction:
        return EmptyAction(self._game_state)


class SpawnAsteroid1(SpawnAsteroid):
    ASTEROID_CONSTRUCTOR = Asteroid1
