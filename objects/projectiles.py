import math
from controller.controller import *
from images.graphic import *
from objects.gameaction import *
from objects.gameobject import *
from physic.physic import PhysicConstants
from typing import List


class RedLaser(GameObject):
    PHYSIC_CONSTANTS = PhysicConstants(mass=100, turn_rate=0.02, max_speed=18,
                                       speed_lose_coefficient=0.0051,
                                       physic_radius=10,
                                       forward_force=5, backward_force=1,
                                       side_force=1)
    COLLISION_INFO = CollisionInfo(input_damage=100,
                                   output_damage=40,
                                   ignore_damage=True,
                                   ignored_types={GameObjectTypes.projectile})
    BASE_CONTROLLER = EmptyController()
    MAX_TIME_OF_LIFE = 80
    HEALTH_MAX = 1
    HEALTH_REGEN_RATE = 0
    ENERGY_MAX = 1
    ENERGY_REGEN_RATE = 0

    def _init_spells(self) -> List[Spell]:
        return []

    @property
    def get_graphic_info(self) -> GraphicInfo:
        return Graphic.P_RED_LASER_1.value

    @property
    def death_action(self) -> GameAction:
        return EmptyAction(self._game_state)

    @property
    def object_type(self) -> GameObjectTypes:
        return GameObjectTypes.projectile

    @property
    def collision_info(self) -> CollisionInfo:
        return self.COLLISION_INFO


class BlueLaser(GameObject):
    PHYSIC_CONSTANTS = PhysicConstants(mass=100, turn_rate=0.02, max_speed=18,
                                       speed_lose_coefficient=0.01,
                                       physic_radius=4,
                                       forward_force=5, backward_force=1,
                                       side_force=1)
    COLLISION_INFO = CollisionInfo(input_damage=100,
                                   output_damage=5,
                                   ignore_damage=True,
                                   ignored_types=set())
    BASE_CONTROLLER = EmptyController()
    MAX_TIME_OF_LIFE = 70
    HEALTH_MAX = 1
    HEALTH_REGEN_RATE = 0
    ENERGY_MAX = 1
    ENERGY_REGEN_RATE = 0

    def _init_spells(self) -> List[Spell]:
        return []

    @property
    def get_graphic_info(self) -> GraphicInfo:
        return Graphic.P_BLUE_LASER_1.value

    @property
    def death_action(self) -> GameAction:
        return EmptyAction(self._game_state)

    @property
    def object_type(self) -> GameObjectTypes:
        return GameObjectTypes.projectile

    @property
    def collision_info(self) -> CollisionInfo:
        return self.COLLISION_INFO


class YellowLaser2(GameObject):
    PHYSIC_CONSTANTS = PhysicConstants(mass=100, turn_rate=0, max_speed=17,
                                       speed_lose_coefficient=0.025,
                                       physic_radius=5,
                                       forward_force=0, backward_force=0,
                                       side_force=0)
    COLLISION_INFO = CollisionInfo(input_damage=100,
                                   output_damage=10,
                                   ignore_damage=True,
                                   ignored_types=set())
    BASE_CONTROLLER = EmptyController()
    MAX_TIME_OF_LIFE = 70
    HEALTH_MAX = 1
    HEALTH_REGEN_RATE = 0
    ENERGY_MAX = 1
    ENERGY_REGEN_RATE = 0

    def _init_spells(self) -> List[Spell]:
        return []

    @property
    def get_graphic_info(self) -> GraphicInfo:
        return Graphic.P_YELLOW_LASER_2.value

    @property
    def death_action(self) -> GameAction:
        return EmptyAction(self._game_state)

    @property
    def object_type(self) -> GameObjectTypes:
        return GameObjectTypes.projectile

    @property
    def collision_info(self) -> CollisionInfo:
        return self.COLLISION_INFO
