"""Modules providing a functionality of system path, pygame and objects of the created game"""
from pathlib import Path
import pygame
from sprite import Sprite
from fighter import Fighter
from cpu import Cpu
from button import Button
from healthbar import HealthBar

class Game():
    """
    Class representing a game instance.

    Attributes:
        SCR_WIDTH (int): Width of the screen.
        SCR_HEIGHT (int): Height of the screen.
        bg_img (str): Path to the background image.
        font (str): Fonts for different texts.
    """
    def __init__(self, SCR_WIDTH, SCR_HEIGHT, bg_img, font):
        pygame.init()
        pygame.display.set_caption('Tatakae!')

        self.SCR_WIDTH = SCR_WIDTH
        self.SCR_HEIGHT = SCR_HEIGHT
        self.screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT), pygame.SCALED)
        self.bg_img = pygame.image.load(bg_img).convert_alpha()
        self.font = {
            'button': pygame.font.Font(font, 40),
            'round': pygame.font.Font(font, 80),
            'score': pygame.font.Font(font, 40),
            'title': pygame.font.Font(font, 120)
        }

    def draw_bg(self):
        """Function to draw the background on the display"""
        fixed_img = pygame.transform.scale(self.bg_img, (self.SCR_WIDTH, self.SCR_HEIGHT))
        self.screen.blit(fixed_img, (0, 0))

    def menu(self):
        """
        Manages the main menu and its functionality.
        """
        pygame.init()
        menu = True
        versus_btn = Button(self.SCR_WIDTH//2, 400, 'VERSUS', self.font['button'])
        cpu_btn = Button(self.SCR_WIDTH//2, 600, 'VS CPU', self.font['button'])
        quit_btn = Button(self.SCR_WIDTH//2, 800, 'QUIT', self.font['button'])

        while menu:
            pos = pygame.mouse.get_pos()
            self.screen.fill((31, 122, 122))

            self.draw_text('TATAKAE!', [self.SCR_WIDTH//2, 200], (230, 0, 92), 'title')
            versus_btn.draw(self.screen, pos)
            cpu_btn.draw(self.screen, pos)
            quit_btn.draw(self.screen, pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                if event.type == pygame.VIDEORESIZE:
                    continue
                if event.type == pygame.MOUSEBUTTONUP:
                    if versus_btn.rect.collidepoint(pos):
                        menu = self.match('versus')
                    elif cpu_btn.rect.collidepoint(pos):
                        menu = self.match('cpu')
                    elif quit_btn.rect.collidepoint(pos):
                        menu = False

            pygame.display.update()

        pygame.quit()

    def post_match(self, score):
        """
        Manages the post-match screen and its functionality.

        Args:
            score (list): The final score of the match.

        Returns:
            tuple: A tuple indicating whether to play again and the starting scores.
        """
        player = ''
        if score[0] == 2:
            player = 'PLAYER 1'
        else:
            player = 'PLAYER 2'

        score_new = [0, 0]
        post_menu = True

        again_btn = Button(self.SCR_WIDTH//2, 400, 'PLAY AGAIN', self.font['button'])
        menu_btn = Button(self.SCR_WIDTH//2, 600, 'RETURN', self.font['button'])
        while post_menu:
            pos = pygame.mouse.get_pos()
            self.screen.fill((31, 122, 122))

            self.draw_text(player + ' WON', [self.SCR_WIDTH//2, 200], (230, 0, 92), 'title')
            again_btn.draw(self.screen, pos)
            menu_btn.draw(self.screen, pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    post_menu = False
                if event.type == pygame.VIDEORESIZE:
                    continue
                if event.type == pygame.MOUSEBUTTONUP:
                    if again_btn.rect.collidepoint(pos):
                        return True, score_new
                    if menu_btn.rect.collidepoint(pos):
                        post_menu = False

            pygame.display.update()

        return False, score_new

    def load_sprites(self, dest):
        """
        Loads spritesheets from the desired destination.

        Args:
            dest (str): Path to the destination folder.

        Returns:
            list: A list containing loaded spritesheets for each action.
        """
        sprites = []
        moves = ['Idle', 'Run', 'Jump', 'Attack1', 'Take hit', 'Death']

        for x in moves:
            sprite_dest = dest + x + '.png'
            tmp = pygame.image.load(Path(__file__).parent.parent / sprite_dest).convert_alpha()
            sprites.append(tmp)

        return sprites

    def draw_text(self, text, pos, color, font):
        """
        Draws text on the display.

        Args:
            text (str): Text to be displayed.
            pos (list): Position coordinates (x, y) to display the text.
            color (tuple): Color of the text in RGB format.
            font (pygame.font.Font): Font type to be used.
        """
        text_pr = self.font[font].render(text, True, color)
        text_rect = text_pr.get_rect(center=(pos[0], pos[1]))
        self.screen.blit(text_pr, text_rect)

    def draw_score(self, text, x, y, color):
        """
        Draws the game score on the display.

        Args:
            text (str): Text to be displayed.
            x (int): X-coordinate position.
            y (int): Y-coordinate position.
            color (tuple): Color of the text in RGB format.
        """
        text_pr = self.font['score'].render(text, True, color)
        self.screen.blit(text_pr, (x, y))

    def fighters_setup(self, mode):
        """
        Sets up fighters based on the game mode. Their initial position, health and spritesheets.

        Args:
            mode (str): The game mode (versus or cpu).

        Returns:
            tuple: A tuple containing fighter instances.
        """
        moves_img1 = self.load_sprites('assets/fighter1/')
        moves_img2 = self.load_sprites('assets/fighter2/')

        fighter1_sprite = {
            'player': 1,
            'width': self.SCR_WIDTH//15,
            'height': self.SCR_HEIGHT//3.3,
            'sprite_sheet': moves_img1,
            'frames': [4, 8, 1, 3, 3, 7],
            'size': 200,
            'scale': 5,
            'offset': [88, 63],
            'orientation': False
        }

        fighter2_sprite = {
            'player': 2,
            'width': self.SCR_WIDTH//15,
            'height': self.SCR_HEIGHT//3.3,
            'sprite_sheet': moves_img2,
            'frames': [8, 8, 2, 3, 4, 6],
            'size': 200,
            'scale': 5,
            'offset': [88, 57],
            'orientation': True
        }

        sprite1 = Sprite(fighter1_sprite)
        sprite2 = Sprite(fighter2_sprite)

        hp_size = (self.SCR_WIDTH - (4 * (self.SCR_WIDTH//19.2))) // 2
        hp1 = HealthBar(self.SCR_WIDTH//19.2, 40)
        fighter1 = Fighter(200, self.SCR_HEIGHT//1.6, hp1, sprite1)

        hp2 = HealthBar(3 * (self.SCR_WIDTH//19.2) + hp_size, 40)
        if mode == 'versus':
            fighter2 = Fighter((self.SCR_WIDTH-200-self.SCR_WIDTH//15), self.SCR_HEIGHT//1.6, hp2, sprite2)
        elif mode == 'cpu':
            fighter2 = Cpu((self.SCR_WIDTH-200-self.SCR_WIDTH//15), self.SCR_HEIGHT//1.6, hp2, sprite2)

        return fighter1, fighter2

    def check_round(self, fighter1, fighter2, wait_p):
        """
        Checks the if any of the players is dead.

        Args:
            fighter1 (Fighter): Fighter instance for player 1.
            fighter2 (Fighter): Fighter instance for player 2.
            wait_p (int): The time of checking.

        Returns:
            tuple: A tuple containing current round status, round result, and updated wait time.
        """
        round_res = ''
        curr_round = True
        wait = wait_p
        if fighter1.hp_bar.hp <= 0:
            round_res = 'p2'
            curr_round = False
            wait = pygame.time.get_ticks()
        elif fighter2.hp_bar.hp <= 0:
            round_res = 'p1'
            curr_round = False
            wait = pygame.time.get_ticks()

        return curr_round, round_res, wait

    def match(self, mode):
        """
        Manages the game match functionality. Each match is a best-of-three format.

        Args:
            mode (str): The game mode (versus or cpu).

        Returns:
            bool: Indicates whether to continue playing or not.
        """
        clock = pygame.time.Clock()

        fighter1, fighter2 = self.fighters_setup(mode)

        score = [0, 0]
        running = True
        curr_round = True
        initial = 3
        wait = pygame.time.get_ticks()
        round_res = ''
        while running:
            clock.tick(60)
            self.draw_bg()

            if initial == 0:
                fighter1.move(self.screen, fighter2)
                fighter2.move(self.screen, fighter1)
            else:
                self.draw_text(str(initial), [self.SCR_WIDTH//2, 400], 'white', 'round')
                if pygame.time.get_ticks() - wait >= 1000:
                    initial -= 1
                    wait = pygame.time.get_ticks()

            fighter1.draw(self.screen)
            fighter2.draw(self.screen)

            self.draw_score('P1: ' + str(score[0]), fighter1.hp_bar.x, fighter1.hp_bar.y + 50, 'white')
            self.draw_score('P2: ' + str(score[1]), fighter2.hp_bar.x, fighter2.hp_bar.y + 50, 'white')

            if curr_round:
                curr_round, round_res, wait = self.check_round(fighter1, fighter2, wait)
                score[0] += (fighter2.hp_bar.hp <= 0)
                score[1] += (fighter1.hp_bar.hp <= 0)
            else:
                outcomes = {
                    'p1': 'PLAYER 1 ROUND',
                    'p2': 'PLAYER 2 ROUND'
                }

                self.draw_text(outcomes[round_res], [self.SCR_WIDTH//2, 400], 'white', 'round')

                if pygame.time.get_ticks() - wait >= 2000:
                    initial = 3
                    curr_round = True

                    if (score[0] == 2 or score[1] == 2):
                        running, score = self.post_match(score)

                    fighter1, fighter2 = self.fighters_setup(mode)
                    wait = pygame.time.get_ticks()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            pygame.display.update()

        return True
