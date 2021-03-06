import pygame
from pygame.locals import *

import tkinter as tk
import os
from monodepth2.test_simple import test_simple
from functions.gaussian_blur import *
from tkinter import filedialog
from PIL import Image
from functions import colorblind, light_detection as ld
from functions.glasses_animation import Glasses

def draw_extra_main_surface(main_surface):
    """ Draws extra UI elements onto the main surface.
    :param surface: The main surface.
    """

    # Add background lines.
    curr_x = 50
    while curr_x <= 1500:
        pygame.draw.line(main_surface, (60, 117, 78), (curr_x, 0), (curr_x - 300, 690), 5)
        curr_x += 50

    # Title
    pygame.display.set_caption('Glasses Visualizer')   # Name of the window.

    # Draw Logo
    logo_img = pygame.image.load("images/logo.png")
    main_surface.blit(logo_img, (335, 28))

    # Copyright Text
    copyright_img = pygame.image.load("images/copyright.png")
    main_surface.blit(copyright_img, (1140, 665))


def draw_extra_screen(screen):
    """ Draws extra UI elements onto the screen (subsurface) where the image will be shown.
    :param screen: The subsurface where the image will be shown (eventually).
    """
    # Add Screen Shadow
    pygame.draw.line(screen, (170, 191, 176), (0, 0), (840, 0), 15)
    pygame.draw.line(screen, (170, 191, 176), (0, 0), (0, 497), 15)
    pygame.draw.line(screen, (145, 163, 150), (0, 0), (7, 7), 1)

    # Add Upload Text
    font = pygame.font.SysFont('lato', 42)
    text1 = font.render("Please Upload", 1, (152, 171, 157))
    text2 = font.render("a Picture", 1, (152, 171, 157))
    screen.blit(text1, (315, 150))
    screen.blit(text2, (355, 200))

    # Draw Arrow
    arrow_img = pygame.image.load("images/arrow.png")
    screen.blit(arrow_img, (360, 260))

    return


def monodepth(filename, image_size, model_name):
    """ Runs Monodepth on an image using the given model. It outputs the depth map in the
    same directory as where the original image was.
    :param filename: The global file path of the image.
    :param model_name: The name of the model we want to use.
    """
    return test_simple(filename, image_size, model_name)


def blit_img(surface, img):
    """ Given a PIL image, blits it onto the surface.
    :param surface: The surface we're blitting to.
    :param img: A PIL image. HAS TO BE A PIL IMAGE!
    """
    if img is None:
        return

    mode = img.mode
    size = img.size
    data = img.tobytes()

    py_image = pygame.image.fromstring(data, size, mode)
    py_image = pygame.transform.scale(py_image, (surface.get_size()))

    surface.blit(py_image, (0, 0))


def upload_btn_handler(surface, sightval):
    """ Handles everything related to uploading an image.
    :return The PyGame surface object containing the resulting image.
    """
    root = tk.Tk()
    root.attributes('-topmost', True)   # We want the "choose file" window on top of PyGame.
    root.withdraw()                     # Hide that annoying little screen that comes with initializing tk.

    # Asks the user for an image, runs that through Monodepth
    # using the (hard-coded) model.
    img_global_filename = filedialog.askopenfilename()
    monodepth_model = 'mono+stereo_1024x320'
    depth_map = monodepth(img_global_filename, (640, 427), monodepth_model)

    # Monodepth outputs a depth map with the file name
    # '<original-image-name>_disp.jpg' in the directory of the original image.
    # We want to find that path so we can find the depth map.
    output_directory = os.path.dirname(img_global_filename)
    img_local_filename = os.path.splitext(os.path.basename(img_global_filename))[0]
    depth_map_global_filename = os.path.join(output_directory, "{}_disp.jpeg".format(img_local_filename))
    monodepth_img = Image.open(depth_map_global_filename).resize((640, 427)).convert('RGB')

    kernel_vals = calculate_kernel_values_from_colormap(depth_map, sightval)
    orig_img = Image.open(img_global_filename).resize((640, 427)).convert('RGB')
    blurred_img = convolution(orig_img, kernel_vals, sightval)  # outputting the blurred image

    blit_img(surface, blurred_img)
    return img_global_filename, orig_img, monodepth_img, blurred_img  # Return the PIL image


