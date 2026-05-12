"""ui_utils.py uses imgui to render the UI (the toolbar with its buttons, etc...)"""

import imgui
import pyglet
from pyglet import gl

from constants import PANEL_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH
from transformations_2d import ReflectionType

def draw_toolbar_and_window(imgui_renderer, canvas_state, font):
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

    # Whether to show the axes
    imgui.set_cursor_pos_x(10)
    _, canvas_state.show_axes = imgui.checkbox("Show/Hide Axes", canvas_state.show_axes)

    # Whether to show the grid
    imgui.set_cursor_pos_x(10)
    _, canvas_state.show_grid = imgui.checkbox("Show/Hide Grid", canvas_state.show_grid)

    # Button to exit the application
    imgui.set_cursor_pos((240, 17))
    imgui.push_style_color(imgui.COLOR_BUTTON, 0.8, 0, 0, 0.8)
    imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 1, 0, 0)
    imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.7, 0, 0)
    if imgui.button("Exit App", width=110, height=40):
        pyglet.app.exit()
    imgui.pop_style_color(3)

    imgui.end_child()
    imgui.dummy(0, 5)

    # Boxes to show the current coordinates the mouse is hovering over
    imgui.begin_child("Mouse Coordinates", width=0, height=35, border=True)
    x, y = canvas_state.get_hover_coords()
    imgui.text(f"Mouse Coordinates X: {x}, Y: {y}")
    imgui.end_child()
    imgui.dummy(0, 5)

    if imgui.begin_tab_bar("MainTabBar"):

        if imgui.begin_tab_item("Line Drawing")[0]:

            # Integer input to select start and end points for the line (can also be done clicking on the canvas)
            imgui.begin_child("Draw Lines", width=0, height=245, border=True)
            draw_start_end_points_input(canvas_state)

            # Dropdown to select line algorithm
            imgui.text("Line Algorithm:")
            imgui.same_line()
            imgui.push_item_width(228)
            imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - 3)
            dropdown_entries = ["Slope Intercept",
                                "DDA", 
                                "Bresenham's (Integers)",
                                "Bresenham's (Floats)"]
            changed, current = imgui.combo("##algorithm", 
                                        canvas_state.selected_line_drawing_algorithm, 
                                        dropdown_entries)
            imgui.pop_item_width()
            if changed:
                canvas_state.change_algorithm(current)
            imgui.dummy(0, 5)

            # Select line color
            imgui.text("Select Color:")
            imgui.same_line()
            color_changed, new_color = imgui.color_edit4("##color", 
                                                        *rgb_to_percentage_color(canvas_state.get_color()), 
                                                        flags=imgui.COLOR_EDIT_NO_INPUTS)
            if color_changed:
                # Convert from percentages to RGBA (0-255)
                new_color = percentage_to_rgb_color(new_color)
                canvas_state.set_color(new_color)

            # Select line style
            imgui.same_line()
            imgui.set_cursor_pos_x(imgui.get_cursor_pos_x() + 17)
            imgui.text("Style:")
            imgui.same_line()
            imgui.push_item_width(145)
            imgui.set_cursor_pos_y(imgui.get_cursor_pos_y() - 3)
            dropdown_styles = ["Solid",
                                "Dotted",
                                "Dashed"]
            changed_style, current_style = imgui.combo("##style", 
                                        canvas_state.selected_line_style, 
                                        dropdown_styles)
            imgui.pop_item_width()
            if changed_style:
                canvas_state.change_style(current_style)
            imgui.dummy(0, 5)

            # Button to draw the currently specified line
            imgui.set_cursor_pos_x(60)
            imgui.push_style_color(imgui.COLOR_BUTTON, 0,0.8,0,0.8)
            imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0,0.9,0)
            imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0,0.5,0)
            if imgui.button("Draw Line", width=120, height=40):
                canvas_state.draw_buffered_line()
            imgui.pop_style_color(3)
            imgui.same_line()

            # Button to clear the canvas
            imgui.push_style_color(imgui.COLOR_BUTTON, 0.8,0.8,0,0.8)
            imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.9,0.9,0,1)
            imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.7,0.5,0)
            if imgui.button("Clear Canvas", width=120, height=40):
                canvas_state.clear_canvas()
            imgui.pop_style_color(3)

            imgui.end_child()

            # Button to show or hide the list of activated pixels of the last line
            imgui.dummy(0, 5)
            _, canvas_state.show_last_line_points = imgui.checkbox("Show/Hide List of Activated Pixels (Last Line)", 
                                                                                    canvas_state.show_last_line_points)
            imgui.dummy(0, 5)

            # Dinamically-sized area to show the line's points
            if canvas_state.show_last_line_points:
                lines = canvas_state.get_lines()
                if len(lines) != 0:
                    pixels = lines[-1].get_pixels()
                    chunk_size = 4 # How many points to show per line
                    imgui.begin_child("last_line_points", width=0, height=300, border=False)
                    line_str = ", ".join(str(pixel.get_coords()) for pixel in pixels)
                    for i in range(0, len(pixels), chunk_size):
                        line_str = ", ".join(str(p.get_coords()) for p in pixels[i:i+chunk_size])
                        imgui.text(line_str)
                        imgui.dummy(0, 5)
                    imgui.end_child()

            imgui.end_tab_item()
        if imgui.begin_tab_item("2D Transformations")[0]:
            translation_child(canvas_state, 50)
            imgui.same_line()
            rotation_child(canvas_state, 50)
            sclaing_child(canvas_state, 50)
            imgui.same_line()
            shearing_child(canvas_state, 50)
            reflection_child(canvas_state, 50)
            imgui.dummy(0,2)
            imgui.push_style_color(imgui.COLOR_BUTTON, 0.8,0.8,0,0.8)
            imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.9,0.9,0,1.0)
            imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.7,0.5,0,1.0)
            if imgui.button("Undo Last (Permanent)", width=180, height=40):
                canvas_state.undo_last()
            imgui.pop_style_color(3)
            imgui.same_line()
            imgui.push_style_color(imgui.COLOR_BUTTON, 0,0.7,0.1,0.4)
            imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0,0.8,0.2,0.6)
            imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0,0.6,0,1)
            if imgui.button(" |> Play Animation", width=170, height=40):
                canvas_state.run_animation = True
            imgui.pop_style_color(3)
            imgui.end_tab_item()
    imgui.end_tab_bar()
    imgui.pop_style_color(14)
    imgui.pop_font()
    imgui.end()

    # Render imgui
    imgui.render()
    imgui_renderer.render(imgui.get_draw_data())

