import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import ttk
from turtle import *
from constants import *
from functools import partial
from canvas import CanvasState, ConstantMeanings, Rule
import canvasvg
import os

class PRESETS:
    KOCH = 0
    SIERPINSKI_T = 1
    DRAGON = 2
    SQUARE_PATTERN = 3
    HEX_GOSPER = 4
    DENSE_TREE = 5
    BRANCH = 6
    CORAL = 7
    DENSE_CORAL = 8
    WINDY_TREE = 9
    COLORED_BRANCH = 10
    COLORED_SQUARE_PATTERN = 11


    def all():
        return set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

ui_color = {
    "toolbar": "#D1D1D1",

    "tab_active": "#70C0E7",
    "tab_hover": "#3297DF",

    "btn_clear_background": "#E7E700",
    "btn_clear_active": "#D0A300",

    "btn_exit_background": "#FF4D4D",
    "btn_exit_active": "#CC2D2D",

    "btn_green_background": "#00EA00",
    "btn_green_active": "#00A400"
}

def prepare_ui():
    root = tk.Tk()
    root.title("4. L-Systems")
    root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

    canvas = tk.Canvas(root, width=600, height=500)
    canvas.pack(side="left", fill="both", expand=True)
    canvas.pack_propagate(False)

    make_canvas_navigable(canvas, root)

    screen = TurtleScreen(canvas)
    return root,screen, canvas

def make_canvas_navigable(canvas, root):
    canvas.scale_factor = 1.0
    PAN_STEP = 20

    def zoom(event):
        factor = 1.1 if event.delta > 0 else 0.9
        canvas.scale_factor *= factor

        canvas.scale("all", event.x, event.y, factor, factor)

        canvas.configure(scrollregion=canvas.bbox("all"))

    def pan_left(event):
        canvas.xview_scroll(-PAN_STEP, "units")

    def pan_right(event):
        canvas.xview_scroll(PAN_STEP, "units")

    def pan_up(event):
        canvas.yview_scroll(-PAN_STEP, "units")

    def pan_down(event):
        canvas.yview_scroll(PAN_STEP, "units")

    canvas.bind("<MouseWheel>", zoom)
    root.bind("<Left>", pan_left)
    root.bind("<Right>", pan_right)
    root.bind("<Up>", pan_up)
    root.bind("<Down>", pan_down)

    canvas.zoom = zoom
    canvas.pan_left = pan_left
    canvas.pan_right = pan_right
    canvas.pan_up = pan_up
    canvas.pan_down = pan_down

def draw_toolbar(root):
    toolbar = tk.Frame(root, width=PANEL_WIDTH, height=WINDOW_HEIGHT, bg=ui_color["toolbar"])
    toolbar.pack(side="right", fill="y")
    toolbar.pack_propagate(False)
    toolbar.config(height=PANEL_HEIGHT)
    toolbar.config(width=PANEL_WIDTH)
    toolbar.grid_columnconfigure(0, weight=1)
    toolbar.grid_columnconfigure(1, weight=1)
    return toolbar

