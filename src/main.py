import pygame
from game import Game

pygame.init()
pygame.font.init()
# print(pygame.font.get_fonts())

game = Game()
game.run_game_loop()

pygame.quit()
quit()