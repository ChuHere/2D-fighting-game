"""Modules providing a functionality the tested game and necessarry tools"""
from fighter import Fighter
from cpu import Cpu
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
    sprite = Sprite()
    cpu = Cpu(0, 0, hp_bar, sprite)

    cpu.move_right(10)
    assert cpu.rect.x == 10
    assert cpu.states['running'] is True

def test_move_left():
    """Test movement left and its flags"""
    hp_bar = HealthBar(0, 0)
    sprite = Sprite()
    cpu = Cpu(10, 0, hp_bar, sprite)

    cpu.move_left(10)
    assert cpu.rect.x == 0
    assert cpu.states['running'] is True

def test_move_up():
    """Test movement up and its flags"""
    hp_bar = HealthBar(0, 0)
    sprite = Sprite()
    cpu = Cpu(0, 0, hp_bar, sprite)

    cpu.move_up()
    assert cpu.rect.y == 0
    assert cpu.terrain['jump_vel'] == -45
    assert cpu.states['jumping'] is True

def test_attack():
    """Test attack - collision and damage taken"""
    hp_bar = HealthBar(0, 0)
    sprite = Sprite()
    target = Fighter(70, 30, hp_bar, sprite)
    cpu = Cpu(10, 30, hp_bar, sprite)

    assert target.hp_bar.hp == 100

    cpu.attack(target)
    assert cpu.states['attacking']
    assert target.hp_bar.hp == 75

def test_dodge():
    """Test dodge and its flags"""
    hp_bar = HealthBar(0, 0)
    sprite = Sprite()
    cpu = Cpu(70, 30, hp_bar, sprite)
    fighter = Fighter(10, 30, hp_bar, sprite)

    cpu.dodge()
    assert cpu.states['dodging']
    assert cpu.cooldowns['dodge'] == 55
    assert cpu.terrain['bonus'] == 15
    assert cpu.hp_bar.hp == 100

    fighter.attack(cpu)
    assert cpu.hp_bar.hp == 100

def test_dodge_attack():
    """Cpu can't dodge when attacking - test"""
    hp_bar = HealthBar(0, 0)
    sprite = Sprite()
    target = Fighter(70, 30, hp_bar, sprite)
    cpu = Cpu(10, 30, hp_bar, sprite)

    assert target.hp_bar.hp == 100

    cpu.dodge()
    cpu.attack(target)
    assert not cpu.states['attacking']
    assert target.hp_bar.hp == 100

def test_attack_dodge():
    """Cpu can't dodge when attacking - test"""
    hp_bar = HealthBar(0, 0)
    sprite = Sprite()
    target = Fighter(70, 30, hp_bar, sprite)
    cpu = Cpu(10, 30, hp_bar, sprite)

    assert target.hp_bar.hp == 100

    cpu.attack(target)
    cpu.dodge()
    assert not cpu.states['dodging']
    assert cpu.cooldowns['dodge'] == 0
    assert cpu.terrain['bonus'] == 0
