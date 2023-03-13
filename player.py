from settings import *
import pygame as pg
import math


class Player:
    """Class to create player object."""

    def __init__(self, game):
        """Initializes player coordinates."""
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.health_recovery_delay = 700
        self.time_prev = pg.time.get_ticks()

    def recover_health(self):
        """Implements health recovery for player if lower than original."""
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self):
        """Checks player health to see if it is lower than initial."""
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def check_game_over(self):
        """Checks if player health is 0."""
        if self.health < 1:
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def get_damage(self, damage):
        """Applies damage to player, renders health and sound, checks if player is dead."""
        self.health -= damage
        self.game.object_renderer.player_damage()
        self.game.sound.player_pain.play()
        self.check_game_over()

    def single_fire_event(self, event):
        """Reacts to player action of shooting weapon."""
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                # Plays shooting sound of shotgun.
                self.game.sound.shotgun.play()
                # Initiates process to animate shooting.
                self.shot = True
                self.game.weapon.reloading = True

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

        # Implements the use of keys for debugging purposes.
        # if keys[pg.K_LEFT]:
        #     self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        # if keys[pg.K_RIGHT]:
        #     self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau

    def check_wall(self, x, y):
        """Checks if coordinates do not match coordinates in world map."""
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        """Checks if player coordinates do not match coordinates in world map."""
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        """Creates visual for player."""
        # pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
        #              (self.x * 100 + WIDTH * math.cos(self.angle),
        #               self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        """Allows user to use mouse to move character."""
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        """Updates the coordinates, movement and health of player."""
        self.movement()
        self.mouse_control()
        self.recover_health()

    @property
    def pos(self):
        """Returns player coordinates."""
        return self.x, self.y

    @property
    def map_pos(self):
        """Returns coordinates of the tile of the map the player is on."""
        return int(self.x), int(self.y)
