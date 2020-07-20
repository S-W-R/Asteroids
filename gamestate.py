from __future__ import annotations
from objects.ships import *
from physic.collider import Collider
from physic.physic import Physic
from vectors.vector import *
from objects.gameobject import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class GameState:
    def __init__(self, physic: Physic, collider: Collider, size: Vector):
        self.game_objects = set()  # type: Set[GameObject]
        self._physic = physic
        self._collider = collider
        self._size = size
        self._player_controller = None
        self._current_iteration = 0
        self.current_state = States.playing
        self._future_game_objects = set()  # type: Set[GameObject]
        self._optimisation_ships = set()  # type: Set[GameObject]
        self._optimisation_projectiles = set()  # type: Set[GameObject]
        self._optimisation_asteroids = set()  # type: Set[GameObject]

    @property
    def current_iteration(self):
        return self._current_iteration

    @property
    def size(self):
        return self._size

    @property
    def height(self):
        return self._size.y

    @property
    def width(self):
        return self._size.x

    @property
    def center_cord(self) -> Vector:
        return self.size.div(2)

    def add_game_object(self, new_game_object: GameObject):
        self._future_game_objects.add(new_game_object)

    def is_enemies(self, obj1: GameObject, obj2: GameObject) -> bool:
        return obj1.faction != obj2.faction

    def update_game_state(self):
        if self.current_state is not States.playing:
            return None
        self._current_iteration += 1
        deleted_objects = set()
        for game_object in self.game_objects:  # type: GameObject
            if game_object.is_dead:
                game_object.death_action.change_game_state()
                game_object.delete()
            if game_object.is_deleted:
                deleted_objects.add(game_object)
                continue
            game_object.update_base()
            self._physic.update_move_object(game_object, self.size)
            game_object.use_spells()
            game_object.update_controller()
        if self.current_iteration % 3 == 0:
            self.__update_collision()
        self.__add_new_game_objects()
        for deleted_object in deleted_objects:
            self.game_objects.remove(deleted_object)
            self._optimisation_ships.discard(deleted_object)
            self._optimisation_asteroids.discard(deleted_object)
            self._optimisation_projectiles.discard(deleted_object)

    def __update_collision(self):
        ships = list(
            self._optimisation_ships.union(self._optimisation_asteroids))
        projectiles = list(self._optimisation_projectiles)
        self._collider.simple_collision(self, ships, projectiles)

    def __add_new_game_objects(self):
        for new_object in self._future_game_objects:
            self.game_objects.add(new_object)
            if new_object.object_type is GameObjectTypes.ship:
                self._optimisation_ships.add(new_object)
            if new_object.object_type is GameObjectTypes.asteroid:
                self._optimisation_asteroids.add(new_object)
            if new_object.object_type is GameObjectTypes.projectile:
                self._optimisation_projectiles.add(new_object)
        self._future_game_objects.clear()