def draw_ui(toolbar, root, turtle, canvas:CanvasState, tk_canvas):

    # Early definition of initial state combo and rules list
    group_color = tk.LabelFrame(toolbar, text="DRAWING COLOR", padx=10, pady=12)
    label_color = tk.Label(group_color, text="Color: #000000", width=15, anchor="w")

    group_ini = tk.LabelFrame(toolbar, text="3. INITIAL STATE", padx=10, pady=12)

    vars = canvas.list_variables()
    default_text = "No Variables Yet"  
    selected_var = tk.StringVar(group_ini, default_text)
    combo_ini = ttk.Combobox(group_ini, textvariable=selected_var, values=vars, state="readonly")
    combo_ini.set("No Variables")

    group_rules_list = tk.LabelFrame(toolbar, text="List of Rules", padx=10, pady=10)
    listbox_rule = tk.Listbox(group_rules_list, height=12, width=25)

    # List of variables/constants
    group_listvar = tk.LabelFrame(toolbar, text="Variables/Constants List", padx=10, pady=10)
    group_listvar.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nw")

    listbox_var = tk.Listbox(group_listvar, height=12, width=25)
    listbox_var.grid(row=0, column=0, sticky="n", padx=(0,5), pady=5)

    btn_remove_const = tk.Button(group_listvar, text="Remove Item", 
                                 command=partial(remove_item, canvas, listbox_var, combo_ini, listbox_rule), 
                                 background=ui_color["btn_clear_background"],
                                 activebackground=ui_color["btn_clear_active"])
    btn_remove_const.grid(row=1, column=0, sticky="n", padx=(0,5), pady=5)

    # Variables
    group_var = tk.LabelFrame(toolbar, text="1. VARIABLES", padx=10, pady=12)
    group_var.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    label_var = tk.Label(group_var, 
                         text="•  To add a variable: type its name into the text area and click\n   'Add Variable'."
                                " It will appear in the list.\n"
                                "•  To remove a variable: select it on the list, then click 'Remove Item'.", 
                         justify="left",
                         anchor="w")
    label_var.grid(row=0, column=0, columnspan=3, pady=(0, 0), sticky="ew")

    textarea_var = tk.Text(group_var, width=10, height=1)
    textarea_var.grid(row=1, column=0, sticky="n", padx=(0,5), pady=5)

    var_meanings = list(ConstantMeanings.list_all())
    selected_variable = tk.StringVar(group_var, var_meanings[0])
    combo_vars = ttk.Combobox(group_var, textvariable=selected_variable, values=var_meanings, state="readonly")
    combo_vars.grid(row=1, column=1, sticky="n", padx=(0,5), pady=5)
    combo_vars.set(var_meanings[0])

    btn_add_var = tk.Button(group_var, text="Add Variable", 
                            command=partial(add_variable_from_text, textarea_var, canvas, listbox_var, combo_ini, combo_vars),
                            background=ui_color["btn_green_background"],
                            activebackground=ui_color["btn_green_active"])
    btn_add_var.grid(row=1, column=2, sticky="n", padx=(0,5), pady=5)

    # Constants
    group_const = tk.LabelFrame(toolbar, text="2. CONSTANTS", padx=10, pady=12)
    group_const.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

    label_const = tk.Label(group_const, 
                         text="•  To add a constant: type its name into the text area and click\n   'Add Constant'."
                                " It will appear in the list.\n"
                                "•  To remove a variable: select it on the list, then click 'Remove Item'.", 
                         justify="left",
                         anchor="w")
    label_const.grid(row=0, column=0, columnspan=3, pady=(0, 0), sticky="ew")

    textarea_const = tk.Text(group_const, width=10, height=1)
    textarea_const.grid(row=1, column=0, sticky="n", padx=(0,5), pady=5)

    const_meanings = list(ConstantMeanings.list_all())
    selected_const = tk.StringVar(group_const, const_meanings[0])
    combo = ttk.Combobox(group_const, textvariable=selected_const, values=const_meanings, state="readonly")
    combo.grid(row=1, column=1, sticky="n", padx=(0,5), pady=5)
    combo.set(const_meanings[0])

    btn_add_const = tk.Button(group_const, text="Add Constant", 
                              command=partial(add_constant_from_text, textarea_const, canvas, listbox_var, combo),
                              background=ui_color["btn_green_background"],
                              activebackground=ui_color["btn_green_active"])
    btn_add_const.grid(row=1, column=2, sticky="n", padx=(0,5), pady=5)

    # Initial State
    group_ini.grid(row=2, column=0, padx=10, pady=10, sticky="nw")

    label_const = tk.Label(group_ini, 
                         text="Choose one of the specified variables to act as the initial state.",
                         justify="left",
                         anchor="w")
    label_const.grid(row=0, column=0, columnspan=3, pady=(0, 0), sticky="ew")

    combo_ini.grid(row=1, column=0, sticky="n", padx=(0,5), pady=5)

    btn_add_ini = tk.Button(group_ini, text="Set as Initial State", 
                              command=partial(set_initial, canvas, combo_ini, listbox_var),
                              background=ui_color["tab_active"],
                              activebackground=ui_color["tab_hover"])
    btn_add_ini.grid(row=1, column=1, sticky="n", padx=(0,5), pady=5)

    # Rules
    group_rules = tk.LabelFrame(toolbar, text="4. RULES", padx=10, pady=12)
    group_rules.grid(row=3, column=0, padx=10, pady=10, sticky="nw")

    textarea_ori = tk.Text(group_rules, width=10, height=1)
    textarea_ori.grid(row=0, column=0, sticky="n", padx=(0,5), pady=5)
    label = tk.Label(group_rules, 
                         text=" --> ",
                         justify="left",
                         anchor="w")
    label.grid(row=0, column=1, pady=(0, 0), sticky="ew")
    textarea_des = tk.Text(group_rules, width=25, height=1)
    textarea_des.grid(row=0, column=3, sticky="n", padx=(0,10), pady=5)

    btn_add_rule = tk.Button(group_rules, text="Add Rule", 
                              command=partial(add_rule_from_text, canvas, textarea_ori, textarea_des, listbox_rule),
                              background=ui_color["btn_green_background"],
                              activebackground=ui_color["btn_green_active"])
    btn_add_rule.grid(row=0, column=4, sticky="n", padx=(0,5), pady=5)

    # List of rules
    group_rules_list.grid(row=2, column=1, rowspan=40, padx=10, pady=10, sticky="nw")

    listbox_rule.grid(row=0, column=0, sticky="n", padx=(0,5), pady=5)

    btn_remove_rule = tk.Button(group_rules_list, text="Remove Rule", 
                                 command=partial(remove_rule, canvas, listbox_rule), 
                                 background=ui_color["btn_clear_background"],
                                 activebackground=ui_color["btn_clear_active"])
    btn_remove_rule.grid(row=1, column=0, sticky="n", padx=(0,5), pady=5)

    # Controls
    group_control = tk.LabelFrame(toolbar, text="5. CONTROL PANEL", padx=10, pady=12)
    group_control.grid(row=4, column=0, padx=10, pady=10, sticky="nw")
    label_iters = tk.Label(group_control, text="Iterations:")
    label_iters.grid(row=0, column=0, padx=5, pady=5)
    textarea_iters = tk.Text(group_control, width=4, height=1)
    textarea_iters.grid(row=0, column=1, sticky="n", padx=(0,10), pady=5)
    btn_draw = tk.Button(group_control, text="Draw", 
                              command=partial(draw_system, canvas, textarea_iters, turtle, label_color),
                              background=ui_color["btn_green_background"],
                              activebackground=ui_color["btn_green_active"])
    btn_draw.grid(row=0, column=2, sticky="n", padx=(0,5), pady=5)
    btn_clear = tk.Button(group_control, text="Clear Canvas", 
                                 command=partial(clear_canvas, turtle, canvas), 
                                 background=ui_color["btn_clear_background"],
                                 activebackground=ui_color["btn_clear_active"])
    btn_clear.grid(row=0, column=3, sticky="n", padx=(0,5), pady=5)
    btn_save = tk.Button(group_control, text="Save to Image", 
                              command=partial(save_to_image, tk_canvas, turtle, canvas),
                              background=ui_color["tab_active"],
                              activebackground=ui_color["tab_hover"])
    btn_save.grid(row=0, column=4, sticky="n", padx=(0,5), pady=5)
    exit_btn = tk.Button(group_control, text="Exit", 
                         command=root.destroy,
                         background=ui_color["btn_exit_background"],
                         activebackground=ui_color["btn_exit_active"])
    exit_btn.grid(row=0, column=5, sticky="n", padx=(0,5), pady=5)
    var_show_turtle = tk.BooleanVar()
    var_show_turtle.set(canvas.show_turtle)
    chk_show_turtle = tk.Checkbutton(group_control, 
                                    text="Show Turtle", 
                                    variable=var_show_turtle, 
                                    command=partial(toggle_turtle_from_var, canvas, turtle, var_show_turtle),
                                    anchor="w",
                                    justify="left")
    chk_show_turtle.grid(row=0, column=6, columnspan=2, sticky="n", padx=5, pady=2)

    # Color
    group_color.grid(row=5, column=1, padx=10, pady=10, sticky="nw")
    label_color.grid(row=0, column=0, padx=5, pady=5)
    chk_color_turtle = tk.Button(
        group_color,
        text="Change Color",
        background=ui_color["tab_active"],
        activebackground=ui_color["tab_hover"])
    chk_color_turtle.config(
        command=partial(change_color, turtle, label_color))
    chk_color_turtle.grid(row=1, column=0, columnspan=2, sticky="n", padx=5, pady=2)

    # Presets
    group_pre = tk.LabelFrame(toolbar, text="PRESETS", padx=10, pady=12)
    group_pre.grid(row=5, column=0, padx=10, pady=10, sticky="nw")
    btn_f = tk.Button(group_pre, text="Koch", 
                              command=partial(input_presets, PRESETS.KOCH, canvas, listbox_var, listbox_rule, combo_ini, turtle, textarea_iters),
                              background=ui_color["tab_active"],
                              activebackground=ui_color["tab_hover"])
    btn_f.grid(row=0, column=0, sticky="n", padx=(0,5), pady=5)
    btn_f = tk.Button(group_pre, text="Sierpinski Triangle", 
                              command=partial(input_presets, PRESETS.SIERPINSKI_T, canvas, listbox_var, listbox_rule, combo_ini, turtle, textarea_iters),
                              background=ui_color["tab_active"],
                              activebackground=ui_color["tab_hover"])
    btn_f.grid(row=0, column=1, sticky="n", padx=(0,5), pady=5)
    btn_f = tk.Button(group_pre, text="Dragon", 
                              command=partial(input_presets, PRESETS.DRAGON, canvas, listbox_var, listbox_rule, combo_ini, turtle, textarea_iters),
                              background=ui_color["tab_active"],
                              activebackground=ui_color["tab_hover"])
    btn_f.grid(row=0, column=2, sticky="n", padx=(0,5), pady=5)
    btn_f = tk.Button(group_pre, text="Square Pattern", 
                              command=partial(input_presets, PRESETS.SQUARE_PATTERN, canvas, listbox_var, listbox_rule, combo_ini, turtle, textarea_iters),
                              background=ui_color["tab_active"],
                              activebackground=ui_color["tab_hover"])
    btn_f.grid(row=0, column=3, sticky="n", padx=(0,5), pady=5)
    btn_f = tk.Button(group_pre, text="Hex Gosper", 
                              command=partial(input_presets, PRESETS.HEX_GOSPER, canvas, listbox_var, listbox_rule, combo_ini, turtle, textarea_iters),
                              background=ui_color["tab_active"],
                              activebackground=ui_color["tab_hover"])
    btn_f.grid(row=0, column=4, sticky="n", padx=(0,5), pady=5)
    btn_f = tk.Button(group_pre, text="Branch", 
                              command=partial(input_presets, PRESETS.BRANCH, canvas, listbox_var, listbox_rule, combo_ini, turtle, textarea_iters),
                              background=ui_color["tab_active"],
                              activebackground=ui_color["tab_hover"])
    btn_f.grid(row=1, column=0, sticky="n", padx=(0,5), pady=5)
    btn_f = tk.Button(group_pre, text="Dense Tree", 
                              command=partial(input_presets, PRESETS.DENSE_TREE, canvas, listbox_var, listbox_rule, combo_ini, turtle, textarea_iters),
                              background=ui_color["tab_active"],
                              activebackground=ui_color["tab_hover"])
    btn_f.grid(row=1, column=1, sticky="n", padx=(0,5), pady=5)
    btn_f = tk.Button(group_pre, text="Coral", 
                              command=partial(input_presets, PRESETS.CORAL, canvas, listbox_var, listbox_rule, combo_ini, turtle, textarea_iters),
                              background=ui_color["tab_active"],
                              activebackground=ui_color["tab_hover"])
    btn_f.grid(row=1, column=2, sticky="n", padx=(0,5), pady=5)
    btn_f = tk.Button(group_pre, text="Dense Coral", 
                              command=partial(input_presets, PRESETS.DENSE_CORAL, canvas, listbox_var, listbox_rule, combo_ini, turtle, textarea_iters),
                              background=ui_color["tab_active"],
                              activebackground=ui_color["tab_hover"])
    btn_f.grid(row=1, column=3, sticky="n", padx=(0,5), pady=5)
    btn_f = tk.Button(group_pre, text="Windy Tree", 
                              command=partial(input_presets, PRESETS.WINDY_TREE, canvas, listbox_var, listbox_rule, combo_ini, turtle, textarea_iters),
                              background=ui_color["tab_active"],
                              activebackground=ui_color["tab_hover"])
    btn_f.grid(row=1, column=4, sticky="n", padx=(0,5), pady=5)
    btn_f = tk.Button(group_pre, text="Colored Branch", 
                              command=partial(input_presets, PRESETS.COLORED_BRANCH, canvas, listbox_var, listbox_rule, combo_ini, turtle, textarea_iters),
                              background=ui_color["tab_active"],
                              activebackground=ui_color["tab_hover"])
    btn_f.grid(row=1, column=5, sticky="n", padx=(0,5), pady=5)
    btn_f = tk.Button(group_pre, text="Colored Square Pattern", 
                              command=partial(input_presets, PRESETS.COLORED_SQUARE_PATTERN, canvas, listbox_var, listbox_rule, combo_ini, turtle, textarea_iters),
                              background=ui_color["tab_active"],
                              activebackground=ui_color["tab_hover"])
    btn_f.grid(row=0, column=5, sticky="n", padx=(0,5), pady=5)

