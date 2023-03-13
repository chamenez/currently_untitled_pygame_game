import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *


class Game:
    """Class for game object."""

    def __init__(self):
        """Initializes game attributes."""
        pg.init()
        pg.mouse.set_visible(False)  # Disables view of mouse.
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False  # Global trigger for when death trigger is cued.
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        """Initializes objects in game."""
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

        # self.static_sprite = SpriteObject(self)
        # self.animated_sprite = AnimatedSprite(self)

    def update(self):
        """Updates game frame."""
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        # self.static_sprite.update()
        # self.animated_sprite.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        """Creates on screen visual of different objects."""
        # self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()
        # Draws map and character for debugging purposes.
        # self.map.draw()
        # self.player.draw()

    def check_events(self):
        """Allows player to exit application through checking for input of escape."""
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        """Runs instances of objects while also checking for any events."""
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
