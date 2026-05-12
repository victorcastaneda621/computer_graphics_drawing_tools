"""ui_utils.py uses imgui to render the UI (the toolbar with its buttons, etc...)"""

import imgui
import pyglet
from pyglet import gl
from OpenGL.error import GLError

from constants import PANEL_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH

def draw_all(imgui_renderer, canvas_state, font):
    """Draws the toolbar with its UI elements, as well as the window itself."""
    # Start a new imgui frame
    imgui_renderer.refresh_font_texture()
    imgui.new_frame()
    imgui.push_font(font)

    # Position panel on the right side
    imgui.set_next_window_position(WINDOW_WIDTH - PANEL_WIDTH, 0)
    imgui.set_next_window_size(PANEL_WIDTH, WINDOW_HEIGHT)


    # Styles
    imgui.push_style_color(imgui.COLOR_BORDER, 1.0, 1.0, 1.0, 1.0)
    imgui.push_style_color(imgui.COLOR_WINDOW_BACKGROUND, 0.82, 0.82, 0.82, 1)
    imgui.push_style_color(imgui.COLOR_TEXT, 0.0, 0.0, 0.0, 1.0)
    imgui.push_style_color(imgui.COLOR_TAB, 0.7,0.75,0.7,1.0)
    imgui.push_style_color(imgui.COLOR_TAB_ACTIVE, 0.3,0.7,0.9,1.0)
    imgui.push_style_color(imgui.COLOR_TAB_HOVERED, 0.3,0.7,1.0,1.0)
    imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, 0.9, 0.9, 0.9, 1.0)
    imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND, 0.2,0.6,0.9,1.0)
    imgui.push_style_color(imgui.COLOR_TITLE_BACKGROUND_ACTIVE, 0.2,0.6,0.9,1.0)
    imgui.push_style_color(imgui.COLOR_POPUP_BACKGROUND, 0.9,0.9,0.9,1.0)
    imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, 0.85,0.85,0.85,1.0)
    imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_HOVERED, 0.9,0.9,0.9,1.0)
    imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_ACTIVE, 0.8,0.8,0.8,1.0)
    imgui.push_style_color(imgui.COLOR_BORDER, 0.0,0.0,0.0,1.0)

    # Create the panel
    imgui.begin(
        "Toolbar",
        flags=imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_COLLAPSE
    )

    imgui.begin_child("Controls", width=0, height=70, border=True)

    # Control buttons
    imgui.push_style_color(imgui.COLOR_BUTTON, 0.8,0.8,0,0.8)
    imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.9,0.9,0,1)
    imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.7,0.5,0)
    if imgui.button("Clear Canvas", width=120, height=40):
        canvas_state.clear_canvas()
    imgui.pop_style_color(3)
    imgui.set_cursor_pos((130, 17))
    imgui.same_line()
    if imgui.button("Export", width=110, height=40):
        imgui.open_popup("Export fractal as PNG")

    if imgui.begin_popup_modal("Export fractal as PNG", flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE)[0]:
        imgui.text("Enter filename (without extension):")
        changed_filename, canvas_state.export_filename = imgui.input_text(
            "##export_filename", canvas_state.export_filename, 256)
        imgui.dummy(0, 10)
        if imgui.button("Save", width=120, height=30):
            canvas_state.export_png(canvas_state.export_filename)
            imgui.close_current_popup()
        imgui.same_line()
        if imgui.button("Cancel", width=120, height=30):
            imgui.close_current_popup()
        imgui.end_popup()

    imgui.set_cursor_pos((240, 17))
    imgui.push_style_color(imgui.COLOR_BUTTON, 0.8, 0, 0, 0.8)
    imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 1, 0, 0)
    imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.7, 0, 0)
    imgui.same_line()
    if imgui.button("Exit App", width=100, height=40):
        pyglet.app.exit()
    imgui.pop_style_color(3)

    imgui.end_child()
    imgui.dummy(0, 5)

    if imgui.begin_tab_bar("MainTabBar"):

        if imgui.begin_tab_item("Recursive")[0]:

            imgui.begin_child("##RecursiveChild", width=358, height=245, border=True)
            title("RECURSIVE FRACTALS", 50)
            imgui.dummy(0, 5)
            imgui.text("(If 'animated?' is true, then click on the draw")
            imgui.text("button to advance one frame. In this mode,")
            imgui.text("don't clear the canvas manually)")
            imgui.dummy(0, 5)

            dropdown_entries = ["Sierpinsky Triangle",
                                "Koch Curve",
                                "Koch Snowflake",
                                "Cantor Set"]
            imgui.push_item_width(200)
            changed_recursive, current_recursive = imgui.combo("##recursive", 
                                        canvas_state.selected_recursive, 
                                        dropdown_entries)
            if changed_recursive:
                canvas_state.change_recursive(current_recursive)
            imgui.same_line()
            toggled, canvas_state.animated = imgui.checkbox(
            "##animated", canvas_state.animated)
            imgui.same_line()
            imgui.text("Animated?")

            imgui.dummy(0, 2)
            imgui.text("Number of Iterations:")
            imgui.same_line()
            imgui.push_item_width(120)
            changed_iters, new_iters = imgui.slider_int(
                "##iterations", canvas_state.recursive_iterations, 1, 20)
            imgui.pop_item_width()

            if changed_iters:
                canvas_state.recursive_iterations = new_iters

            imgui.dummy(0, 5)

            imgui.set_cursor_pos_x(60)
            imgui.push_style_color(imgui.COLOR_BUTTON, 0,0.8,0,0.8)
            imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0,0.9,0)
            imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0,0.5,0)
            if imgui.button("Draw Selected Recursive Fractal", width=250, height=40):
                canvas_state.draw_selected_recursive()
            imgui.pop_style_color(3)
            imgui.end_child()

            imgui.dummy(0, 5)
            imgui.begin_child("##RecursiveChildMax", width=358, height=163, border=True)
            title("RECOMMENDED MAXIMUM ITERATIONS", 50)
            imgui.dummy(0, 5)
            imgui.bullet_text("Sierpinsky Triangle: 10")
            imgui.bullet_text("Koch Curve: 10")
            imgui.bullet_text("Koch Snowflake: 9")
            imgui.bullet_text("Cantor Set: 17")
            imgui.end_child()

            imgui.end_tab_item()

        if imgui.begin_tab_item("Julia/Mandelbrot")[0]:
            imgui.begin_child("##jmcolor", width=358, height=77, border=True)
            imgui.dummy(0, 5)
            title("JULIA / MANDELBROT STYLE", 50)

            dropdown_entries = ["Grayscale",
                                "Orange/White/Green",
                                "Yellow/Blue/Green",
                                "Pink/Green"]
            imgui.push_item_width(200)
            changed_julia_color, current_julia_color = imgui.combo("##jmc", 
                                        canvas_state.julia_color, 
                                        dropdown_entries)
            if changed_julia_color:
                canvas_state.change_julia_style(current_julia_color)
            imgui.end_child()

            julia_child(canvas_state, 50)

            imgui.begin_child("##mandelbrot", width=358, height=97, border=True)
            imgui.dummy(0, 5)
            title("MANDELBROT SET", 50)
            imgui.dummy(0, 2)
            imgui.set_cursor_pos_x(60)
            imgui.push_style_color(imgui.COLOR_BUTTON, 0,0.8,0,0.8)
            imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0,0.9,0)
            imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0,0.5,0)
            if imgui.button("Draw Mandelbrot Set", width=250, height=40):
                canvas_state.draw_mandelbrot()
            imgui.pop_style_color(3)
            imgui.end_child()

            imgui.end_tab_item()
        
        if imgui.begin_tab_item("  IFS  ")[0]:
            imgui.begin_child("##IFSChild", width=358, height=165, border=True)
            title("IFS", 50)
            imgui.dummy(0, 5)

            dropdown_entries_ifs = ["Sierpinsky Triangle",
                                "Koch Curve",
                                "Koch 2",
                                "Cantor Set",
                                "Barnsley's Fern",
                                "Christmas Tree",
                                "Blocks",
                                "Cloud",
                                "Leaf",
                                "Noisy",
                                "Chaos"]
            imgui.push_item_width(200)
            changed_ifs, current_ifs = imgui.combo("##ifs_combo", 
                                        canvas_state.selected_ifs, 
                                        dropdown_entries_ifs)
            if changed_ifs:
                canvas_state.change_ifs(current_ifs)

            imgui.dummy(0, 2)
            imgui.text("Number of Points:")
            imgui.same_line()
            imgui.push_item_width(120)
            changed_iters_ifs, new_iters_ifs = imgui.slider_int(
                "##ifs_iter", canvas_state.ifs_iterations, 1, 600000)
            imgui.pop_item_width()

            if changed_iters_ifs:
                canvas_state.ifs_iterations = new_iters_ifs

            imgui.dummy(0, 5)

            imgui.set_cursor_pos_x(60)
            imgui.push_style_color(imgui.COLOR_BUTTON, 0,0.8,0,0.8)
            imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0,0.9,0)
            imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0,0.5,0)
            if imgui.button("Draw Selected IFS", width=250, height=40):
                canvas_state.draw_selected_ifs()
            imgui.pop_style_color(3)
            imgui.end_child()

            imgui.end_tab_item()

        imgui.end_tab_bar()
    imgui.pop_style_color(14)
    imgui.end()

    # Render imgui
    imgui.pop_font()
    imgui.render()
    try:
        imgui_renderer.render(imgui.get_draw_data())
    except GLError as e:
        print("OpenGL render error ignored:", e)

