"""Module providing functionality of a pygame module and random number in range"""
from random import randint
import pygame

class Cpu():
    """
    Class representing a CPU-controlled fighter in the game.

    Attributes:
        rect (pygame.Rect): The rectangle representing the Cpu's position and size.
        terrain (dict): Related to interactions with the terrain (gravity, speed, ground).
        states (dict): Dict of possible states.
        cooldowns (dict): Current cooldowns of attack and dodge.
        frames_move (dict): Dictionary storing movement frame data.
        hp_bar (HealthBar): Cpu's HealthBar instance.
        sprite (Sprite): Cpu's Sprite instance.
    """
    def __init__(self, x, y, hp_bar, sprite):
        self.rect = pygame.Rect(x, y, sprite.get('width'), sprite.get('height'))
        self.terrain = {
            'jump_vel': 0,
            'bonus': 0,
            'ground': sprite.get('height') + y
        }
        self.states = {
            'player': sprite.get('player'),
            'running': False,
            'jumping': False,
            'attacking': False,
            'damage': False,
            'dodging': 0
        }
        self.cooldowns = {
            'attack': 0,
            'dodge': 0
        }
        self.frames_move = {
            'frame': 0,
            'dir': 0
        }
        self.hp_bar = hp_bar
        self.sprite = sprite

    def move_left(self, speed):
        """
        Move Cpu to the left.

        Args:
            speed (int): Move by how much.
        """
        self.rect.x -= speed + self.terrain['bonus']
        self.states['running'] = True

    def move_right(self, speed):
        """
        Move Cpu to the right.

        Args:
            speed (int): Move by how much.
        """
        self.rect.x += speed + self.terrain['bonus']
        self.states['running'] = True

    def move_up(self):
        """
        Set Cpu to jump/rise vertically.
        """
        self.terrain['jump_vel'] = -45
        self.states['jumping'] = True

    def long_dist(self, speed, target):
        """
        Moves the Cpu uses when it's far from the opponent.

        Args:
            speed (int): The movement speed.
            target (Fighter): The target Fighter instance.
        """
        if self.rect.centerx < target.rect.centerx:
            self.move_right(speed)
        else:
            self.move_left(speed)

        self.states['running'] = True

    def generate_dir(self, speed):
        """
        Generates randomly the direction for the Cpu's movement.
        Chances: left (5/11), right (5/11), jump(1/11)

        Args:
            speed (int): The movement speed.
        """
        choice = randint(1, 11)
        choice_len = randint(5, 8)

        if choice <= 5:
            self.move_left(speed)
            self.frames_move['frame'] = choice_len
            self.frames_move['dir'] = -speed
        elif choice <= 10:
            self.move_right(speed)
            self.frames_move['frame'] = choice_len
            self.frames_move['dir'] = speed
        elif not self.states['jumping']:
            self.move_up()

    def generate_action(self, speed, target):
        """
        Generates action for the Cpu.
        Chances: attack (60%), dodge (40%) 

        Args:
            speed (int): The movement speed.
            target (Fighter): The target Fighter instance.
        """
        choice = randint(1, 10)

        if choice <= 6 and self.cooldowns['attack'] <= 0 and not self.states['attacking']:
            self.attack(target)
            return

        if self.cooldowns['dodge'] <= 0:
            self.dodge()
        else:
            if self.cooldowns['attack'] <= 0 and not self.states['attacking']:
                self.attack(target)
            else:
                self.generate_dir(speed)

    def close_dist(self, speed, target):
        """
        Handles close-distance movements and actions of the Cpu.
        Chances: attack/dodge (50%), move (50%)

        Args:
            speed (int): The movement speed.
            target (Fighter): The target Fighter instance.
        """
        choice = randint(0, 1)

        if choice == 0 or (self.states['attacking'] and (self.states['dodging'] != 0)):
            self.generate_dir(speed)
        else:
            self.generate_action(speed, target)


    def move(self, screen, target):
        """
        Manages the movement of the Cpu.

        Args:
            screen (pygame.Surface): The game screen surface.
            target (Fighter): The target Fighter instance.
        """
        speed = 10
        GRAVITY = 2

        if self.hp_bar.hp > 0 and target.hp_bar.hp > 0:
            if self.frames_move['frame'] > 0:
                self.rect.x += self.frames_move['dir']
                self.frames_move['frame'] -= 1
            else:
                self.states['running'] = False
                if abs(self.rect.centerx - target.rect.centerx) > 770:
                    self.long_dist(speed, target)
                else:
                    self.close_dist(speed, target)

        #Apply gravity and cooldown ticks
        self.terrain['jump_vel'] += GRAVITY
        self.rect.y += self.terrain['jump_vel']

        if self.cooldowns['attack'] > 0:
            self.cooldowns['attack'] -= 1

        if self.cooldowns['dodge'] > 0:
            self.cooldowns['dodge'] -= 1

        #Orientation to face each other
        if self.rect.centerx < target.rect.centerx:
            self.sprite.set('orientation', False)
        else:
            self.sprite.set('orientation', True)

        #Boundaries
        if self.rect.bottom > self.terrain['ground']:
            self.rect.bottom = self.terrain['ground']
            self.states['jumping'] = False

        self.rect.clamp_ip(screen.get_rect())

    def animation(self):
        """Manages Cpu animations."""
        if self.hp_bar.hp <= 0:
            self.sprite.update_action(5) #Death animation
        elif self.states['damage']:
            self.sprite.update_action(4) #Take hit animation
        elif self.states['attacking']:
            self.sprite.update_action(3) #Attack animation
        elif self.states['jumping']:
            self.sprite.update_action(2) #Jump animation
        elif self.states['running']:
            self.sprite.update_action(1) #Run animation
        else:
            self.sprite.update_action(0) #Idle animation

        if self.sprite.update_frame(self.hp_bar.hp):
            if self.sprite.action[0] == 3:
                self.states['attacking'] = False
                self.cooldowns['attack'] = 35

            if self.sprite.action[0] == 4:
                self.states['damage'] = False

                if self.states['attacking']:
                    self.states['attacking'] = False
                    self.cooldowns['attack'] = 35

    def attack(self, target):
        """
        Manages the attack functionality of the Cpu.

        Args:
            target (Fighter): The Fighter instance of the opponent.
        """
        #Check if not dodging and attack not on cooldown
        if self.cooldowns['attack'] == 0 and self.states['dodging'] == 0:
            self.states['attacking'] = True

            if self.sprite.get('orientation'):
                offset_x = 3 * self.rect.width
            else:
                offset_x = 0

            attack_move = pygame.Rect(self.rect.centerx - offset_x, self.rect.y, 3 * self.rect.width, 0.75 * self.rect.height)

            #Attack reached check
            if attack_move.colliderect(target.rect):
                if not target.states['dodging'] > 0:
                    target.hp_bar.damage()
                    target.states['damage'] = True


    def dodge(self):
        """Manages the dodge functionality of the Cpu."""
        if self.cooldowns['dodge'] == 0 and not self.states['attacking']:
            self.states['dodging'] = 15
            self.cooldowns['dodge'] = 55
            self.terrain['bonus'] = 15

    def draw(self, screen):
        """
        Draws the Cpu and its related components on the screen.

        Args:
            screen (pygame.Surface): The game screen surface.
        """
        self.animation()
        self.hp_bar.draw(screen)

        tmp = self.sprite.get_frame()

        #Dodge animation - white flash
        if self.states['dodging'] > 0:
            tmp.fill((255,255,255),None,pygame.BLEND_ADD)
            self.states['dodging'] -= 1
        else:
            self.terrain['bonus'] = 0

        offset_x = self.sprite.get('offset')[0] * self.sprite.get('scale')
        offset_y = self.sprite.get('offset')[1] * self.sprite.get('scale')

        screen.blit(tmp, (self.rect.x - offset_x, self.rect.y - offset_y))
