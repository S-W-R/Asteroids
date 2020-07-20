from __future__ import annotations

import functools

from vectors.vector import Vector
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.gameobject import GameObject
    from gamestate import GameState


class GameAction(ABC):
    def __init__(self, game_state: GameState):
        self._game_state = game_state

    @abstractmethod
    def change_game_state(self):
        pass


class EmptyAction(GameAction):

    def change_game_state(self):
        pass


class Spell(GameAction, ABC):
    def __init__(self, game_object: GameObject, game_state: GameState):
        super().__init__(game_state)
        self._game_object = game_object
        self._last_use_time = 0

    @property
    def last_use_time(self):
        return self._last_use_time

    @property
    @abstractmethod
    def reload_time(self) -> int:
        pass

    @property
    @abstractmethod
    def energy_cost(self) -> float:
        pass

    def is_available(self) -> bool:
        return self._game_object.energy.value > self.energy_cost \
               and self.__time_since_last_use > self.reload_time \
               and self._check_other_condition()

    @property
    def __time_since_last_use(self):
        return self._game_state.current_iteration - self.last_use_time

    @abstractmethod
    def _check_other_condition(self) -> bool:
        pass

    def change_game_state(self):
        self._last_use_time = self._game_state.current_iteration
        self._spell_change_game_state()

    @abstractmethod
    def _spell_change_game_state(self):
        pass