def listbox_selected(listbox):
    selected = listbox.curselection()
    if not selected:
        return
    else:
        return listbox.get(selected[0]).split(" ")[0]
    
def refresh_listbox(canvas, listbox):
    listbox.delete(0, tk.END)
    for var in canvas.list_variables():
        if var in canvas.initial_list():
            match canvas.variable_meanings[var]:
                case ConstantMeanings.TURN_90_RIGHT:
                    formatted = f"{var:1} [Ini][Turn 90º R]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.TURN_90_LEFT:
                    formatted = f"{var:1} [Ini][Turn 90º L]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.MOVE_FORWARD:
                    formatted = f"{var:1} [Ini][Move Forward]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.DO_NOTHING:
                    formatted = f"{var:1} [Ini][Do Nothing]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.TURN_60_LEFT:
                    formatted = f"{var:1} [Ini][Turn 60º L]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.TURN_60_RIGHT:
                    formatted = f"{var:1} [Ini][Turn 60º R]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.START_SAVING:
                    formatted = f"{var:1} [Ini][Start Saving]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.STOP_SAVING:
                    formatted = f"{var:1} [Ini][Stop Saving]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.TURN_22_5_LEFT:
                    formatted = f"{var:1} [Ini][Turn 22.5º L]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.TURN_22_5_RIGHT:
                    formatted = f"{var:1} [Ini][Turn 22.5º R]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.CHANGE_COLOR_BROWN:
                    formatted = f"{var:1} [Ini][Color: Brown]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.CHANGE_COLOR_GREEN:
                    formatted = f"{var:1} [Ini][Color: Green]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.CHANGE_COLOR_BLUE:
                    formatted = f"{var:1} [Ini][Color: Blue]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.CHANGE_COLOR_PURPLE:
                    formatted = f"{var:1} [Ini][Color: Purple]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
        else:
            match canvas.variable_meanings[var]:
                case ConstantMeanings.TURN_90_RIGHT:
                    formatted = f"{var:1} [Turn 90º R]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.TURN_90_LEFT:
                    formatted = f"{var:1} [Turn 90º L]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.MOVE_FORWARD:
                    formatted = f"{var:1} [Move Forward]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.DO_NOTHING:
                    formatted = f"{var:1} [Do Nothing]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.TURN_60_LEFT:
                    formatted = f"{var:1} [Turn 60º L]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.TURN_60_RIGHT:
                    formatted = f"{var:1} [Turn 60º R]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.START_SAVING:
                    formatted = f"{var:1} [Start Saving]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.STOP_SAVING:
                    formatted = f"{var:1} [Stop Saving]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.TURN_22_5_LEFT:
                    formatted = f"{var:1} [Turn 22.5º L]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.TURN_22_5_RIGHT:
                    formatted = f"{var:1} [Turn 22.5º R]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.CHANGE_COLOR_BROWN:
                    formatted = f"{var:1} [Color: Brown]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.CHANGE_COLOR_GREEN:
                    formatted = f"{var:1} [Color: Green]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.CHANGE_COLOR_BLUE:
                    formatted = f"{var:1} [Color: Blue]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
                case ConstantMeanings.CHANGE_COLOR_PURPLE:
                    formatted = f"{var:1} [Color: Purple]{'':1}(Var)"
                    listbox.insert(tk.END, formatted)
    for var in canvas.list_constants():
        match canvas.constant_meanings[var]:
            case ConstantMeanings.TURN_90_RIGHT:
                formatted = f"{var:1} [Turn 90º R]{'':1}(Const)"
                listbox.insert(tk.END, formatted)
            case ConstantMeanings.TURN_90_LEFT:
                formatted = f"{var:1} [Turn 90º L]{'':1}(Const)"
                listbox.insert(tk.END, formatted)
            case ConstantMeanings.MOVE_FORWARD:
                formatted = f"{var:1} [Move Forward]{'':1}(Const)"
                listbox.insert(tk.END, formatted)
            case ConstantMeanings.DO_NOTHING:
                formatted = f"{var:1} [Do Nothing]{'':1}(Const)"
                listbox.insert(tk.END, formatted)
            case ConstantMeanings.TURN_60_LEFT:
                formatted = f"{var:1} [Turn 60º L]{'':1}(Const)"
                listbox.insert(tk.END, formatted)
            case ConstantMeanings.TURN_60_RIGHT:
                formatted = f"{var:1} [Turn 60º R]{'':1}(Const)"
                listbox.insert(tk.END, formatted)
            case ConstantMeanings.START_SAVING:
                formatted = f"{var:1} [Start Saving]{'':1}(Const)"
                listbox.insert(tk.END, formatted)
            case ConstantMeanings.STOP_SAVING:
                formatted = f"{var:1} [Stop Saving]{'':1}(Const)"
                listbox.insert(tk.END, formatted)
            case ConstantMeanings.TURN_22_5_LEFT:
                formatted = f"{var:1} [Turn 22.5º L]{'':1}(Const)"
                listbox.insert(tk.END, formatted)
            case ConstantMeanings.TURN_22_5_RIGHT:
                formatted = f"{var:1} [Turn 22.5º R]{'':1}(Const)"
                listbox.insert(tk.END, formatted)
            case ConstantMeanings.CHANGE_COLOR_BROWN:
                formatted = f"{var:1} [Color: Brown]{'':1}(Const)"
                listbox.insert(tk.END, formatted)
            case ConstantMeanings.CHANGE_COLOR_GREEN:
                formatted = f"{var:1} [Color: Green]{'':1}(Const)"
                listbox.insert(tk.END, formatted)
            case ConstantMeanings.CHANGE_COLOR_BLUE:
                formatted = f"{var:1} [Color: Blue]{'':1}(Const)"
                listbox.insert(tk.END, formatted)
            case ConstantMeanings.CHANGE_COLOR_PURPLE:
                formatted = f"{var:1} [Color: Purple]{'':1}(Const)"
                listbox.insert(tk.END, formatted)

