from __future__ import annotations

import random
from controller.controller import *
from objects.projectiles import *
from images.graphic import *
from objects.gameobject import *

if TYPE_CHECKING:
    pass


class AttackLaserRed(Spell):
    INITIAL_SPEED = 14
    SPREAD_ANGLE = 15

    @property
    def reload_time(self) -> int:
        return 17

    @property
    def energy_cost(self) -> float:
        return 25

    def _spell_change_game_state(self):
        radius = self._game_object.physic_info.physic_constants.radius
        # self._spawn_red_laser_with_local_cord(Vector(-radius/4, radius))
        # self._spawn_red_laser_with_local_cord(Vector(radius/4, radius))
        self._spawn_red_laser_with_local_cord(Vector(0, radius), 0,
                                              self.SPREAD_ANGLE)

    def _spawn_red_laser_with_local_cord(self, local_cord: Vector,
                                         local_angle: float,
                                         spread_angle: float):
        obj_physic_info = self._game_object.physic_info
        initial_position = self._game_object.from_local_cord(local_cord)
        init_dir = (obj_physic_info.direction + local_angle +
                    spread_angle * math.pi / 180 * (1 / 2 - random.random()))
        initial_speed = obj_physic_info.speed + Vector(1, 0).rotate(init_dir) \
            .normalize_to(self.INITIAL_SPEED)
        projectile = RedLaser(game_state=self._game_state,
                              initial_position=initial_position,
                              initial_direction=init_dir,
                              initial_speed=initial_speed,
                              faction=self._game_object.faction,
                              controller=RedLaser.BASE_CONTROLLER)
        self._game_state.add_game_object(projectile)

    def _check_other_condition(self) -> bool:
        return True


class AttackLaserYellow2(Spell):
    INITIAL_SPEED = 14
    SPREAD_ANGLE = 35

    @property
    def reload_time(self) -> int:
        return 10

    @property
    def energy_cost(self) -> float:
        return 20

    def _spell_change_game_state(self):
        radius = self._game_object.physic_info.physic_constants.radius
        self._spawn_yellow_laser(Vector(-radius / 2, -radius / 2),
                                 math.pi / 6,
                                 self.SPREAD_ANGLE)
        self._spawn_yellow_laser(Vector(radius / 2, -radius / 2),
                                 -math.pi / 6,
                                 self.SPREAD_ANGLE)
        self._spawn_yellow_laser(Vector(0, radius), 0, self.SPREAD_ANGLE)

    def _spawn_yellow_laser(self, local_cord: Vector, local_angle: float,
                            spread_angle: float):
        obj_physic_info = self._game_object.physic_info
        initial_position = self._game_object.from_local_cord(local_cord)
        init_dir = (obj_physic_info.direction + local_angle +
                    spread_angle * math.pi / 180 * (1 / 2 - random.random()))
        initial_speed = obj_physic_info.speed + Vector(1, 0).rotate(init_dir) \
            .normalize_to(self.INITIAL_SPEED)
        projectile = YellowLaser2(game_state=self._game_state,
                                  initial_position=initial_position,
                                  initial_direction=init_dir,
                                  initial_speed=initial_speed,
                                  faction=self._game_object.faction,
                                  controller=RedLaser.BASE_CONTROLLER)
        self._game_state.add_game_object(projectile)

    def _check_other_condition(self) -> bool:
        return True


class AttackLaserBlue(Spell):
    INITIAL_SPEED = 10
    SPREAD_ANGLE = 30

    @property
    def reload_time(self) -> int:
        return 13

    @property
    def energy_cost(self) -> float:
        return 10

    def _spell_change_game_state(self):
        radius = self._game_object.physic_info.physic_constants.radius
        angle = 0 * math.pi / 180 * (1 / 2 - random.random())
        self._spawn_blue_laser(Vector(-radius / 2, 0), 0, self.SPREAD_ANGLE)
        self._spawn_blue_laser(Vector(radius / 2, 0), 0, self.SPREAD_ANGLE)

    def _spawn_blue_laser(self, local_cord: Vector, local_angle: float,
                          spread_angle: float):
        obj_physic_info = self._game_object.physic_info
        initial_position = self._game_object.from_local_cord(local_cord)
        init_dir = (obj_physic_info.direction + local_angle +
                    spread_angle * math.pi / 180 * (1 / 2 - random.random()))
        initial_speed = obj_physic_info.speed + Vector(1, 0).rotate(init_dir) \
            .normalize_to(self.INITIAL_SPEED)
        projectile = BlueLaser(game_state=self._game_state,
                               initial_position=initial_position,
                               initial_direction=init_dir,
                               initial_speed=initial_speed,
                               faction=self._game_object.faction,
                               controller=RedLaser.BASE_CONTROLLER)
        self._game_state.add_game_object(projectile)

    def _check_other_condition(self) -> bool:
        return True
