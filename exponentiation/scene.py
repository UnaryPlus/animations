from manim import *

blue = "#B4C7DC"
green = "#AECF94"

title_size = 80
sub_size = 60

title_buff = 1.25
line_buff = 0.75

tem = TexTemplate()
tem.add_to_preamble(r"\usepackage{tgtermes}")

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
        self.slide1()
        self.slide2()
        self.slide3()
        self.wait(1)

    def play_equation(self, eq1, eq2, pairs):
        anims = []
        seen1 = [False] * len(eq1)
        seen2 = [False] * len(eq2)
        for pair in pairs:
            anims.append(ReplacementTransform(eq1[pair[0]], eq2[pair[1]]))
            seen1[pair[0]] = True
            seen2[pair[1]] = True
        for i in range(len(eq1)):
            if not seen1[i]:
                anims.append(FadeOut(eq1[i]))
        for i in range(len(eq2)):
            if not seen2[i]:
                anims.append(FadeIn(eq2[i]))
        self.play(*anims)

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
        self.play(FadeIn(arr1))

        arr2 = Arrow(start=alg.get_left(), end=t4.get_right(), buff=0.25, color=green)
        self.play(FadeIn(arr2))

        self.play(FadeOut(t1, t2, t3, t4, alg, ana, arr1, arr2))
        self.play(Unwrite(title))

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
        self.play(Unwrite(title))

    def slide3(self):
        title = Tex("Product function", tex_template=tem, font_size=title_size)
        title.to_corner(UL, buff=title_buff)
        self.play(Write(title))