from manim import *
import numpy as np


class RenderConfig:
    left_offset = LEFT * 4
    right_offset = RIGHT * 4
    cam_pitch = 0.27 * np.pi
    cam_yaw = -0.65 * np.pi
    cam_neutral_yaw = -np.pi / 2.0

    resolution = (5, 5)



class Manifold3DAxes(VGroup):
    def __init__(self):
        self.config = {
            'color': BLACK,
            'stroke_color': BLACK,
            'x_length': 4.5,
            'y_length': 4.5,
            'z_length': 4,
            "x_range": np.array([-1, 1, 0.1]),
            "y_range": np.array([-1, 1, 0.1]),
            "z_range": np.array([-1, 1, 0.1]),
            "gloss": 0.0,
            'z_axis_config': {
                'color': BLACK,
                'stroke_color': BLACK
            },
            'x_axis_config': {
                'color': BLACK,
                'stroke_color': BLACK
            },
            'y_axis_config': {
                'color': BLACK,
                'stroke_color': BLACK
            }
        }
        VGroup.__init__(self, ThreeDAxes(**self.config))


class Manifold3D(ParametricSurface):
    def __init__(self, **kwargs):
        kwargs = {
            "u_min": -2,
            "u_max": 2,
            "v_min": -2,
            "v_max": 2,
            "resolution": RenderConfig.resolution,
            "checkerboard_colors": [BLUE_D]
        }
        ParametricSurface.__init__(self, self.func, **kwargs)

    def func(self, x, y):
        return np.array([x, y, np.sin(x) * np.cos(y)])


class Manifold2D(ParametricSurface):

    def __init__(self, **kwargs):
        kwargs = {
            "u_min": -2,
            "u_max": 2,
            "v_min": -2,
            "v_max": 2,
            "resolution": RenderConfig.resolution,
            "checkerboard_colors": [BLUE_D]
        }
        ParametricSurface.__init__(self, self.func, **kwargs)

    def func(self, x, y):
        return np.array([x, y, 0])


class Manifold2DAxes(Axes):
    def __init__(self):
        Axes.__init__(self, x_length=4.5, y_length=4.5, x_axis_config={'color': BLACK},
                      y_axis_config={'color': BLACK})
