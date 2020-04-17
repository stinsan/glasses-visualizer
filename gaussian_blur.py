import math
import numpy as np
import time
from tkinter.filedialog import askopenfilename
from PIL import Image


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


def vertical_convolution(img, kernel):
    img_width, img_height = img.size
    kernel_width = len(kernel)
    kernel_half = kernel_width // 2
    kernel_tot = np.sum(kernel)

    orig_pixels = img.load()
    img_copy = img.copy()
    copy_pixels = img_copy.load()

    # For every pixel in image
    n = 0
    for img_y in range(img_height):
        for img_x in range(img_width):

            n += 1
            print('{} / {} done!'.format(n, img_height * img_width))
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


def horizontal_convolution(img, kernel):
    img_width, img_height = img.size
    kernel_width = len(kernel)
    kernel_half = kernel_width // 2
    kernel_tot = np.sum(kernel)

    orig_pixels = img.load()
    img_copy = img.copy()
    copy_pixels = img_copy.load()

    # For every pixel in image
    n = 0
    for img_y in range(img_height):
        for img_x in range(img_width):

            n += 1
            print('{} / {} done!'.format(n, img_height * img_width))
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


def convolution(img, kernel):
    start = time.time()
    h_img = horizontal_convolution(img, kernel)
    v_img = vertical_convolution(h_img, kernel)

    diff = time.time() - start

    print('Time taken: {}'.format(diff))
    img.show()
    v_img.show()

if __name__ == '__main__':
    fp = askopenfilename()
    img = Image.open(fp).convert('RGB')
    kernel = gaussian_kernel(101, sd=5)

    convolution(img, kernel)
