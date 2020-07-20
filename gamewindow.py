from __future__ import annotations

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.Qt import Qt, QPointF
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QTransform, QPixmap, QColor
from PyQt5.QtWidgets import *

from objects.ships import *
from objects.asteroids.asteroids import *
from controller.ai import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gamestate import GameState
    from physic.physic import *


class GameWindow(QMainWindow):
    BACKGROUND_COLOR = QColor(17, 10, 21, 255)

    def __init__(self, game_state: GameState):
        super().__init__()
        self.__init_game_state(game_state)
        self.__init_window()
        self.__init_timer()

    def __init_window(self):
        self.graphic_label = QtWidgets.QLabel()
        self.graphic_label.setAlignment(Qt.AlignHCenter)
        canvas = QtGui.QPixmap(400, 300)
        self.graphic_label.setPixmap(canvas)
        self.setCentralWidget(self.graphic_label)
        self.setWindowTitle("Asteroids")
        self.show()

    def __init_game_state(self, game_state: GameState):
        self.game_state = game_state
        self.player_controller = PlayerController()
        self.key_down_set = set()
        player_obj = Battleship(game_state=self.game_state,
                                initial_position=self.game_state.center_cord,
                                initial_direction=0,
                                initial_speed=Vector.zero(),
                                faction=Factions.player,
                                controller=self.player_controller)
        self.player_game_object = player_obj
        self.game_state.add_game_object(self.player_game_object)
        enemy1 = ImperialFighter(game_state=self.game_state,
                                 initial_position=(
                                         self.game_state.center_cord +
                                         Vector(100, 100)),
                                 initial_direction=0,
                                 initial_speed=Vector.zero(),
                                 faction=Factions.empire,
                                 controller=StandardAi())
        self.game_state.add_game_object(enemy1)
        enemy2 = ImperialFighter(game_state=self.game_state,
                                 initial_position=(
                                         self.game_state.center_cord +
                                         Vector(-1000, -100)),
                                 initial_direction=0,
                                 initial_speed=Vector.zero(),
                                 faction=Factions.empire,
                                 controller=StandardAi())
        self.game_state.add_game_object(enemy2)
        ast = Asteroid4(game_state=self.game_state,
                        initial_position=(
                                self.game_state.center_cord +
                                Vector(-400, 500)),
                        initial_direction=10,
                        initial_speed=Vector(10, 0).rotate(10),
                        faction=Factions.asteroids,
                        controller=StandardAi())
        self.game_state.add_game_object(ast)

    def __init_timer(self):
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_game_window)
        self.game_timer.start(1000 / 60)
        self.drawer_timer = QTimer(self)
        self.drawer_timer.timeout.connect(self.update_drawer)
        self.drawer_timer.start(1000 / 1)

    def update_game_window(self):
        self.update_player_controller()
        self.game_state.update_game_state()

    def update_drawer(self):
        self.update()

    def update_player_controller(self):
        move_commands = set()
        if Qt.Key_W in self.key_down_set:
            move_commands.add(MoveCommands.move_forward)
        if Qt.Key_A in self.key_down_set:
            move_commands.add(MoveCommands.rotate_left)
        if Qt.Key_D in self.key_down_set:
            move_commands.add(MoveCommands.rotate_right)
        self.player_controller.move_commands = move_commands
        spell_commands = set()
        if Qt.Key_Space in self.key_down_set:
            spell_commands.add(0)
        if Qt.Key_Control in self.key_down_set:
            spell_commands.add(1)
        self.player_controller.spell_commands = spell_commands

    def keyPressEvent(self, event):
        self.key_down_set.add(event.key())
        return super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_P:
            self.update_pause()
        self.key_down_set.discard(event.key())
        return super().keyReleaseEvent(event)

    def update_pause(self):
        if self.game_state.current_state is States.paused:
            self.game_state.current_state = States.playing
        elif self.game_state.current_state is States.playing:
            self.game_state.current_state = States.paused

    def paintEvent(self, event):
        self.draw_game_state()

    def draw_game_state(self):
        canvas = QtGui.QPixmap(self.game_state.width,
                               self.game_state.height + 20)
        painter = QPainter(canvas)
        painter.begin(self)
        self.draw_background(painter)
        for game_object in self.game_state.game_objects:
            self.draw_game_object(game_object, painter, self.game_state.size)
        self.draw_player_info(painter, self.game_state.size)
        painter.end()
        self.graphic_label.setPixmap(canvas)

    def draw_background(self, painter: QPainter):
        painter.setBrush(self.BACKGROUND_COLOR)
        painter.drawRect(0, 0, self.game_state.width, self.game_state.height)
        painter.setBrush(Qt.NoBrush)

    def draw_game_object(self, game_object: GameObject, painter: QPainter,
                         size: Vector):
        angle = game_object.physic_info.direction
        position = game_object.physic_info.position
        x = position.x
        y = size.y - position.y
        radius = game_object.physic_info.physic_constants.radius
        diameter = radius * 2
        pixmap = QPixmap(game_object.get_graphic_info.sprite)
        scale = game_object.get_graphic_info.scale_coefficient
        original = pixmap.scaled(diameter * scale, diameter * scale,
                                 QtCore.Qt.KeepAspectRatio)
        transform = QTransform().rotate(90 - angle * 180 / math.pi)
        rotated = original.transformed(transform,
                                       QtCore.Qt.SmoothTransformation)
        point = QPointF(x - rotated.width() / 2, y - rotated.height() / 2)
        painter.drawPixmap(point, rotated)
        # self.__debug_draw_object_radius(game_object, painter, size)

    def draw_player_info(self, painter: QPainter, size: Vector):
        height = 20
        painter.setPen(Qt.black)
        painter.setBrush(Qt.black)
        painter.drawRect(0, size.y, size.x, height)
        painter.setPen(Qt.red)
        painter.setBrush(Qt.red)
        health = self.player_game_object.health
        width = self._get_player_characteristic_width(size, 2, health)
        painter.drawRect(0, size.y, width, height)
        painter.setPen(Qt.blue)
        painter.setBrush(Qt.blue)
        energy = self.player_game_object.energy
        width = self._get_player_characteristic_width(size, 2, energy)
        painter.drawRect(size.x / 2, size.y, width, height)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(Qt.NoPen)

    def _get_player_characteristic_width(self, size: Vector, char_count: int,
                                         characteristic: MainCharacteristic):
        return (size.x / char_count) * (
                characteristic.value / characteristic.max_value)

    def __debug_draw_object_radius(self, game_object: GameObject,
                                   painter: QPainter, size: Vector):
        painter.setPen(Qt.red)
        position = game_object.physic_info.position
        x = position.x
        y = size.y - position.y
        radius = game_object.physic_info.physic_constants.radius
        painter.drawEllipse(x - radius, y - radius, 2 * radius, 2 * radius)
