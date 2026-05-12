"""line_algorithms.py contains the class Line as well as implementations of the line drawing algorithms."""
import math

from pixel_coordinates import Pixel
from constants import DEFAULT_LINE_COLOR

# Identifiers for the different line algorithms
class LINE_ALGORITHMS:
    """Class acting as an enumerate for the available line drawing algorithms."""
    SLOPE_INTERCEPT = 0
    DDA = 1
    BRESENHAM_INT = 2
    BRESENHAM_FLOAT = 3

    def all():
        """Returns all available line drawing algorithms."""
        return set([0,1,2,3])
    
# Identifiers for the different line styles
class LINE_STYLES:
    """Class acting as an enumerate for the available line styles."""
    SOLID = 0
    DOTTED = 1
    DASHED = 2

    def all():
        """Returns all available line styles."""
        return set([0,1,2])

class Line:
    """Class that represents a line, storing all pixels that must be visible to draw it on screen."""
    pixels = list()
    color = DEFAULT_LINE_COLOR
    style =LINE_STYLES.SOLID
    def __init__(self, pixels, color, style):
        """To create a Line, a list of Pixel(x,y) must be given."""
        self.pixels = pixels
        self.color = color
        self.style = style

    def draw(self):
        """Draws the line on the canvas."""
        match self.style:
            case LINE_STYLES.SOLID:
                for pixel in self.pixels:
                    pixel.draw(self.color)
            case LINE_STYLES.DOTTED:
                for i in range(0, len(self.pixels), 2):
                    self.pixels[i].draw(self.color)
            case LINE_STYLES.DASHED:
                counter = 0
                for i in range(0, len(self.pixels)):
                    if counter != 3:
                        self.pixels[i].draw(self.color)
                    counter = (counter + 1) % 4
                self.pixels[-1].draw(self.color)

    def print(self):
        """Prints the canvas coordinates of every pixel that is part of the line."""
        for pixel in self.pixels:
            pixel.print()
    
    def get_pixels(self):
        return self.pixels

def slope_intercept(x_start, y_start, x_end, y_end):
    """Given two (x,y) pairs (start and end), the method calculates what
        other pixels must be activated following the Slope Intercept Algorithm,
        adapted for every quadrant.
    """
    line_pixels = []

    # If the line goes to the left, we swap the initial and final points,
    # and draw from left to right
    if x_end < x_start:
        x_start, y_start, x_end, y_end = x_end, y_end, x_start, y_start # Swap start and end

    # Assign initial value to x and y
    x = x_start
    y = y_start

    # If y is the same at the start and end, the line will be horizontal, so we 
    # just add 1 to x until reaching x_end
    if y_start == y_end:
        return horizontal_line(x, x_end, y)

    # If x is the same at the start and end, the line will be vertical, so we just add 1 to
    # y until reaching y_end
    if x_start == x_end:
        if y_end < y_start: # It might happen that y_end < y_start, so we might need to swap start and end
            y_start, y_end = y_end, y_start
            y = y_start
        return vertical_line(x, y, y_end)

    dx = x_end - x_start
    dy = y_end - y_start
    m = dy / dx
    x_y_swapped = False

    # If abs(m) > 1, we swap x and y so the line is on the other half of the quadrant,
    # we calculate the line and swap back the coordinates for x and y of each point.
    if abs(m) > 1:
        x,y = y,x
        x_start, y_start = y_start, x_start
        x_end, y_end = y_end, x_end
        m = 1 / m
        x_y_swapped = True
        if x_end < x_start: # It might have been the case the y_end < y_start, so we might need to swap start and end
            x_start, y_start, x_end, y_end = x_end, y_end, x_start, y_start # Swap start and end
            x = x_start
            y = y_start

    b = y_start - (m*x_start)

    while x <= x_end:
        if x_y_swapped: # We need to swap back
            line_pixels.append(Pixel(y,x))
        else:
            line_pixels.append(Pixel(x,y))
        x += 1
        y = round((m*x) + b)
    return line_pixels