def julia_child(canvas_state, input_width):
    imgui.begin_child("##JuliaInput", width=358, height=165, border=True)

    title("JULIA SETS", input_width)
    imgui.dummy(0, 0.5)

    imgui.text("Input the complex number C = a + bi, to ")
    imgui.text("generate the Julia set:")
    imgui.text("a:")
    imgui.same_line()
    imgui.push_item_width(2*input_width)
    changed_a, new_a = imgui.input_float("##juliaa", canvas_state.julia_a, step=0, step_fast=0, format="%.6f")
    imgui.pop_item_width()
    imgui.same_line()
    imgui.text("b:")
    imgui.same_line()
    imgui.push_item_width(2*input_width)
    changed_b, new_b = imgui.input_float("##juliab", canvas_state.julia_b, step=0, step_fast=0, format="%.6f")
    imgui.pop_item_width()

    if changed_a:
        canvas_state.julia_a = new_a
    if changed_b:
        canvas_state.julia_b = new_b

    imgui.dummy(0, 2)
    imgui.set_cursor_pos_x(60)
    imgui.push_style_color(imgui.COLOR_BUTTON, 0,0.8,0,0.8)
    imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0,0.9,0)
    imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0,0.5,0)
    if imgui.button("Draw Julia Set For C", width=250, height=40):
        canvas_state.draw_julia()
    imgui.pop_style_color(3)
    imgui.end_child()
    imgui.dummy(0, 5)
    imgui.begin_child("##JuliaInputPresets", width=358, height=200, border=True)
    title("PRESETS", input_width)
    imgui.text("The following are some values that generate a ")
    imgui.text("visible Julia set.")
    
    if imgui.button(f"0.34 - 0.05i", width=100, height=25):
        canvas_state.julia_a = 0.34
        canvas_state.julia_b = -0.05
    if imgui.is_item_hovered():
        imgui.begin_tooltip()
        imgui.text("Spiral")
        imgui.end_tooltip()

    imgui.same_line()
    if imgui.button(f"-1.5 + 0.2i", width=100, height=25):
        canvas_state.julia_a = -1.5
        canvas_state.julia_b = 0.
    if imgui.is_item_hovered():
        imgui.begin_tooltip()
        imgui.text("Symmetry")
        imgui.end_tooltip()

    imgui.same_line()
    if imgui.button(f"-0.54 + 0.54i", width=100, height=25):
        canvas_state.julia_a = -0.54
        canvas_state.julia_b = 0.54
    if imgui.is_item_hovered():
        imgui.begin_tooltip()
        imgui.text("Dragon Spirals")
        imgui.end_tooltip()

    if imgui.button(f"-1.476 - 0i", width=90, height=25):
            canvas_state.julia_a = -1.476
            canvas_state.julia_b = -0.0
    if imgui.is_item_hovered():
        imgui.begin_tooltip()
        imgui.text("Antenna")
        imgui.end_tooltip()

    imgui.same_line()
    if imgui.button(f"0 + 0.8i", width=70, height=25):
        canvas_state.julia_a = 0.0
        canvas_state.julia_b = 0.8
    if imgui.is_item_hovered():
        imgui.begin_tooltip()
        imgui.text("Veins")
        imgui.end_tooltip()

    imgui.same_line()
    if imgui.button(f"-2 + 0i", width=60, height=25):
            canvas_state.julia_a = -2
            canvas_state.julia_b = -0.0
    if imgui.is_item_hovered():
        imgui.begin_tooltip()
        imgui.text("Line")
        imgui.end_tooltip()

    imgui.same_line()
    if imgui.button(f"-0.75 + 0.1i", width=100, height=25):
        canvas_state.julia_a = -0.75
        canvas_state.julia_b = 0.1
    if imgui.is_item_hovered():
        imgui.begin_tooltip()
        imgui.text("Orbits")
        imgui.end_tooltip()

    if imgui.button(f"0.355534 - 0.337292i", width=190, height=25):
        canvas_state.julia_a = 0.355534
        canvas_state.julia_b = -0.337292
    if imgui.is_item_hovered():
        imgui.begin_tooltip()
        imgui.text("Fjords")
        imgui.end_tooltip()
    
    imgui.same_line()
    if imgui.button(f"0.285 + 0.01i", width=120, height=25):
        canvas_state.julia_a = 0.285
        canvas_state.julia_b = 0.01
    if imgui.is_item_hovered():
        imgui.begin_tooltip()
        imgui.text("Flower")
        imgui.end_tooltip()

    if imgui.button(f"0.38 - 0.234i", width=120, height=25):
        canvas_state.julia_a = 0.38
        canvas_state.julia_b = 0.234
    if imgui.is_item_hovered():
        imgui.begin_tooltip()
        imgui.text("Galaxies")
        imgui.end_tooltip()

    imgui.same_line()
    if imgui.button(f"0.185719 - 0.588005i", width=180, height=25):
            canvas_state.julia_a = 0.185719
            canvas_state.julia_b = -0.588005
    if imgui.is_item_hovered():
        imgui.begin_tooltip()
        imgui.text("Molecule")
        imgui.end_tooltip()


    imgui.end_child()

def set_up_window():
    """Sets up the Pyglet window, so the canvas can be used."""
    # Create the Pyglet window
    window = pyglet.window.Window(width=WINDOW_WIDTH, 
                                height=WINDOW_HEIGHT, 
                                caption="3. Fractals")
    window.set_location(x=100, y=100)

    # Set the background color to white
    gl.glClearColor(1, 1, 1, 1)

    # Create imgui context
    imgui.create_context()
    return window

# Color helper functions
def percentage_to_rgb_color(color):
    r,g,b,a = color
    return (int(r * 255), int(g * 255), int(b * 255), int(a * 255))

def rgb_to_percentage_color(color):
    r,g,b,a = color
    return (r / 255,g / 255,b / 255,a / 255)

def title(title, input_width):
    window_width = imgui.get_window_width()
    text_width = imgui.calc_text_size(title)[0]
    imgui.set_cursor_pos_x((window_width - text_width) * 0.5)

    imgui.push_item_width(input_width)
    imgui.text(title)
    imgui.push_style_color(imgui.COLOR_SEPARATOR, 0.0, 0.0, 0.0, 1.0)
    imgui.separator()
    imgui.pop_style_color()