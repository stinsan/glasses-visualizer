import numpy as np
from PIL import Image


def remove_gamma(val):
    """ Transforming the color into Linear RGB space """
    val = val / 255
    if val <= 0.04045:
        new_val = val / 12.92
    else:
        new_val = ((val + 0.055) / 1.055) ** 2.4

    return new_val


def apply_gamma(val):
    """ Applying Gamma Correction to get RGB"""
    if val <= 0.0031308:
        new_val = 255 * (12.92 * val)
    else:
        new_val = 255 * (1.055 * (val ** 0.4166) - 0.055)

    return new_val


def linear_lms(color):
    """ Converting color in linear space to a color in LMS color space"""
    tmatrix = np.array([[0.31399022, 0.63951294, 0.04649755], [0.15537241, 0.75789446, 0.08670142],
                        [0.01775239, 0.10944209, 0.87256922]])  # Transformation matrix
    new_color = np.matmul(tmatrix, color)
    return new_color


def lms_linear(color):
    """ Converting color in LMS space to linear space"""
    invtmatrix = np.array([
        [5.47221206, -4.6419601, 0.16963708], [-1.1252419, 2.29317094, -0.1678952], [0.02980165, -0.19318073,
                                                                                     1.16364789]])
    # inverse transformation matrix
    new_color = np.matmul(invtmatrix, color)
    return new_color


def protanopia(color):
    """ Multiplying by Protanopia simulation matrix to get red green color blindness"""
    psimmatrix = np.array([[0, 1.05118294, -0.05116099], [0, 1, 0], [0, 0, 1]])  # lack of L cone
    new_color = np.matmul(psimmatrix, color)
    return new_color


def tritanopia(color):
    """ Multiplying by Tritanopia simulation matrix to get blue yellow color blindness"""
    tsimmatrix = np.array([[1, 0, 0], [0, 1, 0], [-0.86744736, 1.86727089, 0]])  # lack of m cone
    new_color = np.matmul(tsimmatrix, color)
    return new_color


def monochromat(color):
    """Multiplying by Achromatopsia simulation matrix to get total color blindess"""
    asimmatrix = np.array([0.01775, 0.10945, 0.87262])
    dot_color = np.dot(asimmatrix, color)
    new_color = np.array([dot_color, dot_color, dot_color])
    return new_color


def rg(img):
    """ Alters an image to Red/Green colorblindess"""
    img_width, img_height = img.size
    orig_pixels = img.load()
    for img_y in range(img_height):
        for img_x in range(img_width):
            r, g, b = orig_pixels[img_x, img_y]
            color = np.array([r, g, b])

            # change color
            linear_color = np.array(
                [remove_gamma(color[0]), remove_gamma(color[1]), remove_gamma(color[2])])  # remove gamma
            lms_color = linear_lms(linear_color)  # convert to lms
            pcolor = protanopia(lms_color)  # apply
            linear_color2 = lms_linear(pcolor)  # convert to linear
            new_color = np.array([apply_gamma(linear_color2[0]), apply_gamma(linear_color2[1]),
                                 apply_gamma(linear_color2[2])])  # reapply gamma

            orig_pixels[img_x, img_y] = int(new_color[0]), int(new_color[1]), int(new_color[2])  # replace color


def BY(img):
    """ Alters an image to Blue/Yellow colorblindess"""
    img_width, img_height = img.size
    orig_pixels = img.load()
    for img_y in range(img_height):
        for img_x in range(img_width):
            r, g, b = orig_pixels[img_x, img_y]
            color = np.array([r, g, b])

            # change color
            linear_color = np.array(
                [remove_gamma(color[0]), remove_gamma(color[1]), remove_gamma(color[2])])  # remove gamma
            lms_color = linear_lms(linear_color)  # convert to lms
            tcolor = tritanopia(lms_color)  # apply
            linear_color2 = lms_linear(tcolor)  # convert to linear
            new_color = np.array([apply_gamma(linear_color2[0]), apply_gamma(linear_color2[1]),
                                 apply_gamma(linear_color2[2])])  # reapply gamma

            orig_pixels[img_x, img_y] = int(new_color[0]), int(new_color[1]), int(new_color[2])  # replace color


def mono(img):
    """ Alters an image to be fully color blind (monochromatic)"""
    img_width, img_height = img.size
    orig_pixels = img.load()
    for img_y in range(img_height):
        for img_x in range(img_width):
            r, g, b = orig_pixels[img_x, img_y]
            color = np.array([r, g, b])

            new_color = monochromat(color)
            orig_pixels[img_x, img_y] = int(new_color[0]), int(new_color[1]), int(new_color[2])  # replace color