def opia_btn_handler(surface, val, filename):

    img_global_filename = filename
    monodepth_model = 'mono+stereo_1024x320'
    depth_map = monodepth(img_global_filename, (640, 427), monodepth_model)

    # Monodepth outputs a depth map with the file name
    # '<original-image-name>_disp.jpg' in the directory of the original image.
    # We want to find that path so we can find the depth map.
    output_directory = os.path.dirname(img_global_filename)
    img_local_filename = os.path.splitext(os.path.basename(img_global_filename))[0]
    depth_map_global_filename = os.path.join(output_directory, "{}_disp.jpeg".format(img_local_filename))
    monodepth_img = Image.open(depth_map_global_filename).resize((640, 427)).convert('RGB')

    kernel_vals = calculate_kernel_values_from_colormap(depth_map, val)
    orig_img = Image.open(img_global_filename).resize((640, 427)).convert('RGB')
    blurred_img = convolution(orig_img, kernel_vals, val)  # outputting the blurred image

    blit_img(surface, blurred_img)

    return orig_img, monodepth_img, blurred_img  # Return the PIL image


def rg_btn_handler(surface, img):
    """
    :param surface:
    :param img:
    :return:
    """
    if img is None:
        return

    rg_colorblind_img = colorblind.rg(img)
    blit_img(surface, rg_colorblind_img)

    return rg_colorblind_img


def by_btn_handler(surface, img):
    """
    :param surface:
    :param img:
    :return:
    """
    if img is None:
        return

    by_colorblind_img = colorblind.by(img)
    blit_img(surface, by_colorblind_img)

    return by_colorblind_img


def total_btn_handler(surface, img):
    """
    :param surface:
    :param img:
    :return:
    """
    if img is None:
        return

    by_colorblind_img = colorblind.total(img)
    blit_img(surface, by_colorblind_img)

    return by_colorblind_img


