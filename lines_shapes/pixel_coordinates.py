"""pixel_coordinates.py contains the class Pixel and related utility functions."""

from pyglet import shapes
import constants

def canvas_to_screen_coordinates(x, y):
    """Converts a set of canvas coordinates into screen coordinates.
        For example, if called with (0,0), it will return the position
        of the canvas' origin point in real pixels.
    """
    x = constants.PIXEL_SIZE*x + ((constants.WINDOW_WIDTH - constants.PANEL_WIDTH) // 2)
    y = constants.PIXEL_SIZE*y + (constants.WINDOW_HEIGHT // 2)
    return (int(x), int(y))

def screen_to_canvas_coordinates(x, y):
    """Converts a set of real screen coordinates into canvas coordinates."""
    x = (x - ((constants.WINDOW_WIDTH - constants.PANEL_WIDTH) // 2)) // constants.PIXEL_SIZE
    y = (y - (constants.WINDOW_HEIGHT // 2)) // constants.PIXEL_SIZE
    return (int(x), int(y))

def draw_axes():
    """Draws the X and Y axes on the canvas."""
    (x, y) = canvas_to_screen_coordinates(0, 0)
    x += constants.PIXEL_SIZE // 2
    y += constants.PIXEL_SIZE // 2
    gray_color = (138,138,138)
    thickness = constants.PIXEL_SIZE
    x_axis = shapes.Line(x=constants.WINDOW_WIDTH, 
                            y=y, 
                            x2=-constants.WINDOW_WIDTH, 
                            y2=y, 
                            thickness=thickness,
                            color=gray_color)
    y_axis = shapes.Line(x=x,
                            y=constants.WINDOW_HEIGHT,
                            x2=x,
                            y2=-constants.WINDOW_HEIGHT,
                            thickness=thickness,
                            color=gray_color)
    x_axis.draw()
    y_axis.draw()


def draw_grid():
    (origin_x, origin_y) = canvas_to_screen_coordinates(0, 0)
    origin_x += constants.PIXEL_SIZE
    origin_y += constants.PIXEL_SIZE

    gray_color = (138, 138, 138)
    thickness = 1

    # Vertical grid lines
    ten_count = 9
    for i in range(0, 72, 1):
        if ten_count == 9:
            thickness = 2
        x = origin_x + i * constants.PIXEL_SIZE
        line = shapes.Line(
            x=x,
            y=0,
            x2=x,
            y2=constants.WINDOW_HEIGHT,
            thickness=thickness,
            color=gray_color
        )
        line.draw()
        if ten_count == 9:
            thickness = 1
        ten_count = (ten_count + 1) % 10
    ten_count = 9
    for i in range(0, -74, -1):
        if ten_count == 9:
            thickness = 2
        x = origin_x + i * constants.PIXEL_SIZE
        line = shapes.Line(
            x=x,
            y=0,
            x2=x,
            y2=constants.WINDOW_HEIGHT,
            thickness=thickness,
            color=gray_color
        )
        line.draw()
        if ten_count == 9:
            thickness = 1
        ten_count = (ten_count + 1) % 10

    # Horizontal grid lines
    ten_count = 0
    for i in range(-50, 0, 1):
        y = origin_y + i * constants.PIXEL_SIZE
        if ten_count == 9:
            thickness = 2
        line = shapes.Line(
            x=0,
            y=y,
            x2=constants.WINDOW_WIDTH,
            y2=y,
            thickness=thickness,
            color=gray_color
        )
        line.draw()
        if ten_count == 9:
            thickness = 1
        ten_count = (ten_count + 1) % 10
    ten_count = 0
    for i in range(0, 50, 1):
        y = origin_y + i * constants.PIXEL_SIZE
        if ten_count == 9:
            thickness = 2
        line = shapes.Line(
            x=0,
            y=y,
            x2=constants.WINDOW_WIDTH,
            y2=y,
            thickness=thickness,
            color=gray_color
        )
        line.draw()
        if ten_count == 9:
            thickness = 1
        ten_count = (ten_count + 1) % 10


class Pixel(shapes.Rectangle):
    """Class that represents a pixel on the canvas,
        with coordinates (x,y). 
    """
    # The pixel's coordinates
    x = None
    y = None

    def __init__(self, x, y):
        """Save the canvas placement of the canvas pixel."""
        self.x, self.y = x,y
    
    def draw(self, color):
        """Draws the pixel, making it visible."""
        x,y = canvas_to_screen_coordinates(self.x, self.y)
        canvas_pixel = shapes.Rectangle(x,
                                        y,
                                        width=constants.PIXEL_SIZE,
                                        height=constants.PIXEL_SIZE,
                                        color=color)
        canvas_pixel.draw()

    def print(self):
        """Prints the canvas coordinates of the pixel."""
        x,y = screen_to_canvas_coordinates(self.x, self.y)
        print(f"({x}, {y})")

    def get_coords(self):
        return self.x, self.y
    
