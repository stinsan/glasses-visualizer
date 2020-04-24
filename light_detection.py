import numpy as np
from random import randint
import pygame
import pygame.gfxdraw
from PIL import Image


class Point:
    def __init__(self, x, y, luminance):
        self.x = x
        self.y = y
        self.luminance = luminance


def random_point(w, h):
    """ Get a random point from the image """
    randx = randint(0, w - 1)
    randy = randint(0, h - 1)
    return randx, randy


def find_brightest_point(img, pixels):
    """ Determining the brightest point in a set of random points"""
    img_width, img_height = img.size
    numpoints = int(img.width * img_height / 1000)

    brightest_lum = -1  # initialize to dark luminence

    for i in range(numpoints):  # find brightest in list
        rando = random_point(img_width, img_height)

        r, g, b = pixels[rando]
        lum = (0.2126 * r + 0.7152 * g + 0.0722 * b)

        if lum > brightest_lum:  # brighter than current brightest
            brightest_point = rando
            brightest_lum = lum

    return brightest_point, brightest_lum

def list_of_light_points(img, orig_pixels):
    """ Create list of points where we will create light affects"""
    brightest_points = []  # size 50 list of bright points
    for i in range(50):
        pt, luminance = find_brightest_point(img, orig_pixels)
        brightest_points.append(Point(pt[0], pt[1], luminance))

    list.sort(brightest_points, key=lambda pt: pt.luminance, reverse=True)  # sort the bright points in order of brightness
    return brightest_points


def halo(img):
    """ Create a halo affect on brightest light sources"""
    img_width, img_height = img.size
    orig_pixels = img.load()

    brightest_points = list_of_light_points(img, orig_pixels)

    for i in range(20):  # get the 20 brightest points
        r, g, b = orig_pixels[brightest_points[i].x, brightest_points[i].y]  # get the color of the point
        lum = (0.2126 * r + 0.7152 * g + 0.0722 * b)  # get the luminocity of the point
        pygame.gfxdraw.filled_circle(img, brightest_points[i].x, brightest_points[i].y, int(lum / 10),
                                     (r, g, b, 50))   # draw a filled circle for the halo