def toggle_turtle(canvas, turtle, bool):
    canvas.show_turtle = bool
    if canvas.show_turtle:
        turtle.showturtle()
    else:
        turtle.hideturtle()

def toggle_turtle_from_var(canvas, turtle, bool):
    toggle_turtle(canvas, turtle, bool.get())

def add_variable_from_text(textarea_var, canvas, listbox, combo_ini, combo_vars):
    text = textarea_var.get("1.0", "end-1c")
    meaning = combo_vars.get()
    add_variable(text, canvas, listbox, combo_ini, meaning)
    textarea_var.delete("1.0", tk.END)

def add_variable(text, canvas, listbox, combo_ini, meaning):
    canvas.add_variable(text, meaning)
    listbox.delete(0, tk.END)
    refresh_listbox(canvas, listbox)

    combo_ini.set(canvas.list_variables()[0])
    combo_ini['values'] = canvas.list_variables()

def add_constant_from_text(textarea_const, canvas, listbox, combo):
    text = textarea_const.get("1.0", "end-1c")
    meaning = combo.get()
    add_constant(text, canvas, listbox, meaning)
    textarea_const.delete("1.0", tk.END)

def add_constant(text, canvas, listbox, meaning):
    canvas.add_constant(text, meaning)
    listbox.delete(0, tk.END)
    refresh_listbox(canvas, listbox)

