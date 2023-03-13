from sprite_object import *
from npc import *


class ObjectHandler:
    """Class for handling in game instances of objects."""

    def __init__(self, game):
        """Create instances that store sprites in list to be rendered in game."""
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites'
        self.anim_sprite_path = 'resources/sprites/animated_sprites'
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        self.npc_positions = {}

        # Sprite map which adds sprite objects in game.
        add_sprite(SpriteObject(game))
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 4.5)))

        # Npc map which adds enemy objects to game.
        add_npc(NPC(game))
        add_npc(NPC(game, pos=(11.5, 4.5)))

    def update(self):
        """Updates sprites in list."""
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]

    def add_npc(self, npc):
        """Adds npc to list to be rendered in game."""
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        """Adds sprite to list to be rendered in game."""
        self.sprite_list.append(sprite)
