"""Modules providing a functionality of system path and the created game"""
from pathlib import Path
from game import Game

def main():
    """
    Sets up the game parameters and initializes the game instance.
    """
    SCR_WIDTH = 1920
    SCR_HEIGHT = 1080
    bg_img = 'assets/background.png'
    font = 'assets/ariblk.ttf'
    path = Path(__file__).parent.parent / bg_img
    path2 = Path(__file__).parent.parent / font
    g = Game(SCR_WIDTH, SCR_HEIGHT, path, path2)

    g.menu()


if __name__ == '__main__':
    main()
