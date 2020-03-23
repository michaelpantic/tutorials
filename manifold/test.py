from manimlib.imports import *
import os
import pyclbr

class PlotTwoGraphsAtOnce(Scene):

    def construct(self):
        plane1 = NumberPlane()
        plane2 = NumberPlane()

        plane1.set_width(1)
        plane1.scale_in_place(6)

        self.play(
            ShowCreation(plane1)
        )

        self.wait(3)