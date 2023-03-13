import pygame as pg
from settings import *
import os
from collections import deque


class SpriteObject:
    """Class to create instance of sprite object."""

    def __init__(self, game, path='resources/sprites/static_sprites/1.png',
                 pos=(10.5, 3.5), scale=0.7, shift=0.27):  # Add position, scale and shift to correct size of sprite.
        """Creates instance of sprite object with attributes."""
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def get_sprite_projection(self):
        """Calculates projection of sprite object from player object."""
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        # Adjust correct projection size.
        image = pg.transform.scale(self.image, (proj_width, proj_height))
        # Scale sprite to calculated projection size.
        self.sprite_half_width = proj_width // 2

        # Makes sprite object not float in the air.
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift

        # Adds sprite to array of wall textures that is obtained from results of raycasting.
        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        """Calculates image of placed sprite from the position of player."""
        # Calculates image of placed sprite when player looks directly at sprite.
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        # Calculates image of placed sprite when player is not looking directly at sprite.
        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        # Calculates size of sprites projection.
        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        # Removes fishbowl effect and over processing of getting too close to sprite.
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        """Updates distance of sprite object from player."""
        self.get_sprite()


class AnimatedSprite(SpriteObject):
    """Inheriting class for creating instances of animated sprite objects."""

    def __init__(self, game, path='resources/sprites/animated_sprites/coin/1.png',
                 pos=(11.5, 3.5), scale=0.8, shift=0.15, animation_time=120):
        """Creates instance of animated sprite and their attributes."""
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        """Updates animation of sprite."""
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        """Animates image by checking animation time."""
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        """Checks time of tick and changes boolean value of trigger."""
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path):
        """Gets images from path and places in que."""
        images = deque()
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):
                img = pg.image.load(path + '/' + file_name).convert_alpha()
                images.append(img)
        return images