def title(title, input_width):

    window_width = imgui.get_window_width()
    text_width = imgui.calc_text_size(title)[0]
    imgui.set_cursor_pos_x((window_width - text_width) * 0.5)

    imgui.push_item_width(input_width)
    imgui.text(title)
    imgui.push_style_color(imgui.COLOR_SEPARATOR, 0.0, 0.0, 0.0, 1.0)
    imgui.separator()
    imgui.pop_style_color()

def translation_child(canvas_state, input_width):
    # Translation
    imgui.begin_child("##Translation", width=155, height=137, border=True)

    title("TRANSLATION", input_width)
    imgui.dummy(0,0.5)

    # x value
    imgui.text("x_delta:")
    imgui.same_line()

    # x input
    imgui.push_item_width(input_width)
    changed_translation_x, new_translation_x = imgui.input_int(
        "##translation_x", canvas_state.get_translation_x(), step=0, step_fast=0
    )

    # y value
    imgui.text("y_delta:")
    imgui.same_line()

    # y input
    imgui.push_item_width(input_width)
    changed_translation_y, new_translation_y = imgui.input_int(
        "##translation_y", canvas_state.get_translation_y(), step=0, step_fast=0
    )

    if changed_translation_x:
        canvas_state.set_translation_x(new_translation_x)
    if changed_translation_y:
        canvas_state.set_translation_y(new_translation_y)

    imgui.dummy(0,0.5)
    imgui.set_cursor_pos_x(17)
    if imgui.button("Apply", width=120, height=30):
        canvas_state.apply_translation()
    imgui.end_child()

def rotation_child(canvas_state, input_width):
    # Translation
    imgui.begin_child("##Rotation", width=195, height=137, border=True)

    title("ROTATION", input_width)
    imgui.dummy(0,0.5)

    # alpha (angle)
    imgui.text("Angle:")
    imgui.same_line()
    imgui.push_item_width(input_width)
    changed_alpha, new_alpha = imgui.input_float(
        "##alpha", canvas_state.get_rotation_alpha(), step=0, step_fast=0, format="%.2f"
    )

    # Clockwise or counter-clockwise
    imgui.text("Counter-clockwise?")
    imgui.same_line()
    imgui.push_item_width(input_width)
    _, canvas_state.rotation_is_counter_clockwise  = imgui.checkbox(
        "##CC", canvas_state.rotation_is_counter_clockwise)

    if changed_alpha:
        canvas_state.set_rotation_alpha(new_alpha)

    imgui.dummy(0,1)
    imgui.set_cursor_pos_x(37)
    if imgui.button("Apply", width=120, height=30):
        canvas_state.apply_rotation()
    imgui.end_child()

