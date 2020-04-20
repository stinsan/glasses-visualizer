import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import tkinter as tk
import os
from monodepth2.test_simple import test_simple
from tkinter.filedialog import askopenfilename
from gaussian_blur import *

class Button:
    def __init__(self, x, y, width, height, color, borderColor, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.borderColor = borderColor
        self.text = text  # Default no text.
        self.select = False # button's state of being selected

    def draw(self, font_size, window):
        """ Draws the button onto the window.
        :param window: The surface we want to draw the button on.
        """
        # Border for button
        pygame.draw.rect(window, self.borderColor, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        # Main rectangle for button.
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)

        # Draw text
        if self.text != '':
            font = pygame.font.SysFont('consolas', font_size)                 # Consolas font of size 24.
            text = font.render(self.text, 1, (0, 0, 0))                       # Render font black.
            center = (self.x + (self.width / 2 - text.get_width() / 2),       # Center of button.
                      self.y + (self.height / 2 - text.get_height() / 2) + 2)

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

    def getSelect(self):
        return self.select


def monodepth(filename, image_size, model_name):
    """ Runs Monodepth on an image using the given model. It outputs the depth map in the
    same directory as where the original image was.
    :param filename: The global file path of the image.
    :param model_name: The name of the model we want to use.
    """
    return test_simple(filename, image_size, model_name)


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
    depth_map = monodepth(img_global_filename, (640, 427), monodepth_model)

    # Monodepth outputs a depth map with the file name
    # '<original-image-name>_disp.jpg' in the directory of the original image.
    # We want to find that path so we can find the depth map.
    output_directory = os.path.dirname(img_global_filename)
    img_local_filename = os.path.splitext(os.path.basename(img_global_filename))[0]
    depth_map_global_filename = os.path.join(output_directory, "{}_disp.jpeg".format(img_local_filename))

    kernel_vals = calculate_kernel_values_from_colormap(depth_map)
    imgthang = Image.open(img_global_filename).resize((640, 427)).convert('RGB')
    img = convolution(imgthang, kernel_vals)  # outputting the blurred image

    mode = img.mode
    size = img.size
    data = img.tobytes()

    py_image = pygame.image.fromstring(data, size, mode)
    py_image = pygame.transform.scale(py_image, (surface.get_size()))

    # Return the PyGame surface object.
    surface.blit(py_image, (0, 0))

if __name__ == '__main__':
    pygame.init()  # Initialize PyGame.
    main_surf = pygame.display.set_mode((1240, 690))
    main_surf.fill((53,105,69)) # gray moss green background

    # Add background lines
    currX = 50
    while currX <= 1500:
        pygame.draw.line(main_surf, (60, 117, 78), (currX, 0), (currX - 300, 690), 5)
        currX += 50

    # Set dimension for screen, where image is displayed.
    # Image resolutions should be 3:2 (640 x 427).
    screen = main_surf.subsurface(Rect(200, 100, 840, 497))
    screen.fill((197, 222, 204))

    # Add Screen Shadow
    pygame.draw.line(screen, (170, 191, 176), (0, 0), (840, 0), 15)
    pygame.draw.line(screen, (170, 191, 176), (0, 0), (0, 497), 15)
    pygame.draw.line(screen, (145, 163, 150), (0, 0), (7, 7), 1)

    # Title
    pygame.display.set_caption('Glasses Visualizer')   # Name of the window.

    # Draw Logo
    logo_img = pygame.image.load("images/logo.png")
    main_surf.blit(logo_img, (335, 28))

    # Add Upload Text
    font = pygame.font.SysFont('lato', 42)
    text1 = font.render("Please Upload", 1, (152, 171, 157))
    text2 = font.render("a Picture", 1, (152, 171, 157))
    screen.blit(text1, (280, 150))
    screen.blit(text2, (330, 200))

    # Draw Arrow
    arrow_img = pygame.image.load("images/arrow.png")
    screen.blit(arrow_img, (360, 260))

    # Copyright Text
    copyright_img = pygame.image.load("images/copyright.png")
    main_surf.blit(copyright_img, (1140, 665))

    # Bottom of Screen
    upload_btn = Button(555, 625, 120, 35, (191, 117, 105), (87, 13, 13), 'UPLOAD')   # Initialize the upload button.
    # Left of Screen
    rg_btn = Button(26, 232, 150, 50, (255, 255, 255), (0, 60, 0), 'R/G Colorblindness')      # Initialize the rg colorblind button.
    by_btn = Button(26, 302, 150, 50, (255, 255, 255), (0, 60, 0), 'B/Y Colorblindness')      # Initialize the yg colorblind button.
    pygame.draw.rect(main_surf, (34, 69, 45), (16, 373, 170, 2), 0)                 # DIVIDER
    total_btn = Button(26, 397, 150, 50, (255, 255, 255), (0, 60, 0), 'Total Colorblindness') # Initialize the total colorblind button.
    # Right of Screen
    myopia_btn = Button(1064, 232, 150, 50, (255, 255, 255), (0, 60, 0), 'Myopia')   # Initialize the upload button.
    hyperopia_btn = Button(1064, 302, 150, 50, (255, 255, 255), (0, 60, 0), 'Hyperopia')   # Initialize the upload button.
    pygame.draw.rect(main_surf, (34, 69, 45), (1054, 373, 170, 2), 0)
    glasses_btn = Button(1064, 397, 150, 50, (255, 255, 255), (0, 60, 0), 'Glasses On')  # Initialize the glass button.

    is_running = True

    while is_running:
        upload_btn.draw(20, main_surf)    # Draw the upload button.
        rg_btn.draw(12, main_surf)        # Draw the red-green colorblind button.
        by_btn.draw(12, main_surf)        # Draw the blue-yellow colorblind button.
        total_btn.draw(12, main_surf)     # Draw the total colorblind button.
        glasses_btn.draw(12, main_surf)   # Draw the total colorblind button.
        myopia_btn.draw(12, main_surf)    # Draw the red-green colorblind button.
        hyperopia_btn.draw(12, main_surf) # Draw the red-green colorblind button.

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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if upload_btn.is_hovered(mouse_pos):
                    # Get the modified image and show it onto the screen.
                    upload_btn_handler(screen)

                # For colorblind buttons
                elif rg_btn.is_hovered(mouse_pos):  # Red Green button listener
                    rg_btn.setColor((67,168,94))
                    rg_btn.setSelect(True)
                        # Disable total colorblindness
                    total_btn.setColor((255, 255, 255))
                    total_btn.setSelect(False)
                    """TODO: APPLY red-green colorblindness here"""

                elif by_btn.is_hovered(mouse_pos):  # Blue Yellow button listener
                    by_btn.setColor((67,168,94))
                    by_btn.setSelect(True)
                        # Disable total colorblindness
                    total_btn.setColor((255, 255, 255))
                    total_btn.setSelect(False)
                    """TODO: APPLY blue yellow colorblindness here"""

                elif total_btn.is_hovered(mouse_pos):  # Total button listener
                    total_btn.setColor((67,168,94))
                    total_btn.setSelect(True)
                        # Disable red-green and blue-yellow colorblindness
                    rg_btn.setColor((255, 255, 255))
                    rg_btn.setSelect(False)
                    by_btn.setColor((255, 255, 255))
                    by_btn.setSelect(False)
                    """TODO: APPLY total colorblindness here"""

                # For refractive buttons
                elif myopia_btn.is_hovered(mouse_pos):  # Myopia button listener
                    myopia_btn.setColor((67,168,94))
                    myopia_btn.setSelect(True)
                        # Disable hyperopia colorblindness
                    hyperopia_btn.setColor((255, 255, 255))
                    hyperopia_btn.setSelect(False)
                    """TODO: APPLY myopia here"""
                
                elif hyperopia_btn.is_hovered(mouse_pos):  # Hyperopia button listener
                    hyperopia_btn.setColor((67,168,94))
                    hyperopia_btn.setSelect(True)
                        # Disable myopia colorblindness
                    myopia_btn.setColor((255, 255, 255))
                    myopia_btn.setSelect(False)
                    """TODO: APPLY hyperopia here"""

                elif glasses_btn.is_hovered(mouse_pos):  # Hyperopia button listener
                    glasses_btn.setColor((67,168,94))
                    glasses_btn.setSelect(True)
                    glasses_img = pygame.image.load("images/glasses.png")
                    screen.blit(glasses_img, (78, 100))
                    """TODO: APPLY glasses here (correct colorblind or myopia etc.)"""
            
            # Right click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                # For colorblind buttons
                if rg_btn.is_hovered(mouse_pos) and rg_btn.getSelect(): # Red Green button listener
                    rg_btn.setColor((255, 255, 255))
                    rg_btn.setSelect(False)
                    """TODO: UNAPPLY red-green colorblindness here"""

                elif by_btn.is_hovered(mouse_pos) and by_btn.getSelect(): # Blue Yellow button listener
                    by_btn.setColor((255, 255, 255))
                    by_btn.setSelect(False)
                    """TODO: UNAPPLY blue yellow colorblindness here"""

                elif total_btn.is_hovered(mouse_pos) and total_btn.getSelect(): # Total button listener
                    total_btn.setColor((255, 255, 255))
                    total_btn.setSelect(False)
                    """TODO: UNAPPLY total colorblindness here"""

                # For refractive buttons
                elif myopia_btn.is_hovered(mouse_pos) and myopia_btn.getSelect():  # Myopia button listener
                    myopia_btn.setColor((255, 255, 255))
                    myopia_btn.setSelect(False)
                    """TODO: UNAPPLY myopia here"""
                
                elif hyperopia_btn.is_hovered(mouse_pos) and hyperopia_btn.getSelect():  # Hyperopia button listener
                    hyperopia_btn.setColor((255, 255, 255))
                    hyperopia_btn.setSelect(False)
                    """TODO: UNAPPLY hyperopia here"""

                elif glasses_btn.is_hovered(mouse_pos) and glasses_btn.getSelect():  # Hyperopia button listener
                    glasses_btn.setColor((255, 255, 255))
                    glasses_btn.setSelect(False)
                    """TODO: UNAPPLY glasses here (apply colorblind or myopia etc.)"""

            # Key press
            """TODO: Change the values of myopia and hyperopia, have a pop-up to display the values"""

            # Hovering
            if upload_btn.is_hovered(mouse_pos):
                upload_btn.setColor((138, 84, 74))
            else:
                upload_btn.setColor((158, 96, 85))

            if not rg_btn.getSelect():
                if rg_btn.is_hovered(mouse_pos):
                    rg_btn.setColor((220, 220, 220))
                else:
                    rg_btn.setColor((255, 255, 255))

            if not by_btn.getSelect():
                if by_btn.is_hovered(mouse_pos):
                    by_btn.setColor((220, 220, 220))
                else:
                    by_btn.setColor((255, 255, 255))

            if not total_btn.getSelect():
                if total_btn.is_hovered(mouse_pos):
                    total_btn.setColor((220, 220, 220))
                else:
                    total_btn.setColor((255, 255, 255))

            if not myopia_btn.getSelect():
                if myopia_btn.is_hovered(mouse_pos):
                    myopia_btn.setColor((220, 220, 220))
                else:
                    myopia_btn.setColor((255, 255, 255))
            
            if not hyperopia_btn.getSelect():
                if hyperopia_btn.is_hovered(mouse_pos):
                    hyperopia_btn.setColor((220, 220, 220))
                else:
                    hyperopia_btn.setColor((255, 255, 255))

            if not glasses_btn.getSelect():
                if glasses_btn.is_hovered(mouse_pos):
                    glasses_btn.setColor((220, 220, 220))
                else:
                    glasses_btn.setColor((255, 255, 255))