def remove_item(canvas, listbox, combo_ini, ruleslist):
    remove_that_item(canvas, listbox, combo_ini, ruleslist, listbox_selected(listbox))

def remove_that_item(canvas, listbox, combo_ini, ruleslist, selected):
    canvas.remove_item(selected)
    listbox.delete(0, tk.END)
    refresh_listbox(canvas, listbox)
    if not canvas.list_variables():
        combo_ini.set("No Variables") 
    combo_ini['values'] = canvas.list_variables()
    rules_copy = list(canvas.rules_list())
    for rule in rules_copy:
        base, result = rule.separate(False)
        if selected == base or selected in result:
            canvas.remove_rule(rule)
    refresh_rules(canvas, ruleslist)

def set_initial(canvas, combo, listbox):
    set_that_as_initial(canvas, listbox, combo.get())

def set_that_as_initial(canvas, listbox, variable):
    canvas.initial = variable
    refresh_listbox(canvas, listbox)

def add_rule_from_text(canvas, base, result, ruleslist):
    add_rule(canvas, base.get("1.0", "end-1c"), result.get("1.0", "end-1c"), ruleslist)

def add_rule(canvas, base, result, ruleslist):
    rule = Rule(base, result)
    canvas.add_rule(rule)
    refresh_rules(canvas, ruleslist)

