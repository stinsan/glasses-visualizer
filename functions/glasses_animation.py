from PIL import Image, ImageDraw
import pygame


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


class Glasses:
    def __init__(self):
        self.GLASSES_RECTS = [(50, 140, 300, 220), (500, 140, 300, 220)]
        self.GLASSES_BRIDGE = (350, 180, 150, 20)
        self.MASK_RECTS = [(50, 135, 260, 300), (390, 135, 600, 300)]

        self.clear_image = None
        self.blurred_image = None

    def round_rect(self, surface, rect, color, rad=20, border=0, inside=(0,0,0,0)):
        """ Draw a rect with rounded corners to surface.  Argument rad can be specified
        to adjust curvature of edges (given in pixels).  An optional border
        width can also be supplied; if not provided the rect will be filled.
        Both the color and optional interior color (the inside argument) support
        alpha.
        """
        rect = pygame.Rect(rect)
        zeroed_rect = rect.copy()
        zeroed_rect.topleft = 0,0
        image = pygame.Surface(rect.size).convert_alpha()
        image.fill((0,0,0,0))
        self.render_region(image, zeroed_rect, color, rad)
        if border:
            zeroed_rect.inflate_ip(-2*border, -2*border)
            self.render_region(image, zeroed_rect, inside, rad)
        surface.blit(image, rect)

    def render_region(self, image, rect, color, rad):
        """Helper function for round_rect."""
        corners = rect.inflate(-2*rad, -2*rad)
        for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
            pygame.draw.circle(image, color, getattr(corners,attribute), rad)
        image.fill(color, rect.inflate(-2*rad,0))
        image.fill(color, rect.inflate(0,-2*rad))

    def draw_glasses(self, surface, rects, bridge):
        pygame.draw.rect(surface, (50, 50, 50), bridge, 0)
        for rect in rects:
            self.round_rect(surface, rect, (50, 50, 50), rad=30, border=15)

    def draw_composite(self, surface, rects, clear_image, blurred_image):
        clear_image.resize(surface.get_size())
        blurred_image.resize(surface.get_size())

        mask = Image.new("L", clear_image.size, 0)
        draw = ImageDraw.Draw(mask)

        for rect in rects:
            draw.rectangle(rect, fill=255)

        composite = Image.composite(clear_image, blurred_image, mask)

        return composite

    def clear_glasses(self, surface, image):
        if image is None:
            surface.fill((197, 222, 204))  # Lime-ish green.
            draw_extra_screen(surface)  # Draw extra UI elements.
        else:
            blit_img(surface, image)

    def start_up_animation(self, surface, clear_image, blurred_image):
        if clear_image is None or blurred_image is None:
            return

        self.clear_image = clear_image
        self.blurred_image = blurred_image

        for i in range(61):

            dy_glasses = 360 * self.ease_in_out_back(1 - (i / 60))
            dy_mask = 300 * self.ease_in_out_back(1 - (i / 60))

            glasses_rects = [(x, y + dy_glasses, w, l) for x, y, w, l in self.GLASSES_RECTS]
            mask_rects = [(x1, y1 + dy_mask, x2, y2 + dy_mask) for x1, y1, x2, y2 in self.MASK_RECTS]
            bridge = (self.GLASSES_BRIDGE[0], self.GLASSES_BRIDGE[1] + dy_glasses, self.GLASSES_BRIDGE[2], self.GLASSES_BRIDGE[3])

            composite_img = self.draw_composite(surface, mask_rects, clear_image, blurred_image)
            # Transform PIL image to PyGame Surface.
            blit_img(surface, composite_img)

            self.clear_glasses(surface, composite_img)

            self.draw_glasses(surface, glasses_rects, bridge)

            pygame.display.update()

    def start_down_animation(self, surface, clear_image, blurred_image):
        if clear_image is None or blurred_image is None:
            return

        self.clear_image = clear_image
        self.blurred_image = blurred_image

        for i in range(61):
            dy_glasses = 360 * self.ease_in_out_back(i / 60)
            dy_mask = 300 * self.ease_in_out_back(i / 60)

            glasses_rects = [(x, y + dy_glasses, w, l) for x, y, w, l in self.GLASSES_RECTS]
            mask_rects = [(x1, y1 + dy_mask, x2, y2 + dy_mask) for x1, y1, x2, y2 in self.MASK_RECTS]
            bridge = (self.GLASSES_BRIDGE[0], self.GLASSES_BRIDGE[1] + dy_glasses, self.GLASSES_BRIDGE[2], self.GLASSES_BRIDGE[3])

            composite_img = self.draw_composite(surface, mask_rects, clear_image, blurred_image)
            # Transform PIL image to PyGame Surface.
            blit_img(surface, composite_img)

            self.clear_glasses(surface, composite_img)

            self.draw_glasses(surface, glasses_rects, bridge)

            pygame.display.update()

    def ease_in_out_back(self, x):
        """ From https://easings.net/#easeInOutBack.
        :param x:
        :return:
        """
        c1 = 1.70158
        c2 = c1 * 1.525

        if x < 0.5:
            return (pow(2 * x, 2) * ((c2 + 1) * 2 * x - c2)) / 2
        else:
            return (pow(2 * x - 2, 2) * ((c2 + 1) * (x * 2 - 2) + c2) + 2) / 2

    def draw_glasses_static(self, surface):
        if self.clear_image is None or self.blurred_image is None:
            return

        glasses_rects = [(x, y, w, l) for x, y, w, l in self.GLASSES_RECTS]
        mask_rects = [(x1, y1, x2, y2) for x1, y1, x2, y2 in self.MASK_RECTS]
        bridge = (self.GLASSES_BRIDGE[0], self.GLASSES_BRIDGE[1], self.GLASSES_BRIDGE[2], self.GLASSES_BRIDGE[3])

        composite_img = self.draw_composite(surface, mask_rects, self.clear_image, self.blurred_image)

        blit_img(surface, composite_img)

        self.clear_glasses(surface, composite_img)

        self.draw_glasses(surface, glasses_rects, bridge)
