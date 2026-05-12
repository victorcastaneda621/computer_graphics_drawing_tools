from basic_geometry.pixel_coordinates import Pixel
import constants

X_MIN, X_MAX = -2.0, 2.0
Y_MIN, Y_MAX = -2.0, 2.0

class JuliaStyle:

    GRAYSCALE = 0
    ORANGESCALE = 1
    GREEN_BLUE = 2
    GREEN_PINK = 3

    def all():
        return set([0, 1, 2, 3])

def calculate_julia(c: complex, n_iters, style):
    julia_points = []

    for z0y in range(-constants.CANVAS_HEIGHT, constants.CANVAS_HEIGHT):
        for z0x in range(-constants.CANVAS_WIDTH, constants.CANVAS_WIDTH):
            zx = X_MIN + (z0x + constants.CANVAS_WIDTH) * (X_MAX - X_MIN) / (2* constants.CANVAS_WIDTH)
            zy = Y_MIN + (z0y + constants.CANVAS_HEIGHT) * (Y_MAX - Y_MIN) / (2 * constants.CANVAS_HEIGHT)
            z = complex(zx, zy)
            iter = map_julia(z, c, n_iters, 0)
            julia_points.append((Pixel(z0x, z0y), iter))
    return draw_julia(julia_points, n_iters, style)

def map_julia(z, c, n_iters, iter):
    if abs(z) > 2: # Doesnt belog to Julia set for c
        return iter
    if iter >= n_iters: # Belogs to Julia set for c
        return n_iters
    # Still inside, and we havent reached n_iters
    return map_julia(z*z + c, c, n_iters, iter + 1)

def draw_julia(julia_points, n_iters, style):
    coloured_julia_points = []
    inside_color = (0,0,0,255)
    r = 0
    g = 0
    b = 0

    match style:
        case JuliaStyle.GRAYSCALE:
            inside_color = (0,0,0,255)
        case JuliaStyle.ORANGESCALE:
            inside_color = (230, 149, 0, 255)
        case JuliaStyle.GREEN_BLUE:
            inside_color = (255, 255, 0, 255)
        case JuliaStyle.GREEN_PINK:
            inside_color = (236, 128, 255, 255)

    for p, iter in julia_points:
        px, py = p.get_coords()
        if iter == n_iters: # Black
            coloured_julia_points.append(Pixel(px, py, inside_color))
        else: # Depending on how far the point was from being included in the set
            match style:
                case JuliaStyle.GRAYSCALE:
                    grayscale = 255 - int((255 * (iter + 1)) / (n_iters + 1))
                    r = grayscale
                    g = grayscale
                    b = grayscale
                case JuliaStyle.ORANGESCALE:
                    r = int((230 * (iter + 1)) / (n_iters + 1))
                    g = 149 + int(((255 - 149) * (iter + 1)) / (n_iters + 1))
                    b = int((255 * (iter + 1)) / (n_iters + 1))
                case JuliaStyle.GREEN_BLUE:
                    scale = (iter + 1) / (n_iters + 1)
                    g = int(255 - 215 * scale)
                    b = int(120 + 135 * scale)
                    r = 0
                case JuliaStyle.GREEN_PINK:
                    scale = (iter + 1) / (n_iters + 1)

                    r = int(236 * scale + 50 * (1- scale))
                    g = int(128 * scale + 220 * (1- scale))
                    b = int(255 * scale + 100 * (1- scale))

            coloured_julia_points.append(Pixel(px, py, (r,g,b,255)))
    return coloured_julia_points