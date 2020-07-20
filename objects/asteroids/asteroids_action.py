from __future__ import annotations

import random
from controller.controller import *
from objects.projectiles import *
from images.graphic import *
from objects.gameobject import *

if TYPE_CHECKING:
    from objects.asteroids.asteroids import Asteroid


class SpawnAsteroid(Spell):
    ASTEROID_CONSTRUCTOR = None  # type: Callable[[...], Asteroid]

    def __init__(self, game_object: GameObject, game_state: GameState,
                 count: int):
        super().__init__(game_object, game_state)
        self._item_count = count

    @property
    def reload_time(self) -> int:
        return 0

    @property
    def energy_cost(self) -> float:
        return 0

    def _check_other_condition(self) -> bool:
        return True

    def _spell_change_game_state(self):
        obj_pos = self._game_object.physic_info.position
        for i in range(self._item_count):
            init_dir = random.random() * math.pi * 2
            init_speed = Vector(10000, 0).rotate(init_dir)
            new_ast = self.ASTEROID_CONSTRUCTOR(game_state=self._game_state,
                                                initial_position=obj_pos,
                                                initial_direction=init_dir,
                                                initial_speed=init_speed,
                                                faction=Factions.asteroids,
                                                controller=EmptyController())
            self._game_state.add_game_object(new_ast)


