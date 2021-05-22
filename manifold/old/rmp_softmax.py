from manimlib.imports import *
import os
import pyclbr

class RMPSoftMax(Scene):
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

        formula = TexMobject("f_{g}(x, \dot{x}) = \\alpha\\ s(x_{g} -x)")
        formula.bg=BackgroundRectangle(formula,fill_opacity=1)
        label_group = VGroup(formula.bg, formula)  # Order matters
        label_group.scale(1.25)
        label_group.move_to(UP*3.5+LEFT*3.5)

        self.play(ShowCreation(source_charge))
        self.add_foreground_mobject(source_charge)

        self.play(ShowCreation(label_group))
        self.add_foreground_mobject(label_group)

        self.wait(5)
        self.play(ShowCreation(field))
        self.wait(5)
        self.play(ShowCreation(self.lines))
        self.moving_charge()

    def h(self, z):
        c = 0.05
        h=  z + c * np.log(1.0+np.exp(-2.0*c*z))
        return h



    def field_at_point(self, point):
        alpha =1.5
        v = (self.goal_loc - point)
        s = v/self.h(np.linalg.norm(v))
        return alpha * s

    def calc_field_simpleA(self, point):
        efield = self.field_at_point(point)
        v = Vector(efield).shift(point)
        v.scale(0.33)
        v.tip.scale_handle_to_anchor_distances(0.5)
        return v

    def moving_charge(self):
        numb_charges = 1

        self.start_particle =  self.RoundMarker("S")
        self.start_particle.move_to(self.start_loc)
        self.start_particle.velocity = np.array((0, 0, 0))
        self.wait(5)

        self.play(FadeIn(self.start_particle))
        self.add_foreground_mobjects(self.start_particle)
        self.always_update_mobjects = True
        self.wait(20)

    def update_mobjects(self, *args, **kwargs):
        if hasattr(self, "start_particle"):
            dt = 1 / self.camera.frame_rate

            accel = self.field_at_point(self.start_particle.get_center())
            p1 = self.start_particle.get_center()

            self.start_particle.velocity = self.start_particle.velocity + accel * dt
            self.start_particle.shift(self.start_particle.velocity * dt)
            p2 = self.start_particle.get_center()
            l = Line(p1,p2)
            l.set_stroke(GREEN)
            self.lines.add(l)



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

