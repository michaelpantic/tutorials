from manimlib.imports import *
import os
import pyclbr

class PlotTwoGraphsAtOnce(ThreeDScene):

    def construct(self):
        plane1 = NumberPlane()
        self.surface = self.ThreeDSurface()

        plane1.set_width(1)
        plane1.scale_in_place(6)
        plane1.move_to(LEFT*4)

        self.surface.move_to(RIGHT*4)
        self.set_camera_orientation(0.9, -1.4, 95   )

        self.play(
            ShowCreation(plane1)
        )
        self.play(ShowCreation(self.surface))

        self.sphere = Sphere()
        self.sphere.move_to(LEFT*4)
        self.sphere.set_fill_by_checkerboard(RED)
        self.sphere.scale_in_place(0.1)
        self.play(ShowCreation(self.sphere))

        self.sphere2 = Sphere()
        self.sphere2.move_to(RIGHT * 4)
        self.sphere2.set_fill_by_checkerboard(RED)
        self.sphere2.scale_in_place(0.1)
        self.play(ShowCreation(self.sphere2))

        self.vector = Line(UP)
        self.vector.move_to(LEFT * 4)

        self.vector2 = Line(UP)
        self.vector2.move_to(RIGHT * 4)

        self.wait(3)
        self.always_update_mobjects = True
        self.play(ShowCreation(self.vector2))
        self.play(ShowCreation(self.vector))
        self.wait(5)

    def update_mobjects(self, *args, **kwargs):
        if self.always_update_mobjects:
            dt = 1 / self.camera.frame_rate

            self.sphere.shift(dt*LEFT)
            self.vector.shift(dt*LEFT)

            p3d = self.surface.map(self.sphere.get_center()-LEFT*4)
            d3d = self.surface.J(self.sphere.get_center()-LEFT*4).dot(UP[0:2])
            print(p3d+RIGHT*4)
            print( p3d+RIGHT*4+d3d)
            print(self.vector2.get_start())
            print(self.vector2.get_end())

            self.sphere2.move_to(p3d+RIGHT*4)


            self.vector2.put_start_and_end_on(p3d+RIGHT*4, p3d+RIGHT*4+d3d)


    class ThreeDSurface(ParametricSurface):

        def __init__(self, **kwargs):
            kwargs = {
            "u_min": -2,
            "u_max": 2,
            "v_min": -2,
            "v_max": 2,
            "checkerboard_colors": [BLUE_D]
            }
            ParametricSurface.__init__(self, self.func, **kwargs)

        def map(self,point):
            return [point[0], point[1], point[0]**2 - point[1]**2]

        def J(self,point):
            j = np.zeros([2,3])
            j[0,0] = 1.0
            j[1,1] = 1.0
            j[0,2] = 2 * point[0]
            j[1, 2] = 2 * point[1]
            return j.T


        def func(self, x, y):
            return np.array([x,y,x**2 - y**2])

    class RoundMarker(Circle):
        CONFIG = {
            "radius": 0.2,
            "stroke_width": 3,
            "color": GREEN,
            "fill_color": GREEN,
            "fill_opacity": 0.5,
        }

        def __init__(self, label,**kwargs):
            Circle.__init__(self, **kwargs)
            plus = TexMobject(label)
            plus.scale(0.7)
            plus.move_to(self)
            self.add(plus)