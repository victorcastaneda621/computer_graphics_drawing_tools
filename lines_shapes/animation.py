from transformations_2d import Shape2D
from pixel_coordinates import Pixel
from canvas import CanvasState, ReflectionType

import time


animation_state = {
    "frame": 0,
    "l_shape": None,
    "upper_limits": None,
    "lower_limits": None,
    "pong_decor": None,
    "pong_paddle_left": None,
    "l_shape_2": None,
    "block_shape": None,
    "block_shape_2": None,
    "four_shape": None,
    "vertical_shape": None,
    "brick_1": None,
    "brick_2": None,
    "brick_3": None,
    "brick_4": None,
    "zero": None,
    "one": None,
    "four_shape_2": None,
    "fin_f_l_shape_1": None,
    "fin_f_l_shape_2": None,
    "fin_i_cross_shape_1": None,
    "fin_i_cross_shape_2": None,
    "fin_n_vertical_shape_1": None,
    "fin_n_vertical_shape_2": None,
    "fin_n_l_shape_1": None,
    "fin_n_l_shape_2": None
}

def run_animation(window, canvas_state: CanvasState):
    # Simulate a wait between frames
    time.sleep(0.5)

    global animation_state

    # Create shapes the first time
    if animation_state["l_shape"] is None:
        # Create a L shape
        l_shape = Shape2D([])
        l_shape.add_line(Pixel(0, 58), Pixel(16, 58))
        l_shape.add_line(Pixel(0, 50), Pixel(0, 58))
        l_shape.add_line(Pixel(0, 54), Pixel(16, 54))
        l_shape.add_line(Pixel(0, 50), Pixel(4, 50))
        l_shape.add_line(Pixel(4, 50), Pixel(4, 58))
        l_shape.add_line(Pixel(8, 54), Pixel(8, 58))
        l_shape.add_line(Pixel(16, 54), Pixel(4, 54))
        l_shape.add_line(Pixel(12, 54), Pixel(12, 58))
        l_shape.add_line(Pixel(16, 54), Pixel(16, 58))
        animation_state["l_shape"] = l_shape

        # Create another L shape
        l_shape_2 = Shape2D([])
        l_shape_2.add_line(Pixel(0, 58), Pixel(16, 58))
        l_shape_2.add_line(Pixel(0, 50), Pixel(0, 58))
        l_shape_2.add_line(Pixel(0, 54), Pixel(16, 54))
        l_shape_2.add_line(Pixel(0, 50), Pixel(4, 50))
        l_shape_2.add_line(Pixel(4, 50), Pixel(4, 58))
        l_shape_2.add_line(Pixel(8, 54), Pixel(8, 58))
        l_shape_2.add_line(Pixel(16, 54), Pixel(4, 54))
        l_shape_2.add_line(Pixel(12, 54), Pixel(12, 58))
        l_shape_2.add_line(Pixel(16, 54), Pixel(16, 58))
        animation_state["l_shape_2"] = l_shape_2

        # Create a block shape
        block_shape = Shape2D([])
        block_shape.add_line(Pixel(0, 58), Pixel(8, 58))
        block_shape.add_line(Pixel(8, 50), Pixel(8, 58))
        block_shape.add_line(Pixel(0, 50), Pixel(8, 50))
        block_shape.add_line(Pixel(0, 50), Pixel(0, 58))
        block_shape.add_line(Pixel(4, 50), Pixel(4, 58))
        block_shape.add_line(Pixel(0, 54), Pixel(8, 54))
        animation_state["block_shape"] = block_shape

        # Create another block shape
        block_shape_2 = Shape2D([])
        block_shape_2.add_line(Pixel(-58, 58), Pixel(-66, 58))
        block_shape_2.add_line(Pixel(-66, 50), Pixel(-66, 58))
        block_shape_2.add_line(Pixel(-58, 50), Pixel(-66, 50))
        block_shape_2.add_line(Pixel(-58, 50), Pixel(-58, 58))
        block_shape_2.add_line(Pixel(-62, 50), Pixel(-62, 58))
        block_shape_2.add_line(Pixel(-58, 54), Pixel(-66, 54))
        animation_state["block_shape_2"] = block_shape_2

        # Create a 4 shape
        four_shape = Shape2D([])
        four_shape.add_line(Pixel(-12, 58), Pixel(0, 58))
        four_shape.add_line(Pixel(-12, 58), Pixel(-12, 62))
        four_shape.add_line(Pixel(-12, 62), Pixel(-4, 62))
        four_shape.add_line(Pixel(-4, 62), Pixel(-4, 54))
        four_shape.add_line(Pixel(0, 54), Pixel(0, 58))
        four_shape.add_line(Pixel(-12, 58), Pixel(-12, 62))
        four_shape.add_line(Pixel(0, 54), Pixel(-8, 54))
        four_shape.add_line(Pixel(-8, 54), Pixel(-8, 62))
        animation_state["four_shape"] = four_shape

        # Create another 4 shape
        four_shape_2 = Shape2D([])
        four_shape_2.add_line(Pixel(-12, 58), Pixel(0, 58))
        four_shape_2.add_line(Pixel(-12, 58), Pixel(-12, 62))
        four_shape_2.add_line(Pixel(-12, 62), Pixel(-4, 62))
        four_shape_2.add_line(Pixel(-4, 62), Pixel(-4, 54))
        four_shape_2.add_line(Pixel(0, 54), Pixel(0, 58))
        four_shape_2.add_line(Pixel(-12, 58), Pixel(-12, 62))
        four_shape_2.add_line(Pixel(0, 54), Pixel(-8, 54))
        four_shape_2.add_line(Pixel(-8, 54), Pixel(-8, 62))
        animation_state["four_shape_2"] = four_shape_2

        # Create a vertical shape
        vertical_shape = Shape2D([])
        vertical_shape.add_line(Pixel(-72, -44), Pixel(-72, -40))
        vertical_shape.add_line(Pixel(-72, -44), Pixel(-88, -44))
        vertical_shape.add_line(Pixel(-88, -44), Pixel(-88, -40))
        vertical_shape.add_line(Pixel(-88, -40), Pixel(-72, -40))
        vertical_shape.add_line(Pixel(-76, -40), Pixel(-76, -44))
        vertical_shape.add_line(Pixel(-80, -40), Pixel(-80, -44))
        vertical_shape.add_line(Pixel(-84, -40), Pixel(-84, -44))
        animation_state["vertical_shape"] = vertical_shape

        # Create the bricks
        brick_1 = Shape2D([])
        brick_1.add_line(Pixel(72, -4), Pixel(74, -4))
        brick_1.add_line(Pixel(74, -4), Pixel(74, 4))
        brick_1.add_line(Pixel(74, 4), Pixel(72, 4))
        brick_1.add_line(Pixel(72, 4), Pixel(72, -4))
        animation_state["brick_1"] = brick_1
        brick_2 = Shape2D([])
        brick_2.add_line(Pixel(74, -4), Pixel(76, -4))
        brick_2.add_line(Pixel(76, -4), Pixel(76, 4))
        brick_2.add_line(Pixel(76, 4), Pixel(74, 4))
        brick_2.add_line(Pixel(74, 4), Pixel(74, -4))
        animation_state["brick_2"] = brick_2
        brick_3 = Shape2D([])
        brick_3.add_line(Pixel(74, 4), Pixel(76, 4))
        brick_3.add_line(Pixel(76, 4), Pixel(76, 12))
        brick_3.add_line(Pixel(76, 12), Pixel(74, 12))
        brick_3.add_line(Pixel(74, 12), Pixel(74, 4))
        animation_state["brick_3"] = brick_3
        brick_4 = Shape2D([])
        brick_4.add_line(Pixel(74, -12), Pixel(76, -12))
        brick_4.add_line(Pixel(76, -12), Pixel(76, -4))
        brick_4.add_line(Pixel(76, -4), Pixel(74, -4))
        brick_4.add_line(Pixel(74, -4), Pixel(74, -12))
        animation_state["brick_4"] = brick_4

        # Create the limits
        upper_limits = Shape2D([])
        upper_limits.add_line(Pixel(-30, 50), Pixel(-30, 10))
        upper_limits.add_line(Pixel(30, 50), Pixel(30, 50))
        animation_state["upper_limits"] = upper_limits
        lower_limits = Shape2D([])
        lower_limits.add_line(Pixel(-30, -50), Pixel(-30, -10))
        lower_limits.add_line(Pixel(30, -50), Pixel(30, 50))
        animation_state["lower_limits"] = lower_limits

        pong_decor = Shape2D([])
        pong_decor.add_line(Pixel(-70, -50), Pixel(-70, 49))
        pong_decor.add_line(Pixel(-70, -50), Pixel(-60, -50))
        pong_decor.add_line(Pixel(-70, 49), Pixel(-60, 49))
        animation_state["pong_decor"] = pong_decor

        pong_paddle_left = Shape2D([])
        pong_paddle_left.add_line(Pixel(-30, -10), Pixel(-30, 10))
        animation_state["pong_paddle_left"] = pong_paddle_left

        # Create the numbers
        zero = Shape2D([])
        zero.add_line(Pixel(-35, 45), Pixel(-30, 45))
        zero.add_line(Pixel(-30, 45), Pixel(-30, 35))
        zero.add_line(Pixel(-30, 35), Pixel(-35, 35))
        zero.add_line(Pixel(-35, 45), Pixel(-35, 35))
        animation_state["zero"] = zero

        one = Shape2D([])
        one.add_line(Pixel(-32, 45), Pixel(-32, 35))
        animation_state["one"] = one

        # Create FIN
        fin_f_l_shape_1 = Shape2D([])
        fin_f_l_shape_1.add_line(Pixel(-20, -50), Pixel(-16, -50))
        fin_f_l_shape_1.add_line(Pixel(-20, -46), Pixel(-8, -46))
        fin_f_l_shape_1.add_line(Pixel(-20, -42), Pixel(-8, -42))
        fin_f_l_shape_1.add_line(Pixel(-20, -42), Pixel(-20, -50))
        fin_f_l_shape_1.add_line(Pixel(-16, -42), Pixel(-16, -50))
        fin_f_l_shape_1.add_line(Pixel(-12, -42), Pixel(-12, -46))
        fin_f_l_shape_1.add_line(Pixel(-8, -42), Pixel(-8, -46))
        animation_state["fin_f_l_shape_1"] = fin_f_l_shape_1
        fin_f_l_shape_2 = Shape2D([])
        fin_f_l_shape_2.add_line(Pixel(-20, -50), Pixel(-16, -50))
        fin_f_l_shape_2.add_line(Pixel(-20, -46), Pixel(-8, -46))
        fin_f_l_shape_2.add_line(Pixel(-20, -42), Pixel(-8, -42))
        fin_f_l_shape_2.add_line(Pixel(-20, -42), Pixel(-20, -50))
        fin_f_l_shape_2.add_line(Pixel(-16, -42), Pixel(-16, -50))
        fin_f_l_shape_2.add_line(Pixel(-12, -42), Pixel(-12, -46))
        fin_f_l_shape_2.add_line(Pixel(-8, -42), Pixel(-8, -46))
        animation_state["fin_f_l_shape_2"] = fin_f_l_shape_2
        fin_i_cross_shape_1 = Shape2D([])
        fin_i_cross_shape_1.add_line(Pixel(-20, -50), Pixel(-8, -50))
        fin_i_cross_shape_1.add_line(Pixel(-20, -46), Pixel(-8, -46))
        fin_i_cross_shape_1.add_line(Pixel(-16, -42), Pixel(-12, -42))
        fin_i_cross_shape_1.add_line(Pixel(-20, -50), Pixel(-20, -46))
        fin_i_cross_shape_1.add_line(Pixel(-16, -50), Pixel(-16, -42))
        fin_i_cross_shape_1.add_line(Pixel(-12, -50), Pixel(-12, -42))
        fin_i_cross_shape_1.add_line(Pixel(-8, -50), Pixel(-8, -46))
        animation_state["fin_i_cross_shape_1"] = fin_i_cross_shape_1
        fin_i_cross_shape_2 = Shape2D([])
        fin_i_cross_shape_2.add_line(Pixel(-20, -50), Pixel(-8, -50))
        fin_i_cross_shape_2.add_line(Pixel(-20, -46), Pixel(-8, -46))
        fin_i_cross_shape_2.add_line(Pixel(-16, -42), Pixel(-12, -42))
        fin_i_cross_shape_2.add_line(Pixel(-20, -50), Pixel(-20, -46))
        fin_i_cross_shape_2.add_line(Pixel(-16, -50), Pixel(-16, -42))
        fin_i_cross_shape_2.add_line(Pixel(-12, -50), Pixel(-12, -42))
        fin_i_cross_shape_2.add_line(Pixel(-8, -50), Pixel(-8, -46))
        animation_state["fin_i_cross_shape_2"] = fin_i_cross_shape_2
        fin_n_l_shape_1 = Shape2D([])
        fin_n_l_shape_1.add_line(Pixel(-20, -50), Pixel(-16, -50))
        fin_n_l_shape_1.add_line(Pixel(-20, -46), Pixel(-8, -46))
        fin_n_l_shape_1.add_line(Pixel(-20, -42), Pixel(-8, -42))
        fin_n_l_shape_1.add_line(Pixel(-20, -42), Pixel(-20, -50))
        fin_n_l_shape_1.add_line(Pixel(-16, -42), Pixel(-16, -50))
        fin_n_l_shape_1.add_line(Pixel(-12, -42), Pixel(-12, -46))
        fin_n_l_shape_1.add_line(Pixel(-8, -42), Pixel(-8, -46))
        animation_state["fin_n_l_shape_1"] = fin_n_l_shape_1
        fin_n_l_shape_2 = Shape2D([])
        fin_n_l_shape_2.add_line(Pixel(-20, -50), Pixel(-16, -50))
        fin_n_l_shape_2.add_line(Pixel(-20, -46), Pixel(-8, -46))
        fin_n_l_shape_2.add_line(Pixel(-20, -42), Pixel(-8, -42))
        fin_n_l_shape_2.add_line(Pixel(-20, -42), Pixel(-20, -50))
        fin_n_l_shape_2.add_line(Pixel(-16, -42), Pixel(-16, -50))
        fin_n_l_shape_2.add_line(Pixel(-12, -42), Pixel(-12, -46))
        fin_n_l_shape_2.add_line(Pixel(-8, -42), Pixel(-8, -46))
        animation_state["fin_n_l_shape_2"] = fin_n_l_shape_2
        fin_n_vertical_shape_1 = Shape2D([])
        fin_n_vertical_shape_1.add_line(Pixel(0, -50), Pixel(4, -50))
        fin_n_vertical_shape_1.add_line(Pixel(0, -46), Pixel(4, -46))
        fin_n_vertical_shape_1.add_line(Pixel(0, -42), Pixel(4, -42))
        fin_n_vertical_shape_1.add_line(Pixel(0, -38), Pixel(4, -38))
        fin_n_vertical_shape_1.add_line(Pixel(0, -34), Pixel(4, -34))
        fin_n_vertical_shape_1.add_line(Pixel(0, -34), Pixel(0, -50))
        fin_n_vertical_shape_1.add_line(Pixel(4, -34), Pixel(4, -50))
        animation_state["fin_n_vertical_shape_1"] = fin_n_vertical_shape_1
        fin_n_vertical_shape_2 = Shape2D([])
        fin_n_vertical_shape_2.add_line(Pixel(0, -50), Pixel(4, -50))
        fin_n_vertical_shape_2.add_line(Pixel(0, -46), Pixel(4, -46))
        fin_n_vertical_shape_2.add_line(Pixel(0, -42), Pixel(4, -42))
        fin_n_vertical_shape_2.add_line(Pixel(0, -38), Pixel(4, -38))
        fin_n_vertical_shape_2.add_line(Pixel(0, -34), Pixel(4, -34))
        fin_n_vertical_shape_2.add_line(Pixel(0, -34), Pixel(0, -50))
        fin_n_vertical_shape_2.add_line(Pixel(4, -34), Pixel(4, -50))
        animation_state["fin_n_vertical_shape_2"] = fin_n_vertical_shape_2

    else: # For every other frame, just read the saved global data
        l_shape = animation_state["l_shape"]
        l_shape_2 = animation_state["l_shape_2"]
        block_shape = animation_state["block_shape"]
        upper_limits = animation_state["upper_limits"]
        lower_limits = animation_state["lower_limits"]
        pong_decor = animation_state["pong_decor"]
        pong_paddle_left = animation_state["pong_paddle_left"]
        block_shape_2 = animation_state["block_shape_2"]
        brick_1 = animation_state["brick_1"]
        brick_2 = animation_state["brick_2"]
        brick_3 = animation_state["brick_3"]
        brick_4 = animation_state["brick_4"]
        four_shape = animation_state["four_shape"]
        vertical_shape = animation_state["vertical_shape"]
        zero = animation_state["zero"]
        one = animation_state["one"]
        four_shape_2 = animation_state["four_shape_2"]
        fin_f_l_shape_1 = animation_state["fin_f_l_shape_1"]
        fin_f_l_shape_2 = animation_state["fin_f_l_shape_2"]
        fin_i_cross_shape_1 = animation_state["fin_i_cross_shape_1"]
        fin_i_cross_shape_2 = animation_state["fin_i_cross_shape_2"]
        fin_n_l_shape_1 = animation_state["fin_n_l_shape_1"]
        fin_n_l_shape_2 = animation_state["fin_n_l_shape_2"]
        fin_n_vertical_shape_1 = animation_state["fin_n_vertical_shape_1"]
        fin_n_vertical_shape_2 = animation_state["fin_n_vertical_shape_2"]

    # Clear the canvas before drawing the transformed shapes
    canvas_state.clear_canvas()
    print(animation_state["frame"])

    ## Every if statement represents what happens in a frame.
    ## It should at least call redraw_on_canvas() for the shapes
    ## that we don't want to erase (not redraw them again).
    ## Shapes can also be transformed in a frame.
    if animation_state["frame"] == 0: # Draw the first frame
        l_shape.redraw_on_canvas(canvas_state)
        l_shape_2.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] < 12: # Apply the transformations in this frame and redraw
        canvas_state.apply_translation(0, -4, l_shape)
        l_shape.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] == 12:
        canvas_state.apply_translation(0, -16, l_shape)
        canvas_state.apply_rotation(90, True, l_shape)
        l_shape.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state) 
        pong_paddle_left.redraw_on_canvas(canvas_state)
    
    elif animation_state["frame"] in  {13, 15, 17, 20}:
        canvas_state.apply_translation(-4, -4, l_shape)
        l_shape.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        
    elif animation_state["frame"] in {14, 16, 18, 19, 21, 22, 23, 24}:
        canvas_state.apply_translation(0, -4, l_shape)
        l_shape_2.redraw_on_canvas(canvas_state)
        l_shape.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
    
    elif animation_state["frame"] == 25:
        canvas_state.apply_translation(0, -2, l_shape)
        l_shape_2.redraw_on_canvas(canvas_state)
        l_shape.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {26, 27, 28, 29, 30, 31, 34, 36, 38, 41}:
        canvas_state.apply_translation(0, -4, l_shape_2)
        l_shape_2.redraw_on_canvas(canvas_state)
        l_shape.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in  {33, 35, 37, 39}:
        canvas_state.apply_translation(-4, -4, l_shape_2)
        l_shape_2.redraw_on_canvas(canvas_state)
        l_shape.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
    
    elif animation_state["frame"] in {32}:
        canvas_state.apply_rotation(90, False, l_shape_2)
        canvas_state.apply_translation(-22, 34, l_shape_2)
        l_shape_2.redraw_on_canvas(canvas_state)
        l_shape.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] == 43:
        canvas_state.apply_translation(-2, -8, l_shape_2)
        l_shape_2.redraw_on_canvas(canvas_state)
        l_shape.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {40, 42, 43, 44}:
        canvas_state.apply_translation(0, -8, l_shape_2)
        l_shape_2.redraw_on_canvas(canvas_state)
        l_shape.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
    
    elif animation_state["frame"] in {46, 48}:
        canvas_state.apply_translation(0, -4, block_shape)
        block_shape.redraw_on_canvas(canvas_state)
        l_shape.redraw_on_canvas(canvas_state)
        l_shape_2.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state) 
        pong_paddle_left.redraw_on_canvas(canvas_state)
    
    elif animation_state["frame"] in {45}:
        canvas_state.apply_translation(-4, -4, block_shape)
        block_shape.redraw_on_canvas(canvas_state)
        l_shape.redraw_on_canvas(canvas_state)
        l_shape_2.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state) 
        pong_paddle_left.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {47}:
        canvas_state.apply_translation(4, -4, block_shape)
        block_shape.redraw_on_canvas(canvas_state)
        l_shape.redraw_on_canvas(canvas_state)
        l_shape_2.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state) 
        pong_paddle_left.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {49}:
        canvas_state.apply_translation(-4, -8, block_shape)
        canvas_state.apply_scaling(1, 1.2, block_shape)
        block_shape.redraw_on_canvas(canvas_state)
        l_shape.redraw_on_canvas(canvas_state)
        l_shape_2.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state) 
        pong_paddle_left.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {50, 51, 52, 53, 54, 55, 56, 57, 58, 59}:
        canvas_state.apply_translation(0, -8, block_shape)
        canvas_state.apply_scaling(1, 1, block_shape)
        block_shape.redraw_on_canvas(canvas_state)
        l_shape.redraw_on_canvas(canvas_state)
        l_shape_2.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)  
        pong_paddle_left.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] == 60:
        canvas_state.apply_translation(-2, -11, block_shape)
        canvas_state.apply_scaling(1, (1/1.2), block_shape)
        block_shape.redraw_on_canvas(canvas_state)
        l_shape.redraw_on_canvas(canvas_state)
        l_shape_2.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {60, 61, 62, 63, 64}:
        canvas_state.apply_scaling(1.3, 1.2, block_shape)
        canvas_state.apply_scaling(1.3, 1.2, l_shape)
        canvas_state.apply_scaling(1.3, 1.2, l_shape_2)
        canvas_state.apply_scaling(1.3, 1.2, upper_limits)
        canvas_state.apply_scaling(1.3, 1.2, lower_limits)
        canvas_state.apply_translation(-10, 0, pong_paddle_left)
        block_shape.redraw_on_canvas(canvas_state)
        l_shape.redraw_on_canvas(canvas_state)
        l_shape_2.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state) 
        pong_paddle_left.redraw_on_canvas(canvas_state)
    
    elif animation_state["frame"] == 65:
        canvas_state.apply_translation(-1, 0, pong_paddle_left)
        canvas_state.apply_translation(0, -16, block_shape_2)
        block_shape_2.redraw_on_canvas(canvas_state)
        block_shape.redraw_on_canvas(canvas_state)
        l_shape.redraw_on_canvas(canvas_state)
        l_shape_2.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {66, 67}:
        canvas_state.apply_translation(64, -32, block_shape_2)
        canvas_state.apply_scaling(0.7, 0.7, block_shape_2)
        canvas_state.apply_translation(-64, 16, block_shape_2)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] == 68:
        canvas_state.apply_scaling(0.6, 0.6, block_shape_2)
        canvas_state.apply_translation(-32, 0, block_shape_2)
        canvas_state.apply_translation(-5, 0, brick_1)
        canvas_state.apply_translation(-5, 0, brick_2)
        canvas_state.apply_translation(-5, 0, brick_3)
        canvas_state.apply_translation(-5, 0, brick_4)
        brick_1.redraw_on_canvas(canvas_state)
        brick_2.redraw_on_canvas(canvas_state)
        brick_3.redraw_on_canvas(canvas_state)
        brick_4.redraw_on_canvas(canvas_state)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {69, 70, 71, 72, 73, 74, 75}:
        canvas_state.apply_translation(8,4,block_shape_2)
        brick_1.redraw_on_canvas(canvas_state)
        brick_2.redraw_on_canvas(canvas_state)
        brick_3.redraw_on_canvas(canvas_state)
        brick_4.redraw_on_canvas(canvas_state)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        four_shape.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {76}:
        canvas_state.apply_translation(8,4,block_shape_2)
        canvas_state.apply_translation(0, -16, four_shape)
        brick_1.redraw_on_canvas(canvas_state)
        brick_2.redraw_on_canvas(canvas_state)
        brick_3.redraw_on_canvas(canvas_state)
        brick_4.redraw_on_canvas(canvas_state)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        four_shape.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] == 77:
        canvas_state.apply_translation(8,-4,block_shape_2)
        canvas_state.apply_translation(-6, -38, four_shape)
        canvas_state.apply_rotation(90, False, four_shape)
        canvas_state.apply_translation(0, 38, four_shape)
        brick_1.redraw_on_canvas(canvas_state)
        brick_2.redraw_on_canvas(canvas_state)
        brick_3.redraw_on_canvas(canvas_state)
        brick_4.redraw_on_canvas(canvas_state)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        four_shape.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {80, 81}:
        canvas_state.apply_translation(0, 16, pong_paddle_left)
        canvas_state.apply_translation(8,-4,block_shape_2)
        canvas_state.apply_translation(0, -16, four_shape)
        brick_1.redraw_on_canvas(canvas_state)
        brick_2.redraw_on_canvas(canvas_state)
        brick_3.redraw_on_canvas(canvas_state)
        brick_4.redraw_on_canvas(canvas_state)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        four_shape.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {84}:
        canvas_state.apply_translation(0, -16, pong_paddle_left)
        canvas_state.apply_translation(8,-4,block_shape_2)
        canvas_state.apply_translation(0, -16, four_shape)
        brick_1.redraw_on_canvas(canvas_state)
        brick_2.redraw_on_canvas(canvas_state)
        brick_3.redraw_on_canvas(canvas_state)
        brick_4.redraw_on_canvas(canvas_state)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        four_shape.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {78, 79, 82, 83, 85}:
        canvas_state.apply_translation(8,-4,block_shape_2)
        canvas_state.apply_translation(0, -16, four_shape)
        brick_1.redraw_on_canvas(canvas_state)
        brick_2.redraw_on_canvas(canvas_state)
        brick_3.redraw_on_canvas(canvas_state)
        brick_4.redraw_on_canvas(canvas_state)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        four_shape.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {86}:
        canvas_state.apply_translation(0, -16, pong_paddle_left)
        canvas_state.apply_translation(-8,-7,block_shape_2)
        canvas_state.apply_translation(0, -16, four_shape)
        brick_2.redraw_on_canvas(canvas_state)
        brick_3.redraw_on_canvas(canvas_state)
        brick_4.redraw_on_canvas(canvas_state)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        four_shape.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {87}:
        canvas_state.apply_translation(0, -16, pong_paddle_left)
        canvas_state.apply_translation(-8,-6,block_shape_2)
        canvas_state.apply_translation(0, -16, four_shape)
        canvas_state.apply_translation(26, 16, vertical_shape)
        brick_2.redraw_on_canvas(canvas_state)
        brick_3.redraw_on_canvas(canvas_state)
        brick_4.redraw_on_canvas(canvas_state)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        four_shape.redraw_on_canvas(canvas_state)
        vertical_shape.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {88}:
        canvas_state.apply_translation(0, 16, pong_paddle_left)
        canvas_state.apply_translation(-8,-6,block_shape_2)
        canvas_state.apply_shearing(0.5, 0, vertical_shape)
        canvas_state.apply_translation(16, -4, vertical_shape)
        brick_2.redraw_on_canvas(canvas_state)
        brick_3.redraw_on_canvas(canvas_state)
        brick_4.redraw_on_canvas(canvas_state)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        four_shape.redraw_on_canvas(canvas_state)
        vertical_shape.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {89, 90}:
        canvas_state.apply_translation(0, -16, pong_paddle_left)
        canvas_state.apply_translation(-8,-6,block_shape_2)
        canvas_state.apply_translation(16, -4, vertical_shape)
        brick_2.redraw_on_canvas(canvas_state)
        brick_3.redraw_on_canvas(canvas_state)
        brick_4.redraw_on_canvas(canvas_state)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        four_shape.redraw_on_canvas(canvas_state)
        vertical_shape.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {91, 92}:
        canvas_state.apply_translation(0, 16, pong_paddle_left)
        canvas_state.apply_translation(-8,-6,block_shape_2)
        canvas_state.apply_translation(17, -4, vertical_shape)
        brick_2.redraw_on_canvas(canvas_state)
        brick_3.redraw_on_canvas(canvas_state)
        brick_4.redraw_on_canvas(canvas_state)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        four_shape.redraw_on_canvas(canvas_state)
        vertical_shape.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {93}:
        canvas_state.apply_translation(0, -16, pong_paddle_left)
        canvas_state.apply_translation(-8,8,block_shape_2)
        canvas_state.apply_shearing(-0.5, 0, vertical_shape)
        canvas_state.apply_translation(-16, -4, vertical_shape)
        brick_2.redraw_on_canvas(canvas_state)
        brick_3.redraw_on_canvas(canvas_state)
        brick_4.redraw_on_canvas(canvas_state)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        four_shape.redraw_on_canvas(canvas_state)
        vertical_shape.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {94}:
        canvas_state.apply_translation(0, -16, pong_paddle_left)
        canvas_state.apply_translation(-2,8,block_shape_2)
        canvas_state.apply_translation(0, -16, vertical_shape)
        canvas_state.apply_translation(16, 0, brick_2)
        canvas_state.apply_translation(16, 0, brick_3)
        canvas_state.apply_translation(16, 0, brick_4)
        brick_2.redraw_on_canvas(canvas_state)
        brick_3.redraw_on_canvas(canvas_state)
        brick_4.redraw_on_canvas(canvas_state)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        vertical_shape.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {95}:
        canvas_state.apply_translation(8, 0, pong_paddle_left)
        canvas_state.apply_translation(-8,8,block_shape_2)
        canvas_state.apply_scaling(1, 0.8, pong_paddle_left)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {96}:
        canvas_state.apply_translation(0, -16, pong_paddle_left)
        canvas_state.apply_scaling(1, 0.8, pong_paddle_left)
        canvas_state.apply_translation(-8,8,block_shape_2)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {97}:
        canvas_state.apply_translation(0, -16, pong_paddle_left)
        canvas_state.apply_translation(-8,8,block_shape_2)
        canvas_state.apply_scaling(1, 0.8, pong_paddle_left)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {98, 99, 100, 101}:
        canvas_state.apply_translation(0, 16, pong_paddle_left)
        canvas_state.apply_translation(-8,8,block_shape_2)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        pong_decor.redraw_on_canvas(canvas_state)
        zero.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {102}:
        canvas_state.apply_translation(0, 16, pong_paddle_left)
        canvas_state.apply_translation(-5,8,block_shape_2)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        pong_decor.redraw_on_canvas(canvas_state)
        zero.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {103, 104, 105, 106}:
        canvas_state.apply_translation(0, -8, pong_paddle_left)
        canvas_state.apply_translation(8,-10,block_shape_2)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        pong_decor.redraw_on_canvas(canvas_state)
        zero.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {107}:
        canvas_state.apply_translation(0, -8, pong_paddle_left)
        canvas_state.apply_translation(15,-10,block_shape_2)
        canvas_state.apply_translation(-32, -40, four_shape_2)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        pong_decor.redraw_on_canvas(canvas_state)
        zero.redraw_on_canvas(canvas_state)
        four_shape_2.redraw_on_canvas(canvas_state)
    
    elif animation_state["frame"] in {108, 109}:
        canvas_state.apply_translation(0, -16, pong_paddle_left)
        canvas_state.apply_translation(15,-10,block_shape_2)
        canvas_state.apply_translation(25, -27, four_shape_2)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        pong_decor.redraw_on_canvas(canvas_state)
        zero.redraw_on_canvas(canvas_state)
        four_shape_2.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {110}:
        canvas_state.apply_reflection(ReflectionType.Y_AXIS, shape=pong_paddle_left)
        canvas_state.apply_reflection(ReflectionType.Y_AXIS, shape=pong_decor)
        canvas_state.apply_reflection(ReflectionType.Y_AXIS, shape=zero)
        canvas_state.apply_translation(0, 16, pong_paddle_left)
        canvas_state.apply_translation(15, 4,block_shape_2)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        pong_decor.redraw_on_canvas(canvas_state)
        zero.redraw_on_canvas(canvas_state)
        four_shape_2.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {111}:
        canvas_state.apply_translation(0, 16, pong_paddle_left)
        canvas_state.apply_translation(8, 4,block_shape_2)
        canvas_state.apply_translation(13, -12, four_shape_2)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        pong_decor.redraw_on_canvas(canvas_state)
        zero.redraw_on_canvas(canvas_state)
        four_shape_2.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {112}:
        canvas_state.apply_shearing(0.4, 0, four_shape_2)
        canvas_state.apply_translation(0, 16, pong_paddle_left)
        canvas_state.apply_translation(16, 8,block_shape_2)
        canvas_state.apply_translation(16, -8, four_shape_2)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        pong_decor.redraw_on_canvas(canvas_state)
        zero.redraw_on_canvas(canvas_state)
        four_shape_2.redraw_on_canvas(canvas_state)
    
    elif animation_state["frame"] in {113}:
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        pong_decor.redraw_on_canvas(canvas_state)
        zero.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {114}:
        canvas_state.apply_translation(0, 16, pong_paddle_left)
        canvas_state.apply_translation(16, 8,block_shape_2)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        pong_decor.redraw_on_canvas(canvas_state)
        zero.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {115}:
        canvas_state.apply_translation(16, 8,block_shape_2)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        pong_decor.redraw_on_canvas(canvas_state)
        zero.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {116}:
        canvas_state.apply_translation(0, -16, pong_paddle_left)
        canvas_state.apply_translation(16, 8,block_shape_2)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        pong_decor.redraw_on_canvas(canvas_state)
        zero.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {117}:
        canvas_state.apply_reflection(ReflectionType.Y_AXIS, shape=pong_paddle_left)
        canvas_state.apply_reflection(ReflectionType.Y_AXIS, shape=pong_decor)
        canvas_state.apply_reflection(ReflectionType.Y_AXIS, shape=block_shape_2)
        canvas_state.apply_translation(42,12, block_shape_2)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        pong_decor.redraw_on_canvas(canvas_state)
        one.redraw_on_canvas(canvas_state)
        block_shape_2.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {118, 119, 120}:
        canvas_state.apply_translation(8, -10,block_shape_2)
        block_shape_2.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        pong_decor.redraw_on_canvas(canvas_state)
        one.redraw_on_canvas(canvas_state)
        block_shape_2.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {121, 122, 123}:
        canvas_state.apply_scaling(0.5, 0.5, pong_decor)
        canvas_state.apply_scaling(0.5, 0.5, one)
        canvas_state.apply_scaling(0.5, 0.5, pong_paddle_left)
        canvas_state.apply_scaling(0.5, 0.5, block_shape_2)
        canvas_state.apply_scaling(1/1.3, 1/1.2, upper_limits)
        canvas_state.apply_scaling(1/1.3, 1/1.2, lower_limits)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        pong_decor.redraw_on_canvas(canvas_state)
        one.redraw_on_canvas(canvas_state)
        block_shape_2.redraw_on_canvas(canvas_state)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {124}:
        canvas_state.apply_scaling(1/1.3, 1/1.2, upper_limits)
        canvas_state.apply_scaling(1/1.3, 1/1.2, lower_limits)
        canvas_state.apply_scaling(1, 20, pong_paddle_left)
        canvas_state.apply_translation(-22,-50, pong_paddle_left)
        canvas_state.apply_reflection(ReflectionType.ANY_LINE, m=0, b=-42, shape=fin_i_cross_shape_2)
        canvas_state.apply_rotation(90, True, fin_n_l_shape_1)
        canvas_state.apply_rotation(90, False, fin_n_l_shape_2)
        canvas_state.apply_translation(4, 0, fin_n_vertical_shape_1)
        canvas_state.apply_translation(24, 0, fin_n_vertical_shape_2)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {125}:
        canvas_state.apply_translation(-8,0,fin_f_l_shape_1)
        canvas_state.apply_translation(24, 24, fin_f_l_shape_2)
        canvas_state.apply_translation(8, 0, fin_i_cross_shape_1)
        canvas_state.apply_translation(8, 180, fin_i_cross_shape_2)
        canvas_state.apply_translation(-50, 120, fin_n_l_shape_1)
        canvas_state.apply_translation(28, 60, fin_n_l_shape_2)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_1.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_1.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_2.redraw_on_canvas(canvas_state)
        
    elif animation_state["frame"] in  {126, 127}:
        canvas_state.apply_translation(-16, -8, fin_f_l_shape_2)
        canvas_state.apply_translation(0, -16, fin_i_cross_shape_2)
        canvas_state.apply_translation(0, -16, fin_n_l_shape_1)
        canvas_state.apply_translation(0, -16, fin_n_l_shape_2)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        fin_f_l_shape_1.redraw_on_canvas(canvas_state)
        fin_f_l_shape_2.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_1.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_1.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_2.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in  {128, 129, 131, 132}:
        canvas_state.apply_translation(0, -16, fin_i_cross_shape_2)
        canvas_state.apply_translation(0, -16, fin_n_l_shape_1)
        canvas_state.apply_translation(8, -16, fin_n_l_shape_2)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        fin_f_l_shape_1.redraw_on_canvas(canvas_state)
        fin_f_l_shape_2.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_1.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_1.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_2.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in  {130}:
        canvas_state.apply_translation(0, -16, fin_i_cross_shape_2)
        canvas_state.apply_translation(10, -16, fin_n_l_shape_1)
        canvas_state.apply_translation(-8, -2, fin_n_l_shape_2)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        fin_f_l_shape_1.redraw_on_canvas(canvas_state)
        fin_f_l_shape_2.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_1.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_1.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_2.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in  {133}:
        canvas_state.apply_translation(0, -8, fin_i_cross_shape_2)
        canvas_state.apply_translation(0, -8, fin_n_l_shape_1)
        canvas_state.apply_translation(6, -8, fin_n_l_shape_2)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        fin_f_l_shape_1.redraw_on_canvas(canvas_state)
        fin_f_l_shape_2.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_1.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_1.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_2.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in  {134}:
        canvas_state.apply_translation(0, -8, fin_i_cross_shape_2)
        canvas_state.apply_translation(8, -8, fin_n_l_shape_1)
        canvas_state.apply_translation(0, -8, fin_n_l_shape_2)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        fin_f_l_shape_1.redraw_on_canvas(canvas_state)
        fin_f_l_shape_2.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_1.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_1.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_2.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in  {134}:
        canvas_state.apply_translation(0, -8, fin_i_cross_shape_2)
        canvas_state.apply_translation(7, -8, fin_n_l_shape_1)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        fin_f_l_shape_1.redraw_on_canvas(canvas_state)
        fin_f_l_shape_2.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_1.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_1.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_2.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in  {135}:
        canvas_state.apply_translation(0, -8, fin_i_cross_shape_2)
        canvas_state.apply_translation(6, -8, fin_n_l_shape_1)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        fin_f_l_shape_1.redraw_on_canvas(canvas_state)
        fin_f_l_shape_2.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_1.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_1.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_2.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in  {136, 137}:
        canvas_state.apply_translation(0, -8, fin_i_cross_shape_2)
        canvas_state.apply_translation(0, -7, fin_n_l_shape_1)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        fin_f_l_shape_1.redraw_on_canvas(canvas_state)
        fin_f_l_shape_2.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_1.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_1.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_2.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in  {138}:
        canvas_state.apply_translation(0, -16, fin_i_cross_shape_2)
        canvas_state.apply_shearing(0, 0.3, fin_i_cross_shape_2)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        fin_f_l_shape_1.redraw_on_canvas(canvas_state)
        fin_f_l_shape_2.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_1.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_1.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_2.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in  {139}:
        canvas_state.apply_translation(0, -12, fin_i_cross_shape_2)
        canvas_state.apply_shearing(0, -0.3, fin_i_cross_shape_2)
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        fin_f_l_shape_1.redraw_on_canvas(canvas_state)
        fin_f_l_shape_2.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_1.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_1.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_2.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] in {140, 141, 142}:
        upper_limits.redraw_on_canvas(canvas_state)
        lower_limits.redraw_on_canvas(canvas_state)
        pong_paddle_left.redraw_on_canvas(canvas_state)
        fin_f_l_shape_1.redraw_on_canvas(canvas_state)
        fin_f_l_shape_2.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_1.redraw_on_canvas(canvas_state)
        fin_i_cross_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_l_shape_1.redraw_on_canvas(canvas_state)
        fin_n_l_shape_2.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_1.redraw_on_canvas(canvas_state)
        fin_n_vertical_shape_2.redraw_on_canvas(canvas_state)

    elif animation_state["frame"] == 143: # Last frame, so indicate that by returning False
        return False

    # Add one to the global frame counter and return True (the animation didn't finish this frame)
    animation_state["frame"] = animation_state["frame"] + 1
    return True