def sclaing_child(canvas_state, input_width):
    # Translation
    imgui.begin_child("##Scaling", width=155, height=137, border=True)

    title("SCALING", input_width)
    imgui.dummy(0,0.5)

    # x value
    imgui.text("x_scale:")
    imgui.same_line()

    # x input
    imgui.push_item_width(input_width)
    changed_scaling_x, new_scaling_x = imgui.input_float(
        "##scaling_x", canvas_state.get_scaling_x(), step=0, step_fast=0, format="%.2f"
    )

    # y value
    imgui.text("y_scale:")
    imgui.same_line()

    # y input
    imgui.push_item_width(input_width)
    changed_scaling_y, new_scaling_y = imgui.input_float(
        "##scaling_y", canvas_state.get_scaling_y(), step=0, step_fast=0, format="%.2f"
    )

    if changed_scaling_x:
        canvas_state.set_scaling_x(new_scaling_x)
    if changed_scaling_y:
        canvas_state.set_scaling_y(new_scaling_y)

    imgui.dummy(0,0.5)
    imgui.set_cursor_pos_x(17)
    if imgui.button("Apply", width=120, height=30):
        canvas_state.apply_scaling()
    imgui.end_child()    

def shearing_child(canvas_state, input_width):
    # Translation
    imgui.begin_child("##Shearing", width=195, height=137, border=True)

    title("SHEARING", input_width)
    imgui.dummy(0,0.5)

    # x value
    imgui.text("Shearing in X:")
    imgui.same_line()

    # x input
    imgui.push_item_width(input_width)
    changed_shearing_x, new_shearing_x = imgui.input_float(
        "##shear_x", canvas_state.get_shear_x(), step=0, step_fast=0, format="%.2f"
    )

    # y value
    imgui.text("Shearing in Y:")
    imgui.same_line()

    # y input
    imgui.push_item_width(input_width)
    changed_shearing_y, new_shearing_y = imgui.input_float(
        "##shear_y", canvas_state.get_shear_y(), step=0, step_fast=0, format="%.2f"
    )

    if changed_shearing_x:
        canvas_state.set_shear_x(new_shearing_x)
    if changed_shearing_y:
        canvas_state.set_shear_y(new_shearing_y)

    imgui.dummy(0,0.5)
    imgui.set_cursor_pos_x(37)
    if imgui.button("Apply", width=120, height=30):
        canvas_state.apply_shearing()
    imgui.end_child()

