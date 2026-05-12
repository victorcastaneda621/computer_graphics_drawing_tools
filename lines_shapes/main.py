import pyglet
import imgui
import imgui.integrations.pyglet as igp
import os

from ui_utils import draw_toolbar_and_window, set_up_window
from pixel_coordinates import draw_axes, screen_to_canvas_coordinates, draw_grid
from canvas import CanvasState
import animation

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

# Receive coordinates from clicking with the mouse
@window.event
def on_mouse_press(x, y, button, modifiers):
    io = imgui.get_io() # Allows us to know if the click is on the canvas or on the imgui UI
    if not io.want_capture_mouse and button == pyglet.window.mouse.LEFT:
            x, y = screen_to_canvas_coordinates(x, y)
            canvas_state.click_add_point_to_buffer(x, y)

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
    # Draw Pyglet elements
    if canvas_state.run_animation:
        if animation.run_animation(window, canvas_state) == False:
             canvas_state.run_animation = False
    else:
        if canvas_state.show_axes:
            draw_axes() # Shows the X and Y 
        if canvas_state.show_grid:
            draw_grid()
        for line in canvas_state.lines:
            line.draw()
        if canvas_state.reflection_line:
            canvas_state.reflection_line.draw()


    # Draw the toolbar and canvas (using imgui)
    draw_toolbar_and_window(imgui_renderer, canvas_state, arial_font)

pyglet.app.run()