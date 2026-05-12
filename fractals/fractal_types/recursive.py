import math

from basic_geometry.pixel_coordinates import canvas_to_screen_coordinates
from constants import DEFAULT_COLOR
from basic_geometry.line_algorithms import Line, bresenham_int


def draw_line(x1, y1, x2, y2):
    pixels = bresenham_int(x1, y1, x2, y2)
    print((x1, y1), (x2, y2))
    return Line(pixels, color=DEFAULT_COLOR)

def sierpinsky_triangle(p1, p2, p3, n):
    x1, y1 = p1.get_coords()
    x2, y2 = p2.get_coords()
    x3, y3 = p3.get_coords()
    lines = []
    sierpinsky_aux(x1, y1, x2, y2, x3, y3, n-1, lines)
    return lines


def sierpinsky_aux(x1, y1, x2, y2, x3, y3, n, lines):
    if n == 0:
        lines += [draw_line(x1, y1, x2, y2),
                  draw_line(x2, y2, x3, y3),
                  draw_line(x3, y3, x1, y1)]
        return
    else:
        ax = x1 + ((x2 - x1) / 2)
        ay = y1 + ((y2 - y1) / 2)
        bx = x3 + ((x2 - x3) / 2)
        by = y3 + ((y2 - y3) / 2)
        cx = x1 + ((x3 - x1) / 2)
        cy = y1 + ((y3 - y1) / 2)
        sierpinsky_aux(ax, ay, x2, y2, bx, by, n-1, lines)
        sierpinsky_aux(x1, y1, ax, ay, cx, cy, n-1, lines)
        sierpinsky_aux(cx, cy, bx, by, x3, y3, n-1, lines)

def koch_curve(p1, p2, n):
    x1, y1 = p1.get_coords()
    x4, y4 = p2.get_coords()
    lines = []
    koch_curve_aux(x1, y1, x4, y4, n-1, lines)
    return lines

def koch_curve_aux(x1, y1, x4, y4, n, lines):
    if n == 0:
        lines += [draw_line(x1, y1, x4, y4)]
        return
    else:
        dx = (x4 - x1) / 3
        dy = (y4 - y1) / 3
        x2 = x1 + dx
        y2 = y1 + dy
        x3 = x2 + dx
        y3 = y2 + dy
        x = ((dx - math.sqrt(3)*dy) / 2) + (x1 + dx)
        y = ((math.sqrt(3)*dx + dy) / 2) + (y1 + dy)

        koch_curve_aux(x1, y1, x2, y2, n-1, lines)
        koch_curve_aux(x2, y2, x, y, n-1, lines)
        koch_curve_aux(x, y, x3, y3, n-1, lines)
        koch_curve_aux(x3, y3, x4, y4, n-1, lines)

def koch_snowflake(p1, p2, p3, n):
    lines = []
    lines += koch_curve(p1, p2, n)
    lines += koch_curve(p2, p3, n)
    lines += koch_curve(p3, p1, n)
    return lines
        
def cantor_set(p1, p2, n):
    x1, y1 = p1.get_coords()
    x2, y2 = p2.get_coords()
    lines = cantor_set_aux(x1, x2, y1, n-1)
    return lines

def cantor_set_aux(x1, x2, y, n):
    lines = []
    if n == 0:
        return [draw_line(x1, y, x2, y)]
    else:
        dx = (x2 - x1) / 3
        nx1 = x1 + dx
        nx2 = x2 - dx

        lines.append(draw_line(x1, y, x2, y))
        lines += cantor_set_aux(x1, nx1, y - 40, n-1)
        lines += cantor_set_aux(nx2, x2, y - 40, n-1)

        return lines
