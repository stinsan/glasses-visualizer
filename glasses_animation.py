import pygame
from pygame.locals import *

GLASSES_RECT = [(50, 140, 300, 220), (500, 140, 300, 220)]
GLASSES_BRIDGE = (350, 180, 150, 20)


def draw_glasses(surface):
    pygame.draw.rect(surface, (0, 0, 0), GLASSES_BRIDGE, 0)
    for rect in GLASSES_RECT:
        pygame.draw.rect(surface, (0, 0, 0), rect, 20)


def clear_glasses(surface, image):
    if image is None:
        surface.fill((197, 222, 204))  # Lime-ish green.
    else:
        surface.blit(image, (0, 0))