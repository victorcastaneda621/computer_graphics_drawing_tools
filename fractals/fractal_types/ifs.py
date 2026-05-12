import numpy as np
import random
from basic_geometry.pixel_coordinates import Pixel
import constants

def draw_ifs(functions: list, p_ini, n_iter, small=0.9, barnsley=False):
    det_total = 0
    functions_p = []
    min_x = 10000
    max_x = -10000
    min_y = 10000
    max_y = -10000
    # Calulate probabilites, and fill out the max and min while we're at it
    for fucntion_matrix, function_vector in functions:
        x = function_vector[0,0]
        y = function_vector[1,0]
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

        det = abs(np.linalg.det(fucntion_matrix))
        det_total += det
        functions_p.append((fucntion_matrix, function_vector, det))
        
    functions.clear()
    range_x = max_x - min_x
    range_y = max_y - min_y
    if range_y == 0:
        range_y = 1

    for fucntion_matrix, function_vector, det in functions_p:
        probability = det / det_total
        functions.append((fucntion_matrix, function_vector, probability))
    if barnsley:
        fs = sorted(functions, key=lambda x: x[2])
        functions.clear()
        i = 0
        values = [0.01, 0.25, 0.25, 0.49]
        for fm, fv, p in fs:
            print(p, values[i])
            functions.append((fm, fv, values[i]))
            i += 1

    p = np.matrix([[p_ini.get_coords()[0]], [p_ini.get_coords()[1]]])
    for i in range(0, 200):
        selected_f_matrix, selected_f_vector = select_f(functions)
        p = (selected_f_matrix @ p) + selected_f_vector

    points = []
    for i in range(0, n_iter):
        selected_f_matrix, selected_f_vector = select_f(functions)
        p = (selected_f_matrix @ p) + selected_f_vector
        points.append(scale(p, range_x, range_y, small))
    return points


def select_f(functions):
    matrices, vectors, probabilities = zip(*functions)
    chosen = random.choices(range(len(functions)), weights=probabilities, k=1)[0]
    return (matrices[chosen], vectors[chosen])

def scale(p, range_x, range_y, small):
    px = p[0, 0]
    py = p[1, 0]
    print(p)
    scale = small * min((constants.CANVAS_WIDTH)/range_x, (constants.CANVAS_HEIGHT)/range_y)
    px = px * scale
    py = py * scale
    return Pixel(px, py)