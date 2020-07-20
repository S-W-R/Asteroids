from __future__ import annotations
from vectors.vector import *
from const.globalconst import MoveCommands
import math
from typing import TYPE_CHECKING, Set

if TYPE_CHECKING:
    from objects.gameobject import GameObject


class PhysicConstants:
    def __init__(self, mass: float, turn_rate: float,
                 max_speed: float, speed_lose_coefficient: float,
                 physic_radius: float, forward_force: float,
                 backward_force: float, side_force: float):
        self._mass = mass
        self._turn_rate = turn_rate
        self._max_speed = max_speed
        self._speed_lose_coefficient = speed_lose_coefficient
        self._physic_radius = physic_radius
        self._forward_force = forward_force
        self._backward_force = backward_force
        self._side_force = side_force

    @property
    def mass(self):
        return self._mass

    @property
    def turn_rate(self):
        return self._turn_rate

    @property
    def max_speed(self):
        return self._max_speed

    @property
    def speed_lose_coefficient(self):
        return self._speed_lose_coefficient

    @property
    def radius(self):
        return self._physic_radius

    @property
    def forward_force(self):
        return self._forward_force

    @property
    def backward_force(self):
        return self._backward_force

    @property
    def side_force(self):
        return self._side_force


class PhysicInfo:
    def __init__(self, physic_constants: PhysicConstants, position: Vector,
                 speed: Vector = Vector(0, 0), direction=0):
        self._physic_constants = physic_constants
        self.position = position
        self.speed = speed
        self._direction = direction

    @property
    def physic_constants(self):
        return self._physic_constants

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, new_dir: float):
        self._direction = new_dir % (2 * math.pi)


class Physic:
    def __init__(self, minimum_speed: float):
        self._minimum_speed = minimum_speed

    def update_move_object(self, game_object: GameObject, size: Vector):
        obj_info = game_object.physic_info
        acceleration = self.__calc_acceleration(game_object)
        new_speed = self.__calc_new_speed(game_object, acceleration)
        if new_speed.length < self._minimum_speed:
            new_speed = Vector.zero()
        obj_info.position = self.__calc_new_position(obj_info.position,
                                                     new_speed, size)
        obj_info.direction = self.__calc_new_dir(game_object)
        obj_info.speed = new_speed

    @staticmethod
    def __calc_new_position(old_position: Vector, speed: Vector, size: Vector):
        new_position = old_position + speed
        return Vector(new_position.x % size.x, new_position.y % size.y)

    @staticmethod
    def __calc_new_speed(game_object: GameObject, acceleration: Vector):
        obj_info = game_object.physic_info
        obj_const = obj_info.physic_constants
        new_speed = obj_info.speed + acceleration
        if new_speed.length > obj_const.max_speed:
            new_speed = new_speed.normalize_to(obj_const.max_speed)
        return new_speed.multiple(1 - obj_const.speed_lose_coefficient)

    @staticmethod
    def __calc_acceleration(game_object: GameObject):
        obj_info = game_object.physic_info
        obj_const = obj_info.physic_constants
        move_commands = game_object.move_commands
        force_sum = Vector(0, 0)
        if MoveCommands.move_forward in move_commands:
            force_sum += Vector(obj_const.forward_force, 0) \
                .rotate(obj_info.direction)
        if MoveCommands.move_backward in move_commands:
            force_sum += Vector(obj_const.backward_force, 0) \
                .rotate(obj_info.direction + math.pi)
        if MoveCommands.move_left in move_commands:
            force_sum += Vector(obj_const.side_force, 0) \
                .rotate(obj_info.direction + math.pi / 2)
        if MoveCommands.move_right in move_commands:
            force_sum += Vector(obj_const.side_force, 0) \
                .rotate(obj_info.direction - math.pi / 2)
        return force_sum.div(obj_const.mass)

    @staticmethod
    def __calc_new_dir(game_object: GameObject):
        obj_info = game_object.physic_info
        obj_const = obj_info.physic_constants
        move_commands = game_object.move_commands
        new_dir = obj_info.direction
        if MoveCommands.rotate_left in move_commands:
            new_dir += obj_const.turn_rate
        if MoveCommands.rotate_right in move_commands:
            new_dir -= obj_const.turn_rate
        return new_dir
