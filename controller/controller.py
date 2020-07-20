from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Set
from const.globalconst import MoveCommands

if TYPE_CHECKING:
    from objects.gameobject import GameObject
    from gamestate import GameState


class Controller(ABC):

    @abstractmethod
    def update(self, game_object: GameObject, game_state: GameState) -> None:
        pass

    @property
    @abstractmethod
    def move_commands(self) -> Set[MoveCommands]:
        pass

    @property
    @abstractmethod
    def spell_commands(self) -> Set[int]:
        pass


class EmptyController(Controller):

    @property
    def move_commands(self):
        return set()

    @property
    def spell_commands(self):
        return set()

    def update(self, game_object: GameObject, game_state: GameState):
        pass


class PlayerController(Controller):
    def __init__(self):
        self._move_commands = set()
        self._spell_commands = set()

    @property
    def move_commands(self):
        return self._move_commands

    @move_commands.setter
    def move_commands(self, new_move_commands: Set[MoveCommands]):
        self._move_commands = new_move_commands

    @property
    def spell_commands(self):
        return self._spell_commands

    @spell_commands.setter
    def spell_commands(self, new_spell_commands: Set[int]):
        self._spell_commands = new_spell_commands

    def update(self, game_object: GameObject, game_states: GameState) -> None:
        pass
