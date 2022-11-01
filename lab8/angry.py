import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill((255, 255, 255))
circle(screen, (255, 255, 0), (200, 200), 100)
circle(screen, (0, 0, 0), (200, 200), 100, 1)
rect(screen, (0, 0, 0), (150, 250, 100, 18))
circle(screen, (255, 0, 0), (160, 170), 22)
circle(screen, (0, 0, 0), (160, 170), 22, 1)
circle(screen, (0, 0, 0), (160, 170), 10)
circle(screen, (255, 0, 0), (240, 170), 18)
circle(screen, (0, 0, 0), (240, 170), 18, 1)
circle(screen, (0, 0, 0), (240, 170), 10)
line(screen, (0, 0, 0), (190, 160), (110, 110), 8)
line(screen, (0, 0, 0), (210, 158), (290, 130), 8)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()