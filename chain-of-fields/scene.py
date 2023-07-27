from manim import *
import numpy as np
import math

blue = BLUE_D
red = RED_D
green = GREEN_D
yellow = YELLOW_D

def add_bookmarks(text):
    return text.replace('{', '<bookmark mark="').replace('}', '"/>')

def circle_chain(start, direction, buff, start_radius, delta_radius, n, **kwargs):
    pos = start
    unit = direction / np.linalg.norm(direction)
    circles = []
    for i in range(n):
        r = start_radius + i * delta_radius
        pos += unit * r
        circles.append(Circle(radius=r, **kwargs).move_to(pos))
        pos += unit * (r + buff)
    return circles

class ChainOfFields(Scene):
    def construct(self):
        # self.scene1()
        self.scene2()

    def fade_all(self, *mobjects, reverse=False, lag_ratio=0.05):
        fade_iter = reversed(mobjects) if reverse else mobjects
        self.play(AnimationGroup(*[ FadeOut(m) for m in fade_iter ], lag_ratio=lag_ratio))
    
    def scene1(self): 
        owen = SVGMobject('assets/owen.svg').scale(2.5).to_corner(DL, buff=0)
        me = Text('me', font='Didot', slant=ITALIC, font_size=50, color=blue).shift(UP * 2.4 + LEFT * 4.4)
        arrow = Arrow(me.get_bottom(), owen.get_top(), buff=0.2, color=blue)

        c_start = owen.get_corner(UR) + DOWN * 0.6 + LEFT * 0.95
        c_direction = UP * 0.25 + RIGHT
        circles = circle_chain(start=c_start, direction=c_direction, buff=0.3, start_radius=0.2, delta_radius=0.1, n=3, color=red)
        circles.append(Ellipse(width=6, height=4, color=red).next_to(circles[-1], RIGHT, buff=0.3))
 
        self.play(DrawBorderThenFill(owen))
        self.play(FadeIn(me), GrowArrow(arrow, point_color=BLACK))
        self.play(AnimationGroup(*[ FadeIn(c) for c in circles ], lag_ratio=0.2))

        bop = Text('binary operations', font='Didot', slant=ITALIC, font_size=50, color=red, stroke_color=red).move_to(circles[-1])
        self.play(Write(bop))

        node = Circle(radius=0.15, color=blue).next_to(bop, UP, buff=0.5).shift(RIGHT * 0.3)
        input1 = Arrow(node.get_corner(UL) + LEFT + UP * 0.3, node.get_corner(UL), buff=0.1, color=blue)
        input2 = Arrow(node.get_corner(DL) + LEFT + DOWN * 0.3, node.get_corner(DL), buff=0.1, color=blue)
        output = Arrow(node.get_right(), node.get_right() + RIGHT * 1.1, buff=0.15, color=blue)

        self.play(FadeIn(node))
        self.play(GrowArrow(input1, point_color=BLACK), GrowArrow(input2, point_color=BLACK))
        self.play(GrowArrow(output, point_color=BLACK))

        mul = MathTex('\cdot', font_size=125, color=blue).next_to(bop, DOWN, buff=0.45)
        add = MathTex('+', font_size=75, color=blue).next_to(mul, LEFT, buff=1)
        self.play(FadeIn(add))
        self.play(FadeIn(mul))

        distr1 = MathTex('a {{\cdot}} (x {{+}} y) = (a {{\cdot}} x) {{+}} (a {{\cdot}} y)', font_size=50, color=blue).next_to(circles[-1], DOWN, buff=0.5).shift(LEFT * 1.2)
        distr2 = MathTex('(a {{+}} b) {{\cdot}} x = (a {{\cdot}} x) {{+}} (b {{\cdot}} x)', font_size=50, color=blue).next_to(distr1, DOWN, buff=0.5)
        self.play(FadeIn(distr1))
        self.play(FadeIn(distr2))

        ques = MathTex('?', font_size=75, color=green).next_to(mul, RIGHT, buff=1)
        star = MathTex('\star', font_size=75, color=green).move_to(ques)
        self.play(FadeIn(ques))
        self.play(ReplacementTransform(ques, star))

        distr1_star = MathTex('a {{\star}} (x {{\cdot}} y) = (a {{\star}} x) {{\cdot}} (a {{\star}} y)', font_size=50, color=blue).move_to(distr1)
        distr2_star = MathTex('(a {{\cdot}} b) {{\star}} x = (a {{\star}} x) {{\cdot}} (b {{\star}} x)', font_size=50, color=blue).move_to(distr2)
        distr1_star.get_parts_by_tex('\star').set_color(green)
        distr2_star.get_parts_by_tex('\star').set_color(green)
        self.play(ReplacementTransform(distr1, distr1_star), ReplacementTransform(distr2, distr2_star))

        self.fade_all(owen, me, arrow, *circles, bop, node, input1, input2, output, add, mul, star, reverse=True)

        star_exp = MathTex('x {{\star}} y = x^y?', font_size=50, color=blue).to_edge(UP, buff=1)
        star_exp.get_parts_by_tex('\star').set_color(green)
        self.play(FadeIn(star_exp))            

        rep_add = MathTex('x \cdot n', '= \\underbrace{x + \dots + x}_{n \\text{ copies}}', color=red).to_edge(LEFT, buff=2).shift(UP, 0.15)
        rep_mul = MathTex('x^n', '= \\underbrace{x \cdot \dots \cdot x}_{n \\text{ copies}}', color=red).next_to(rep_add, DOWN, buff=0.25)
        self.play(FadeIn(rep_add[0], rep_mul[0]))
        self.play(FadeIn(rep_add[1]))
        self.play(FadeIn(rep_mul[1]))

        self.play(FadeOut(rep_add, rep_mul))

        box1 = SurroundingRectangle(distr1_star, color=yellow, buff=0.1)
        box2 = SurroundingRectangle(distr2_star, color=yellow, buff=0.1)
        distr1_exp = MathTex('a^{xy}', '\\neq', 'a^x a^y', font_size=50, color=blue).next_to(star_exp, DOWN, buff=0.5)
        distr2_exp = MathTex('(ab)^x = a^x b^x', font_size=50, color=blue).next_to(distr1_exp, DOWN, buff=0.5)
        distr1_exp[1].set_color(red)

        self.play(Create(box2))
        self.play(FadeIn(distr2_exp))
        self.play(ReplacementTransform(box2, box1))
        self.play(FadeIn(distr1_exp))

        strike = Line(star_exp.get_left(), star_exp.get_right(), color=red)
        self.play(GrowFromPoint(strike, strike.get_start()))

        self.fade_all(box1, distr2_exp, distr1_exp, star_exp, strike)

        chal = Text('Try it yourself:', font='Didot', slant=ITALIC, font_size=50).shift(UP)
        laws = VGroup(distr1_star, distr2_star)
        self.play(FadeIn(chal), laws.animate.next_to(chal, DOWN, buff=0.5))

        self.play(FadeOut(chal, laws))
    
    def scene2(self):
        exp = Text('exponential function', font='Didot', slant=ITALIC, font_size=50).to_edge(UP, buff=1)
        nots = MathTex('e^x', '\quad \exp x', font_size=50, color=blue).next_to(exp, DOWN, buff=0.5)
        strike = Line(nots[0].get_left(), nots[0].get_right(), color=red).shift(DOWN * 0.1 + LEFT * 0.05)
        nots[1].set_color(red)

        axes = Axes(x_range=(-3, 3), y_range=(-1, 3)).scale(0.4).to_edge(DOWN, buff=1)
        curve = axes.plot(lambda x: math.exp(x), x_range=(-3, 1.5), color=red)

        self.play(FadeIn(axes))
        self.play(AnimationGroup(Write(exp), Create(curve), lag_ratio=0.3))
        self.play(FadeIn(nots[0]))
        self.play(GrowFromPoint(strike, strike.get_start()), FadeIn(nots[1]))

        self.play(AnimationGroup(
            FadeOut(nots, strike), 
            AnimationGroup(exp.animate.to_corner(UL, buff=1), VGroup(axes, curve).animate.to_corner(DR, buff=1)), 
            lag_ratio=0.3))

        prop1 = Tex('1. $ \exp(x + y) = \exp x \cdot \exp y $', font_size=50, color=blue).next_to(exp, DOWN, buff=0.5, aligned_edge=LEFT)
        prop2 = Tex('2. ', 'real numbers ', '$\longleftrightarrow$ positive numbers', color=green).next_to(prop1, DOWN, buff=1.5, aligned_edge=LEFT)
        pos_axis = Line(axes[1].number_to_point(0), axes[1].get_end())
        real_brace = Brace(axes[0], DOWN, color=green)
        pos_brace = Brace(pos_axis, RIGHT, color=green)

        self.play(FadeIn(prop1))
        self.play(FadeIn(prop2[0]))
        self.play(FadeIn(prop2[1], real_brace))
        self.play(FadeIn(prop2[2]), ReplacementTransform(real_brace, pos_brace))
        self.play(FadeOut(pos_brace))



    


        

      

