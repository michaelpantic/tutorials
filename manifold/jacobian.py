from manim import *
from manifolds import *
import numpy as np


class Jacobian(ThreeDScene):

    def __init__(self):
        super().__init__()
        config["frame_rate"] = 30

    def m3d_pos(self, angle):
        vec3d = Vector(direction=UP, color=RED_D).shift(RenderConfig.right_offset)
        vec3d.shift(UP * angle / 720).rotate(
            angle * DEGREES, axis=OUT, about_point=RenderConfig.right_offset
        )

        vec3d_nonshift = Vector(direction=UP).shift(UP * angle / 720).rotate_about_origin(
            angle * DEGREES, axis=OUT)

        start_vec = self.m_3d.func(vec3d_nonshift.get_start()[0], vec3d_nonshift.get_start()[1])
        end_vec = self.m_3d.func(vec3d_nonshift.get_end()[0], vec3d_nonshift.get_end()[1])

        vec3d.put_start_and_end_on(start_vec, end_vec)

        return vec3d.shift(RenderConfig.right_offset)

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
        self.set_camera_orientation(cam_neutral_pitch, cam_neutral_yaw, distance=150)
        self.renderer.camera.light_source.move_to(20 * IN + 10 * RIGHT)
        self.wait(2.0)

        # create vector on 2D set and animate
        angle_tracker = ValueTracker(45)

        vec2d = Vector(direction=UP, color=RED_D).shift(RenderConfig.left_offset)
        vec2d_ref = vec2d.copy()
        vec2d.add_updater(lambda x: x.become(vec2d_ref.copy()).shift(UP * angle_tracker.get_value() / 720).
                          rotate(
            angle_tracker.get_value() * DEGREES, axis=OUT, about_point=RenderConfig.left_offset
        ))

        # create vector on 3D set and animate
        vec3d = Vector(direction=UP, color=RED_D).shift(RenderConfig.right_offset)
        vec3d_ref = vec3d.copy()

        vec3d.add_updater(lambda x: x.move_to(self.m3d_pos(angle_tracker.get_value())).become(
            self.m3d_pos(angle_tracker.get_value())))

        self.play(FadeIn(vec2d))
        speed = 10.0/360
        self.play(angle_tracker.animate.set_value(180), rate_func=wiggle, run_time=180*speed)
        self.move_camera(cam_neutral_pitch + 0.5, cam_neutral_yaw,
                         added_anims=[angle_tracker.animate(run_time=180*speed, rate_fun=wiggle).set_value(360), FadeIn(vec3d)],
                         rate_func=linear, run_time=180*speed)

        self.move_camera(cam_neutral_pitch + 1.0, cam_neutral_yaw,
                         added_anims=[angle_tracker.animate(run_time=360*speed, rate_fun=wiggle).set_value(720)],
                         rate_func=linear, run_time=6)
        self.begin_3dillusion_camera_rotation(rate=0.1, origin_phi=cam_neutral_pitch + 1.0, origin_theta=cam_neutral_yaw)
        self.play(angle_tracker.animate(run_time=360*speed, rate_fun=wiggle).set_value(360*3))
        self.play(angle_tracker.animate(run_time=360*3*speed, rate_fun=wiggle).set_value(0))
        self.stop_3dillusion_camera_rotation()
        self.wait(1.0)
