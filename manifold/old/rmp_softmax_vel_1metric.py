from manimlib.imports import *
import os
import pyclbr

class RMPSoftMaxVelMetric(Scene):
    CONFIG = {
        "plane_kwargs": {
            "color": RED_B
        },
        "goal_loc": 1.75 * RIGHT - 0.5 * UP,
        "start_loc": 0.5 * LEFT + 0.5 * UP
    }

    def construct(self):

        plane = NumberPlane(**self.plane_kwargs)
        # plane.main_lines.fade(.9)  #Doesn't work in most recent commit
        plane.add(plane.get_axis_labels("x_{\mathcal{T}}","y_{\mathcal{T}}"))
        self.add(plane)
        self.start_particle = self.RoundMarker("S")
        self.start_particle.move_to(self.start_loc)
        self.start_particle.velocity = np.array((0, 0, 0))

        field = VGroup(*[self.calc_field_simpleA(x * RIGHT + y * UP)
                         for x in np.arange(-9, 9, 0.5)
                         for y in np.arange(-5, 4, 0.5)
                         ])

        self.lines = VGroup(*[])

        field.set_opacity(0.85)

        self.field = field

        source_charge = self.RoundMarker("G").move_to(self.goal_loc)
        source_charge.set_color(RED)
        source_charge.set_opacity(1.0)




        formula = TexMobject("f_{g}(x, \dot{x}) = \\alpha\\ s(x_{g} -x) - \\beta \dot{x}")
        formula.bg=BackgroundRectangle(formula,fill_opacity=1)
        metric = TexMobject("A = diag(1,0)")
        metric.bg = BackgroundRectangle(formula, fill_opacity=1)
        formula_group = VGroup(formula.bg, formula)  # Order matters
        metric_group = VGroup(metric.bg, metric)  # Order matters
        formula_group.scale(1.0)
        formula_group.move_to(UP*3.5+LEFT*3.25)
        metric_group.next_to(formula_group,DOWN)

        self.play(ShowCreation(source_charge))
        self.add_foreground_mobject(source_charge)

        self.play(ShowCreation(formula_group))
        self.add_foreground_mobject(formula_group)

        self.play(ShowCreation(metric_group))
        self.add_foreground_mobject(metric_group)

        self.wait(5)
        self.play(ShowCreation(field))

        self.play(ShowCreation(self.lines))
        self.moving_charge()

    def h(self, z):
        c = 0.05
        h=  z + c * np.log(1.0+np.exp(-2.0*c*z))
        return h



    def field_at_point(self, point):
        alpha =1.5
        beta = 4.0
        v = (self.goal_loc - point)
        s = v/self.h(np.linalg.norm(v))
        f = alpha * s - beta * self.start_particle.velocity
        f2 = alpha *s - 0.2* self.start_particle.velocity

        A = np.eye(3)
        A[1,1] = 0.0
        A2 = np.eye(3)
        A2[0,0] = 0.0

        J = np.eye(3)

        # puul backs
        h1 = np.linalg.pinv(J).dot(f)
        h2 = np.linalg.pinv(J).dot(f2)
        B1 = J.T.dot(A).dot(J)
        B2 = J.T.dot(A2).dot(J)

        # sum
        s1 = (B1)
        s2 = B1.dot(h1)
        return np.linalg.pinv(s1).dot(s2)


    def calc_field_simpleA(self, point):
        efield = self.field_at_point(point)
        v = Vector()
        v.put_start_and_end_on(point, point+efield/4)
        v.set_stroke(width=1.0)
        v.tip.scale_handle_to_anchor_distances(0.1)
        return v

    def moving_charge(self):
        numb_charges = 1


        self.play(FadeIn(self.start_particle))
        self.wait(5)

        self.add_foreground_mobjects(self.start_particle)
        self.always_update_mobjects = True
        self.wait(20)

    def update_mobjects(self, *args, **kwargs):
        if  self.always_update_mobjects:
            dt = 1 / self.camera.frame_rate

            accel = self.field_at_point(self.start_particle.get_center())
            p1 = self.start_particle.get_center()

            self.start_particle.velocity = self.start_particle.velocity + accel * dt
            self.start_particle.shift(self.start_particle.velocity * dt)
            p2 = self.start_particle.get_center()
            l = Line(p1,p2)
            l.set_stroke(GREEN)
            self.lines.add(l)

            # update field
            for v in self.field:
                v.put_start_and_end_on(v.get_start(), self.field_at_point(v.get_start())/4 + v.get_start())
                v.set_stroke(width=1.0)
                v.tip.scale_handle_to_anchor_distances(0.1)







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

