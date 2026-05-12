from turtle import *
import tkinter as tk

from constants import *
from ui_utils import *
from canvas import CanvasState

root, screen, tk_canvas = prepare_ui()

toolbar = draw_toolbar(root)

turtle = RawTurtle(screen)
turtle.speed(0)
turtle.shape("turtle")

canvas = CanvasState()

draw_ui(toolbar, root, turtle, canvas, tk_canvas)

root.mainloop()