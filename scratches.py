import pygame
import pygame.gfxdraw

def drawScratch(img, pixelx, pixely):
    """ Alter the image to make a "scratch" appear where the user clicks"""
    color = (255, 255, 255, 100) # white see through color

    pygame.gfxdraw.line(img, pixelx, pixely, pixelx, pixely, color)


def drawSmudge(img, pixelx, pixely):
    """ Alter the image to make a "smudge" appear where the user clicks"""
    color = (255, 255, 255, 100) # white see through color

    pixels = img.load()
    # check to see if there is already a smuge there
    if(pixels[pixelx, pixely]):
        # do not draw over another circle
        print("tea")

    pygame.gfxdraw.filled_circle(img, pixelx, pixely, 20, color)  # draw a filled circle smudge

