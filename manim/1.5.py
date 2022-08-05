from manim import *
import numpy as np
from utils import ChangingMatrix
# size = (2, 2)
#         bounds = (-10, 10)
#         iterations = 100
#         arr = [[[np.round(bounds[0]+(bounds[1]-bounds[0])*np.random.random(), decimals=2) for y in range(size[1])] for x in range(size[0])] for _ in range(iterations)]
        
#         m = arr.pop()
#         eq = MathTex("trace(M) = " + str(np.round(np.trace(m), decimals=2)))
#         mg = Group(MathTex("M = "), Matrix(m, h_buff=1.6))

#         g = Group(mg.arrange(), eq).arrange(direction=DOWN)
#         self.add(g)
        
#         eq2 = MathTex("det(M) = " + str(np.round(np.linalg.det(m), decimals=2))).move_to(eq)
#         self.play(TransformMatchingShapes(eq, eq2))
#         g = Group(mg.arrange(), eq2).arrange(direction=DOWN)
        
#         total, n = np.round(np.linalg.det(m), decimals=2), 1
#         averageEq = MathTex("Average = " + str(np.round(total/n, decimals=2)))

#         g2 = Group(Group(MathTex("M = "), Matrix(m, h_buff=1.6)).arrange(), eq2.copy(), averageEq.copy()).arrange(direction=DOWN)
#         self.remove(eq2, mg)
#         self.play(TransformMatchingShapes(g, g2))
#         self.remove(g2)
        
#         # ensemble = [Group]
#         for i in range(10):
#             self.wait(0.5)
#             self.remove(g2)
#             m = arr.pop()
#             eq2 = MathTex("det(M) = " + str(np.round(np.linalg.det(m), decimals=2)))
#             total += np.round(np.linalg.det(m), decimals=2)
#             n += 1
#             averageEq = MathTex("Average = " + str(np.round(total/n, decimals=2)))
#             g2 = Group(Group(MathTex("M = "), Matrix(m, h_buff=1.6)).arrange(), eq2, averageEq).arrange(direction=DOWN)
#             self.add(g2)
        
#         # t = ValueTracker(0)
#         # g = Group()
#         # self.add(g)
#         # g.add_updater(lambda g: g.become(ensemble[int(t.get_value())]))
#         # self.play(t.animate.set_value(9))
        
#         self.wait(5)



