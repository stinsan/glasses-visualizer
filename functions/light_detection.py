from random import randint
import pygame
import pygame.gfxdraw


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
    numpoints = int(img_width * img_height / 1000)

    brightest_lum = -1  # initialize to dark luminence
    brightest_point = None
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


def halo(surface, img):
    """ Create a halo effect on brightest light sources"""
    if img is None:
        return

    img = img.resize(surface.get_size())
    orig_pixels = img.load()

    brightest_points = list_of_light_points(img, orig_pixels)

    for i in range(10):  # get the 20 brightest points
        r, g, b = orig_pixels[brightest_points[i].x, brightest_points[i].y]  # get the color of the point
        lum = (0.2126 * r + 0.7152 * g + 0.0722 * b)  # get the luminocity of the point
        pygame.gfxdraw.filled_circle(surface, brightest_points[i].x, brightest_points[i].y, int(lum / 10),
                                     (r, g, b, 50))   # draw a filled circle for the halo

    return brightest_points


def halo_static(surface, img, brightest_points):
    if img is None:
        return

    img = img.resize(surface.get_size())
    orig_pixels = img.load()

    if brightest_points is None:
        brightest_points = list_of_light_points(img, orig_pixels)

    for i in range(10):  # get the 20 brightest points
        r, g, b = orig_pixels[brightest_points[i].x, brightest_points[i].y]  # get the color of the point
        lum = (0.2126 * r + 0.7152 * g + 0.0722 * b)  # get the luminocity of the point
        pygame.gfxdraw.filled_circle(surface, brightest_points[i].x, brightest_points[i].y, int(lum / 10),
                                     (r, g, b, 50))   # draw a filled circle for the halo

    return brightest_points

def starburst(surface, img):
    """ Create starburst effect on brightest light sources"""
    if img is None:
        return

    img = img.resize(surface.get_size())
    orig_pixels = img.load()

    img_width, img_height = img.size

    brightest_points = list_of_light_points(img, orig_pixels)

    for i in range(20):  # get the 20 brightest points
        r, g, b = orig_pixels[brightest_points[i].x, brightest_points[i].y]  # get the color of the point
        lum = (0.2126 * r + 0.7152 * g + 0.0722 * b)  # get the luminocity of the point

        x = brightest_points[i].x
        y = brightest_points[i].y

        leftx = x - (lum / 10)  # left corner of the starburst
        rightx = x + (lum / 10)  # right corner of the starburst
        topy = y + (lum / 10)  # top corner of the starburst
        bottomy = y - (lum / 10)  # bottom corner of the starburst

        if leftx > 0 and rightx < img_width and topy < img_height and bottomy > 0:  # check that starburst will be in image
            pygame.gfxdraw.filled_polygon(surface, [[x - 3, y], [x, topy], [x + 3, y], [x, bottomy]], (r, g, b, 70))
            pygame.gfxdraw.filled_polygon(surface, [[x, y - 3], [rightx, y], [x, y + 3], [leftx, y]], (r, g, b, 70))

    return brightest_points


def starburst_static(surface, img, brightest_points):
    if img is None:
        return

    img = img.resize(surface.get_size())
    orig_pixels = img.load()

    img_width, img_height = img.size

    if brightest_points is None:
        brightest_points = list_of_light_points(img, orig_pixels)

    for i in range(20):  # get the 20 brightest points
        r, g, b = orig_pixels[brightest_points[i].x, brightest_points[i].y]  # get the color of the point
        lum = (0.2126 * r + 0.7152 * g + 0.0722 * b)  # get the luminocity of the point

        x = brightest_points[i].x
        y = brightest_points[i].y

        leftx = x - (lum / 10)  # left corner of the starburst
        rightx = x + (lum / 10)  # right corner of the starburst
        topy = y + (lum / 10)  # top corner of the starburst
        bottomy = y - (lum / 10)  # bottom corner of the starburst

        if leftx > 0 and rightx < img_width and topy < img_height and bottomy > 0:  # check that starburst will be in image
            pygame.gfxdraw.filled_polygon(surface, [[x - 3, y], [x, topy], [x + 3, y], [x, bottomy]], (r, g, b, 70))
            pygame.gfxdraw.filled_polygon(surface, [[x, y - 3], [rightx, y], [x, y + 3], [leftx, y]], (r, g, b, 70))

    return brightest_points