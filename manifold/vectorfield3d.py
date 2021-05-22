from manim import *
from manifolds import *
import numpy as np


class VectorField3d(ThreeDScene):

    def __init__(self):
        super().__init__()
        config["frame_rate"] = 30

    def m3d_pos(self, start, end):


        start_vec = self.m_3d.func(start[0], start[1])
        end_vec = self.m_3d.func(end[0], end[1])
        vec3d = Vector()
        vec3d.put_start_and_end_on(start_vec, end_vec)

        return vec3d

    def h(self, z):
        c = 0.05
        h = z + c * np.log(1.0 + np.exp(-2.0 * c * z))
        return h

    def field_at_point(self, point):
        alpha = 1.5
        v = (np.zeros(3) - point)
        s = v / self.h(np.linalg.norm(v))
        return alpha * s

    def calc_field_simpleA(self, point, offset):
        efield = self.field_at_point(point)
        v = Vector(efield * 0.2).shift(point + offset)
        v.set_stroke_width_from_length()
        # v.scale(0.01)
        v.tip.scale_handle_to_anchor_distances(0.01)

        return v

    def calc_field_simple3D(self, point, offset):
        efield = self.field_at_point(point)
        v = Vector(efield * 0.1).shift(point + offset)
        v = self.m3d_pos(v.get_start(), v.get_end())
        v.set_stroke_width_from_length()
        v.scale(0.01)
        v.tip.scale_handle_to_anchor_distances(0.01)

        return v

    def construct(self):
        left_offset = RenderConfig.left_offset
        right_offset = RenderConfig.right_offset
        cam_pitch = RenderConfig.cam_pitch
        cam_yaw = RenderConfig.cam_yaw
        cam_neutral_yaw = RenderConfig.cam_neutral_yaw
        cam_neutral_pitch = 0.0

        # create 3D manifold
        m_3d = Manifold3D().shift(right_offset)
        self.m_3d = m_3d
        ax_3d = Manifold3DAxes().shift(right_offset)
        self.add(m_3d)
        self.add(ax_3d)

        # create 2D manifold
        m_2d = Manifold2D().shift(left_offset)
        ax_2d = Manifold2DAxes().shift(left_offset)
        self.add(m_2d)
        self.add(ax_2d)

        # set scene
        self.set_camera_orientation(cam_neutral_pitch+1.0, cam_neutral_yaw, distance=150)
        self.renderer.camera.light_source.move_to(20 * IN + 10 * RIGHT)
        self.wait(2.0)

        # field
        field = VGroup(*[self.calc_field_simpleA(x * RIGHT + y * UP, RenderConfig.left_offset)
                         for x in np.arange(-4, 4, 0.25)
                         for y in np.arange(-4, 4, 0.25)
                         ])

        field3d = VGroup(*[self.calc_field_simple3D(x * RIGHT + y * UP, RenderConfig.right_offset)
                         for x in np.arange(-4, 4, 0.25)
                         for y in np.arange(-4, 4, 0.25)
                         ])

        self.play(FadeIn(field))
        self.play(FadeIn(field3d))
