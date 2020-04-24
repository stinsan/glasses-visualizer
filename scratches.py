import pygame
import pygame.gfxdraw

def draw_scratch(surface, img, pixelx, pixely):
    """ Alter the image to make a "scratch" appear where the user clicks"""
    color = (255, 255, 255, 100) # white see through color

    pygame.gfxdraw.pixel(surface, pixelx, pixely, color)


def draw_smudge(surface, img, pixelx, pixely):
    """ Alter the image to make a "smudge" appear where the user clicks"""
    color = (255, 255, 255, 100) # white see through color

    pixels = img.load()

    pygame.gfxdraw.filled_circle(surface, pixelx, pixely, 20, color)  # draw a filled circle smudge

