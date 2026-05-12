"""canvas.py contains a class to save information about the current state of the canvas."""
import pyglet
import os

from constants import *
from fractal import Fractal, PointFractal, RECURSIVE, IFS, get_ifs_functions
import fractal_types.recursive as recursive
import fractal_types.julia as julia
import fractal_types.ifs as ifs
import fractal_types.mandelbrot as mandelbrot
from basic_geometry.pixel_coordinates import Pixel

class CanvasState:
    """Singleton class that stores the current canvas state."""

    needs_redraw = True
    batch = None

    # List of fractals
    fractals = list()

    # Currently selected recursive fractal
    selected_recursive = RECURSIVE.SIERPINSKY_TRIANGLE
    recursive_iterations = 1
    animated = False
    animated_frame = 1

    # Julia sets parameters
    julia_a = 0.0
    julia_b = 0.0
    julia_color = julia.JuliaStyle.GRAYSCALE
    export_filename = "fractal"

    # Currently selected IFS
    selected_ifs = IFS.SIERPINSKY_TRIANGLE
    ifs_iterations = 1

    # Color of the next line's pixels
    color = DEFAULT_COLOR

    hover_coords = (0,0)

    def __init__(self):
        self.batch = pyglet.graphics.Batch()

    def set_hover_coords(self,x,y):
        """Changes the value of hover_coords."""
        self.hover_coords = (x,y)

    def get_hover_coords(self):
        """Returns the coordinates the mouse is currently hovering over."""
        return self.hover_coords

    def clear_canvas(self):
        """Erases everything that has been drawn on the canvas."""
        self.fractals.clear()
        self.needs_redraw = True

    # Getter and setter for the color of the next line to draw
    def get_color(self): return self.color
    def set_color(self, new_color): self.color = new_color

    def change_recursive(self, new_recursive):
        if new_recursive in RECURSIVE.all():
            self.selected_recursive = new_recursive
            self.animated_frame = 1
        else:
            raise Exception("Tried to draw invalid Recursive Fractal:", new_recursive)
        
    def draw_selected_recursive(self):
        if not self.animated:
            self.animated_frame = 1
            self.clear_canvas()
            match self.selected_recursive:
                case RECURSIVE.SIERPINSKY_TRIANGLE:
                    new_lines = recursive.sierpinsky_triangle(Pixel(-500,-200), Pixel(500,-200), Pixel(0,300), self.recursive_iterations)
                case RECURSIVE.KOCH_CURVE:
                    new_lines = recursive.koch_curve(Pixel(-500,-200), Pixel(500,-200), self.recursive_iterations)
                case RECURSIVE.KOCH_SNOWFLAKE:
                    new_lines = recursive.koch_snowflake(Pixel(-300,-150), Pixel(0,370), Pixel(300,-150), self.recursive_iterations)
                case RECURSIVE.CANTOR_SET:
                    new_lines = recursive.cantor_set(Pixel(-500,340), Pixel(500,340), self.recursive_iterations)
            self.fractals.append(Fractal(new_lines))
            self.needs_redraw = True
        else:
            append = True
            if self.animated_frame == self.recursive_iterations + 1:
                self.animated_frame = 1
                self.needs_redraw = False
                append = False
                self.clear_canvas()

            match self.selected_recursive:
                case RECURSIVE.SIERPINSKY_TRIANGLE:
                    new_lines = recursive.sierpinsky_triangle(Pixel(-500,-200), Pixel(500,-200), Pixel(0,300), self.animated_frame)
                case RECURSIVE.KOCH_CURVE:
                    new_lines = recursive.koch_curve(Pixel(-500,-200), Pixel(500,-200), self.animated_frame)
                case RECURSIVE.KOCH_SNOWFLAKE:
                    new_lines = recursive.koch_snowflake(Pixel(-300,-150), Pixel(0,370), Pixel(300,-150), self.animated_frame)
                case RECURSIVE.CANTOR_SET:
                    new_lines = recursive.cantor_set(Pixel(-500,340), Pixel(500,340), self.animated_frame)
            if append:
                self.clear_canvas()
                self.fractals.append(Fractal(new_lines))
                self.needs_redraw = True
                self.animated_frame += 1

    def change_julia_style(self, new_style):
        if new_style in julia.JuliaStyle.all():
            self.julia_color = new_style
        else:
            raise Exception("Tried to draw invalid Recursive Fractal:", new_style)

    def draw_julia(self):
        self.clear_canvas()
        new_points = julia.calculate_julia(complex(self.julia_a, self.julia_b), 100, self.julia_color)
        self.fractals.append(PointFractal(new_points))
        self.needs_redraw = True

    def draw_mandelbrot(self):
        self.clear_canvas()
        new_points = mandelbrot.calculate_mandelbrot(100, self.julia_color)
        self.fractals.append(PointFractal(new_points))
        self.needs_redraw = True
    
    def change_ifs(self, new_ifs):
        if new_ifs in IFS.all():
            self.selected_ifs = new_ifs
        else:
            raise Exception("Tried to draw invalid IFS:", new_ifs)
        
    def draw_selected_ifs(self):
        self.clear_canvas()
        match self.selected_ifs:
            case IFS.SIERPINSKY_TRIANGLE:
                functions = get_ifs_functions(IFS.SIERPINSKY_TRIANGLE)
                new_points = ifs.draw_ifs(functions, Pixel(0, 0), self.ifs_iterations)
            case IFS.KOCH_CURVE:
                functions = get_ifs_functions(IFS.KOCH_CURVE)
                n_points = ifs.draw_ifs(functions, Pixel(0, 0), self.ifs_iterations)
                new_points = []
                for p in n_points:
                    px, py = p.get_coords()
                    px -= 350
                    new_points.append(Pixel(px, py))
            case IFS.KOCH_2:
                functions = get_ifs_functions(IFS.KOCH_2)
                n_points = ifs.draw_ifs(functions, Pixel(0, 0), self.ifs_iterations)
                new_points = []
                for p in n_points:
                    px, py = p.get_coords()
                    py -= 350
                    new_points.append(Pixel(px, py))
            case IFS.CANTOR_SET:
                functions = get_ifs_functions(IFS.CANTOR_SET)
                new_points = ifs.draw_ifs(functions, Pixel(0, 0), self.ifs_iterations)
            case IFS.BARNSLEY_FERN:
                functions = get_ifs_functions(IFS.BARNSLEY_FERN)
                n_points = ifs.draw_ifs(functions, Pixel(0, 0), self.ifs_iterations, 0.3, True)
                new_points = []
                for p in n_points:
                    px, py = p.get_coords()
                    py -= 350
                    px -= 100
                    new_points.append(Pixel(px, py))
            case IFS.CHRISTMAS_TREE:
                functions = get_ifs_functions(IFS.CHRISTMAS_TREE)
                n_points = ifs.draw_ifs(functions, Pixel(0, 0), self.ifs_iterations)
                new_points = []
                for p in n_points:
                    px, py = p.get_coords()
                    px -= 200
                    py -= 350
                    new_points.append(Pixel(px, py))
            case IFS.BLOCKS:
                functions = get_ifs_functions(IFS.BLOCKS)
                n_points = ifs.draw_ifs(functions, Pixel(0, 0), self.ifs_iterations)
                new_points = []
                for p in n_points:
                    px, py = p.get_coords()
                    px -= 300
                    py -= 350
                    new_points.append(Pixel(px, py))
            case IFS.CLOUD:
                functions = get_ifs_functions(IFS.CLOUD)
                n_points = ifs.draw_ifs(functions, Pixel(0, 0), self.ifs_iterations)
                new_points = []
                for p in n_points:
                    px, py = p.get_coords()
                    py -= 150
                    new_points.append(Pixel(px, py))
            case IFS.NOISY:
                functions = get_ifs_functions(IFS.NOISY)
                n_points = ifs.draw_ifs(functions, Pixel(0, 0), self.ifs_iterations)
                new_points = []
                for p in n_points:
                    px, py = p.get_coords()
                    py -= 300
                    new_points.append(Pixel(px, py))
            case IFS.LEAF:
                functions = get_ifs_functions(IFS.LEAF)
                n_points = ifs.draw_ifs(functions, Pixel(0, 0), self.ifs_iterations, 0.7)
                new_points = []
                for p in n_points:
                    px, py = p.get_coords()
                    py -= 370
                    new_points.append(Pixel(px, py))
            
            case IFS.CHAOS:
                functions = get_ifs_functions(IFS.CHAOS)
                new_points = ifs.draw_ifs(functions, Pixel(0, 0), self.ifs_iterations)
                


        self.fractals.append(PointFractal(new_points))
        self.needs_redraw = True

    def export_png(self, filename):
        buffer = pyglet.image.get_buffer_manager().get_color_buffer()
        region = buffer.get_region(0, 0, 2*CANVAS_WIDTH, 2*CANVAS_HEIGHT)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        export_dir = os.path.join(base_dir, "exported")

        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        region.save(os.path.join(export_dir, filename + ".png"))
