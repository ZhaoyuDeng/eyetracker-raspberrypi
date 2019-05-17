import pygame
from sys import exit
import time


pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
pygame.display.set_caption("Hello, World!")
background = pygame.image.load('./GetPosPic/test2.png').convert()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(background, (0, 0))
    x, y = pygame.mouse.get_pos()
    print([x, y])
    time.sleep(0.2)
    pygame.display.update()
