import numpy as np

class Fractal:

    def __init__(self, lines):
        self.lines = lines

    def add_lines(self, new_lines):
        self.lines.extend(new_lines)

    def draw(self, batch):
        for line in self.lines:
            line.draw(batch)

class PointFractal(Fractal):
    def __init__(self, points):
        self.points = points

    def add_lines(self, new_points):
        self.points.extend(new_points)

    def draw(self, batch):
        for point in self.points:
            print(point.get_coords())
            point.draw(batch=batch)

class RECURSIVE:
    SIERPINSKY_TRIANGLE = 0
    KOCH_CURVE = 1
    KOCH_SNOWFLAKE = 2
    CANTOR_SET = 3

    def all():
        return set([0, 1, 2, 3])
    
class IFS:
    SIERPINSKY_TRIANGLE = 0
    KOCH_CURVE = 1
    KOCH_2 = 2
    CANTOR_SET = 3
    BARNSLEY_FERN = 4
    CHRISTMAS_TREE = 5
    BLOCKS = 6
    CLOUD = 7
    LEAF = 8
    NOISY = 9
    CHAOS = 10

    def all():
        return set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    
def get_ifs_functions(ifs):
    match ifs:
        case IFS.SIERPINSKY_TRIANGLE:
            return [(np.matrix([[0.5, 0], [0, 0.5]]), np.matrix([[-1], [1]])),
                    (np.matrix([[0.5, 0], [0, 0.5]]), np.matrix([[1], [1]])),
                    (np.matrix([[0.5, 0], [0, 0.5]]), np.matrix([[0], [-1]]))]
        case IFS.KOCH_CURVE:
            return [(np.matrix([[0.333, 0.0], [0.0, 0.333]]), np.matrix([[0.0], [0.0]])),
                    (np.matrix([[0.167, -0.288], [0.288, 0.167]]), np.matrix([[0.333], [0.0]])),
                    (np.matrix([[0.167, 0.288], [-0.288, 0.167]]), np.matrix([[0.5], [0.288]])),
                    (np.matrix([[0.333, 0.0], [0.0, 0.333]]), np.matrix([[0.667], [0.0]]))]
        case IFS.KOCH_2:
            return [(np.matrix([[0.31, 0.0], [0.0, 0.29]]), np.matrix([[4.12], [1.6]])),
                    (np.matrix([[0.19, -0.21], [0.65, 0.09]]), np.matrix([[-0.69], [5.98]])),
                    (np.matrix([[0.19, 0.21], [-0.65, 0.09]]), np.matrix([[0.67], [5.96]])),
                    (np.matrix([[0.31, 0.0], [0.0, 0.29]]), np.matrix([[-4.14], [1.6]])),
                    (np.matrix([[0.38, 0.0], [0.0, -0.29]]), np.matrix([[-0.01], [2.94]]))]
        case IFS.CANTOR_SET:
            return [(np.matrix([[0.33, 0.0], [0.0, 0.33]]), np.matrix([[0.0], [0.4]])),
                    (np.matrix([[0.33, 0.0], [0.0, 0.33]]), np.matrix([[0.67], [0.4]]))]
        case IFS.BARNSLEY_FERN: # TOO BIG
            return [(np.matrix([[0.81, 0.07], [-0.04, 0.84]]), np.matrix([[0.12], [0.195]])),
                    (np.matrix([[0.18, -0.25], [0.27, 0.23]]), np.matrix([[0.12], [0.02]])),
                    (np.matrix([[0.19, 0.275], [0.238, -0.14]]), np.matrix([[0.16], [0.12]])),
                    (np.matrix([[0.0235, 0.087], [0.045, 0.1666]]), np.matrix([[0.11], [0.0]]))]
        case IFS.CHRISTMAS_TREE:
            return [(np.matrix([[0.0, -0.5], [0.5, 0.0]]), np.matrix([[0.5], [0.0]])),
                    (np.matrix([[0.0, 0.5], [-0.5, 0.0]]), np.matrix([[0.5], [0.5]])),
                    (np.matrix([[0.5, 0.0], [0.0, 0.5]]), np.matrix([[0.25], [0.5]]))]
        case IFS.BLOCKS:
            return [(np.matrix([[0.0, 0.3], [0.54, 0.0]]), np.matrix([[0.69], [0.44]])),
                    (np.matrix([[-0.65, 0.0], [0.0, 0.41]]), np.matrix([[0.66], [0.57]])),
                    (np.matrix([[0.24, 0.0], [0.0, -0.32]]), np.matrix([[0.33], [0.35]])),
                    (np.matrix([[0.38, 0.0], [0.0, 0.41]]), np.matrix([[0.6], [0.02]])),
                    (np.matrix([[-0.28, 0.0], [0.0, -0.523]]), np.matrix([[0.3], [0.53]]))]
        
        case IFS.CLOUD:
            return [(np.matrix([[0.75, 0.0], [0.0, -0.75]]), np.matrix([[1.025], [8.419]])),
                    (np.matrix([[-0.75, 0.0], [0.0, 0.75]]), np.matrix([[-1.468], [1.203]])),
                    (np.matrix([[-0.75, 0.0], [0.0, 0.75]]), np.matrix([[-2.549], [2.283]])),
                    (np.matrix([[0.75, 0.0], [0.0, -0.75]]), np.matrix([[2.106], [7.338]]))]
        
        case IFS.LEAF:
            return [(np.matrix([[0.242,-0.640], [-0.909,-0.318]]), np.matrix([[4.612], [5.593]])),
                    (np.matrix([[-0.091,-0.557], [-0.485, 0.155]]), np.matrix([[-1.064], [5.654]]))]
        
        case IFS.NOISY:
            return [(np.matrix([[0.424, -0.651], [0.485, -0.345]]), np.matrix([[3.964], [4.222]])),
                    (np.matrix([[-0.08, -0.203], [-0.743, 0.205]]), np.matrix([[-4.092], [3.957]]))]
        case IFS.CHAOS:
            return [(np.matrix([[0.0, 0.053], [-0.429, 0.0]]), np.matrix([[-7.083], [5.43]])),
                    (np.matrix([[0.143, 0.0], [0.0, -0.053]]), np.matrix([[-5.619], [8.513]])),
                    (np.matrix([[0.143, 0.0], [0.0, 0.083]]), np.matrix([[-5.619], [2.057]])),
                    (np.matrix([[0.0, 0.053], [0.429, 0.0]]), np.matrix([[-3.952], [5.43]])),
                    (np.matrix([[0.119, 0.0], [0.0, 0.053]]), np.matrix([[-2.555], [4.536]])),
                    (np.matrix([[-0.0123806, -0.0649723], [0.423819, 0.00189797]]), np.matrix([[-1.226], [5.235]])),
                    (np.matrix([[0.0852291, 0.0506328], [0.420449, 0.0156626]]), np.matrix([[-0.421], [4.569]])),
                    (np.matrix([[0.104432, 0.00529117], [0.0570516, 0.0527352]]), np.matrix([[0.976], [8.113]])),
                    (np.matrix([[-0.00814186, -0.0417935], [0.423922, 0.00415972]]), np.matrix([[1.934], [5.37]])),
                    (np.matrix([[0.093, 0.0], [0.0, 0.053]]), np.matrix([[0.861], [4.536]])),
                    (np.matrix([[0.0, 0.053], [-0.429, 0.0]]), np.matrix([[2.447], [5.43]])),
                    (np.matrix([[0.119, 0.0], [0.0, -0.053]]), np.matrix([[3.363], [8.513]])),
                    (np.matrix([[0.119, 0.0], [0.0, 0.053]]), np.matrix([[3.363], [1.487]])),
                    (np.matrix([[0.0, 0.053], [0.429, 0.0]]), np.matrix([[3.972], [4.569]])),
                    (np.matrix([[0.123998, -0.00183957], [0.000691208, 0.0629731]]), np.matrix([[6.275], [7.716]])),
                    (np.matrix([[0.0, 0.053], [0.167, 0.0]]), np.matrix([[5.215], [6.483]])),
                    (np.matrix([[0.071, 0.0], [0.0, 0.053]]), np.matrix([[6.279], [5.298]])),
                    (np.matrix([[0.0, -0.053], [-0.238, 0.0]]), np.matrix([[6.805], [3.714]])),
                    (np.matrix([[-0.121, 0.0], [0.0, 0.053]]), np.matrix([[5.941], [1.487]]))]