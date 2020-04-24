import pygame
from pygame import gfxdraw

from ui import draw_extra_screen, blit_img
from PIL import Image, ImageDraw


GLASSES_RECTS = [(50, 140, 300, 220), (500, 140, 300, 220)]
GLASSES_BRIDGE = (350, 180, 150, 20)
MASK_RECTS = [(50, 135, 260, 300), (390, 135, 600, 300)]


def round_rect(surface, rect, color, rad=20, border=0, inside=(0,0,0,0)):
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
    render_region(image, zeroed_rect, color, rad)
    if border:
        zeroed_rect.inflate_ip(-2*border, -2*border)
        render_region(image, zeroed_rect, inside, rad)
    surface.blit(image, rect)


def render_region(image, rect, color, rad):
    """Helper function for round_rect."""
    corners = rect.inflate(-2*rad, -2*rad)
    for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
        pygame.draw.circle(image, color, getattr(corners,attribute), rad)
    image.fill(color, rect.inflate(-2*rad,0))
    image.fill(color, rect.inflate(0,-2*rad))


def draw_glasses(surface, rects, bridge):
    pygame.draw.rect(surface, (50, 50, 50), bridge, 0)
    for rect in rects:
        round_rect(surface, rect, (50, 50, 50), rad=30, border=15)


def clear_glasses(surface, image):
    if image is None:
        surface.fill((197, 222, 204))  # Lime-ish green.
        draw_extra_screen(surface)     # Draw extra UI elements.
    else:
        blit_img(surface, image)


def draw_composite(surface, rects, clear_image, blurred_image):
    clear_image.resize(surface.get_size())
    blurred_image.resize(surface.get_size())

    mask = Image.new("L", clear_image.size, 0)
    draw = ImageDraw.Draw(mask)

    for rect in rects:
        draw.rectangle(rect, fill=255)

    composite = Image.composite(clear_image, blurred_image, mask)

    return composite


def start_animation(surface, clear_image, blurred_image):

    if clear_image is None or blurred_image is None:
        return

    dy_glasses = 360
    dy_mask = 300
    for _ in range(60):
        glasses_rects = [(x, y + dy_glasses, w, l) for x, y, w, l in GLASSES_RECTS]
        mask_rects = [(x1, y1 + dy_mask, x2, y2 + dy_mask) for x1, y1, x2, y2 in MASK_RECTS]
        bridge = (GLASSES_BRIDGE[0], GLASSES_BRIDGE[1] + dy_glasses, GLASSES_BRIDGE[2], GLASSES_BRIDGE[3])


        composite_img = draw_composite(surface, mask_rects, clear_image, blurred_image)
        # Transform PIL image to PyGame Surface.
        blit_img(surface, composite_img)

        clear_glasses(surface, composite_img)

        draw_glasses(surface, glasses_rects, bridge)
        dy_glasses -= 6
        dy_mask -= 5

        pygame.display.update()
