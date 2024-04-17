"""Module providing functionality of a pygame module"""
import pygame

class HealthBar():
    """
    Class representing a health bar instance.

    Attributes:
        hp (int): Current health.
        ratio (int): Ratio between the current health and the maximum health.
        x (int): X-coordinate of the healthbar.
        Y (int): Y-coordinate of the healthbar.
    """
    def __init__(self, x, y):
        self.hp = 100
        self.ratio = self.hp / 100
        self.x = x
        self.y = y

    def damage(self):
        """Function to decrease health"""
        self.hp -= 25

    def draw(self, surface):
        """
        Draws the health bar on the specified surface.

        Args:
            surface (pygame.Surface): Surface on which the health bar will be drawn.
        """
        width, height = pygame.display.get_surface().get_size()
        size = (width - (4 * (width//19.2))) // 2

        pygame.draw.rect(surface, 'white', (self.x-2, self.y-2, size+6, (height//20)+6))
        pygame.draw.rect(surface, 'red', (self.x, self.y, size, height//20))
        pygame.draw.rect(surface, 'green', (self.x, self.y, (self.hp/100) * size, height//20))