def rule_selected(ruleslist):
    selected = ruleslist.curselection()
    if not selected:
        return
    else:
        base = ruleslist.get(selected[0]).split(" ")[0]
        result = ruleslist.get(selected[0]).split("--> ")[1]
        return Rule(base, result)
    
def refresh_rules(canvas, ruleslist):
    ruleslist.delete(0, tk.END)
    for rule in canvas.rules_list():
        base, result = rule.separate(True)
        formatted = f'{base} --> {result}'
        ruleslist.insert(tk.END, formatted)

def remove_rule(canvas, ruleslist):
    selected = rule_selected(ruleslist)
    remove_that_rule(canvas, ruleslist, selected)

def remove_that_rule(canvas, ruleslist, selected):
    canvas.remove_rule(selected)
    ruleslist.delete(0, tk.END)
    refresh_rules(canvas, ruleslist)

def save_to_image(tk_canvas, turtle, canvas):
    turtle.hideturtle()
    os.makedirs("practica_4/exported", exist_ok=True)

    filename = filedialog.asksaveasfilename(
        title="Save L-System as...",
        initialdir="practica_4/exported",
        defaultextension=".svg",
        filetypes=[("SVG files", "*.svg")]
    )
    if not filename:
        if canvas.show_turtle:
            turtle.showturtle()
        return
    
    canvasvg.saveall(filename, tk_canvas)
    if canvas.show_turtle:
        turtle.showturtle()

def draw_system(canvas, textarea_iters, turtle, color_label):
    canvas.should_draw = True
    rules = canvas.rules_list()
    var_meanings = canvas.variable_meanings
    const_meanings = canvas.constant_meanings
    meanings = var_meanings | const_meanings
    iterations = int(textarea_iters.get("1.0", "end-1c"))

    toggle_turtle(canvas, turtle, True)

    # First we calculate the nth result of applying the rules
    partial = canvas.initial_list()
    for _ in range(0, iterations):
        partial_iter = []
        for j in range(0, len(partial)):
            found = False
            for rule in rules:
                base, result = rule.separate(False)
                if base == partial[j]:
                    partial_iter.extend(result)
                    found = True
                    break # We already found the matching rule
            if not found:
                partial_iter.append(partial[j])
        partial = partial_iter
    print(partial)

    # Then we follow the movements according to the var/const meanings of the result of that nth iteration
    save_stack = []
    i = 0
    for symbol in partial:
        print(f'Symbol {i} out of {len(partial)}')
        i += 1
        if not canvas.should_draw:
            return
        else:
            match meanings[symbol]:
                case ConstantMeanings.TURN_90_RIGHT:
                    turtle.right(90)
                case ConstantMeanings.TURN_90_LEFT:
                    turtle.left(90)
                case ConstantMeanings.DO_NOTHING:
                    pass
                case ConstantMeanings.MOVE_FORWARD:
                    turtle.forward(5)
                case ConstantMeanings.TURN_60_RIGHT:
                    turtle.right(60)
                case ConstantMeanings.TURN_60_LEFT:
                    turtle.left(60)
                case ConstantMeanings.START_SAVING:
                    pos = turtle.position()
                    heading = turtle.heading()
                    save_stack.append((pos, heading))
                case ConstantMeanings.STOP_SAVING:
                    pos, heading = save_stack.pop()
                    turtle.penup()
                    turtle.setposition(pos)
                    turtle.setheading(heading)
                    turtle.pendown()
                case ConstantMeanings.TURN_22_5_RIGHT:
                    turtle.right(22.5)
                case ConstantMeanings.TURN_22_5_LEFT:
                    turtle.left(22.5)
                case ConstantMeanings.CHANGE_COLOR_BROWN:
                    change_color(turtle, color_label, (None, "#804000"))
                case ConstantMeanings.CHANGE_COLOR_GREEN:
                    change_color(turtle, color_label, (None, "#80ff80"))
                case ConstantMeanings.CHANGE_COLOR_BLUE:
                    change_color(turtle, color_label, (None, "#1D72DB"))
                case ConstantMeanings.CHANGE_COLOR_PURPLE:
                    change_color(turtle, color_label, (None, "#961DE1"))

