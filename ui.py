import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import tkinter as tk
import os
from monodepth2.test_simple import test_simple
from tkinter.filedialog import askopenfilename


class Button():
    def __init__(self, x, y, width, height, color, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text        # Default no text.

    def draw(self, window):
        """ Draws the button onto the window.
        :param window: The window we want to draw the button on.
        """
        # Border for button: dark ass green.
        pygame.draw.rect(window, (0, 60, 0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        # Main rectangle for button.
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)

        # Draw text
        if self.text != '':
            font = pygame.font.SysFont('consolas', 24)                      # Consolas font of size 24.
            text = font.render(self.text, 1, (0, 0, 0))                     # Render font black.
            center = (self.x + (self.width / 2 - text.get_width() / 2),     # Center of button.
                      self.y + (self.height / 2 - text.get_height() / 2))

            # Draw text at center of button.
            window.blit(text, center)

    def is_hovered(self, mouse_pos):
        """ Is the mouse hovering over the button?
        :param mouse_pos: The position of the mouse.
        :return: True if the mouse is hovering over the button, else false.
        """
        if self.x < mouse_pos[0] < self.x + self.width:
            if self.y < mouse_pos[1] < self.y + self.height:
                return True

        return False


def monodepth(filename, model_name):
    """ Runs Monodepth on an image using the given model. It outputs the depth map in the
    same directory as where the original image was.
    :param filename: The global file path of the image.
    :param model_name: The name of the model we want to use.
    """
    test_simple(filename, model_name)

def upload_btn_handler():
    """ Handles everything related to uploading an image.
    TODO: Gaussian blur would probably be called here somewhere.
    :return The PyGame surface object containing the resulting image.
    """
    root = tk.Tk()
    root.attributes('-topmost', True)   # We want the "choose file" window on top of PyGame.
    root.withdraw()                     # Hide that annoying little screen that comes with initializing tk.

    # Asks the user for an image, runs that through Monodepth
    # using the (hard-coded) model.
    img_global_filename = askopenfilename()
    monodepth_model = 'mono+stereo_1024x320'
    monodepth(img_global_filename, monodepth_model)

    # Monodepth outputs a depth map with the file name
    # '<original-image-name>_disp.jpg' in the directory of the original image.
    # We want to find that path so we can find the depth map.
    output_directory = os.path.dirname(img_global_filename)
    img_local_filename = os.path.splitext(os.path.basename(img_global_filename))[0]
    depth_map_global_filename = os.path.join(output_directory, "{}_disp.jpeg".format(img_local_filename))

    return pygame.image.load(depth_map_global_filename)  # Return the PyGame surface object.


if __name__ == '__main__':
    pygame.init()  # Initialize PyGame.
    win = pygame.display.set_mode((1024, 676))  # Set the window dimensions.
    pygame.display.set_caption('daddy weaver uwu')  # Name of the window.

    upload_btn = Button(460, 630, 100, 30, (0, 255, 0), 'Upload')   # Initialize the upload button.
    is_running = True

    while is_running:
        upload_btn.draw(win)        # Draw the upload button.
        pygame.display.update()

        # Event handling.
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()  # The mouse's position.

            # Quit.
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                quit()

            # Left click.
            if event.type == pygame.MOUSEBUTTONDOWN:
                if upload_btn.is_hovered(mouse_pos):
                    # Get the modified image and show it onto the screen.
                    img = upload_btn_handler()
                    win.blit(img, (0, 0))