"""Module providing functionality of a pygame module"""
import pygame

class Fighter():
    """
    Class representing a Fighter/player instance.

    Attributes:
        rect (pygame.Rect): The rectangle representing the Fighter's position and size.
        speeds (dict): Jumping velocity and dodge bonus speed velocity.
        states (dict): Dict of possible states.
        cooldowns (dict): Current cooldowns of attack and dodge.
        ground (int): Y-coordinate of the ground.
        hp_bar (HealthBar): Fighter's HealthBar instance.
        sprite (Sprite): Fighter's Sprite instance.
    """
    def __init__(self, x, y, hp_bar, sprite):
        self.rect = pygame.Rect(x, y, sprite.get('width'), sprite.get('height'))
        self.speeds = {
            'jump_vel': 0,
            'bonus': 0
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
        self.ground = sprite.get('height') + y
        self.hp_bar = hp_bar
        self.sprite = sprite

    def move_left(self, speed):
        """
        Move fighter to the left.

        Args:
            speed (int): Move by how much.
        """
        self.rect.x -= speed + self.speeds['bonus']
        self.states['running'] = True

    def move_right(self, speed):
        """
        Move fighter to the right.

        Args:
            speed (int): Move by how much.
        """
        self.rect.x += speed + self.speeds['bonus']
        self.states['running'] = True

    def handle_input(self, target):
        """
        Handles player inputs. Inputs are only valid when the player is alive and is not attacking currently.
        Sets appropriate flags/states.

        Args:
            screen (pygame.Surface): The game screen surface.
            target (Fighter): The Fighter instance of the opponent.
        """
        speed = 10
        keys = pygame.key.get_pressed()
        if self.states['player'] == 1 and self.hp_bar.hp > 0 and not self.states['damage']:
            #movement
            if keys[pygame.K_a]:
                self.move_left(speed)
            if keys[pygame.K_d]:
                self.move_right(speed)
            if keys[pygame.K_w] and not self.states['jumping']:
                self.speeds['jump_vel'] = -45
                self.states['jumping'] = True
            #attack
            if keys[pygame.K_j] and not self.states['attacking']:
                self.attack(target)
            #dodge
            if keys[pygame.K_k]:
                self.dodge()
        elif self.states['player'] == 2 and self.hp_bar.hp > 0 and not self.states['damage']:
            #movement
            if keys[pygame.K_LEFT]:
                self.move_left(speed)
            if keys[pygame.K_RIGHT]:
                self.move_right(speed)
            if keys[pygame.K_UP] and not self.states['jumping']:
                self.speeds['jump_vel'] = -45
                self.states['jumping'] = True
            #attack
            if keys[pygame.K_KP1] and not self.states['attacking']:
                self.attack(target)
            #dodge
            if keys[pygame.K_KP2]:
                self.dodge()

    def move(self, screen, target):
        """
        Manages the movement of the Fighter. Applies gravity and boundaries.
        Takes care of cooldown ticking and orients opponents to face each other.

        Args:
            screen (pygame.Surface): The game screen surface.
            target (Fighter): The target Fighter instance.
        """
        gravity = 2
        self.states['running'] = False

        self.handle_input(target)

        #Applies gravity
        self.speeds['jump_vel'] += gravity
        self.rect.y += self.speeds['jump_vel']

        #Cooldown ticking
        if self.cooldowns['attack'] > 0:
            self.cooldowns['attack'] -= 1

        if self.cooldowns['dodge'] > 0:
            self.cooldowns['dodge'] -= 1

        #Orientation to face each other
        if self.hp_bar.hp > 0:
            if self.rect.centerx < target.rect.centerx:
                self.sprite.set('orientation', False)
            else:
                self.sprite.set('orientation', True)

        #Applies boundaries
        if self.rect.bottom > self.ground:
            # print('test')
            self.rect.bottom = self.ground
            # print(self.rect.bottom)
            # print(self.ground)
            self.states['jumping'] = False
            self.speeds['jump_vel'] = 0

        self.rect.clamp_ip(screen.get_rect())

    def animation(self):
        """Manages Fighter animations."""
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
        Manages the attack functionality of the Fighter.

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
        """Manages the dodge functionality of the Fighter."""
        if self.cooldowns['dodge'] == 0 and not self.states['attacking']:
            self.states['dodging'] = 15
            self.cooldowns['dodge'] = 55
            self.speeds['bonus'] = 15

    def draw(self, screen):
        """
        Draws the Fighter and its related components on the screen.

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
            self.speeds['bonus'] = 0

        offset_x = self.sprite.get('offset')[0] * self.sprite.get('scale')
        offset_y = self.sprite.get('offset')[1] * self.sprite.get('scale')

        screen.blit(tmp, (self.rect.x - offset_x, self.rect.y - offset_y))
