from sprite_object import *


class Weapon(AnimatedSprite):
    """Inheriting class that creates instance of weapon object."""

    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', scale=0.4, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        """Initialises weapon attributes."""
        self.images = deque(
            # Since weapon is the projected, list comprehension just places the image on screen.
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        # Centers weapon image on screen.
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50

    def animate_shot(self):
        """Animates shot of weapon."""
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                # Implements changing image of weapon.
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    # Resets animation to resting image of weapon.
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        """Renders weapon on screen."""
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        """Animates weapon on screen."""
        self.check_animation_time()
        self.animate_shot()
