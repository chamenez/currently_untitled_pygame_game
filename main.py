import pygame as pg
import sys
from settings import *
from map import *
from player import *


class Game:

    def __init__(self):
        """Initializes game."""
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self):
        """Initializes objects in game."""
        self.map = Map(self)
        self.player = Player(self)

    def update(self):
        """Updates game frame."""
        self.player.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        """Creates on screen visual of different objects."""
        self.screen.fill('black')
        self.map.draw()
        self.player.draw()

    def check_events(self):
        """Allows player to exit application through checking for input of escape."""
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        """Runs game while also checking for any events."""
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
