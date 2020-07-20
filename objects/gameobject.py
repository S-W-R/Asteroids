from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from vectors.vector import *
from controller.controller import EmptyController
from physic.physic import PhysicInfo, PhysicConstants
from physic.collider import CollisionInfo
from const.globalconst import *

if TYPE_CHECKING:
    from controller.controller import *
    from objects.gameaction import *
    from typing import List
    from images.graphic import GraphicInfo
    from gamestate import GameState


class MainCharacteristic:
    def __init__(self, max_value: float, regen_rate: float):
        self._max_value = max_value
        self._current_value = max_value
        self._regen_rate = regen_rate

    @property
    def max_value(self) -> float:
        return self._max_value

    @property
    def regen_rate(self) -> float:
        return self._regen_rate

    @property
    def value(self) -> float:
        return self._current_value

    @value.setter
    def value(self, new_value):
        self._current_value = self.max_value \
            if new_value > self.max_value else new_value

    def update(self):
        self.value += self.regen_rate


class GameObject(ABC):
    BASE_CONTROLLER = EmptyController()  # type: Controller
    PHYSIC_CONSTANTS = None  # type: PhysicConstants
    COLLISION_INFO = None  # type: CollisionInfo
    MAX_TIME_OF_LIFE = math.inf  # type: float
    HEALTH_MAX = 0  # type: float
    HEALTH_REGEN_RATE = 0  # type: float
    ENERGY_MAX = 0  # type: float
    ENERGY_REGEN_RATE = 0  # type: float

    def __init__(self, game_state: GameState, initial_position: Vector,
                 initial_direction: float, initial_speed: Vector,
                 faction: Factions, controller: Controller):
        self.physic_info = PhysicInfo(self.PHYSIC_CONSTANTS, initial_position,
                                      initial_speed, initial_direction)
        self._is_deleted = False
        self._is_dead = False
        self._game_state = game_state
        self.controller = controller
        self._time_of_life = 0
        self._health = MainCharacteristic(self.HEALTH_MAX,
                                          self.HEALTH_REGEN_RATE)
        self._energy = MainCharacteristic(self.ENERGY_MAX,
                                          self.ENERGY_REGEN_RATE)
        self._spells = self._init_spells()
        self._faction = faction

    @abstractmethod
    def _init_spells(self) -> List[Spell]:
        pass

    @property
    def faction(self):
        return self._faction

    @property
    def time_of_life(self):
        return self._time_of_life

    @property
    def health(self) -> MainCharacteristic:
        return self._health

    @property
    def energy(self) -> MainCharacteristic:
        return self._energy

    @property
    def move_commands(self):
        return self.controller.move_commands

    @property
    def spell_commands(self):
        return self.controller.spell_commands

    @property
    @abstractmethod
    def get_graphic_info(self) -> GraphicInfo:
        pass

    @property
    @abstractmethod
    def object_type(self) -> GameObjectTypes:
        pass

    @property
    def spells(self) -> List[Spell]:
        return self._spells

    @property
    @abstractmethod
    def death_action(self) -> Spell:
        pass

    @property
    def is_deleted(self) -> bool:
        return self._is_deleted

    @property
    def is_dead(self) -> bool:
        return self._is_dead

    @property
    @abstractmethod
    def collision_info(self) -> CollisionInfo:
        pass

    def get_damage(self, damage_count: float):
        self.health.value -= damage_count

    def use_spells(self):
        for spell_command in self.spell_commands:
            self.try_use_spell(spell_command)

    def try_use_spell(self, spell_index: int):
        if spell_index < 0 or spell_index >= len(self.spells) \
                or not self.spells[spell_index].is_available():
            return
        self.energy.value -= self.spells[spell_index].energy_cost
        self.spells[spell_index].change_game_state()

    def update_base(self):
        self._time_of_life += 1
        self.health.update()
        self.energy.update()
        if self.health.value <= 0 or self.time_of_life > self.MAX_TIME_OF_LIFE:
            self.kill()

    def kill(self):
        self._is_dead = True

    def delete(self):
        self._is_deleted = True

    def update_controller(self):
        self.controller.update(self, self._game_state)

    def from_local_cord(self, cord: Vector) -> Vector:
        direction = self.physic_info.direction - math.pi / 2
        return cord.rotate(direction) + self.physic_info.position
