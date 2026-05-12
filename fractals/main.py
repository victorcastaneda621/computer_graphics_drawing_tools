import pyglet
import imgui
import imgui.integrations.pyglet as igp
import os

from ui_utils import draw_all, set_up_window
from canvas import CanvasState
from basic_geometry.pixel_coordinates import screen_to_canvas_coordinates

# Create and set up the pyglet window, imgui context and renderer
window = set_up_window()
imgui_renderer = igp.PygletProgrammablePipelineRenderer(window)
window.push_handlers(imgui_renderer)

# Load the Arial font
script_dir = os.path.dirname(__file__)
font_path = os.path.join(script_dir, "..", "arial.ttf")
font_path = os.path.normpath(font_path)

io = imgui.get_io()
arial_font = io.fonts.add_font_from_file_ttf(font_path, 18)
if arial_font is None:
    raise RuntimeError("Failed to load Arial font!")
imgui_renderer.refresh_font_texture()

# Create a CanvasState to keep track of elements drawn
canvas_state = CanvasState()

# Prevent the UI integer inputs from doubling the value of the previous frame
@window.event
def on_text(text):
    imgui_renderer.on_text(text)
    return True

# Track what coordinates the user is hovering over
@window.event
def on_mouse_motion(x, y, dx, dy):
    io = imgui.get_io()
    if not io.want_capture_mouse:
        x,y  = screen_to_canvas_coordinates(x, y)
        canvas_state.set_hover_coords(x, y)

# Main drawing loop
@window.event
def on_draw():
    window.clear()
    if canvas_state.needs_redraw:
        # Draw fractals
        for fractal in canvas_state.fractals:
            fractal.draw(canvas_state.batch)
        canvas_state.needs_redraw = False
    canvas_state.batch.draw()

    # Draw the toolbar and canvas (using imgui)
    draw_all(imgui_renderer, canvas_state, arial_font)
pyglet.app.run()