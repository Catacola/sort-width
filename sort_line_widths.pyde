import time
import random
import math

#num_lines = 40

seed = []

def setup():
    size(1024, 768)
    noLoop()
    global seed
    seed = list(range(20))
    random.shuffle(seed)


def draw():
    background(51)

    global seed
    print('seed:', seed)

    layers = sort_with_steps(seed)

    # horiz_quad_gradient(100, 700, 200, 300, 400, 500)
    draw_lines(layers)
    # time.sleep(100)
    # print('Done!')


def sort_with_steps(lst):
    layers = []
    layers.append(lst[:])

    for i in range(len(lst)):
        for j in range(len(lst) - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
            layers.append(lst[:])

    return layers


def draw_lines(layers):
    num_lines = len(layers[0])
    num_layers = len(layers)

    noStroke()

    v_spacing = vertical_spacing(num_layers)
    draw_layer(layers[0], layers[0], 0, int(round(v_spacing)))

    for i in range(num_layers - 1):
        y_top = int(round(v_spacing * (i + 1)))
        y_bottom = int(round(v_spacing * (i + 2)))
        draw_layer(layers[i], layers[i+1], y_top, y_bottom)

    draw_layer(layers[-1], layers[-1], int(round(height - v_spacing)), height)


def draw_layer(start_layer, end_layer, y_top, y_bottom):
    num_lines = len(start_layer)
    for i, (start_width, end_width) in enumerate(zip(start_layer, end_layer)):
        x1, x2 = get_line_edges(start_width, i, num_lines)
        x3, x4 = get_line_edges(end_width, i, num_lines)

        #quad(x1, y_top, x2, y_top, x4, y_bottom, x3, y_bottom)
        horiz_quad_gradient(x1, x2, y_top, x3, x4, y_bottom)


def horiz_quad_gradient(x_topleft, x_topright, y_top, x_bottomleft, x_bottomright, y_bottom):
    # print('foo')
    lower_left = (85, 88, 255)
    upper_right = (255, 255, 0)

    for y in range(y_top, y_bottom):
        pct = 1.0 * (y_top - y) / (y_top - y_bottom)
        x_left = x_topleft + pct * (x_bottomleft - x_topleft)
        x_right = x_topright + pct * (x_bottomright - x_topright)
        for x in range(int(x_left), int(x_right + 1)):
            r, g, b = blend_by_position(lower_left, (0, height), upper_right, (width, 0), (x, y))
            stroke(r, g, b)
            point(x, y)

########################
#
# Helpers
#
########################

def get_line_edges(line_width, line_number, num_lines):
    spacing = width / (num_lines + 1)

    max_width = spacing * 0.9
    this_width = line_width * max_width / num_lines

    center = spacing * (line_number + 1)

    return center - this_width / 2, center + this_width / 2


def vertical_spacing(num_layers):
    return height * 1.0 / (num_layers + 1)


def blend_by_position(c1, p1, c2, p2, x):
    d1 = ((x[0] - p1[0]) ** 2 + (x[1] - p1[1]) ** 2) ** 0.5
    d2 = ((x[0] - p2[0]) ** 2 + (x[1] - p2[1]) ** 2) ** 0.5
    w1 = d2 / (d1 + d2)
    w2 = d1 / (d1 + d2)
    r = w1 * c1[0] + w2 * c2[0]
    g = w1 * c1[1] + w2 * c2[1]
    b = w1 * c1[2] + w2 * c2[2]
    
    return r, g, b