def dda(x_start, y_start, x_end, y_end):
    """Given two (x,y) pairs (start and end), the method calculates what
        other pixels must be activated following the DDA Algorithm,
        which works for any quadrant without modifications.
    """
    dx = x_end - x_start
    dy = y_end - y_start
    line_pixels = []
    M = max(abs(dx), abs(dy))
    dx = dx / M
    dy = dy / M
    x = x_start + 0.5
    y = y_start + 0.5
    i = 0
    while(i <= M):
        line_pixels.append(Pixel(math.floor(x), math.floor(y)))
        x = x + dx
        y = y + dy
        i += 1
    return line_pixels

def bresenham_float(x_start, y_start, x_end, y_end):
    """Given two (x,y) pairs (start and end), the method calculates what
        other pixels must be activated following Bresenham's Algorithm,
        for floating point arithmetic, adapted for every quadrant.
    """
    x = x_start
    y = y_start

    dx = x_end - x_start
    dy = y_end - y_start

    sx = sign(dx)
    sy = sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    # Handle horizontal lines outside the main loop
    if y_start == y_end:
        if x_end < x_start: # It might happen that x_end < x_start, so we might need to swap start and end
            x = x_end
            x_end = x_start
        return horizontal_line(x, x_end, y)

    # Handle vertical lines outside the main loop
    if x_start == x_end:
        if y_end < y_start: # It might happen that y_end < y_start, so we might need to swap start and end
            y = y_end
            y_end = y_start
        return vertical_line(x, y, y_end)

    x_y_swapped = False
    if dy > dx: # Swap x and y
        x_y_swapped = True
        dx, dy = dy, dx
        x, y = y, x
        sx, sy = sy, sx
    m = dy / dx # No need for vertical special cases (dx / 0), since
    # we swap x and y, getting (0 / dx), just like for horizontal lines
    e = m - 1/2
    line_pixels = []
    i = 0
    while i <= dx:
        if x_y_swapped: # We need to swap them back
            line_pixels.append(Pixel(y, x))
        else:
            line_pixels.append(Pixel(x, y))
        if(e > 0):
            y += sy
            e -= 1
        x += sx
        e += m
        i += 1
    return line_pixels

def bresenham_int(x_start, y_start, x_end, y_end):
    """Given two (x,y) pairs (start and end), the method calculates what
        other pixels must be activated following Bresenham's Algorithm,
        for integer arithmetic, adapted for every quadrant.
    """
    x = x_start
    y = y_start

    dx = x_end - x_start
    dy = y_end - y_start

    sx = sign(dx)
    sy = sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    # Handle horizontal lines outside the main loop
    if y_start == y_end:
        if x_end < x_start: # It might happen that x_end < x_start, so we might need to swap start and end
            x = x_end
            x_end = x_start
        return horizontal_line(x, x_end, y)

    # Handle vertical lines outside the main loop
    if x_start == x_end:
        if y_end < y_start: # It might happen that y_end < y_start, so we might need to swap start and end
            y = y_end
            y_end = y_start
        return vertical_line(x, y, y_end)
    
    x_y_swapped = False
    if dy > dx: # Swap x and y
        x_y_swapped = True
        dx, dy = dy, dx
        x, y = y, x
        sx, sy = sy, sx
    m = dy / dx # No need for vertical special cases (dx / 0), since
    # we swap x and y, getting (0 / dx), just like for horizontal lines
    e = (2*dy) - dx
    line_pixels = []
    i = 0
    while i <= dx:
        if x_y_swapped: # We need to swap them back
            line_pixels.append(Pixel(y, x))
        else:
            line_pixels.append(Pixel(x, y))
        if(e > 0):
            y += sy
            e -= 2*dx
        x += sx
        e += 2*dy
        i += 1
    return line_pixels

def sign(x):
    """Returns 1 if x is positive, -1 if it is negative and 0 if x = 0."""
    if x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return 1
    
def horizontal_line(x, x_end, y):
    """Helper function that handles horizontal lines (where y doesn't change)."""
    line_pixels = []
    while x <= x_end:
            line_pixels.append(Pixel(x,y))
            x += 1
    return line_pixels

def vertical_line(x, y, y_end):
    """Helper function that handles vertical lines (where x doesn't change)."""
    line_pixels = []
    while y <= y_end:
        line_pixels.append(Pixel(x,y))
        y += 1
    return line_pixels
