from manim import *
from manifolds import *
import numpy as np


class Morph3d(ThreeDScene):

    def __init__(self):
        super().__init__()
        config["frame_rate"] = 30

    def construct(self):
        left_offset = RenderConfig.left_offset
        right_offset = RenderConfig.right_offset
        cam_pitch = RenderConfig.cam_pitch
        cam_yaw = RenderConfig.cam_yaw
        cam_neutral_yaw = RenderConfig.cam_neutral_yaw

        # create 3D manifold
        m_3d = Manifold3D()
        ax_3d = Manifold3DAxes()
        self.add(m_3d)
        self.add(ax_3d)

        # create 2D-3D manifold
        m_3d_double = m_3d.copy().shift(left_offset)
        m_2d = Manifold2D().shift(left_offset)
        ax_2d = Manifold2DAxes().shift(left_offset)

        # set scene
        self.set_camera_orientation(cam_pitch, cam_yaw, distance=150)
        self.renderer.camera.light_source.move_to(20 * IN + 20 * UP)
        self.begin_3dillusion_camera_rotation(rate=0.1)
        self.wait(2.0)

        # move 3d stuff to the right and rotate
        self.play(m_3d.animate.shift(right_offset),
                  ax_3d.animate.shift(right_offset))
        self.wait(1.0)

        # Fade in 3D double and morph to 2d
        self.play(FadeIn(m_3d_double))
        self.wait(2.0)
        self.play(ReplacementTransform(m_3d_double, m_2d), FadeIn(ax_2d))

        # move view to face 2D manifold
        self.wait(2.0)
        self.stop_3dillusion_camera_rotation()
        self.move_camera(cam_pitch, cam_neutral_yaw, added_anims=[Rotate(m_2d, cam_pitch, axis=RIGHT),
                                                               Rotate(ax_2d, cam_pitch, axis=RIGHT)])
        self.wait(2.0)

