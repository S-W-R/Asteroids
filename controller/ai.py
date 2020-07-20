from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Set, Optional
from const.globalconst import *
from controller.controller import *
from vectors.vector import *

if TYPE_CHECKING:
    from objects.gameobject import GameObject
    from gamestate import GameState


class ObjectAI(Controller, ABC):
    def __init__(self):
        self._game_object = None  # type: Optional[GameObject]
        self._game_state = None  # type: Optional[GameState]
        self._move_commands = set()  # type: Set[MoveCommands]
        self._spell_commands = set()  # type: Set[int]

    def update(self, game_object: GameObject, game_state: GameState) -> None:
        if self._game_object is None and self._game_state is None:
            self._game_state = game_state
            self._game_object = game_object
        self._move_commands.clear()
        self._spell_commands.clear()
        self._update_ai(game_object, game_state)

    @property
    def move_commands(self) -> Set[MoveCommands]:
        return self._move_commands

    @move_commands.setter
    def move_commands(self, new_move_commands: Set[MoveCommands]):
        self._move_commands = new_move_commands

    @property
    def spell_commands(self) -> Set[int]:
        return self._spell_commands

    @spell_commands.setter
    def spell_commands(self, new_spell_commands: Set[int]):
        self._spell_commands = new_spell_commands

    @abstractmethod
    def _update_ai(self, game_object: GameObject, game_state: GameState):
        pass


class StandardAi(ObjectAI):
    def __init__(self):
        super().__init__()
        self._target = None  # type: Optional[GameObject]

    def _update_ai(self, game_object: GameObject, game_state: GameState):
        if self._target is None or self._target.is_deleted:
            self._target = self._get_new_target(game_object, game_state)
        if self._target is None:
            self.spell_commands = set()
            self.move_commands = set()
            return
        self.spell_commands = self._get_spell_commands(game_object, game_state)
        self.move_commands = self._get_move_commands(game_object, game_state)

    @staticmethod
    def _get_new_target(game_object: GameObject, game_state: GameState):
        for obj in game_state.game_objects:
            if obj.object_type is GameObjectTypes.ship \
                    and game_state.is_enemies(game_object, obj):
                return obj
        return None

    def _get_move_commands(self, game_object: GameObject,
                           game_state: GameState) -> Set[MoveCommands]:
        move_commands = {MoveCommands.move_forward}
        expected_vector = (self._target.physic_info.position -
                           game_object.physic_info.position)
        angle = game_object.physic_info.direction
        current_vector = Vector(1, 0).rotate(angle)
        determinant = (current_vector.x * expected_vector.y -
                       current_vector.y * expected_vector.x)
        rotate = (MoveCommands.rotate_left if determinant > 0
                  else MoveCommands.rotate_right)
        move_commands.add(rotate)
        return move_commands

    def _get_spell_commands(self, game_object: GameObject,
                           game_state: GameState) -> Set[int]:
        angle = game_object.physic_info.direction
        current_vector = Vector(1, 0).rotate(angle)
        expected_vector = (self._target.physic_info.position -
                           game_object.physic_info.position)
        angle_between = current_vector.angle_between(expected_vector)
        if abs(angle_between) < math.pi / 4 and expected_vector.length < 450:
            return {0}
        return set()
