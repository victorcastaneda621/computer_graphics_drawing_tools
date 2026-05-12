import numpy as np

import constants
from pixel_coordinates import Pixel

class ReflectionType:
    X_AXIS = 0
    Y_AXIS = 1
    ORIGIN = 2
    ANY_LINE = 3

    def all():
        return set([0,1,2,3])

# Class that represents a 2D shape (set of lines)
class Shape2D:
    # List of vertices of the shape (lines' start and end points)
    # Contains tuples, to know which vertices form an edge
    vertices = []
    drawn_lines = []

    def __init__(self, vertices):
        self.vertices = vertices

    def add_line(self, start, end):
        self.vertices.append((start, end))

    def get_vertices(self):
        return self.vertices
    
    def replace_lines(self, vertices):
        self.vertices = vertices

    def apply_to_vertices(self, matrix):
        new_vertices = []
        for v1, v2 in self.vertices:
            # We apply the transformation to both vertices that form an edge (v1, v2) in the
            # same iteration
            vx1, vy1 = v1.get_coords()
            vx2, vy2 = v2.get_coords()
            vector1 = np.matrix([[vx1], [vy1], [1]])
            vector2 = np.matrix([[vx2], [vy2], [1]])
            new_vertex1 = matrix @ vector1
            new_vertex2 = matrix @ vector2
            new_vertices.append((Pixel(round(new_vertex1[0].item()), round(new_vertex1[1].item())),
                                 Pixel(round(new_vertex2[0].item()), round(new_vertex2[1].item()))))
        self.vertices = new_vertices

    def translation(self, delta_x, delta_y):
        translation_matrix = np.matrix([[1, 0, delta_x], 
                                        [0, 1, delta_y], 
                                        [0, 0, 1]])
        self.apply_to_vertices(translation_matrix)

    def rotation(self, alpha, counter_clockwise):
        alpha = np.deg2rad(alpha)
        if counter_clockwise:
            rotation_matrix = np.matrix([[np.cos(alpha), -np.sin(alpha) ,0], 
                                         [np.sin(alpha), np.cos(alpha), 0], 
                                         [0,0,1]])
        else:
            rotation_matrix = np.matrix([[np.cos(alpha), np.sin(alpha) ,0], 
                                         [-np.sin(alpha), np.cos(alpha), 0], 
                                         [0,0,1]])
        self.apply_to_vertices(rotation_matrix)

    def scaling(self, x_scale, y_scale):
            scaling_matrix = np.matrix([[x_scale, 0, 0], 
                                        [0, y_scale, 0], 
                                        [0, 0, 1]])
            self.apply_to_vertices(scaling_matrix)

    def shearing(self, x_shear, y_shear):
        shearing_matrix = np.matrix([[1, x_shear, 0], 
                                     [y_shear, 1, 0],
                                     [0, 0, 1]])
        self.apply_to_vertices(shearing_matrix)

    def reflection(self, type, last_point=None, m=None, b=None):
        match type:
            case ReflectionType.X_AXIS:
                reflection_matrix = np.matrix([[1, 0, 0], 
                                               [0, -1, 0], 
                                               [0, 0, 1]])
            case ReflectionType.Y_AXIS:
                reflection_matrix = np.matrix([[-1, 0, 0], 
                                               [0, 1, 0], 
                                               [0, 0, 1]])
            case ReflectionType.ORIGIN:
                # We can calculate the line's equation (y = mx + b)
                last_x, last_y = last_point
                dx = -last_x
                dy = -last_y
                if (last_x == 0):
                    reflection_matrix = np.matrix([[-1, 0, 0], 
                                               [0, 1, 0], 
                                               [0, 0, 1]])
                else:
                    m = dy / dx # b = 0
                    angle = np.arctan(m) # This gives us the angle between 
                    ## the line and the X axis
                    rotation_matrix = np.matrix([[np.cos(angle), -np.sin(angle) ,0], 
                                                [np.sin(angle), np.cos(angle), 0], 
                                                [0,0,1]])
                    actual_reflection_matrix = np.matrix([[1, 0, 0], 
                                                        [0, -1, 0], 
                                                        [0, 0, 1]])
                    inverse_rotation_matrix = np.matrix([[np.cos(angle), np.sin(angle) ,0], 
                                                [-np.sin(angle), np.cos(angle), 0], 
                                                [0,0,1]])
                    reflection_matrix = rotation_matrix @ actual_reflection_matrix @ inverse_rotation_matrix

            case ReflectionType.ANY_LINE:
                angle = np.arctan(m) # b means that the line crosses the X axis at (b,0)
                translation_matrix = np.matrix([[1, 0 ,0], 
                                                [0, 1, b], 
                                                [0,0,1]])
                rotation_matrix = np.matrix([[np.cos(angle), -np.sin(angle) ,0],
                                             [np.sin(angle), np.cos(angle), 0], 
                                             [0,0,1]])
                actual_reflection_matrix = np.matrix([[1, 0, 0], 
                                                      [0, -1, 0], 
                                                      [0, 0, 1]])
                inverse_rotation_matrix = np.matrix([[np.cos(angle), np.sin(angle) ,0], 
                                                     [-np.sin(angle), np.cos(angle), 0], 
                                                     [0,0,1]])
                inverse_translation_matrix = np.matrix([[1, 0 ,0], 
                                                        [0, 1, -b], 
                                                        [0,0,1]])
                reflection_matrix_half = translation_matrix @ rotation_matrix @ actual_reflection_matrix 
                reflection_matrix = reflection_matrix_half @ inverse_rotation_matrix @ inverse_translation_matrix
                
        self.apply_to_vertices(reflection_matrix)

    def redraw_on_canvas(self, canvas_state, color=None):
        """Redraw this shape (if it is not the canvas' default shape).
            Only used with shapes external to the canvas_state, not the
            shape stored within it."""
        if color is None:
            color = constants.DEFAULT_LINE_COLOR

        new_lines = []
        for v1, v2 in self.vertices:
            x1, y1 = v1.get_coords()
            x2, y2 = v2.get_coords()
            line = canvas_state.draw_line(x1, y1, x2, y2, color)
            new_lines.append(line)
            line.draw()
        self.drawn_lines = new_lines