def reflection_child(canvas_state, input_width):
    # Translation
    imgui.begin_child("##Reflection", width=358, height=267, border=True)

    title("REFLECTION", input_width)
    imgui.dummy(0,0.5)

    current_type = canvas_state.get_reflection_type()

    if imgui.radio_button("X Axis", current_type == ReflectionType.X_AXIS):
        canvas_state.set_reflection_type(ReflectionType.X_AXIS)
        canvas_state.clear_reflection_line()

    if imgui.radio_button("Y Axis", current_type == ReflectionType.Y_AXIS):
        canvas_state.set_reflection_type(ReflectionType.Y_AXIS)
        canvas_state.clear_reflection_line()

    if imgui.radio_button("Origin", current_type == ReflectionType.ORIGIN):
        canvas_state.set_reflection_type(ReflectionType.ORIGIN)

    if current_type == ReflectionType.ORIGIN:
        imgui.set_cursor_pos_x(38)
        imgui.text("Enter a point (x,y) through which the line")
        imgui.set_cursor_pos_x(38)
        imgui.text("passes, other than (0,0):")
        imgui.set_cursor_pos_x(58)
        imgui.text("(x,y):")
        imgui.same_line()
        changed_refl_line_x, new_refl_line_x = imgui.input_int("##reflect_x", 
                                                canvas_state.get_reflection_last_point()[0], 
                                                step=0, step_fast=0)
        imgui.same_line()
        changed_refl_line_y, new_refl_line_y = imgui.input_int("##reflect_y", 
                                                canvas_state.get_reflection_last_point()[1], 
                                                step=0, step_fast=0)
        if changed_refl_line_x or changed_refl_line_y:
            canvas_state.set_reflection_last_point((new_refl_line_x, new_refl_line_y))
            canvas_state.draw_reflection_line()

    if imgui.radio_button("Any Line", current_type == ReflectionType.ANY_LINE):
        canvas_state.set_reflection_type(ReflectionType.ANY_LINE)
        canvas_state.clear_reflection_line()

    if current_type == ReflectionType.ANY_LINE:
        imgui.set_cursor_pos_x(38)
        imgui.text("Enter the parameters that describe the")
        imgui.set_cursor_pos_x(38)
        imgui.text("desired reflection line (y = mx + b):")
        imgui.set_cursor_pos_x(58)
        imgui.text("m:")
        imgui.same_line()
        changed_refl_m, new_refl_m = imgui.input_float("##reflect_m", 
                                                canvas_state.get_reflection_m(), 
                                                step=0, step_fast=0, format="%.2f")
        imgui.set_cursor_pos_x(58)
        imgui.same_line()
        imgui.text("b:")
        imgui.same_line()
        changed_refl_b, new_refl_b = imgui.input_int("##reflect_b", 
                                                canvas_state.get_reflection_b(), 
                                                step=0, step_fast=0)
        if changed_refl_m:
            canvas_state.set_reflection_m(new_refl_m)
            canvas_state.draw_reflection_line()
        if changed_refl_b:
            canvas_state.set_reflection_b(new_refl_b)
            canvas_state.draw_reflection_line()

    imgui.dummy(0,0.5)
    imgui.set_cursor_pos_x(78)
    if imgui.button("Apply", width=175, height=30):
        canvas_state.apply_reflection(current_type, 
                                      canvas_state.get_reflection_last_point(),
                                      canvas_state.get_reflection_m(),
                                      canvas_state.get_reflection_b())
        canvas_state.clear_reflection_line()
    imgui.end_child()

def draw_start_end_points_input(canvas_state):
    """Function used locally to draw the four input boxes where the user 
        (as an alternative to clicking on the canvas) can select the start 
        and end point for a line. 
    """
    
    imgui.text("Click on the canvas or type the line's start/end")
    imgui.text("coordinates below:")
    imgui.dummy(0, 5)
    
    imgui.columns(4, "coords", border=False)

    # x_start label
    imgui.text("x_start:")
    imgui.next_column()

    # x_start input
    imgui.push_item_width(-1)
    changed_x_start, new_x_start = imgui.input_int(
        "##x_start", canvas_state.get_buffered_x_start(), step=0, step_fast=0
    )
    imgui.pop_item_width()
    imgui.next_column()

    # y_start label
    imgui.text("y_start:")
    imgui.next_column()

    # y_start input
    imgui.push_item_width(-1)
    changed_y_start, new_y_start = imgui.input_int(
        "##y_start", canvas_state.get_buffered_y_start(), step=0, step_fast=0
    )
    imgui.pop_item_width()
    imgui.next_column()

    # The other row (end)
    imgui.text("x_end:")
    imgui.next_column()
    imgui.push_item_width(-1)
    changed_x_end, new_x_end = imgui.input_int(
        "##x_end", canvas_state.get_buffered_x_end(), step=0, step_fast=0
    )
    imgui.pop_item_width()
    imgui.next_column()

    imgui.text("y_end:")
    imgui.next_column()
    imgui.push_item_width(-1)
    changed_y_end, new_y_end = imgui.input_int(
        "##y_end", canvas_state.get_buffered_y_end(), step=0, step_fast=0
    )
    imgui.pop_item_width()
    imgui.next_column()

    imgui.columns(1)  # End column layout
    imgui.dummy(0, 5)

    # Update canvas_state if inputs changed
    if changed_x_start:
        canvas_state.set_buffered_x_start(new_x_start)
    if changed_y_start:
        canvas_state.set_buffered_y_start(new_y_start)
    if changed_x_end:
        canvas_state.set_buffered_x_end(new_x_end)
    if changed_y_end:
        canvas_state.set_buffered_y_end(new_y_end)

def set_up_window():
    """Sets up the Pyglet window, so the canvas can be used."""
    # Create the Pyglet window
    window = pyglet.window.Window(width=WINDOW_WIDTH, 
                                height=WINDOW_HEIGHT, 
                                caption="2. Line Algorithms and 2D Transformations")
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