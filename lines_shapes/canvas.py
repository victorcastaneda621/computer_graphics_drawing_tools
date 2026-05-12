"""canvas.py contains a class to save information about the current state of the canvas."""
import copy

from line_algorithms import Line, slope_intercept, dda, bresenham_float, bresenham_int, LINE_ALGORITHMS, LINE_STYLES
from constants import DEFAULT_LINE_COLOR
from transformations_2d import Shape2D, ReflectionType
from pixel_coordinates import Pixel

class CanvasState:
    """Singleton class that stores the current canvas state, allowing for modifications.
        Many of the 2d transformation -related methods have a shape=None parameter, that
        allows the transformations to be applied to the canvasState's shape or to an
        external shape passed."""
    # Points introduced by the user, cleared after drawing a line
    line_x_start = 0
    line_y_start = 0
    line_x_end = 0
    line_y_end = 0

    # When clicking on the cnavas, this boolean tells us if the next point to buffer
    # is the starting or ending point
    is_start_next = True

    # When the user clicks the UI button, the line's pixels will be shown or not
    show_last_line_points = False

    # Line algorithm currently selected by the user, Slope Intercept is the default
    selected_line_drawing_algorithm = LINE_ALGORITHMS.BRESENHAM_INT

    # Style currently selected by the user, Solid is the default
    selected_line_style = LINE_STYLES.SOLID

    # List of lines drawn by the user
    lines = list()

    # List of performed transformations
    transformation_history = list()

    # Figure made up of every line in the canvas
    shape = Shape2D([])

    # Coordinates the user is currently hovering over
    hover_coords = (0,0)

    # Color of the next line's pixels
    color = DEFAULT_LINE_COLOR

    # Whether the axes and / or grid should be drawn
    show_axes = True
    show_grid = False
    grid_lines = list()

    # Current values of the 2D Transformations input boxes
    translation_x = 0
    translation_y = 0
    rotation_alpha = 0
    rotation_is_counter_clockwise = False
    scaling_x = 0
    scaling_y = 0
    shear_x = 0
    shear_y = 0
    reflection_type = ReflectionType.X_AXIS
    reflection_last_point = (0,0)
    reflection_line = None
    reflection_b = 0
    reflection_m = 0

    # Avoid saving undo transformations to history
    undoing = False

    # Control whwther to play the animation
    run_animation = False

    def change_algorithm(self, new_algorithm):
        """Changes the algorithm that is currently selected by the user.
            The algorithm ID should be one of the available in 
            line_algorithms.LINE_ALGORITHMS. 
            Throws a ValueError if the algorithm ID is invalid.
        """
        if new_algorithm in LINE_ALGORITHMS.all():
            self.selected_line_drawing_algorithm = new_algorithm
        else:
            raise ValueError("Invalid line drawing algorithm in CanvasState.change_algorithm.")
        
    def change_style(self, new_style):
        """Changes the style that is currently selected by the user.
            The style ID should be one of the available in 
            line_algorithms.LINE_STYLES. 
            Throws a ValueError if the algorithm ID is invalid.
        """
        if new_style in LINE_STYLES.all():
            self.selected_line_style = new_style
        else:
            raise ValueError("Not a valid line style.")
            
    def add_start_to_line_point_buffer(self, x, y):
        """A point (x,y) is buffered as the starting point for the line that will be drawn.
        """
        self.line_x_start = x
        self.line_y_start = y

    def add_end_to_line_point_buffer(self, x, y):
        """A point (x,y) is buffered as the ending point for the line that will be drawn.
        """
        self.line_x_end = x
        self.line_y_end = y

    def click_add_point_to_buffer(self, x, y):
        """A point (x,y) is buffered as either the starting on ending point for the line
            that will be drawn, depening on how many times the canvas has been clicked.
            This is only called when the point is inputted via clicking in the canvas.
        """
        if self.is_start_next:
            self.add_start_to_line_point_buffer(x, y)
            self.is_start_next = False
        else:
            self.add_end_to_line_point_buffer(x, y)
            self.is_start_next = True

    def draw_buffered_line(self):
        """Draws the line outputted by the specified algorithm with the buffered
            start and end points.
        """
        new_line = self.draw_line(self.line_x_start, self.line_y_start, self.line_x_end, self.line_y_end)
        self.lines.append(new_line)

        # We also add the line's start and end points as vertices of the shape
        self.shape.add_line(Pixel(self.line_x_start, self.line_y_start), Pixel(self.line_x_end, self.line_y_end))

        # Reset the buffered points' coordinates
        self.line_x_start = 0
        self.line_y_start = 0
        self.line_x_end = 0
        self.line_y_end = 0

    def draw_line(self, x_start, y_start, x_end, y_end, color=None):
        """Draws a line on the canvas, using the specified algorithm, color and style."""
        if color is None:
            color = self.color
        match self.selected_line_drawing_algorithm:
            case LINE_ALGORITHMS.SLOPE_INTERCEPT:
                new_line = Line(slope_intercept(x_start, y_start, 
                                                x_end, y_end), 
                                                color,
                                                self.selected_line_style)
            case LINE_ALGORITHMS.DDA:
                new_line = Line(dda(x_start, y_start, 
                                    x_end, y_end), 
                                    color,
                                    self.selected_line_style)
            case LINE_ALGORITHMS.BRESENHAM_FLOAT:
                new_line = Line(bresenham_float(x_start, y_start,
                                                x_end, y_end), 
                                                color,
                                                self.selected_line_style)
            case LINE_ALGORITHMS.BRESENHAM_INT:
                new_line = Line(bresenham_int(x_start, y_start, 
                                              x_end, y_end), 
                                              color,
                                              self.selected_line_style)
            case _:
                raise ValueError("No valid algorithm selected in CanvasState.")
        return new_line

    def clear_canvas(self):
        """Erases everything that has been drawn on the canvas."""
        self.lines.clear()
        self.shape.replace_lines([])
        self.transformation_history.clear()

    def set_hover_coords(self,x,y):
        """Changes the value of hover_coords."""
        self.hover_coords = (x,y)

    def get_hover_coords(self):
        """Returns the coordinates the mouse is currently hovering over."""
        return self.hover_coords

    # Getter for all drawn lines
    def get_lines(self): return self.lines

    # Getter and setter for the color of the next line to draw
    def get_color(self): return self.color
    def set_color(self, new_color): self.color = new_color
    
    # Buffered start and end point getters
    def get_buffered_x_start(self): return self.line_x_start
    def get_buffered_y_start(self): return self.line_y_start
    def get_buffered_x_end(self): return self.line_x_end
    def get_buffered_y_end(self): return self.line_y_end

    # Buffered start and end point setters
    def set_buffered_x_start(self, x): self.line_x_start = x
    def set_buffered_y_start(self, y): self.line_y_start = y
    def set_buffered_x_end(self, x): self.line_x_end = x
    def set_buffered_y_end(self, y): self.line_y_end = y

    # Set up the canvas after calculating transformed points
    def apply_transformation(self, shape, shape_was_none):
        new_lines = list()
        i = 0
        for line in shape.vertices:
            x_start, y_start = line[0].get_coords()
            x_end, y_end = line[1].get_coords()
            color = self.lines[i].color if i < len(self.lines) else self.color
            new_lines.append(self.draw_line(x_start, y_start, x_end, y_end, color))
            i += 1
        
        # Update the canvasState's lines
        if shape_was_none:
            self.lines = new_lines
        else:
            return new_lines
        
    # Getters and setters for translation
    def get_translation_x(self): return self.translation_x
    def get_translation_y(self): return self.translation_y
    def set_translation_x(self, x): self.translation_x = x
    def set_translation_y(self, y): self.translation_y = y

    # Apply translation with the current values
    def apply_translation(self, translation_x=None, translation_y=None, shape=None):
        if translation_x is None:
            translation_x = self.translation_x
        if translation_y is None:
            translation_y = self.translation_y 
        shape_was_none = False
        if shape == None:
            shape = self.shape
            shape_was_none = True

        shape.translation(translation_x, translation_y)
        if not self.undoing and shape_was_none:
            self.transformation_history.append(("translation", translation_x, translation_y))
        
        self.apply_transformation(shape, shape_was_none)

    # Getters and setters for rotation
    def set_rotation_alpha(self, new_alpha): self.rotation_alpha = new_alpha
    def get_rotation_alpha(self): return self.rotation_alpha

    # Apply rotation with the current values
    def apply_rotation(self, alpha=None, rotation_is_cc=None, shape=None):
        if alpha is None:
            alpha = self.rotation_alpha
        if rotation_is_cc is None:
            rotation_is_cc = self.rotation_is_counter_clockwise
        shape_was_none = False
        if shape == None:
            shape = self.shape
            shape_was_none = True

        shape.rotation(alpha, rotation_is_cc)

        if not self.undoing and shape_was_none:
            self.transformation_history.append(("rotation", 
                                                alpha, rotation_is_cc))
            
        self.apply_transformation(shape, shape_was_none)

    # Getters and setters for scaling
    def get_scaling_x(self): return self.scaling_x
    def get_scaling_y(self): return self.scaling_y
    def set_scaling_x(self, x): self.scaling_x = x
    def set_scaling_y(self, y): self.scaling_y = y

    # Apply scaling with the current values
    def apply_scaling(self, scaling_x=None, scaling_y=None, shape=None):
        if scaling_x is None:
            scaling_x = self.scaling_x
        if scaling_y is None:
            scaling_y = self.scaling_y
        shape_was_none = False
        if shape == None:
            shape = self.shape
            shape_was_none = True
            old_shape = copy.deepcopy(self.shape)
            old_lines = copy.deepcopy(self.lines)

        shape.scaling(scaling_x, scaling_y)

        if not self.undoing and shape_was_none:
            if scaling_x == 0 or scaling_y == 0:
                self.transformation_history.append(("scaling", scaling_x, scaling_y, old_shape, old_lines))
            else:
                self.transformation_history.append(("scaling", scaling_x, scaling_y))

        self.apply_transformation(shape, shape_was_none)

    # Getters and setters for shearing
    def get_shear_x(self): return self.shear_x
    def get_shear_y(self): return self.shear_y
    def set_shear_x(self, x): self.shear_x = x
    def set_shear_y(self, y): self.shear_y = y

    # Apply shearing with the current values
    def apply_shearing(self, shear_x=None, shear_y=None, shape=None):
        if shear_x is None:
            shear_x = self.shear_x
        if shear_y is None:
            shear_y = self.shear_y
        shape_was_none = False
        if shape == None:
            shape = self.shape
            shape_was_none = True
            old_shape = copy.deepcopy(self.shape)
            old_lines = copy.deepcopy(self.lines)

        shape.shearing(shear_x, shear_y)

        if not self.undoing and shape_was_none:
            self.transformation_history.append(("shearing", old_shape, old_lines))

        self.apply_transformation(shape, shape_was_none)

    def get_reflection_type(self): return self.reflection_type
    def set_reflection_type(self, type): self.reflection_type = type
    def get_reflection_last_point(self): return self.reflection_last_point
    def set_reflection_last_point(self, point): self.reflection_last_point = point
    def get_reflection_b(self): return self.reflection_b
    def set_reflection_b(self, b): self.reflection_b = b
    def get_reflection_m(self): return self.reflection_m
    def set_reflection_m(self, m): self.reflection_m = m

    def apply_reflection(self, type=None, last_point=None, m=None, b=None, shape=None):
        # Check selected type
        if type is None:
            type = self.reflection_type
        if last_point is None:
            last_point = self.reflection_last_point
        if m is None:
            m = self.reflection_m
        if b is None:
            b = self.reflection_b
        shape_was_none = False
        if shape == None:
            shape = self.shape
            shape_was_none = True

        # Handle cases that require a line
        if type is ReflectionType.ORIGIN:
            shape.reflection(type, last_point)
            if not self.undoing and shape_was_none:
                self.transformation_history.append(("reflection", type, last_point))
        elif type is ReflectionType.ANY_LINE:
            shape.reflection(type, m=m, b=b)
            if not self.undoing and shape_was_none:
                self.transformation_history.append(("reflection", type, m, b))
        else:
            shape.reflection(type)
            if not self.undoing and shape_was_none:
                self.transformation_history.append(("reflection", type))
        
        return self.apply_transformation(shape, shape_was_none)

    def draw_reflection_line(self):
        if self.reflection_type == ReflectionType.ORIGIN:
            x,y = self.reflection_last_point
            self.reflection_line = self.draw_line(x, y, -x, -y)
        else:
            y_start = (-72*self.reflection_m) + self.reflection_b
            y_end = (72*self.reflection_m) + self.reflection_b
            self.reflection_line = self.draw_line(-72, y_start, 72, y_end)
    
    def clear_reflection_line(self):
        self.reflection_line = None
        self.reflection_last_point = (0,0)
        self.reflection_m = 0
        self.reflection_b = 0

    def undo_last(self):
        self.undoing = True
        if self.transformation_history:
            last_transformation = self.transformation_history.pop()
            # Each element is a tuple of (tranformsation_name, parameters)
            transformation = last_transformation[0]
            match transformation:
                case "translation":
                    # The inverse of the translation (x, y) is doing a transaltion
                    # with (-x, -y)
                    translation_x = -last_transformation[1]
                    translation_y = -last_transformation[2]
                    self.apply_translation(translation_x=translation_x,
                                           translation_y=translation_y)
                case "rotation":
                    # The inverse of the rotaiton (alpha, is_cc) is doing a rotation
                    # with (alpha, not is_cc)
                    alpha = last_transformation[1]
                    is_cc = not last_transformation[2]
                    self.apply_rotation(alpha=alpha, 
                                        rotation_is_cc=is_cc)
                case "scaling":
                    # The inverse of the scaling (scale_x, scale_y) is doing scaling
                    # with (1/scale_x, 1/scale_y)
                    if last_transformation[1] == 0 or last_transformation[2] == 0:
                        self.shape = last_transformation[3]
                        self.lines = last_transformation[4]
                    else:
                        scale_x = 1/last_transformation[1]
                        scale_y = 1/last_transformation[2]
                        self.apply_scaling(scaling_x=scale_x, scaling_y=scale_y)
                case "shearing":
                    # Shearing is non-invertable in many cases, so we just saved the shape's previous state
                    self.shape = last_transformation[1]
                    self.lines = last_transformation[2]
                case "reflection":
                    ## Reflecting again using the same line or axis
                    type = last_transformation[1]
                    if type == ReflectionType.ORIGIN:
                        last_point = last_transformation[2]
                        self.apply_reflection(type=type, last_point=last_point)
                    elif type == ReflectionType.ANY_LINE:
                        m = last_transformation[2]
                        b = last_transformation[3]
                        self.apply_reflection(type=type, m=m, b=b)
                    else:
                        self.apply_reflection(type=type)
        self.undoing = False