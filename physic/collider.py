from __future__ import annotations
from vectors.vector import *
from const.globalconst import MoveCommands
import math
from typing import TYPE_CHECKING, Set, List
from const.globalconst import *
from physic.physic import PhysicConstants

if TYPE_CHECKING:
    from objects.gameobject import GameObject
    from gamestate import GameState


class CollisionInfo:
    def __init__(self, input_damage: float, output_damage: float,
                 ignore_damage: bool, ignored_types: Set[GameObjectTypes]):
        self._input_damage = input_damage
        self._output_damage = output_damage
        self._is_ignore_damage = ignore_damage
        self._ignored_types = ignored_types

    @property
    def input_damage(self) -> float:
        return self._input_damage

    @property
    def output_damage(self) -> float:
        return self._output_damage

    @property
    def ignore_damage(self) -> bool:
        return self._is_ignore_damage

    @property
    def ignored_types(self) -> Set[GameObjectTypes]:
        return self._ignored_types


class Collider:
    def collision_interact(self, game_object1: GameObject,
                           game_object2: GameObject) -> None:
        col_info1 = game_object1.collision_info
        col_info2 = game_object2.collision_info
        game_object1.get_damage(col_info1.input_damage)
        game_object2.get_damage(col_info2.input_damage)
        if not col_info1.ignore_damage:
            game_object1.get_damage(col_info2.output_damage)
        if not col_info2.ignore_damage:
            game_object2.get_damage(col_info1.output_damage)

    def simple_collision(self, game_state: GameState,
                         ships: List[GameObject],
                         projectiles: List[GameObject]) -> None:
        for i in range(len(ships)):
            for j in range(i + 1, len(ships)):
                ship1 = ships[i]
                ship2 = ships[j]
                if self._must_interact(game_state, ship1, ship2):
                    self.collision_interact(ship1, ship2)
        for ship in ships:
            for projectile in projectiles:
                if self._must_interact(game_state, ship, projectile):
                    self.collision_interact(ship, projectile)

    def _must_interact(self, game_state: GameState, game_object1: GameObject,
                       game_object2: GameObject) -> bool:
        return (game_state.is_enemies(game_object1, game_object2) and
                self._can_interact(game_object1, game_object2) and
                self._is_intersect(game_object1, game_object2))

    def _can_interact(self, game_object1: GameObject,
                      game_object2: GameObject) -> bool:
        obj1_ignored_types = game_object1.collision_info.ignored_types
        obj2_ignored_types = game_object2.collision_info.ignored_types
        return not (game_object2.object_type in obj1_ignored_types or
                    game_object1.object_type in obj2_ignored_types)

    def _is_intersect(self, game_object1: GameObject,
                      game_object2: GameObject) -> bool:
        distance_between = (game_object1.physic_info.position -
                            game_object2.physic_info.position).length
        radius_sum = (game_object1.physic_info.physic_constants.radius +
                      game_object2.physic_info.physic_constants.radius)
        return distance_between < radius_sum
