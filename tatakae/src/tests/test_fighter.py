"""Modules providing a functionality the tested game and necessarry tools"""
from unittest.mock import Mock
import pygame
from fighter import Fighter
from healthbar import HealthBar

class Sprite():
    """Mock Sprite class"""
    def __init__(self):
        self.size = {
            'width': 100,
            'height': 100,
            'player': 1,
            'orientation': False
        }

    def dummy(self):
        """Just dummy function for pylint"""
        print('dummy function')

    def get(self, key):
        """Return value based on key from dict"""
        return self.size[key]


def test_move_right():
    """Test movement right and its flags"""
    hp_bar = HealthBar(0, 0)
    screen = Mock(spec=pygame.Surface)
    target = Mock(spec=Fighter)
    sprite = Sprite()
    fighter = Fighter(0, 0, hp_bar, sprite)

    pygame.key.get_pressed = Mock(return_value={pygame.K_a: False, pygame.K_d: True, pygame.K_w: False, pygame.K_j: False, pygame.K_k: False})
    fighter.handle_input(target)
    assert fighter.rect.x == 10
    assert fighter.states['running'] is True

def test_move_left():
    """Test movement left and its flags"""
    hp_bar = HealthBar(0, 0)
    screen = Mock(spec=pygame.Surface)
    target = Mock(spec=Fighter)
    sprite = Sprite()
    fighter = Fighter(10, 0, hp_bar, sprite)

    pygame.key.get_pressed = Mock(return_value={pygame.K_a: True, pygame.K_d: False, pygame.K_w: False, pygame.K_j: False, pygame.K_k: False})
    fighter.handle_input(target)
    assert fighter.rect.x == 0
    assert fighter.states['running'] is True

def test_jump():
    """Test jump and its flags"""
    hp_bar = HealthBar(0, 0)
    screen = Mock(spec=pygame.Surface)
    target = Mock(spec=Fighter)
    sprite = Sprite()
    fighter = Fighter(0, 0, hp_bar, sprite)

    pygame.key.get_pressed = Mock(return_value={pygame.K_a: False, pygame.K_d: False, pygame.K_w: True, pygame.K_j: False, pygame.K_k: False})
    fighter.handle_input(target)
    assert fighter.rect.y == 0
    assert fighter.speeds['jump_vel'] == -45
    assert fighter.states['jumping'] is True

def test_attack():
    """Test attack - collision and damage taken"""
    hp_bar = HealthBar(0, 0)
    sprite = Sprite()
    target = Fighter(70, 30, hp_bar, sprite)
    fighter = Fighter(10, 30, hp_bar, sprite)

    assert target.hp_bar.hp == 100

    fighter.attack(target)
    assert fighter.states['attacking']
    assert target.hp_bar.hp == 75

def test_dodge():
    """Test dodge and its flags"""
    hp_bar = HealthBar(0, 0)
    sprite = Sprite()
    target = Fighter(70, 30, hp_bar, sprite)
    fighter = Fighter(10, 30, hp_bar, sprite)

    target.dodge()
    assert target.states['dodging']
    assert target.cooldowns['dodge'] == 55
    assert target.speeds['bonus'] == 15
    assert target.hp_bar.hp == 100

    fighter.attack(target)
    assert target.hp_bar.hp == 100

def test_dodge_attack():
    """Fighter can't attack when dodging - test"""
    hp_bar = HealthBar(0, 0)
    sprite = Sprite()
    target = Fighter(70, 30, hp_bar, sprite)
    fighter = Fighter(10, 30, hp_bar, sprite)

    assert target.hp_bar.hp == 100

    fighter.dodge()
    fighter.attack(target)
    assert not fighter.states['attacking']
    assert target.hp_bar.hp == 100

def test_attack_dodge():
    """Fighter can't dodge when attacking - test"""
    hp_bar = HealthBar(0, 0)
    sprite = Sprite()
    target = Fighter(70, 30, hp_bar, sprite)
    fighter = Fighter(10, 30, hp_bar, sprite)

    assert target.hp_bar.hp == 100

    fighter.attack(target)
    fighter.dodge()
    assert not fighter.states['dodging']
    assert fighter.cooldowns['dodge'] == 0
    assert fighter.speeds['bonus'] == 0