class EnsembleAverage(Scene):
    def construct(self):

        # m = DecimalMatrix([[1, 0], [0, 0]])
        # print(m[0][0])
        # return
        np.random.seed(1)

        size, bounds = (2, 2), (-10, 10)
        iterations = 100
        matricies = [np.round(bounds[0]+(bounds[1]-bounds[0])*np.random.rand(size[0], size[1]), decimals=2) for _ in range(iterations)]
        matricies[0][1][1] = np.abs(matricies[0][1][1])
        dets = [np.round(np.linalg.det(matricies[i]), decimals=2) for i in range(len(matricies))]
        adets = []
        t = ValueTracker(0)
        
        matrix = ChangingMatrix(matricies,t).move_to(LEFT*0.5)
        # numsV = [[matrix.nums[x][y].get_value() for y in range(len(matrix.nums[0]))] for x in range(len(matrix.nums))]

        matrixLabel = MathTex("M = ").next_to(matrix, direction=LEFT)
        self.add(matrix, matrixLabel)
        nums = [[MathTex(str(matrix.nums[x][y].get_value())).move_to(matrix.nums[x][y]) for y in range(len(matrix.nums[0]))] for x in range(len(matrix.nums))]
        self.wait(1)

        entryEq = MathTex("M_{11} = ").next_to(matrix, direction=DOWN).shift(LEFT*1)
        self.play(nums[0][0].animate.next_to(entryEq), FadeIn(entryEq, scale=1.5))
        self.wait(1)

        traceEq = MathTex("trace(M) = ").move_to(entryEq, aligned_edge=LEFT)
        tracePlus = MathTex(" + ").next_to(nums[0][0].copy().next_to(traceEq))
        self.play(nums[0][0].animate.next_to(traceEq), nums[1][1].animate.next_to(tracePlus), Transform(entryEq, traceEq), FadeIn(tracePlus, scale=1.5))
        self.wait(0.5)
        trace = MathTex(str(np.round(np.trace(matricies[0]), decimals=2))).next_to(traceEq)
        traceRight = Group(nums[0][0], tracePlus, nums[1][1])
        self.play(Transform(traceRight, trace))
        self.wait(1)
        self.remove(entryEq)

        detEq = MathTex("det(M) = ").move_to(entryEq, aligned_edge=LEFT)
        nums = [[MathTex(str(matrix.nums[x][y].get_value())).move_to(matrix.nums[x][y]) for y in range(len(matrix.nums[0]))] for x in range(len(matrix.nums))]
        detRight = MathTex("(", nums[0][0].get_tex_string(), "*", nums[1][1].get_tex_string(), ") - (", nums[0][1].get_tex_string(), "*", nums[1][0].get_tex_string(), ")").next_to(detEq)
        self.play(FadeOut(traceRight, scale = 0.5), Transform(traceEq, detEq), TransformMatchingTex(Group(*nums[0], *nums[1]), detRight))
        self.wait(0.5)

        det = DecimalNumber(dets[0]).next_to(detEq)
        self.play(Transform(detRight, det))
        self.remove(traceEq, detRight)
        self.add(detEq, det)
        det.add_updater(lambda d: d.set_value(dets[int(t.get_value())]))
        self.wait(1)

        g = VGroup(matrixLabel, matrix, detEq, det)
        averageDetTex = MathTex("Average Det:")
        totalDets = [0]
        for x in dets:
            totalDets.append(totalDets[-1]+x)
        averageDet = DecimalNumber().add_updater(lambda a: a.set_value(np.round(totalDets[1+int(t.get_value())]/int(1+t.get_value()), decimals=2))).update()
        self.play(g.animate.shift(LEFT*3+UP*3).scale(0.4), FadeIn(VGroup(averageDetTex, averageDet.next_to(averageDetTex, direction=DOWN)).scale(2).move_to(RIGHT*3+UP*2)))

        # cg = VGroup()
        # cg.add_updater(lambda g: g.become(VGroup(matrix.copy(), detEq.copy(), det.copy())))
        # self.play(t.animate(rate_func=rate_functions.ease_in_quint).set_value(iterations-1), run_time=5)

        times = [0.4, 0.2, 0.1]
        # print(MobjectMatrix(matricies[0]).scale(0.4))
        cg = [VGroup(MobjectMatrix(matricies[i], lambda m: DecimalNumber(m)).scale(0.4).move_to(matrix), detEq.copy(), DecimalNumber(dets[i]).scale(0.4).move_to(det)) for i in range(iterations)]

        startCoords = DOWN*1.5+LEFT*2
        self.play(cg[0].animate.shift(startCoords), run_time=1)
        t.set_value(t.get_value()+1)
        self.play(cg[1].animate.shift(startCoords+RIGHT*2), run_time=0.7)
        t.set_value(t.get_value()+1)
        self.play(cg[2].animate.shift(startCoords+RIGHT*5), FadeIn(MathTex("...").scale(2).move_to(cg[1]).shift(RIGHT*1.5), scale=1.5), run_time=0.5)
        t.set_value(t.get_value()+1)

        # np.min(0.1, )
        for i in range(3, iterations-1):
            self.play(cg[i].animate.shift(startCoords+RIGHT*5), FadeOut(cg[i-1], shift=LEFT*1.5), run_time=times[np.min([2, int(i/5)])])
            t.set_value(t.get_value()+1)
        self.wait(1)

        sumTex = MathTex(r" = \frac{1}{n}" + " \sum_{i=0}^{n}det(M_i)").next_to(averageDet.copy().move_to(DOWN*1+LEFT*5).scale(0.5))
        self.play(FadeOut(averageDetTex, scale=0.5), averageDet.animate.move_to(DOWN*1+LEFT*5).scale(0.5), FadeIn(sumTex, scale=1.5))

        integralEqual = MathTex(" = ").next_to(sumTex)
        shortIntegral = MathTex(r"\int", "... ",  "dM").next_to(integralEqual)
        longIntegral = MathTex(r"\int", "f(M)*p(M) ",  "dM").next_to(integralEqual)
        b = Brace(shortIntegral)
        bTex = MathTex(r"\int\int\int\int ... dM_{11}dM_{12}dM_{21}dM_{22}").scale(0.4).next_to(b, direction=DOWN)
        b2 = Brace(longIntegral)

        self.play(FadeIn(shortIntegral, scale=1.5))
        self.play(FadeIn(b, scale=1.5), FadeIn(bTex, scale=1.5))
        self.wait(1)
        self.play(TransformMatchingTex(shortIntegral, longIntegral), TransformMatchingShapes(b, b2), bTex.animate.next_to(b2, direction=DOWN), FadeIn(integralEqual, scale=1.5))

        self.wait(5)
