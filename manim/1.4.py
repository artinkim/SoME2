from random import Random
from manim import *
import random
import math
import numpy as np

class ChangingMatrix(MobjectMatrix):
    
    def __init__(self, size, bounds, precision, vt):
        self.size = size
        self.bounds = bounds
        self.precision = precision
        self.nums = [[DecimalNumber() for _ in range(self.size[1])] for __ in range(self.size[0])]
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                # self.nums[x][y].arrange(direction=RIGHT)
                self.nums[x][y].add_updater(lambda d: d.set_value(np.round(vt.get_value()*0+self.bounds[0]+(self.bounds[1]-self.bounds[0])*np.random.random(), decimals=self.precision)))

        # self.add_updater(lambda m: vt*0)
        super().__init__(self.nums, h_buff=2, element_alignment_corner=DR)
        

class RandomMatrix(Scene):
    totalChanges = 10

    def construct(self):

        vt = ValueTracker(0)

        size = (3, 5)
        bounds = (1, 10)
        m = []
        m.append(MobjectMatrix([[DecimalNumber(np.round(bounds[0]+(bounds[1]-bounds[0])*np.random.random(), decimals=2)) for y in range(size[1])] for x in range(size[0])], h_buff = 1.6))
        signs = [" + ", " - "]
        m.append(MobjectMatrix([[MathTex(str(int(m[-1][0][size[1]*x+y].get_value()))+np.random.choice(signs)+str(np.random.randint(low=bounds[0], high=bounds[1]))+"i") for y in range(size[1])] for x in range(size[0])], h_buff = 2.6))
        m.append(MobjectMatrix([[MathTex(m[-1][0][size[1]*x+y].tex_string+np.random.choice(signs)+str(np.random.randint(low=bounds[0], high=bounds[1]))+"j"+np.random.choice(signs)+str(np.random.randint(low=bounds[0], high=bounds[1]))+"k") for y in range(size[1])] for x in range(size[0])], h_buff = 4.6))
        m.append(MobjectMatrix([[MathTex(m[-1][0][size[1]*x+y].tex_string+np.random.choice(signs)+"...") for y in range(size[1])] for x in range(size[0])], h_buff = 5.4))
        m.append(MobjectMatrix([
            [MathTex("M_{11}"), MathTex("M_{12}"), MathTex("..."), MathTex("M_{1P}")],
            [MathTex("M_{21}"), MathTex("M_{22}"), MathTex("..."), MathTex("M_{1P}")],
            [MathTex(), MathTex(), MathTex("..."), MathTex()],
            [MathTex("M_{N1}"), MathTex("M_{N2}"), MathTex("..."), MathTex("M_{NP}")]], h_buff = 1.6))
        m.append(MobjectMatrix([
            [MathTex("M_{11}"), MathTex("M_{12}"), MathTex("..."), MathTex("M_{1N}")],
            [MathTex("M_{21}"), MathTex("M_{22}"), MathTex("..."), MathTex("M_{1N}")],
            [MathTex(), MathTex(), MathTex("..."), MathTex()],
            [MathTex("M_{N1}"), MathTex("M_{N2}"), MathTex("..."), MathTex("M_{NN}")]], h_buff = 1.6))

        size = (5, 5)
        bounds = (-10, 10)
        m.append(MobjectMatrix([[DecimalNumber(np.round(bounds[0]+(bounds[1]-bounds[0])*np.random.random(), decimals=2)) for y in range(size[1])] for x in range(size[0])], h_buff = 1.6))
        m.append(ChangingMatrix(size=size, bounds=bounds, precision=2, vt=vt))
        
        for x in m:
            x.scale(0.5)
        a = m[0]
        self.add(a)
        self.play(Transform(a, m[1]))
        self.play(Transform(a, m[2]))
        self.play(Transform(a, m[3]))

        self.wait(1)
        self.play(Transform(a, m[4]))
        b = Brace(a)
        b1tex, b2tex = b.get_tex("N\\text{x}P"), b.get_tex("N\\text{x}N")
        self.add(b, b1tex)
        self.wait(1)
        self.play(Transform(a, m[5]), Transform(b1tex, b2tex))
        self.wait(1)
        self.remove(b, b1tex)
        self.play(Transform(a, m[-2]))
        # self.wait(0.5)
        self.remove(a)
        
        # self.add(a)
        # self.add(b, b1tex)
        # self.play(Transform(a, m[1]), Transform(b1tex, b2tex))
        # self.wait(1)
        # self.remove(b, b1tex)
        # for i in range(1, len(m)-2):
        #     self.play(Transform(a, m[i+1]))
        # self.remove(a)

        self.add(m[-1])
        self.play(vt.animate.set_value(1), run_time=5)
        self.remove(m[-1])

        m = []
        for _ in range(3):
            m.append(Matrix([[np.round(bounds[0]+(bounds[1]-bounds[0])*np.random.random(), decimals=2) for y in range(size[1])] for x in range(size[0])], h_buff = 1.6))
            m[-1].scale(0.5)
        
        # self.add(g)
        for i in range(3):
            self.add(m[i])
            # m[i].move_to(UP*1)
            self.wait(1)
            self.play(m[i].animate.scale(0.4).move_to(LEFT * 2*(1-i) + DOWN * 1.5))
            
        g = Group(m[0], m[1], m[2])
        self.remove(m[0], m[1], m[2])
        self.add(g)
        self.wait(1)
        a, b = MathTex("\\{"), MathTex("\\}")
        a.scale(1.7)
        b.scale(1.7)
        ensemble = Group(MathTex("ensemble: "), a, m[0].copy(), m[1].copy(), MathTex("..."), m[2].copy(), b).arrange_in_grid(rows=1, cols=7)
        self.play(TransformMatchingShapes(g, ensemble))
        # self.add(ensemble)

        self.wait(5)