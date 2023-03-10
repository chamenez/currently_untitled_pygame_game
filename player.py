from settings import *
import pygame as pg
import math


class Player:

    def __init__(self, game):
        """Initializes player coordinates."""
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE

    def movement(self):
        """Implements movement of player coordinates."""
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)

        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time

    def check_wall(self, x, y):
        """Checks if coordinates do not match coordinates in world map."""
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        """Checks if player coordinates do not match coordinates in world map."""
        if self.check_wall(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy)):
            self.y += dy

    def draw(self):
        """Creates visual for player."""
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                     (self.x * 100 + WIDTH * math.cos(self.angle),
                      self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def update(self):
        """Updates the coordinates of player."""
        self.movement()

    @property
    def pos(self):
        """Returns player coordinates."""
        return self.x, self.y

    @property
    def map_pos(self):
        """Returns coordinates of the tile of the map the player is on."""
        return int(self.x), int(self.y)
