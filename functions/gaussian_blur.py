import math
import numpy as np
import time


def norm_dist(x, mean, sd):
    """ Formula from https://en.wikipedia.org/wiki/Normal_distribution.
    """
    return (1 / (sd * math.sqrt(2 * math.pi))) * (math.pow(math.e, (-1/2) * math.pow(((x - mean) / sd), 2)))


def gaussian_kernel(size, sd=1):
    """ Creates a 1D Gaussian kernel.
    :param size: The size of the kernel, can only be odd.
    :param sd: The standard deviation of the kernel, used when calculating the normal distribution.
    :return: A 1D array representing the Gaussian kernel.
    """
    kernel_1d = np.linspace(-(size // 2), size // 2, size)

    for i in range(size):
        kernel_1d[i] = norm_dist(kernel_1d[i], 0, sd)

    kernel_1d *= 1.0 / kernel_1d.max()  # Normalize to get values in [0, 1]

    return kernel_1d


def vertical_convolution(img, kernel_vals, level):
    img_width, img_height = img.size
    orig_pixels = img.load()
    img_copy = img.copy()
    copy_pixels = img_copy.load()

    if level == -5.0 or level == 3.0:
        vsize = 17
    elif level == -4.0 or level == 2.0:
        vsize = 11
    elif level == -3:
        vsize = 5
    elif level == -6.0 or level == 4.0:
        vsize = 23
    elif level == 5.0:
        vsize = 29
    else:
        vsize = 17

    # For every pixel in image
    for img_y in range(img_height):
        for img_x in range(img_width):
            kernel = gaussian_kernel(vsize, kernel_vals[img_y][img_x])
            kernel_width = len(kernel)
            kernel_half = kernel_width // 2
            kernel_tot = np.sum(kernel)

            # For every value in kernel
            new_r, new_g, new_b = 0, 0, 0
            for kernel_offset in range(-kernel_half, kernel_half + 1):

                kernel_index = kernel_offset + kernel_half
                kernel_val = kernel[kernel_index]

                if img_y + kernel_offset < 0 or img_y + kernel_offset >= img_height:
                    new_r += 128 * kernel_val
                    new_g += 128 * kernel_val
                    new_b += 128 * kernel_val
                    continue

                r, g, b = orig_pixels[img_x, img_y + kernel_offset]

                new_r += r * kernel_val
                new_g += g * kernel_val
                new_b += b * kernel_val

            # Average
            new_r /= kernel_tot
            new_g /= kernel_tot
            new_b /= kernel_tot

            copy_pixels[img_x, img_y] = (int(new_r), int(new_g), int(new_b))

    return img_copy


def horizontal_convolution(img, kernel_vals, level):
    img_width, img_height = img.size
    orig_pixels = img.load()
    img_copy = img.copy()
    copy_pixels = img_copy.load()

    print(type(level))

    if level == -5.0 or level == 3.0:
        hsize = 17
    elif level == -4.0 or level == 2.0:
        hsize = 11
    elif level == -3:
        hsize = 5
    elif level == -6.0 or level == 4.0:
        hsize = 23
    elif level == 5.0:
        hsize = 29
    else:
        hsize = 17

    # For every pixel in image
    for img_y in range(img_height):
        for img_x in range(img_width):
            kernel = gaussian_kernel(hsize, kernel_vals[img_y][img_x])
            kernel_width = len(kernel)
            kernel_half = kernel_width // 2
            kernel_tot = np.sum(kernel)

            # For every value in kernel
            new_r, new_g, new_b = 0, 0, 0
            for kernel_offset in range(-kernel_half, kernel_half + 1):

                kernel_index = kernel_offset + kernel_half
                kernel_val = kernel[kernel_index]

                if img_x + kernel_offset < 0 or img_x + kernel_offset >= img_width:
                    new_r += 128 * kernel_val
                    new_g += 128 * kernel_val
                    new_b += 128 * kernel_val
                    continue

                r, g, b = orig_pixels[img_x + kernel_offset, img_y]

                new_r += r * kernel_val
                new_g += g * kernel_val
                new_b += b * kernel_val

            # Average
            new_r /= kernel_tot
            new_g /= kernel_tot
            new_b /= kernel_tot

            copy_pixels[img_x, img_y] = (int(new_r), int(new_g), int(new_b))

    return img_copy


def convolution(img, kernel_values, level):
    start = time.time()

    h_img = horizontal_convolution(img, kernel_values, float(level))
    print('Horizontal convolution complete!')
    v_img = vertical_convolution(h_img, kernel_values, float(level))
    print('Vertical convolution complete!')

    diff = time.time() - start
    print('Blurring time taken: {}'.format(diff))

    return v_img


def kernel_sd_function(color, sight_val):
    """

    :param color:
    :return:
    """

    if(float(sight_val) < 0):  # myopia (cant see far away)
        x = (int(color[0]) + int(color[1]) + int(color[2])) / 765
    else:  # hyperopia (cant see close up)
        x = 1 - (int(color[0]) + int(color[1]) + int(color[2])) / 765
    # return (-10 * x) + 10
    return 10 * math.pow(x - 1, 2)
    # return 10 * math.pow(x - 1, 4)


def calculate_kernel_values_from_colormap(cm, val):
    """
    :param cm:
    :return:
    """
    k_vals = []

    for row in cm:
        k_row_vals = []
        for color in row:
            k_row_vals.append(kernel_sd_function(color, val))

        k_vals.append(k_row_vals)

    return k_vals
