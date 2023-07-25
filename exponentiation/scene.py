# UNFINISHED

from manim import *
import math

# TODO: add more staggered animations

# TODO: change color scheme?
blue = BLUE_D
green = GREEN_D
red = RED
box_color = YELLOW

title_size = 80
sub_size = 60
small_size = 40

title_buff = 1.25
line_buff = 0.75
box_buff = 0.25

tem = TexTemplate()
tem.add_to_preamble("\\usepackage{tgtermes}")

class StrikeOut(Line):
    def __init__(self, mobject, buff=0, color=red, **kwargs):
        super().__init__(mobject.get_left(), mobject.get_right(), buff=buff, color=color, **kwargs)

def tex_line(top, *args):
    t = Tex(*args, tex_template=tem, font_size=sub_size, color=blue)
    t.next_to(top, DOWN, aligned_edge=LEFT, buff=line_buff)
    return t

def mathtex_line(top, *args):
    t = MathTex(*args, tex_template=tem, font_size=sub_size, color=blue)
    t.next_to(top, DOWN, aligned_edge=LEFT, buff=line_buff)
    return t

class Exponentiation(Scene):
    def construct(self):
        # self.slide1()
        # self.slide2()
        # prod_eq, box = self.slide3()
        # self.slide4(prod_eq, box)
        # alg_def = self.slide5(prod_eq, box)
        # alg_title = self.slide6(alg_def)
        # self.slide7(alg_title, alg_def)
        ana = self.slide8()
        exp_title, exp_def = self.slide9(ana)
        self.slide10(exp_title, exp_def)
        self.wait(1)

    def play_equation(self, eq1, eq2, pairs, fade_first=False):
        fades = []
        anims = []
        seen1 = [False] * len(eq1)
        seen2 = [False] * len(eq2)
        for pair in pairs:
            anims.append(ReplacementTransform(eq1[pair[0]], eq2[pair[1]]))
            seen1[pair[0]] = True
            seen2[pair[1]] = True
        for i in range(len(eq1)):
            if not seen1[i]:
                fades.append(FadeOut(eq1[i]))
        for i in range(len(eq2)):
            if not seen2[i]:
                anims.append(FadeIn(eq2[i]))
        if fade_first:
            self.play(*fades)
            self.play(*anims)
        else:
            self.play(*fades, *anims)

    def slide1(self):
        title = Tex("What is $0^0$?", tex_template=tem, font_size=title_size)
        self.play(Write(title))
        self.play(title.animate.to_corner(UL, buff=title_buff))

        t1 = tex_line(title, "undefined?")
        self.play(FadeIn(t1))
        
        t2 = mathtex_line(t1, "0^x = 0").shift(RIGHT)
        self.play(FadeIn(t2))

        t3 = mathtex_line(t2, "x^0 = 1")
        self.play(FadeIn(t3))

        t4 = tex_line(t3, "one?").shift(LEFT)
        self.play(FadeIn(t4))

        alg = Tex("algebraic power", tex_template=tem, font_size=sub_size, color=green)
        alg.shift(RIGHT * 2 + DOWN * 1.75)
        self.play(FadeIn(alg))

        ana = Tex("analytic power", tex_template=tem, font_size=sub_size, color=green)
        ana.shift(RIGHT * 2 + UP * 0.5)
        self.play(FadeIn(ana))

        arr1 = Arrow(start=ana.get_left(), end=t1.get_right(), buff=0.25, color=green)
        self.play(GrowArrow(arr1, point_color=green))

        arr2 = Arrow(start=alg.get_left(), end=t4.get_right(), buff=0.25, color=green)
        self.play(GrowArrow(arr2, point_color=green))

        self.play(FadeOut(t1, t2, t3, t4, alg, ana, arr1, arr2))
        self.play(Unwrite(title, reverse=False))

    def slide2(self):
        title = Tex("Sum function", tex_template=tem, font_size=title_size)
        title.to_corner(UL, buff=title_buff)
        self.play(Write(title))

        t1 = mathtex_line(title, "\mathrm{Sum}(2, 3) = 5")
        self.play(FadeIn(t1))

        t2 = mathtex_line(t1, "\mathrm{Sum}(4, 11, 1", ",", "3", ") = 19")
        self.play(FadeIn(t2))

        t3 = mathtex_line(t2, "\mathrm{Sum}(\mathrm{stuff}, x) = \mathrm{Sum}(\mathrm{stuff}) + x")
        self.play(FadeIn(t3))

        t4 = mathtex_line(t3, "\mathrm{Sum}(\mathrm{stuff}) = \mathrm{Sum}(\mathrm{stuff}, x) - x")
        self.play(FadeIn(t4))
        
        eq1 = t2
        eq2 = mathtex_line(t1, "\mathrm{Sum}(4, 11, 1", ") = 19", "-", "3")

        eq3 = mathtex_line(t1, "\mathrm{Sum}(4, 11", ",", "1", ") =", "19 - 3")
        eq4 = mathtex_line(t1, "\mathrm{Sum}(4, 11", ",", "1", ") =", "16")
        eq5 = mathtex_line(t1, "\mathrm{Sum}(4, 11", ") =", "16", "-", "1")

        eq6 = mathtex_line(t1, "\mathrm{Sum}(4", ",", "11", ") =", "16 - 1")
        eq7 = mathtex_line(t1, "\mathrm{Sum}(4", ",", "11", ") =", "15")
        eq8 = mathtex_line(t1, "\mathrm{Sum}(4", ") =", "15", "-", "11")

        eq9  = mathtex_line(t1, "\mathrm{Sum}(", "4", ") =", "15 - 11")
        eq10 = mathtex_line(t1, "\mathrm{Sum}(", "4", ") =", "4")
        eq11 = mathtex_line(t1, "\mathrm{Sum}(", ") =", "4", "-", "4")

        eq12 = mathtex_line(t1, "\mathrm{Sum}() =", "4 - 4")
        eq13 = mathtex_line(t1, "\mathrm{Sum}() =", "0")

        self.play_equation(eq1, eq2, [(0, 0), (2, 3), (3, 1)])
        self.add(eq3); self.remove(*eq2)
        self.play(ReplacementTransform(eq3, eq4))
        self.play_equation(eq4, eq5, [(0, 0), (2, 4), (3, 1), (4, 2)])
        self.add(eq6); self.remove(*eq5)
        self.play(ReplacementTransform(eq6, eq7))
        self.play_equation(eq7, eq8, [(0, 0), (2, 4), (3, 1), (4, 2)])
        self.add(eq9); self.remove(*eq8)
        self.play(ReplacementTransform(eq9, eq10))
        self.play_equation(eq10, eq11, [(0, 0), (1, 4), (2, 1), (3, 2)])
        self.add(eq12); self.remove(*eq11)
        self.play(ReplacementTransform(eq12, eq13))

        self.play(FadeOut(t1, t3, t4, eq13))
        self.play(Unwrite(title, reverse=False))

    def slide3(self):
        title = Tex("Product function", tex_template=tem, font_size=title_size)
        title.to_corner(UL, buff=title_buff)
        self.play(Write(title))

        t1 = mathtex_line(title, "\mathrm{Prod}(2, 3", ",", "5", ") =", "30", "\\frac00")
        t1[-1].set_opacity(0)
        self.play(FadeIn(t1))

        t2 = mathtex_line(t1, "\mathrm{Prod}(\mathrm{stuff}, x) = \mathrm{Prod}(\mathrm{stuff}) \cdot x")
        self.play(FadeIn(t2))

        t3 = mathtex_line(t2, "\mathrm{Prod}(\mathrm{stuff}) = \\frac{\mathrm{Prod}(\mathrm{stuff}, x)}{x}")
        self.play(FadeIn(t3))

        eq1 = t1
        eq2 = mathtex_line(title, "\mathrm{Prod}(2, 3", ") =", "{30", "\over", "5}")

        eq3 = mathtex_line(title, "\mathrm{Prod}(2", ",", "3", ") =", "{30 \over 5}", "\\frac00")
        eq4 = mathtex_line(title, "\mathrm{Prod}(2", ",", "3", ") =", "6", "\\frac00")
        eq5 = mathtex_line(title, "\mathrm{Prod}(2", ") =", "{6", "\over", "3}")
        eq3[-1].set_opacity(0)
        eq4[-1].set_opacity(0)

        eq6 = mathtex_line(title, "\mathrm{Prod}(", "2", ") =", "{6 \over 3}", "\\frac00")
        eq7 = mathtex_line(title, "\mathrm{Prod}(", "2", ") =", "2", "\\frac00")
        eq8 = mathtex_line(title, "\mathrm{Prod}(", ") =", "{2", "\over", "2}")
        eq6[-1].set_opacity(0)
        eq7[-1].set_opacity(0)

        eq9 = mathtex_line(title, "\mathrm{Prod}() =", "{2 \over 2}", "\\frac00")
        eq10 = mathtex_line(title, "\mathrm{Prod}() =", "1", "\\frac00")
        eq9[-1].set_opacity(0)
        eq10[-1].set_opacity(0)

        self.play_equation(eq1, eq2, [(0, 0), (2, 4), (3, 1), (4, 2)])
        self.add(eq3); self.remove(*eq2)
        self.play(ReplacementTransform(eq3, eq4))
        self.play_equation(eq4, eq5, [(0, 0), (2, 4), (3, 1), (4, 2)])
        self.add(eq6); self.remove(*eq5)
        self.play(ReplacementTransform(eq6, eq7))
        self.play_equation(eq7, eq8, [(0, 0), (1, 4), (2, 1), (3, 2)])
        self.add(eq9); self.remove(*eq8)
        self.play(ReplacementTransform(eq9, eq10))

        self.play(FadeOut(t2, t3))

        t4 = mathtex_line(t1, "\mathrm{Sum}() = 0")
        self.play(FadeIn(t4))

        box = SurroundingRectangle(eq10[0:-1], color=box_color, buff=box_buff, stroke_width=2)
        self.play(Create(box)) 

        self.play(FadeOut(t4))
        self.play(Unwrite(title, reverse=False))
        return eq10, box
    
    def slide4(self, prod_eq, box):
        t1 = MathTex("0! = 1", tex_template=tem, font_size=sub_size, color=green)
        t1.next_to(box, RIGHT, buff=2)
        self.play(FadeIn(t1))

        eq1 = mathtex_line(prod_eq, "n", "! =", "\mathrm{Prod}(", "1, \dots,", "n", ")")
        eq2 = mathtex_line(prod_eq, "0", "! =", "\mathrm{Prod}(", "1, \dots,", "0", ")")
        eq3 = mathtex_line(prod_eq, "0", "! =", "\mathrm{Prod}(", ")")
        self.play(FadeIn(eq1))
        self.play(ReplacementTransform(eq1, eq2))
        self.play_equation(eq2, eq3, [(0, 0), (1, 1), (2, 2), (5, 3)], fade_first=True)

        eq_start = MathTex("\mathrm{Prod}() = 1", tex_template=tem, font_size=sub_size, color=blue)
        eq_end = MathTex("\mathrm{Prod}() = 1", tex_template=tem, font_size=sub_size, color=blue)
        eq_start.move_to(prod_eq[0:-1], aligned_edge=ORIGIN)
        eq_end.move_to(eq3[2], aligned_edge=LEFT)
        self.play(ReplacementTransform(eq_start, eq_end))

        self.play(FadeOut(t1, eq3, eq_end))
    
    def slide5(self, prod_eq, box):
        t1 = mathtex_line(prod_eq, "a", "^b", "= \mathrm{Prod}(\ \\underbrace{a, \dots, a}_{b \\text{ copies}}\ )", "\implies 0^0 = 1")
        self.play(FadeIn(t1[0:-1]))
        self.play(FadeIn(t1[-1]))

        t2 = MathTex("2^0", "= 0^0", "= \mathrm{Prod}()", tex_template=tem, font_size=sub_size, color=green)
        t2.next_to(box, RIGHT, buff=2)
        self.play(FadeIn(t2[0]))
        self.play(FadeIn(t2[1]))
        self.play(FadeIn(t2[2]))

        self.play(FadeOut(prod_eq, box, t2))
        return t1

    def slide6(self, alg_def):
        box = SurroundingRectangle(alg_def, color=box_color, buff=box_buff, stroke_width=2)
        self.play(Create(box)) 

        title = Tex("Algebraic power", tex_template=tem, font_size=title_size)
        title.to_corner(UL, buff=title_buff)
        self.play(Write(title))

        poly = mathtex_line(title, "x^3 + 4x^2 + 1")
        self.play(FadeIn(poly))

        dice = ImageMobject("assets/dice.jpg").scale(0.3).next_to(poly, RIGHT, buff=1.25)
        self.play(FadeIn(dice))

        base = Tex("any number", tex_template=tem, font_size=small_size, color=green)
        base.next_to(box, DOWN, buff=0.3).shift(LEFT * 3)
        arr1 = Arrow(start=base.get_top(), end=alg_def[0].get_corner(DR), buff=0.1, color=green)
        self.play(FadeIn(base, arr1))

        exp = Tex("natural number $(0, 1, \dots)$", tex_template=tem, font_size=small_size, color=green)
        exp.next_to(box, UP, buff=0.3).shift(LEFT * 1)
        arr2 = Arrow(start=exp.get_corner(DL), end=alg_def[1].get_corner(UR), buff=0.075, color=green)
        self.play(FadeIn(exp, arr2))

        self.play(FadeOut(box, poly, dice, base, arr1, exp, arr2))
        self.play(alg_def.animate.scale(0.75).next_to(title, DOWN, aligned_edge=LEFT, buff=line_buff))
        return title
    
    def slide7(self, alg_title, alg_def):
        def wave(t):
            A = 0.3
            N = 2
            cut = 1 + 2 * N * A * math.pi
            end = cut + 0.5
            x = t * end
            
            if x < 1: return x * x / 2
            if x > cut: return x - cut + 0.5
            return A * math.sin((x - 1) / A) + 0.5

        plane = Axes(x_range=(-8, 4, 1), y_range=(-3, 6, 1))
        self.play(FadeIn(plane))

        curve = plane.plot(lambda x: 2 ** x, x_range=(-8, 3), color=green)
        label = plane.get_graph_label(curve, "y = 2^x", x_val=-0.5, direction=UL, buff=0.1)
        dot = Dot(point=curve.get_start(), radius=0.125, color=green)
        self.play(FadeIn(curve, label, dot))
        self.play(MoveAlongPath(dot, curve, rate_func=wave), run_time=8)

        line1 = StrikeOut(alg_def)
        line1.shift(UP * 0.3)
        self.play(GrowFromPoint(line1, line1.get_start()))

        line2 = StrikeOut(alg_title, stroke_width=10)
        self.play(GrowFromPoint(line2, line2.get_start()))

        qmark = Tex("?", font_size=120, color=blue).shift(DL * 2.5)
        self.play(FadeIn(qmark))
        
        self.play(FadeOut(alg_def, plane, curve, label, dot, line1, line2, qmark))
        self.play(Unwrite(alg_title, reverse=False))
    
    def slide8(self):
        t1 = MathTex("x^{-1} = \\frac{1}{x}", tex_template=tem, font_size=sub_size, color=green)
        t1.shift(UP * 1.5)
        self.play(FadeIn(t1))

        t2 = MathTex("x^{1/2} = \\sqrt{x}", tex_template=tem, font_size=sub_size, color=green)
        t2.shift(DOWN * 1.5)
        self.play(FadeIn(t2))

        t3 = Tex("analytic power", tex_template=tem, font_size=sub_size, color=blue)
        self.play(FadeOut(t1, t2), FadeIn(t3))
        return t3

    def slide9(self, ana):
        self.play(FadeOut(ana))

        title = Tex("Exponential function", tex_template=tem, font_size=title_size)
        title.to_corner(UL, buff=title_buff)
        self.play(Write(title))

        t1 = mathtex_line(title, "\exp(x)", "= \sum_{n=0}^{\infty}", "{x^n", "\over n!}", "= 1 + x +", "{x^2", "\over 2} +", "{x^3", "\over 6} + \dots")
        self.play(FadeIn(t1[0]))

        wiki = ImageMobject("assets/wikipedia.png").scale(0.6).shift(DR * 1)
        self.play(FadeIn(wiki))
        self.play(FadeOut(wiki))

        self.play(FadeIn(t1[1:4]))
        self.play(FadeIn(t1[4:]))

        boxes = [ SurroundingRectangle(t1[i], color=box_color, buff=0.1, stroke_width=2) for i in [2, 5, 7] ]
        self.play(*[ Create(box) for box in boxes ])
        self.play(FadeOut(*boxes, t1[4:]))
        return title, t1

    def slide10(self, exp_title, exp_def):
        plane = Axes(x_range=(-8, 4, 1), y_range=(-3, 6, 1))
        plane.shift(DOWN * 0.75 + RIGHT * 0.5)
        self.play(FadeIn(plane))

        curve1 = plane.plot(lambda x: math.exp(x), x_range=(-8, 3), color=green)
        label1 = plane.get_graph_label(curve1, "\exp(x)", x_val=-0.5, direction=UL, buff=0.1)
        self.play(FadeIn(curve1, label1))

        curve2 = plane.plot(lambda x: math.log(x), x_range=(0.01, 5), color=blue)
        label2 = plane.get_graph_label(curve2, "\log(x)", x_val=3, direction=UL, buff=0.1)
        self.play(FadeIn(curve2, label2))

        t1 = MathTex("\exp(\log(x))", "= \log(\exp(x))", "= x", tex_template=tem, font_size=small_size, color=blue)
        t1.shift(DOWN * 2.8 + LEFT * 2)
        self.play(FadeIn(t1[0]))
        self.play(FadeIn(t1[1]))
        self.play(FadeIn(t1[2]))

        self.play(FadeOut(exp_def, plane, curve1, label1, curve2, label2, t1))
        self.play(Unwrite(exp_title, reverse=False))
    
    def slide11(self):
        title = Tex("Analytic power", tex_template=tem, font_size=title_size)
        title.to_corner(UL, buff=title_buff)
        self.play(Write(title))









        

