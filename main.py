# python modules:
import random
# kivy modules:
from kivy.app import App
from kivy import properties as kp
from kivy.config import Config
from kivy.clock import Clock
from kivy.core.window import Window
    # uix:
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
# mine:
import settings


convert_code2key = {
    82: "up",
    79: "right",
    81: "down",
    80: "left",
    44: "spacebar"
}


class Piece(Image):
    def __init__(self, pos, size=(settings.TILESIZE, settings.TILESIZE)):
        super().__init__()

        self.size_hint = None, None
        self.pos = pos
        self.size = size


class Game(Screen):
    pieces = kp.ListProperty()
    tilesize = kp.NumericProperty(settings.TILESIZE)
    n_tiles = kp.NumericProperty(settings.N_TILES)
    vel = kp.NumericProperty(settings.VEL)

    def __init__(self):
        self.size = Window.size
        super().__init__()
        self.add_new_piece()
        Window.bind(on_key_down=self._on_keyboard_down)
        Window.bind(on_key_up=self._on_keyboard_up)
        self.keys = set()

    def add_new_piece(self):
        self.piece = Piece(pos=(Window.width / 2, self.height))
        self.pieces.append(self.piece)
        self.add_widget(self.piece)

    def update(self, dt):
        print("update", dt, self.keys, self.size, self.piece.pos)
        self.piece.y -= dt * self.vel
        # print("self.piece.y", self.piece.y)
        if "right" in self.keys:
            self.piece.x += self.tilesize
        if "left" in self.keys:
            self.piece.x -= self.tilesize
        print("self.piece.pos", self.piece.pos)

        # collisions:
        self.check_collisions()
        print("self.piece.pos", self.piece.pos)


    def _on_keyboard_down(self, *args):
        print("_on_keyboard_down", args)
        code = args[2]
        key = convert_code2key.get(code)
        print(key)
        self.keys.add(key)

    def _on_keyboard_up(self, *args):
        print("_on_keyboard_up", args)
        code = args[2]
        key = convert_code2key.get(code)
        print(key)
        try:
            self.keys.remove(key)
            print(self.keys)
        except KeyError:
            pass

    def check_collisions(self):
        print("check_collisions()")
        # vertical collision:
        if self.piece.y <= 0:
            self.piece.y = 0
            self.add_new_piece()
            return
        # horizontal collision:
        borders = self.calc_borders()
        print("borders", borders)
        if self.piece.x < borders[0]:
            self.piece.x = borders[0]
        if self.piece.right > borders[1]:
            self.piece.right = borders[1]
        # piece-piece collision:
        print([piece.pos for piece in self.pieces])
        for piece in self.pieces:
            print("piece.pos", piece.pos)
            if piece is self.piece:
                print("piece is piece")
                continue
            self.piece.width -= 2
            self.piece.x += 1
            if piece.collide_widget(self.piece):
                print("piece-piece collision", piece.pos, self.piece.pos)
                self.piece.width += 2
                self.piece.x -= 1
                self.piece.y = piece.top
                self.add_new_piece()
                return
            self.piece.width += 2
            self.piece.x -= 1


    def calc_borders(self):
        size_util = self.tilesize * self.n_tiles
        if self.width < size_util:
            raise Exception("game.width=%s < %s (tilesize * n_tiles)" % (self.width, size_util))
        size_left = self.width - size_util
        size_left_1side = size_left / 2
        return [size_left_1side, self.width - size_left_1side]


class GameApp(App):
    def build(self):
        self.game = Game()
        Clock.schedule_interval(self.game.update, 1 / settings.FPS)
        return self.game



if __name__ == "__main__":
    game_app = GameApp()
    game_app.run()