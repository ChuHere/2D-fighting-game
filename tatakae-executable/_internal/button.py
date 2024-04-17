"""Modules providing a functionality of pygame"""
import pygame

class Button():
    """
    Represents a clickable button in the game.

    Attributes:
        rect (pygame.Rect): The rectangle representing the button's position and size.
        font (pygame.font.Font): The font used for the button's text.
        text (str): The text displayed on the button.
        color_btn (str/tuple): The color of the button.
    """
    def __init__(self, x, y, text, font):
        self.rect = pygame.Rect(0, 0, 400, 100)
        self.rect.center = (x, y)
        self.font = font
        self.text = text
        self.color_btn = 'black'

    def check_hover(self, pos):
        """
        Checks if the mouse cursor is hovering over the button.

        Args:
            pos (tuple): The position of the mouse cursor.
        """
        if self.rect.collidepoint(pos):
            self.color_btn = (0, 153, 0)
        else:
            self.color_btn = 'black'

    def draw(self, screen, pos):
        """
        Draws the button on the screen.

        Args:
            screen (pygame.Surface): The game screen surface.
            pos (tuple): The position of the mouse cursor.
        """
        self.check_hover(pos)
        text = self.font.render(self.text, True, 'white')
        text_rect = text.get_rect(center=self.rect.center)

        border = pygame.Rect(0, 0, 420, 120)
        border.center = self.rect.center

        pygame.draw.rect(screen, 'lightgray', border)
        pygame.draw.rect(screen, self.color_btn, self.rect)
        screen.blit(text, text_rect)
