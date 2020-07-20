from controller.ai import StandardAi
from gamestate import *
from const.globalconst import *
from objects.asteroids.asteroids import *
from objects.ships import *


class MakeAnyActionController(Controller):

    def update(self, game_object: GameObject, game_statet: GameState) -> None:
        pass

    @property
    def move_commands(self) -> Set[MoveCommands]:
        return {MoveCommands.move_forward, MoveCommands.rotate_left}

    @property
    def spell_commands(self) -> Set[int]:
        return {0, 1}


if __name__ == '__main__':
    game_state1 = GameState(
        physic=Physic(minimum_speed=0.000005),
        collider=Collider(),
        size=Vector(1500, 900))
    ship = Battleship(game_state=game_state1,
                      initial_position=game_state1.center_cord,
                      initial_direction=0,
                      initial_speed=Vector.zero(),
                      faction=Factions.player,
                      controller=MakeAnyActionController())
    game_state1.add_game_object(ship)
    enemy = ImperialFighter(game_state=game_state1,
                            initial_position=game_state1.center_cord
                                             + Vector(100, 100),
                            initial_direction=0,
                            initial_speed=Vector.zero(),
                            faction=Factions.empire,
                            controller=StandardAi())
    game_state1.add_game_object(enemy)
    ast = Asteroid4(game_state=game_state1,
                    initial_position=(
                            game_state1.center_cord +
                            Vector(-400, 500)),
                    initial_direction=10,
                    initial_speed=Vector(10, 0).rotate(10),
                    faction=Factions.asteroids,
                    controller=StandardAi())
    game_state1.add_game_object(ast)

    while True:
        game_state1.update_game_state()
