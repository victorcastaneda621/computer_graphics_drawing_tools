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

class Pixel(shapes.Rectangle):
    """Class that represents a pixel on the canvas,
        with coordinates (x,y). 
    """
    # The pixel's coordinates
    x = None
    y = None
    color = constants.DEFAULT_COLOR

    def __init__(self, x, y, color=constants.DEFAULT_COLOR):
        self.x, self.y = x,y
        self._rectangle = None
        self.color = color
    
    def draw(self, color=None, batch=None):
        """Draws the pixel, making it visible."""
        x,y =  canvas_to_screen_coordinates(self.x, self.y)
        if color == None:
            color = self.color
        if batch == None:
            self._rectangle = shapes.Rectangle(x,
                                        y,
                                        width=constants.PIXEL_SIZE,
                                        height=constants.PIXEL_SIZE,
                                        color=color)
        else:
            self._rectangle = shapes.Rectangle(x,
                                            y,
                                            width=constants.PIXEL_SIZE,
                                            height=constants.PIXEL_SIZE,
                                            color=color,
                                            batch=batch)

    def get_coords(self):
        return self.x, self.y
    
