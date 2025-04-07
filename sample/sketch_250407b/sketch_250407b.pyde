# imports
import math

# physical hardware props
led_panel_height = 64
led_panel_width = 64
led_panel_count = 5

# image
img_name = "tylo-px.jpg"
img_container_size = 64
img_dp_size = 4

# pixellation parameters
pixel_pitch = 1.2
pixellation_size = 1 # whole numbers, img_container_size must match


def fill_dimension(w, h, box_size):
    scale = float(box_size) / min(w, h)
    return math.trunc(w * scale), math.trunc(h * scale)


def get_center(w, h, box_size):
    box_center = box_size // 2
    start_x = max(w // 2 - box_center, 0)
    start_y = max(h // 2 - box_center, 0)
    min_w = min(box_size, w)
    min_h = min(box_size, h)
    return start_x, start_y, min_w, min_h


def pixellate(arr, dimension, dp_size, px_pitch):
    for i in range(dimension):
        for j in range(dimension):
            x = i * dp_size
            y = j * dp_size
            c = arr[i + j * dimension]
            fill(c)
            stroke(0)
            s = math.trunc(dp_size // px_pitch)
            square(x, y, s)

def setup():
    background(0)
    # led is arranged in sequential manner, hence it will only multiply the width
    # [ ] [ ] [ ] [ ] [ ]
    size(led_panel_width * led_panel_count * img_dp_size, led_panel_height * img_dp_size)
    # load image
    global img
    img = loadImage(img_name)
    # fill the container with pixellated img
    img.resize(*fill_dimension(img.width, img.height, img_container_size))
    img = img.get(*get_center(img.width, img.height, img_container_size))
    pixellate(img.pixels, img_container_size, img_dp_size, pixel_pitch)


def draw():
    pass
