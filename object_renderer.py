import pygame as pg
from settings import *


class ObjectRenderer:
    """Renders all objects in game."""

    def __init__(self, game):
        """Creates instance of items to be rendered in game including their attributes."""
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/2.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)

    def draw(self):
        """Renders objects in game and on screen."""
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()

    def game_over(self):
        """Renders game over image on screen."""
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        """Renders players health on screen."""
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        """Renders red filter when player receives damage on screen."""
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        """Renders sky and floor."""
        # Sky.
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # Floor.
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        """Renders objects in game including walls, sky, and floor."""
        # Added sorted, lambda and reverse to make objects not visible through wall textures.
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        """Loads texture from specified path and returns a scaled image."""
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        """Loads textures into minimap with assigned values from dictionary keys."""
        return {
            1: self.get_texture('resources/textures/1.png')
        }
