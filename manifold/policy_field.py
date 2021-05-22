from manim import *
import numpy as np


class Manifold3D(ParametricSurface):

    def __init__(self, **kwargs):
        kwargs = {
            "u_min": -2,
            "u_max": 2,
            "v_min": -2,
            "v_max": 2,
            "resolution": (30, 30),
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
            "resolution": (30, 30),
            "checkerboard_colors": [BLUE_D]
        }
        ParametricSurface.__init__(self, self.func, **kwargs)

    def func(self, x, y):
        return np.array([x, y, 0])


class PolicyField(ThreeDScene):

    def __init__(self):
        super().__init__()
        config["frame_rate"] = 30

    def build_axes(self):
        axes = VGroup(
            ThreeDAxes(
                # z_min=-1,
                # z_max=20,
                **{
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
                        # 'include_numbers': True,

                        'color': BLACK,
                        'stroke_color': BLACK
                    },
                    'x_axis_config': {
                        # 'include_numbers': True,

                        'color': BLACK,
                        'stroke_color': BLACK
                    },
                    'y_axis_config': {
                        # 'include_numbers': True,

                        'color': BLACK,
                        'stroke_color': BLACK
                    }
                }
            )
        )

        self.three_d_axes = axes
        self.add(self.three_d_axes)

    def construct(self):
        left_offset = LEFT * 4
        right_offset = RIGHT * 4

        manifold3d = Manifold3D()
        self.build_axes()
        self.add(manifold3d)
        manifold3d_double = manifold3d.copy().shift(left_offset)
        manifold2d = Manifold2D().shift(left_offset)
        self.set_camera_orientation(0.27 * np.pi, -0.65 * np.pi, distance=150)
        self.renderer.camera.light_source.move_to(20 * IN + 20 * UP)
        self.begin_ambient_camera_rotation()

        self.wait(2.0)

        # move 3d stuff to the right and rotate
        self.play(manifold3d.animate.shift(right_offset),
                  self.three_d_axes.animate.shift(right_offset))
        self.wait(1.0)

        self.play(FadeIn(manifold3d_double))
        self.wait(2.0)
        graph = Axes(x_length=4.5, y_length=4.5, x_axis_config={'color': BLACK},
                     y_axis_config={'color': BLACK}).shift(left_offset)

        self.play(ReplacementTransform(manifold3d_double, manifold2d), FadeIn(graph))

        self.wait(2.0)
        self.stop_ambient_camera_rotation()
        self.move_camera(0.27 * np.pi, -np.pi / 2.0, added_anims=[Rotate(manifold2d, 0.27 * np.pi, axis=RIGHT),
                                                                  Rotate(graph, 0.27 * np.pi, axis=RIGHT)])
        self.wait(2.0)


    # self.stop_3dillusion_camera_rotation()
    # self.move_camera(0.4 * np.pi, -np.pi / 2.0)

    #
    # self.wait(2.0)
