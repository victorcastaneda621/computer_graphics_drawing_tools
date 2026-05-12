"""line_algorithms.py contains the class Line as well as implementations of the line drawing algorithms."""
from basic_geometry.pixel_coordinates import Pixel
    
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
    def __init__(self, pixels, color, style=None):
        """To create a Line, a list of Pixel(x,y) must be given."""
        self.pixels = pixels
        self.color = color
        self.style = style if style is not None else LINE_STYLES.SOLID

    def draw(self, batch):
        """Draws the line on the canvas."""
        match self.style:
            case LINE_STYLES.SOLID:
                for pixel in self.pixels:
                    pixel.draw(self.color, batch)
            case LINE_STYLES.DOTTED:
                for i in range(0, len(self.pixels), 2):
                    self.pixels[i].draw(self.color, batch)
            case LINE_STYLES.DASHED:
                counter = 0
                for i in range(0, len(self.pixels)):
                    if counter != 3:
                        self.pixels[i].draw(self.color, batch)
                    counter = (counter + 1) % 4
                self.pixels[-1].draw(self.color)

    def print(self):
        """Prints the canvas coordinates of every pixel that is part of the line."""
        for pixel in self.pixels:
            pixel.print()
    
    def get_pixels(self):
        return self.pixels

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
