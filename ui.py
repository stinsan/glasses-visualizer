import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import tkinter as tk
import os
from monodepth2.test_simple import test_simple
from tkinter.filedialog import askopenfilename


class Button:
    def __init__(self, x, y, width, height, color, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text        # Default no text.
        select = False          # button's state of being selected

    def draw(self, font_size, window):
        """ Draws the button onto the window.
        :param window: The surface we want to draw the button on.
        """
        # Border for button: dark ass green.
        pygame.draw.rect(window, (0, 60, 0), (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        # Main rectangle for button.
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)

        # Draw text
        if self.text != '':
            font = pygame.font.SysFont('consolas', font_size)                      # Consolas font of size 24.
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

    def setColor(self, color):
        self.color = color

    def setSelect(self, select):
        self.select = select

    # def getSelect(self):
    #     return self.select



def monodepth(filename, model_name):
    """ Runs Monodepth on an image using the given model. It outputs the depth map in the
    same directory as where the original image was.
    :param filename: The global file path of the image.
    :param model_name: The name of the model we want to use.
    """
    test_simple(filename, model_name)


def upload_btn_handler(surface):
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

    img = pygame.image.load(depth_map_global_filename)  # Return the PyGame surface object.
    surface.blit(img, (0, 0))


if __name__ == '__main__':
    pygame.init()  # Initialize PyGame.
    main_surf = pygame.display.set_mode((1200, 676))
    main_surf.fill((53,105,69)) # gray moss green background

    # Set dimension for screen, where image is display
    screen = main_surf.subsurface(Rect(200, 90, 800, 500))
    screen.fill((197,222,204))

    pygame.display.set_caption('Glasses Visualizer')   # Name of the window.

    # Bottom of Screen
    upload_btn = Button(550, 600, 120, 35, (191, 117, 105), 'UPLOAD')   # Initialize the upload button.
        # Left of Screen
    rg_btn = Button(30, 200, 150, 50, (255, 255, 255), 'R/G Colorblindness')    # Initialize the rg colorblind button.
    by_btn = Button(30, 270, 150, 50, (255, 255, 255), 'B/Y Colorblindness')    # Initialize the yg colorblind button.
    total_btn = Button(30, 340, 150, 50, (255, 255, 255), 'Total Colorblindness')   # Initialize the total colorblind button.
        # Right of Screen
    myopia_btn = Button(1020, 200, 150, 50, (255, 255, 255), 'Myopia')   # Initialize the upload button.
    hyperopia_btn = Button(1020, 270, 150, 50, (255, 255, 255), 'Hyperopia')   # Initialize the upload button.
    glasses_btn = Button(1020, 340, 150, 50, (255, 255, 255), 'Glasses On')  # Initialize the glass button.

    is_running = True

    while is_running:
        upload_btn.draw(20, main_surf)  # Draw the upload button.
        rg_btn.draw(12, main_surf)      # Draw the red-green colorblind button.
        by_btn.draw(12, main_surf)      # Draw the blue-yellow colorblind button.
        total_btn.draw(12, main_surf)   # Draw the total colorblind button.
        glasses_btn.draw(12, main_surf) # Draw the total colorblind button.
        myopia_btn.draw(12, main_surf)  # Draw the red-green colorblind button.
        hyperopia_btn.draw(12, main_surf)   # Draw the red-green colorblind button.

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
                    upload_btn_handler(screen)

                # For colorblind buttons
                elif rg_btn.is_hovered(mouse_pos):  # Red Green button listener
                    rg_btn.setColor((67,168,94))
                    rg_btn.setSelect(True)
                        # Disable total colorblindness
                    total_btn.setColor((139,158,144))
                    total_btn.setSelect(False)
                    """TODO: APPLY red-green colorblindness here"""

                elif by_btn.is_hovered(mouse_pos):  # Blue Yellow button listener
                    by_btn.setColor((67,168,94))
                    by_btn.setSelect(True)
                        # Disable total colorblindness
                    total_btn.setColor((139,158,144))
                    total_btn.setSelect(False)
                    """TODO: APPLY blue yellow colorblindness here"""

                elif total_btn.is_hovered(mouse_pos):  # Total button listener
                    total_btn.setColor((67,168,94))
                    total_btn.setSelect(True)
                        # Disable red-green and blue-yellow colorblindness
                    rg_btn.setColor((139,158,144))
                    rg_btn.setSelect(False)
                    by_btn.setColor((139,158,144))
                    by_btn.setSelect(False)
                    """TODO: APPLY total colorblindness here"""

                # For refractive buttons
                elif myopia_btn.is_hovered(mouse_pos):  # Myopia button listener
                    myopia_btn.setColor((67,168,94))
                    myopia_btn.setSelect(True)
                        # Disable hyperopia colorblindness
                    hyperopia_btn.setColor((139,158,144))
                    hyperopia_btn.setSelect(False)
                    """TODO: APPLY myopia here"""
                
                elif hyperopia_btn.is_hovered(mouse_pos):  # Hyperopia button listener
                    hyperopia_btn.setColor((67,168,94))
                    hyperopia_btn.setSelect(True)
                        # Disable myopia colorblindness
                    myopia_btn.setColor((139,158,144))
                    myopia_btn.setSelect(False)
                    """TODO: APPLY hyperopia here"""

                elif glasses_btn.is_hovered(mouse_pos):  # Hyperopia button listener
                    glasses_btn.setColor((67,168,94))
                    glasses_btn.setSelect(True)
                    glasses_img = pygame.image.load("images/glasses.png")
                    screen.blit(glasses_img, (60, 80))
                    """TODO: APPLY glasses here (correct colorblind or myopia etc.)"""
            
            # Right click
            """TODO: UNDO any pressed button"""

            # Key press
            """TODO: Change the values of myopia and hyperopia, have a pop-up to display the values"""
>>>>>>> 500a18930b3fd997669403b955b4922d612c88e2
