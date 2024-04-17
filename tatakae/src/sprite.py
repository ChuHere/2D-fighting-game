"""Module providing functionality of a pygame module"""
import pygame

class Sprite():
    """
    Class representing a list of sprites of a character.

    Attributes:
        sprite_info (dict): Information about the sprites.
        animation_list (list): Individual frames for each action.
        action (list): Represents current action and frame.

    Methods:
        get(key), set(key), load_images(images, frames), update_action(new_action),
        update_frame(hp)
    """
    def __init__(self, sprite_info):
        self.sprite_info = sprite_info
        self.animation_list = self.load_images(sprite_info['sprite_sheet'], sprite_info['frames'])
        self.action = [0, 0]

    def get(self, key):
        """
        Returns a specified value from sprite_info.

        Args:
            key (str): Key to retrieve the value from sprite_info.

        Returns:
            Value corresponding to the given key in sprite_info.
        """
        return self.sprite_info[key]

    def set(self, key, val):
        """
        Updates a value in sprite_info.

        Args:
            key (str): Key to update in sprite_info.
            val: New value to update with in sprite_info.
        """
        self.sprite_info[key] = val

    def load_images(self, images, frames):
        """
        Loads individual sprites from a spritesheet.

        Args:
            images (list): List containing spritesheets of each action.
            frames (list): List containing the number of frames for each action.

        Returns:
            list: Array of individual sprites extracted from the sprite sheet.
        """
        animation_list = []
        for y, animation in enumerate(frames):
            tmp = []
            for x in range(animation):
                tmp_img = images[y].subsurface(x * self.sprite_info['size'], 0, self.sprite_info['size'], self.sprite_info['size'])
                tmp.append(pygame.transform.scale(tmp_img, (self.sprite_info['size'] * self.sprite_info['scale'], self.sprite_info['size'] * self.sprite_info['scale'])))
            animation_list.append(tmp)
        return animation_list

    def update_action(self, new_action):
        """
        Updates the current action of the sprite.

        Args:
            new_action: New action for the sprite.
        """
        if self.action[0] != new_action:
            self.action[0] = new_action
            self.action[1] = 0

    def update_frame(self, hp):
        """
        Updates the drawn frame of the sprite.

        Args:
            hp (int): Health points of the fighter.

        Returns:
            bool: True if the frame is the last in its animation, False otherwise.
        """
        self.action[1] += 0.1

        if self.action[1] >= (self.sprite_info['frames'][self.action[0]] - 1):
            if hp <= 0:
                self.action[1] = len(self.animation_list[self.action[0]]) - 1
            else:
                self.action[1] = 0
            return True

        return False

    def get_frame(self):
        """
        Returns the current drawn frame of the sprite.

        Returns:
            pygame.Surface: Current drawn frame of the sprite.
        """
        tmp = pygame.transform.flip(self.animation_list[self.action[0]][int(self.action[1])], self.sprite_info['orientation'], False).copy()
        return tmp
