# imports
import math

# physical hardware props
led_panel_height = 64
led_panel_width = 64
led_panel_count = 5

# image
p1_name = "ABCDEFGH"
p1_img_name = "imgs/skaev-px.jpg"
p1_score = 259
p2_name = "IJKLMOPQ"
p2_img_name = "imgs/klyx-px.jpg"
p2_score = 575
top_score = 0
img_container_size = 64
img_dp_size = 4
img_scale = 0.9

# fonts
font_name = "nintendo-nes-font.ttf"
row_size = 40
h1_font_size = 32
h2_font_size = 32
h3_font_size = 16


# pixellation parameters
pixel_pitch = 1.05
pixellation_size = 1 # whole numbers, img_container_size must match

def reset():
    background(0)


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


def pixellate(arr, dimension_x, dimension_y, dp_size, px_pitch, start_x = 0, start_y = 0):
    for i in range(0, dimension_x, dp_size):
        for j in range(0, dimension_y, dp_size):
            x = start_x + i
            y = start_y + j
            offset = dp_size // 2
            c = arr[(i + offset) + (j + offset) * dimension_x]
            fill(c)
            stroke(0)
            rectMode(CENTER)
            s = math.trunc(dp_size // px_pitch)
            square(x, y, s)
            noFill()
            noStroke()

def setup():
    reset()
    # led is arranged in sequential manner, hence it will only multiply the width
    # [ ] [ ] [ ] [ ] [ ]
    size(led_panel_width * led_panel_count * img_dp_size, led_panel_height * img_dp_size)
    rectMode(CENTER)
    
    # load p1 & p2 images
    global p1_img
    global p2_img
    imageMode(CENTER)
    p1_img = loadImage(p1_img_name)
    p2_img = loadImage(p2_img_name)
    # fill the container with pixellated img
    img_size = math.trunc(img_container_size * img_dp_size * img_scale)
    p1_img.resize(*fill_dimension(p1_img.width, p1_img.height, img_size))
    p1_img = p1_img.get(*get_center(p1_img.width, p1_img.height, img_size))
    image(p1_img, 64 * img_dp_size // 2, 64 * img_dp_size // 2)
    # pixellate(p1_img.pixels, p1_img.width, p1_img.height, img_dp_size, pixel_pitch)
    p2_img.resize(*fill_dimension(p2_img.width, p2_img.height, img_size))
    p2_img = p2_img.get(*get_center(p2_img.width, p2_img.height, img_size))
    image(p2_img, (64 * 4 + 32) * img_dp_size, (64 * img_dp_size) // 2)
    # pixellate(p2_img.pixels, p2_img.width, p2_img.height, img_dp_size, pixel_pitch, width - img_container_size * img_dp_size)
    
    # load fonts
    global nintendo_nes_font
    h1_font = createFont(font_name, h1_font_size)
    h2_font = createFont(font_name, h2_font_size)
    h3_font = createFont(font_name, h3_font_size)
    
    # title row
    row = 1.5
    textFont(h1_font)
    fill(255)
    draw_text("LIFC 2025: RETRO ARCADE", row)
    
    # player row
    middle_offset_x = -4
    left_x = (64 * 1 + 32 - middle_offset_x) * img_dp_size
    center_x = (64 * 2 + 32) * img_dp_size
    right_x = (64 * 3 + 32 + middle_offset_x) * img_dp_size
    row += 1.5
    fill(color(255, 64, 64))
    rect((64 * 2 + 32) * img_dp_size, (row - 0.35) * row_size, 128, row_size, 32)
    
    textFont(h2_font)
    draw_text("TOP", row, center_x)
    row += 1
    draw_text("1UP", row, left_x, color(100, 255, 255))
    draw_text(str(top_score).rjust(7, '0'), row, center_x)
    draw_text("2UP", row, right_x, color(100, 255, 255))
    row += 1
    draw_text(str(p1_score).rjust(7, '0'), row, left_x)
    draw_text(str(p2_score).rjust(7, '0'), row, right_x)
    row += 1
    draw_text(p1_name, row, left_x)
    # draw_text("@@@", row, center_x)
    draw_text(p2_name, row, right_x)

    # final row
    row += 1.5
    textFont(h2_font)
    draw_text("CONTINUE?", row)
    
    # pixellate everything
    loadPixels()
    reset()
    pixellate(pixels, width, height, img_dp_size, pixel_pitch)

def draw_text(string, row, custom_x=None, colour=color(255)):
    textAlign(CENTER)
    rectMode(CENTER)
    fill(colour)
    x = custom_x if custom_x else ((64 * 5 // 2) * img_dp_size)
    y = math.trunc(row * row_size)
    text(string, x, y)
    

def draw():
    pass