def run():
    pygame.init()  # Initialize PyGame.
    main_surf = pygame.display.set_mode((1240, 690))
    main_surf.fill((53, 105, 69))  # Gray moss green background
    draw_extra_main_surface(main_surf)  # Draw other UI things.

    myopiaVal = "-5.0"      #-6 to -3
    hyperopiaVal = "3.0"    # 2 to 5

    # Set dimension for screen, where image is displayed.
    # Image resolutions should be 3:2 (640 x 427).
    screen = main_surf.subsurface(Rect(200, 100, 840, 497))
    screen.fill((197, 222, 204))  # Lime-ish green.
    draw_extra_screen(screen)  # Draw other UI things on subsurface.

    # Bottom of Screen
    upload_btn = Button(555, 625, 120, 35, (191, 117, 105), (87, 13, 13), 'UPLOAD')   # Initialize the upload button.

    # Left of Screen
    rg_btn = Button(26, 207, 150, 50, (255, 255, 255), (0, 60, 0), 'R/G Colorblindness')       # R/G colorblind
    by_btn = Button(26, 277, 150, 50, (255, 255, 255), (0, 60, 0), 'B/Y Colorblindness')       # B/Y colorblind
    total_btn = Button(26, 347, 150, 50, (255, 255, 255), (0, 60, 0), 'Total Colorblindness')  # Total colorblind
    pygame.draw.rect(main_surf, (34, 69, 45), (16, 418, 170, 2), 0)
    halos_btn = Button(26, 442, 150, 50, (255, 255, 255), (0, 60, 0), 'Halos')
    starbursts_btn = Button(26, 512, 150, 50, (255, 255, 255), (0, 60, 0), 'Starbursts')

    # Right of Screen
    depth_map_btn = Button(1064, 137, 150, 50, (255, 255, 255), (0, 60, 0), 'Depth Map')
    blurred_btn = Button(1064, 207, 150, 50, (255, 255, 255), (0, 60, 0), 'Blurred')
    pygame.draw.rect(main_surf, (34, 69, 45), (1054, 278, 170, 2), 0)                       # Button Divider
    myopia_btn = Button(1064, 302, 150, 50, (255, 255, 255), (0, 60, 0), 'Myopia')          # Myopia button
    hyperopia_btn = Button(1064, 397, 150, 50, (255, 255, 255), (0, 60, 0), 'Hyperopia')    # Hyperopia button
    pygame.draw.rect(main_surf, (34, 69, 45), (1054, 490, 170, 2), 0)                       # Button Divider
    glasses_btn = Button(1064, 512, 150, 50, (255, 255, 255), (0, 60, 0), 'Glasses On')     # Glasses button.

    downMyopia_btn = Button(1085, 360, 15, 15, (255, 255, 255), (0, 60, 0), '')
    upMyopia_btn = Button(1105, 360, 15, 15, (255, 255, 255), (0, 60, 0), '')
    myopiaVal_btn = Button(1127, 360, 40, 15, (197, 222, 204), (197, 222, 204), myopiaVal)
    selectMyopia_btn = Button(1174, 360, 15, 15, (255, 255, 255), (0, 60, 0), '')
    draw_selectMyopia_btn = False

    downHyperopia_btn = Button(1085, 456, 15, 15, (255, 255, 255), (0, 60, 0), '')
    upHyperopia_btn = Button(1105, 456, 15, 15, (255, 255, 255), (0, 60, 0), '')
    hyperopiaVal_btn = Button(1127, 456, 40, 15, (197, 222, 204), (197, 222, 204), hyperopiaVal)
    selectHyperopia_btn = Button(1174, 456, 15, 15, (255, 255, 255), (0, 60, 0), '')
    draw_selectHyperopia_btn = False

    curr_disp_img = None  # The currently displayed image, initially none.
    img_global_filename = None

    # After we run a process (say, monodepth or colorblinding), we want to save
    # the resulting image so that we don't have to go through that process again
    # if we want to switch settings. Initially, they are all none.
    orig_img = None
    monodepth_img = None
    blurred_img = None
    rg_colorblind_blurred_img = None
    rg_colorblind_orig_img = None
    by_colorblind_blurred_img = None
    by_colorblind_orig_img = None
    total_colorblind_blurred_img = None
    total_colorblind_orig_img = None

    glasses = Glasses()  # Init glasses.
    brightest_points = None  # For static starbursts and halos.

    # Main loop.
    is_running = True
    while is_running:
        check_img = pygame.image.load('images/check.png')
        if draw_selectMyopia_btn:
            selectMyopia_btn.draw(12, main_surf)
            main_surf.blit(check_img, (1175, 362))
        elif draw_selectHyperopia_btn:
            selectHyperopia_btn.draw(12, main_surf)
            main_surf.blit(check_img, (1175, 458))
        else:
            main_surf.fill((53, 105, 69))  # Gray moss green background
            draw_extra_main_surface(main_surf)  # Draw other UI things.

        if curr_disp_img is None:
            screen = main_surf.subsurface(Rect(200, 100, 840, 497))
            screen.fill((197, 222, 204))  # Lime-ish green.
            draw_extra_screen(screen)  # Draw other UI things on subsurface.

        upload_btn.draw(20, main_surf)     # Draw the upload button.
        rg_btn.draw(12, main_surf)         # Draw the red-green colorblind button.
        by_btn.draw(12, main_surf)         # Draw the blue-yellow colorblind button.
        total_btn.draw(12, main_surf)      # Draw the total colorblind button.
        glasses_btn.draw(12, main_surf)    # Draw the total colorblind button.
        myopia_btn.draw(12, main_surf)     # Draw the red-green colorblind button.
        hyperopia_btn.draw(12, main_surf)  # Draw the red-green colorblind button.
        depth_map_btn.draw(12, main_surf)  # Draw depth map button.
        blurred_btn.draw(12, main_surf)    # Draw blurred button.

        pygame.draw.rect(main_surf, (34, 69, 45), (1054, 278, 170, 2), 0)  # Button Divider
        pygame.draw.rect(main_surf, (34, 69, 45), (16, 418, 170, 2), 0)
        pygame.draw.rect(main_surf, (34, 69, 45), (1054, 490, 170, 2), 0)

        # Adjust myopia settings
        upMyopia_btn.draw(12, main_surf)
        downMyopia_btn.draw(12, main_surf)
        downArrow1_img = pygame.image.load("images/downArrow.png")
        main_surf.blit(downArrow1_img, (1087, 362))
        upArrow1_img = pygame.image.load("images/upArrow.png")
        main_surf.blit(upArrow1_img, (1107, 361))
        myopiaVal_btn.draw(12, main_surf)

        # Adjust hyperopia settings
        upHyperopia_btn.draw(12, main_surf)
        downHyperopia_btn.draw(12, main_surf)
        downArrow2_img = pygame.image.load("images/downArrow.png")
        main_surf.blit(downArrow2_img, (1087, 458))
        upArrow2_img = pygame.image.load("images/upArrow.png")
        main_surf.blit(upArrow2_img, (1107, 457))
        hyperopiaVal_btn.draw(12, main_surf)
        blurred_btn.draw(12, main_surf)
        halos_btn.draw(12, main_surf)
        starbursts_btn.draw(12, main_surf)

        blit_img(screen, curr_disp_img)

        if glasses_btn.is_selected:
            glasses.draw_glasses_static(screen)

        if starbursts_btn.is_selected:
            brightest_points = ld.starburst_static(screen, orig_img, brightest_points)

        if halos_btn.is_selected:
            brightest_points = ld.halo_static(screen, orig_img, brightest_points)

        pygame.display.update()

        # Event handling.
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()  # The mouse's position.

            # Quit.
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                quit()

            # ------------------------------------------------------------------------------- LEFT CLICK BUTTON HANDLERS
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # ---------------------------------------------------------------------------------------- UPLOAD BUTTON
                if upload_btn.is_hovered(mouse_pos):
                    # Get the original, monodepth, and blurred image.
                    blurred_btn.is_selected = True
                    myopia_btn.is_selected = True
                    img_global_filename, orig_img, monodepth_img, blurred_img = upload_btn_handler(screen, -5)
                    curr_disp_img = blurred_img  # The blurred image is shown on screen.

                # --------------------------------------------------------------------------- RED / GREEN COLORBLINDNESS
                elif rg_btn.is_hovered(mouse_pos):
                    rg_btn.is_selected = not rg_btn.is_selected
                    by_btn.is_selected = False
                    total_btn.is_selected = False
                    depth_map_btn.is_selected = False
                    halos_btn.is_selected = False
                    starbursts_btn.is_selected = False

                    if rg_btn.is_selected:
                        if blurred_btn.is_selected:
                            # R/G colorblind and blurred image will be displayed.
                            if rg_colorblind_blurred_img is None:
                                rg_colorblind_blurred_img = rg_btn_handler(screen, blurred_img)
                            else:
                                blit_img(screen, rg_colorblind_blurred_img)

                            curr_disp_img = rg_colorblind_blurred_img
                        else:
                            # R/G colorblind and clear image will be displayed.
                            if rg_colorblind_orig_img is None:
                                rg_colorblind_orig_img = rg_btn_handler(screen, orig_img)
                            else:
                                blit_img(screen, rg_colorblind_orig_img)

                            curr_disp_img = rg_colorblind_orig_img
                    else:
                        if blurred_btn.is_selected:
                            # Blurred image will be displayed.
                            blit_img(screen, blurred_img)
                            curr_disp_img = blurred_img
                        else:
                            # Original image will be displayed.
                            blit_img(screen, orig_img)
                            curr_disp_img = orig_img

                # ------------------------------------------------------------------------- BLUE / YELLOW COLORBLINDNESS
                elif by_btn.is_hovered(mouse_pos):
                    by_btn.is_selected = not by_btn.is_selected
                    rg_btn.is_selected = False
                    total_btn.is_selected = False
                    depth_map_btn.is_selected = False
                    halos_btn.is_selected = False
                    starbursts_btn.is_selected = False

                    if by_btn.is_selected:
                        if blurred_btn.is_selected:
                            # B/Y colorblind and blurred image will be displayed.
                            if by_colorblind_blurred_img is None:
                                by_colorblind_blurred_img = by_btn_handler(screen, blurred_img)
                            else:
                                blit_img(screen, by_colorblind_blurred_img)

                            curr_disp_img = by_colorblind_blurred_img
                        else:
                            # B/Y colorblind and clear image will be displayed.
                            if by_colorblind_orig_img is None:
                                by_colorblind_orig_img = by_btn_handler(screen, orig_img)
                            else:
                                blit_img(screen, by_colorblind_orig_img)

                            curr_disp_img = by_colorblind_orig_img
                    else:
                        if blurred_btn.is_selected:
                            # Blurred image will be displayed.
                            blit_img(screen, blurred_img)
                            curr_disp_img = blurred_img
                        else:
                            # Original image will be displayed.
                            blit_img(screen, orig_img)
                            curr_disp_img = orig_img

                # --------------------------------------------------------------------------------- TOTAL COLORBLINDNESS
                elif total_btn.is_hovered(mouse_pos):
                    total_btn.is_selected = not total_btn.is_selected
                    rg_btn.is_selected = False
                    by_btn.is_selected = False
                    depth_map_btn.is_selected = False
                    halos_btn.is_selected = False
                    starbursts_btn.is_selected = False

                    if total_btn.is_selected:
                        if blurred_btn.is_selected:
                            # Total colorblind and blurred image will be displayed.
                            if total_colorblind_blurred_img is None:
                                total_colorblind_blurred_img = total_btn_handler(screen, blurred_img)
                            else:
                                blit_img(screen, total_colorblind_blurred_img)

                            curr_disp_img = total_colorblind_blurred_img
                        else:
                            # Total colorblind and clear image will be displayed.
                            if total_colorblind_orig_img is None:
                                total_colorblind_orig_img = total_btn_handler(screen, orig_img)
                            else:
                                blit_img(screen, total_colorblind_orig_img)

                            curr_disp_img = total_colorblind_orig_img
                    else:
                        if blurred_btn.is_selected:
                            # Blurred image will be displayed.
                            blit_img(screen, blurred_img)
                            curr_disp_img = blurred_img
                        else:
                            # Original image will be displayed.
                            blit_img(screen, orig_img)
                            curr_disp_img = orig_img

                # ------------------------------------------------------------------------------------------------ HALOS
                elif halos_btn.is_hovered(mouse_pos):
                    halos_btn.is_selected = not halos_btn.is_selected
                    starbursts_btn.is_selected = False

                    if halos_btn.is_selected and brightest_points is None:
                        blit_img(screen, curr_disp_img)
                        brightest_points = ld.halo(screen, orig_img)
                    else:
                        blit_img(screen, curr_disp_img)
                        brightest_points = None

                # ------------------------------------------------------------------------------------------- STARBURSTS
                elif starbursts_btn.is_hovered(mouse_pos):
                    starbursts_btn.is_selected = not starbursts_btn.is_selected
                    halos_btn.is_selected = False

                    if starbursts_btn.is_selected and brightest_points is None:
                        blit_img(screen, curr_disp_img)
                        brightest_points = ld.starburst(screen, orig_img)
                    else:
                        blit_img(screen, curr_disp_img)
                        brightest_points = None

                # -------------------------------------------------------------------------------------------- DEPTH MAP
                elif depth_map_btn.is_hovered(mouse_pos):
                    depth_map_btn.is_selected = not depth_map_btn.is_selected
                    rg_btn.is_selected = False
                    by_btn.is_selected = False
                    total_btn.is_selected = False
                    myopia_btn.is_selected = False
                    hyperopia_btn.is_selected = False
                    glasses_btn.is_selected = False
                    blurred_btn.is_selected = False
                    halos_btn.is_selected = False
                    starbursts_btn.is_selected = False

                    if depth_map_btn.is_selected:
                        # Monodepth image will be displayed.
                        blit_img(screen, monodepth_img)
                        curr_disp_img = monodepth_img
                    else:
                        # Blurred image will be displayed.
                        blit_img(screen, orig_img)
                        curr_disp_img = orig_img

                # ---------------------------------------------------------------------------------------------- BLURRED
                elif blurred_btn.is_hovered(mouse_pos):
                    blurred_btn.is_selected = not blurred_btn.is_selected
                    depth_map_btn.is_selected = False
                    hyperopia_btn.is_selected = False
                    glasses_btn.is_selected = False
                    depth_map_btn.is_selected = False

                    if blurred_btn.is_selected:
                        myopia_btn.is_selected = True
                        if rg_btn.is_selected:
                            # R/G colorblind and blurred image will be shown.
                            if rg_colorblind_blurred_img is None:
                                rg_colorblind_blurred_img = rg_btn_handler(screen, blurred_img)
                            else:
                                blit_img(screen, rg_colorblind_blurred_img)

                            curr_disp_img = rg_colorblind_blurred_img

                        elif by_btn.is_selected:
                            # B/Y colorblind and blurred image will be shown.
                            if by_colorblind_blurred_img is None:
                                by_colorblind_blurred_img = by_btn_handler(screen, blurred_img)
                            else:
                                blit_img(screen, by_colorblind_blurred_img)

                            curr_disp_img = by_colorblind_blurred_img

                        elif total_btn.is_selected:
                            # Total colorblind and blurred image will be shown.
                            if total_colorblind_blurred_img is None:
                                total_colorblind_blurred_img = total_btn_handler(screen, blurred_img)
                            else:
                                blit_img(screen, total_colorblind_blurred_img)

                            curr_disp_img = total_colorblind_blurred_img

                        else:
                            # Blurred image will be shown.
                            blit_img(screen, blurred_img)
                            curr_disp_img = blurred_img
                    else:
                        myopia_btn.is_selected = False
                        if rg_btn.is_selected:
                            # R/G colorblind and clear image will be shown.
                            if rg_colorblind_orig_img is None:
                                rg_colorblind_orig_img = rg_btn_handler(screen, orig_img)
                            else:
                                blit_img(screen, rg_colorblind_orig_img)

                            curr_disp_img = rg_colorblind_orig_img

                        elif by_btn.is_selected:
                            # B/Y colorblind and clear image will be shown.
                            if by_colorblind_orig_img is None:
                                by_colorblind_orig_img = by_btn_handler(screen, orig_img)
                            else:
                                blit_img(screen, by_colorblind_orig_img)

                            curr_disp_img = by_colorblind_orig_img

                        elif total_btn.is_selected:
                            # Total colorblind and clear image will be shown.
                            if total_colorblind_orig_img is None:
                                total_colorblind_orig_img = total_btn_handler(screen, orig_img)
                            else:
                                blit_img(screen, total_colorblind_orig_img)

                            curr_disp_img = total_colorblind_orig_img

                        else:
                            # Clear image will be shown.
                            blit_img(screen, orig_img)
                            curr_disp_img = orig_img

                # ----------------------------------------------------------------------------------------------- MYOPIA
                elif myopia_btn.is_hovered(mouse_pos):
                    myopia_btn.is_selected = not myopia_btn.is_selected
                    blurred_btn.is_selected = True
                    depth_map_btn.is_selected = False

                    # Disable hyperopia colorblindness
                    hyperopia_btn.is_selected = False

                    if img_global_filename is not None:
                        orig_img, monodepth_img, blurred_img = opia_btn_handler(screen, myopiaVal, img_global_filename)
                        curr_disp_img = blurred_img
                
                elif upMyopia_btn.is_hovered(mouse_pos):
                    temp = float(myopiaVal)
                    if (temp < -3):
                        temp += 1
                        myopiaVal = str(temp)
                        myopiaVal_btn = Button(1127, 360, 40, 15, (197, 222, 204), (197, 222, 204), myopiaVal)
                        draw_selectMyopia_btn = True
                        draw_selectHyperopia_btn = False

                elif downMyopia_btn.is_hovered(mouse_pos):
                    temp = float(myopiaVal)
                    if (temp > -6):
                        temp -= 1
                        myopiaVal = str(temp)
                        myopiaVal_btn = Button(1127, 360, 40, 15, (197, 222, 204), (197, 222, 204), myopiaVal)
                        draw_selectMyopia_btn = True
                        draw_selectHyperopia_btn = False

                elif selectMyopia_btn.is_hovered(mouse_pos):
                    draw_selectMyopia_btn = False
                    myopia_btn.is_selected = True
                    hyperopia_btn.is_selected = False

                    if img_global_filename is not None:
                        orig_img, monodepth_img, blurred_img = opia_btn_handler(screen, myopiaVal, img_global_filename)
                        curr_disp_img = blurred_img

                # -------------------------------------------------------------------------------------------- HYPEROPIA
                elif hyperopia_btn.is_hovered(mouse_pos):
                    hyperopia_btn.is_selected = not hyperopia_btn.is_selected
                    blurred_btn.is_selected = True
                    depth_map_btn.is_selected = False

                    # Disable myopia colorblindness
                    myopia_btn.is_selected = False

                    if img_global_filename is not None:
                        orig_img, monodepth_img, blurred_img = opia_btn_handler(screen, hyperopiaVal, img_global_filename)
                        curr_disp_img = blurred_img

                elif upHyperopia_btn.is_hovered(mouse_pos):
                    temp = float(hyperopiaVal)
                    if (temp < 5):
                        temp += 1
                        hyperopiaVal = str(temp)
                        hyperopiaVal_btn = Button(1127, 456, 40, 15, (197, 222, 204), (197, 222, 204), hyperopiaVal)
                        draw_selectMyopia_btn = False
                        draw_selectHyperopia_btn = True

                elif downHyperopia_btn.is_hovered(mouse_pos):
                    temp = float(hyperopiaVal)
                    if (temp > 2):
                        temp -= 1
                        hyperopiaVal = str(temp)
                        hyperopiaVal_btn = Button(1127, 456, 40, 15, (197, 222, 204), (197, 222, 204), hyperopiaVal)
                        draw_selectMyopia_btn = False
                        draw_selectHyperopia_btn = True

                elif selectHyperopia_btn.is_hovered(mouse_pos):
                    draw_selectHyperopia_btn = False
                    hyperopia_btn.is_selected = True
                    myopia_btn.is_selected = False

                    if img_global_filename is not None:
                        orig_img, monodepth_img, blurred_img = opia_btn_handler(screen, hyperopiaVal, img_global_filename)
                        curr_disp_img = blurred_img

                # ---------------------------------------------------------------------------------------------- GLASSES
                elif glasses_btn.is_hovered(mouse_pos):
                    glasses_btn.is_selected = not glasses_btn.is_selected
                    depth_map_btn.is_selected = False

                    if glasses_btn.is_selected:
                        if rg_btn.is_selected:
                            if rg_colorblind_orig_img is None:
                                rg_colorblind_orig_img = rg_btn_handler(screen, orig_img)

                            if rg_colorblind_blurred_img is None:
                                rg_colorblind_blurred_img = rg_btn_handler(screen, blurred_img)

                            glasses.start_up_animation(screen, rg_colorblind_orig_img, rg_colorblind_blurred_img)

                        elif by_btn.is_selected:
                            if by_colorblind_orig_img is None:
                                by_colorblind_orig_img = by_btn_handler(screen, orig_img)

                            if by_colorblind_blurred_img is None:
                                by_colorblind_blurred_img = by_btn_handler(screen, blurred_img)

                            glasses.start_up_animation(screen, by_colorblind_orig_img, by_colorblind_blurred_img)

                        elif total_btn.is_selected:
                            if total_colorblind_orig_img is None:
                                total_colorblind_orig_img = total_btn_handler(screen, orig_img)

                            if total_colorblind_blurred_img is None:
                                total_colorblind_blurred_img = total_btn_handler(screen, blurred_img)

                            glasses.start_up_animation(screen, total_colorblind_orig_img, total_colorblind_blurred_img)

                        else:
                            glasses.start_up_animation(screen, orig_img, blurred_img)
                    else:
                        if rg_btn.is_selected:
                            if rg_colorblind_orig_img is None:
                                rg_colorblind_orig_img = rg_btn_handler(screen, orig_img)

                            if rg_colorblind_blurred_img is None:
                                rg_colorblind_blurred_img = rg_btn_handler(screen, blurred_img)

                            glasses.start_down_animation(screen, rg_colorblind_orig_img, rg_colorblind_blurred_img)

                        elif by_btn.is_selected:
                            if by_colorblind_orig_img is None:
                                by_colorblind_orig_img = by_btn_handler(screen, orig_img)

                            if by_colorblind_blurred_img is None:
                                by_colorblind_blurred_img = by_btn_handler(screen, blurred_img)

                            glasses.start_down_animation(screen, by_colorblind_orig_img, by_colorblind_blurred_img)

                        elif total_btn.is_selected:
                            if total_colorblind_orig_img is None:
                                total_colorblind_orig_img = total_btn_handler(screen, orig_img)

                            if total_colorblind_blurred_img is None:
                                total_colorblind_blurred_img = total_btn_handler(screen, blurred_img)

                            glasses.start_down_animation(screen, total_colorblind_orig_img, total_colorblind_blurred_img)

                        else:
                            glasses.start_down_animation(screen, orig_img, blurred_img)

            # ---------------------------------------------------------------------------------------- ON HOVER HANDLERS
            if upload_btn.is_hovered(mouse_pos):
                upload_btn.color = (138, 84, 74)
            else:
                upload_btn.color = (158, 96, 85)

            if not rg_btn.is_selected:
                if rg_btn.is_hovered(mouse_pos):
                    rg_btn.color = (220, 220, 220)
                else:
                    rg_btn.color = (255, 255, 255)

            if not by_btn.is_selected:
                if by_btn.is_hovered(mouse_pos):
                    by_btn.color = (220, 220, 220)
                else:
                    by_btn.color = (255, 255, 255)

            if not total_btn.is_selected:
                if total_btn.is_hovered(mouse_pos):
                    total_btn.color = (220, 220, 220)
                else:
                    total_btn.color = (255, 255, 255)

            if not halos_btn.is_selected:
                if halos_btn.is_hovered(mouse_pos):
                    halos_btn.color = (220, 220, 220)
                else:
                    halos_btn.color = (255, 255, 255)

            if not starbursts_btn.is_selected:
                if starbursts_btn.is_hovered(mouse_pos):
                    starbursts_btn.color = (220, 220, 220)
                else:
                    starbursts_btn.color = (255, 255, 255)

            if not myopia_btn.is_selected:
                if myopia_btn.is_hovered(mouse_pos):
                    myopia_btn.color = (220, 220, 220)
                else:
                    myopia_btn.color = (255, 255, 255)
            
            if not hyperopia_btn.is_selected:
                if hyperopia_btn.is_hovered(mouse_pos):
                    hyperopia_btn.color = (220, 220, 220)
                else:
                    hyperopia_btn.color = (255, 255, 255)

            if not glasses_btn.is_selected:
                if glasses_btn.is_hovered(mouse_pos):
                    glasses_btn.color = (220, 220, 220)
                else:
                    glasses_btn.color = (255, 255, 255)

            if not blurred_btn.is_selected:
                if blurred_btn.is_hovered(mouse_pos):
                    blurred_btn.color = (220, 220, 220)
                else:
                    blurred_btn.color = (255, 255, 255)

            if not depth_map_btn.is_selected:
                if depth_map_btn.is_hovered(mouse_pos):
                    depth_map_btn.color = (220, 220, 220)
                else:
                    depth_map_btn.color = (255, 255, 255)

            if not upMyopia_btn.is_selected:
                if upMyopia_btn.is_hovered(mouse_pos):
                    upMyopia_btn.color = (220, 220, 220)
                else:
                    upMyopia_btn.color = (255, 255, 255)

            if not upMyopia_btn.is_selected:
                if upMyopia_btn.is_hovered(mouse_pos):
                    upMyopia_btn.color = (220, 220, 220)
                else:
                    upMyopia_btn.color = (255, 255, 255)

            if not downMyopia_btn.is_selected:
                if downMyopia_btn.is_hovered(mouse_pos):
                    downMyopia_btn.color = (220, 220, 220)
                else:
                    downMyopia_btn.color = (255, 255, 255)

            if not upHyperopia_btn.is_selected:
                if upHyperopia_btn.is_hovered(mouse_pos):
                    upHyperopia_btn.color = (220, 220, 220)
                else:
                    upHyperopia_btn.color = (255, 255, 255)

            if not downHyperopia_btn.is_selected:
                if downHyperopia_btn.is_hovered(mouse_pos):
                    downHyperopia_btn.color = (220, 220, 220)
                else:
                    downHyperopia_btn.color = (255, 255, 255)

            if selectHyperopia_btn.is_hovered(mouse_pos):
                selectHyperopia_btn.color = (220, 220, 220)
            else:
                selectHyperopia_btn.color = (255, 255, 255)

            if selectMyopia_btn.is_hovered(mouse_pos):
                selectMyopia_btn.color = (220, 220, 220)
            else:
                selectMyopia_btn.color = (255, 255, 255)


class Button:
    def __init__(self, x, y, width, height, color, border_color, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.orig_color = color # Original color at initialization.
        self.color = color      # The current color.
        self.border_color = border_color
        self.text = text  # Default no text.
        self.is_selected = False  # Is button selected?

    def draw(self, font_size, window):
        """ Draws the button onto the window.
        :param window: The surface we want to draw the button on.
        """
        # Border for button
        pygame.draw.rect(window, self.border_color, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

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

        # If the button is currently selected, it's green.
        # Else, it's white.
        if self.is_selected:
            self.color = (67, 168, 94)

    def is_hovered(self, mouse_pos):
        """ Is the mouse hovering over the button?
        :param mouse_pos: The position of the mouse.
        :return: True if the mouse is hovering over the button, else false.
        """
        if self.x < mouse_pos[0] < self.x + self.width:
            if self.y < mouse_pos[1] < self.y + self.height:
                self.color = (220, 220, 220)
                return True

        return False