def clear_canvas(turtle, canvas):
    canvas.should_draw = False
    turtle.penup()
    turtle.home()
    turtle.clear() 
    turtle.setheading(0)
    turtle.pendown()

def clear_everything(canvas, listbox, combo_ini, ruleslist):
    for item in canvas.list_var_const():
        remove_that_item(canvas, listbox, combo_ini, ruleslist, item)
    for rule in canvas.rules_list():
        remove_that_rule(canvas, ruleslist, rule)

def change_color(turtle, color_label, color=None):
    if color is None:
        c = colorchooser.askcolor(title="Pick drawing color")
        if c[1] is None:
            return
    else:
        c = color
    
    turtle.color(c[1])
    color_label.config(text=f'Color: {c[1]}')

def input_presets(preset, canvas, listbox, ruleslist, combo_ini, turtle, textarea_iters=None):
    clear_everything(canvas, listbox, combo_ini, ruleslist)
    turtle.setheading(0)
    if textarea_iters:
        textarea_iters.delete("1.0", "end")
    match preset:
        case PRESETS.KOCH:
            add_variable("F", canvas, listbox, combo_ini, ConstantMeanings.MOVE_FORWARD)
            add_constant("+", canvas, listbox, ConstantMeanings.TURN_90_LEFT)
            add_constant("-", canvas, listbox, ConstantMeanings.TURN_90_RIGHT)
            set_that_as_initial(canvas, listbox, "F")
            add_rule(canvas, "F", "F+F-F-F+F", ruleslist)
            textarea_iters.insert("1.0", "5")
        case PRESETS.SIERPINSKI_T:
            add_variable("A", canvas, listbox, combo_ini, ConstantMeanings.MOVE_FORWARD)
            add_variable("B", canvas, listbox, combo_ini, ConstantMeanings.MOVE_FORWARD)
            add_constant("+", canvas, listbox, ConstantMeanings.TURN_60_LEFT)
            add_constant("-", canvas, listbox, ConstantMeanings.TURN_60_RIGHT)
            set_that_as_initial(canvas, listbox, "A")
            add_rule(canvas, "A", "B-A-B", ruleslist)
            add_rule(canvas, "B", "A+B+A", ruleslist)
            textarea_iters.insert("1.0", "8")
        case PRESETS.DRAGON:
            add_variable("X", canvas, listbox, combo_ini, ConstantMeanings.DO_NOTHING)
            add_variable("Y", canvas, listbox, combo_ini, ConstantMeanings.DO_NOTHING)
            add_variable("F", canvas, listbox, combo_ini, ConstantMeanings.MOVE_FORWARD)
            add_constant("+", canvas, listbox, ConstantMeanings.TURN_90_LEFT)
            add_constant("-", canvas, listbox, ConstantMeanings.TURN_90_RIGHT)
            set_that_as_initial(canvas, listbox, "FX")
            add_rule(canvas, "X", "X+YF+", ruleslist)
            add_rule(canvas, "Y", "-FX-Y", ruleslist)
            textarea_iters.insert("1.0", "10")
        case PRESETS.SQUARE_PATTERN:
            add_variable("F", canvas, listbox, combo_ini, ConstantMeanings.MOVE_FORWARD)
            add_constant("+", canvas, listbox, ConstantMeanings.TURN_90_LEFT)
            add_constant("-", canvas, listbox, ConstantMeanings.TURN_90_RIGHT)
            set_that_as_initial(canvas, listbox, "F-F-F-F")
            add_rule(canvas, "F", "FF-F-F-F-FF", ruleslist)
            textarea_iters.insert("1.0", "4")
        case PRESETS.HEX_GOSPER:
            add_variable("A", canvas, listbox, combo_ini, ConstantMeanings.MOVE_FORWARD)
            add_variable("B", canvas, listbox, combo_ini, ConstantMeanings.MOVE_FORWARD)
            add_constant("+", canvas, listbox, ConstantMeanings.TURN_60_LEFT)
            add_constant("-", canvas, listbox, ConstantMeanings.TURN_60_RIGHT)
            set_that_as_initial(canvas, listbox, "A")
            add_rule(canvas, "A", "A+B++B-A--AA-B+", ruleslist)
            add_rule(canvas, "B", "-A+BB++B+A--A-B", ruleslist)
            textarea_iters.insert("1.0", "4")
        case PRESETS.DENSE_TREE:
            turtle.left(90)
            add_variable("F", canvas, listbox, combo_ini, ConstantMeanings.MOVE_FORWARD)
            add_constant("+", canvas, listbox, ConstantMeanings.TURN_22_5_LEFT)
            add_constant("-", canvas, listbox, ConstantMeanings.TURN_22_5_RIGHT)
            add_constant("[", canvas, listbox, ConstantMeanings.START_SAVING)
            add_constant("]", canvas, listbox, ConstantMeanings.STOP_SAVING)
            set_that_as_initial(canvas, listbox, "F")
            add_rule(canvas, "F", "FF-[-F+F+F]+[+F-F-F]", ruleslist)
            textarea_iters.insert("1.0", "4")
        case PRESETS.BRANCH:
            add_variable("F", canvas, listbox, combo_ini, ConstantMeanings.MOVE_FORWARD)
            add_variable("X", canvas, listbox, combo_ini, ConstantMeanings.MOVE_FORWARD)
            add_constant("+", canvas, listbox, ConstantMeanings.TURN_22_5_LEFT)
            add_constant("-", canvas, listbox, ConstantMeanings.TURN_22_5_RIGHT)
            add_constant("[", canvas, listbox, ConstantMeanings.START_SAVING)
            add_constant("]", canvas, listbox, ConstantMeanings.STOP_SAVING)
            set_that_as_initial(canvas, listbox, "X")
            add_rule(canvas, "X", "F-[[X]+X]+F[+FX]-X", ruleslist)
            add_rule(canvas, "F", "FF", ruleslist)
            textarea_iters.insert("1.0", "5")
        case PRESETS.CORAL:
            turtle.left(90)
            add_variable("F", canvas, listbox, combo_ini, ConstantMeanings.MOVE_FORWARD)
            add_constant("+", canvas, listbox, ConstantMeanings.TURN_22_5_LEFT)
            add_constant("-", canvas, listbox, ConstantMeanings.TURN_22_5_RIGHT)
            add_constant("[", canvas, listbox, ConstantMeanings.START_SAVING)
            add_constant("]", canvas, listbox, ConstantMeanings.STOP_SAVING)
            set_that_as_initial(canvas, listbox, "F")
            add_rule(canvas, "F", "F[+F]F[-F]F", ruleslist)
            textarea_iters.insert("1.0", "5")
        case PRESETS.DENSE_CORAL:
            turtle.left(90)
            add_variable("F", canvas, listbox, combo_ini, ConstantMeanings.MOVE_FORWARD)
            add_constant("+", canvas, listbox, ConstantMeanings.TURN_22_5_LEFT)
            add_constant("-", canvas, listbox, ConstantMeanings.TURN_22_5_RIGHT)
            add_constant("[", canvas, listbox, ConstantMeanings.START_SAVING)
            add_constant("]", canvas, listbox, ConstantMeanings.STOP_SAVING)
            set_that_as_initial(canvas, listbox, "F")
            add_rule(canvas, "F", "F[-F]F[+F][F]", ruleslist)
            textarea_iters.insert("1.0", "4")
        case PRESETS.WINDY_TREE:
            turtle.left(90)
            add_variable("F", canvas, listbox, combo_ini, ConstantMeanings.MOVE_FORWARD)
            add_constant("+", canvas, listbox, ConstantMeanings.TURN_22_5_LEFT)
            add_constant("-", canvas, listbox, ConstantMeanings.TURN_22_5_RIGHT)
            add_constant("[", canvas, listbox, ConstantMeanings.START_SAVING)
            add_constant("]", canvas, listbox, ConstantMeanings.STOP_SAVING)
            set_that_as_initial(canvas, listbox, "F")
            add_rule(canvas, "F", "FFF[+F+F+F][-F+F+F+F+F]", ruleslist)
            textarea_iters.insert("1.0", "3")
        case PRESETS.COLORED_BRANCH:
            add_variable("F", canvas, listbox, combo_ini, ConstantMeanings.MOVE_FORWARD)
            add_variable("X", canvas, listbox, combo_ini, ConstantMeanings.MOVE_FORWARD)
            add_constant("+", canvas, listbox, ConstantMeanings.TURN_22_5_LEFT)
            add_constant("-", canvas, listbox, ConstantMeanings.TURN_22_5_RIGHT)
            add_constant("[", canvas, listbox, ConstantMeanings.START_SAVING)
            add_constant("]", canvas, listbox, ConstantMeanings.STOP_SAVING)
            add_constant("b", canvas, listbox, ConstantMeanings.CHANGE_COLOR_BROWN)
            add_constant("g", canvas, listbox, ConstantMeanings.CHANGE_COLOR_GREEN)
            set_that_as_initial(canvas, listbox, "X")
            add_rule(canvas, "X", "bF-[[gX]+gX]+bF[+bFgX]-gX", ruleslist)
            add_rule(canvas, "F", "bFF", ruleslist)
            textarea_iters.insert("1.0", "5")
        case PRESETS.COLORED_SQUARE_PATTERN:
            add_variable("F", canvas, listbox, combo_ini, ConstantMeanings.MOVE_FORWARD)
            add_constant("+", canvas, listbox, ConstantMeanings.TURN_90_LEFT)
            add_constant("-", canvas, listbox, ConstantMeanings.TURN_90_RIGHT)
            add_constant("p", canvas, listbox, ConstantMeanings.CHANGE_COLOR_PURPLE)
            add_constant("l", canvas, listbox, ConstantMeanings.CHANGE_COLOR_BLUE)
            add_constant("b", canvas, listbox, ConstantMeanings.CHANGE_COLOR_BROWN)
            set_that_as_initial(canvas, listbox, "F-F-F-F")
            add_rule(canvas, "F", "pFFl-F-Fb-F-FpF", ruleslist)
            textarea_iters.insert("1.0", "4")