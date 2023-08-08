# TODO: use constants and adjust them
# TODO: review arrow buffs
# TODO: change color scheme
# TODO: standardize fonts, font sizes, line widths
# TODO: standardize variable name
# TODO: use big dot for multiplication?
# TODO: use arrange()
# TODO: use transparent instead of black

from manim import *
import numpy as np
import math

blue = BLUE_D
red = RED_D
purple = PURPLE_D
green = GREEN_D
purple = PURPLE_D
yellow = YELLOW_D

fancy = dict(font='Didot', slant=ITALIC)
tip_size = lambda x: dict(tip_length=x, tip_width=x)

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

def frange(x, y, jump):
    while(x < y):
        yield x
        x += jump

class ChainOfFields(Scene):
    def construct(self):
        # self.scene1()
        # exp_iso = self.scene2()
        # star_def = self.scene3(exp_iso)
        # self.scene4(star_def)
        # self.scene5(star_def)
        # ops = self.scene6()
        # fields = self.scene7(ops)
        # self.scene8(fields)
        self.scene9()

    def fade_all(self, *mobjects, reverse=False, lag_ratio=0.05):
        fade_iter = reversed(mobjects) if reverse else mobjects
        self.play(AnimationGroup(*[ FadeOut(m) for m in fade_iter ], lag_ratio=lag_ratio))
    
    def fadein_all(self, *mobjects, reverse=False, lag_ratio=0.05):
        fade_iter = reversed(mobjects) if reverse else mobjects
        self.play(AnimationGroup(*[ FadeIn(m) for m in fade_iter ], lag_ratio=lag_ratio))
    
    def scene1(self): 
        owen = SVGMobject('assets/owen.svg').scale(2.5).to_corner(DL, buff=0)
        me = Text('me', **fancy, font_size=50, color=blue).shift(UP * 2.4 + LEFT * 4.4)
        arrow = Arrow(me.get_bottom(), owen.get_top(), buff=0.2, color=blue)

        c_start = owen.get_corner(UR) + DOWN * 0.6 + LEFT * 0.95
        c_direction = UP * 0.25 + RIGHT
        circles = circle_chain(start=c_start, direction=c_direction, buff=0.3, start_radius=0.2, delta_radius=0.1, n=3, color=red)
        circles.append(Ellipse(width=6, height=4, color=red).next_to(circles[-1], RIGHT, buff=0.3))
 
        self.play(DrawBorderThenFill(owen))
        self.play(FadeIn(me), GrowArrow(arrow, point_color=BLACK))
        self.play(AnimationGroup(*[ FadeIn(c) for c in circles ], lag_ratio=0.2))

        bop = Text('binary operations', **fancy, font_size=50, color=red, stroke_color=red).move_to(circles[-1])
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

        chal = Text('Try it yourself:', **fancy, font_size=50).shift(UP)
        laws = VGroup(distr1_star, distr2_star)
        self.play(FadeIn(chal), laws.animate.next_to(chal, DOWN, buff=0.5))

        self.play(FadeOut(chal, laws))
    
    def scene2(self):
        exp = Text('exponential function', **fancy, font_size=50).to_edge(UP, buff=1)
        nots = MathTex('e^x', '\quad \exp x', font_size=60, color=blue).next_to(exp, DOWN, buff=0.5)
        strike = Line(nots[0].get_left(), nots[0].get_right(), color=red).shift(DOWN * 0.1 + LEFT * 0.05)
        nots[1].set_color(red)

        axes = Axes(x_range=(-3, 3), y_range=(-1, 4)).scale(0.5).to_edge(DOWN, buff=0.75)
        curve = axes.plot(lambda x: math.exp(x), x_range=(-3, 1.5), color=red)

        self.play(FadeIn(axes))
        self.play(AnimationGroup(Write(exp), Create(curve), lag_ratio=0.3))
        self.play(FadeIn(nots[0]))
        self.play(GrowFromPoint(strike, strike.get_start()), FadeIn(nots[1]))

        self.play(AnimationGroup(
            FadeOut(nots, strike), 
            AnimationGroup(exp.animate.to_corner(UL, buff=1), VGroup(axes, curve).animate.to_corner(DR, buff=0.75)), 
            lag_ratio=0.3))

        prop1 = Tex('1. $ \exp(x + y) = \exp x \cdot \exp y $', font_size=50, color=blue).next_to(exp, DOWN, buff=0.5, aligned_edge=LEFT)        
        prop2 = Tex('2. ', 'real numbers ', '$\longleftrightarrow$ positive numbers', font_size=50, color=green).next_to(prop1, DOWN, buff=1.5, aligned_edge=LEFT)
        
        pos_axis = Line(axes[1].number_to_point(0), axes[1].get_end())
        real_brace = Brace(axes[0], DOWN, color=green)
        pos_brace = Brace(pos_axis, RIGHT, color=green)

        self.play(FadeIn(prop1))
        self.play(FadeIn(prop2[0]))
        self.play(FadeIn(prop2[1], real_brace))
        self.play(FadeIn(prop2[2]), ReplacementTransform(real_brace, pos_brace))
        self.play(FadeOut(pos_brace))

        y = ValueTracker(2.7)

        y_pt = always_redraw(lambda: Dot(axes[1].number_to_point(y.get_value()), radius=0.07, color=green))
        x_pt = always_redraw(lambda: Dot(axes[0].number_to_point(math.log(y.get_value())), radius=0.07, color=green))
        y_label = always_redraw(lambda: MathTex('y', font_size=35, color=green).next_to(y_pt, LEFT, buff=0.1))
        x_label = always_redraw(lambda: MathTex('x', font_size=35, color=green).next_to(x_pt, DOWN, buff=0.1))
        
        hori = always_redraw(lambda: Line(y_pt.get_center(), axes.coords_to_point(math.log(y.get_value()), y.get_value()), stroke_width=2.5, color=green))
        vert = always_redraw(lambda: Line(x_pt.get_center(), axes.coords_to_point(math.log(y.get_value()), y.get_value()), stroke_width=2.5, color=green))

        self.play(FadeIn(y_pt, y_label))
        self.play(FadeIn(x_pt, x_label))
        self.play(GrowFromPoint(hori, hori.get_start()), GrowFromPoint(vert, vert.get_start()))

        self.play(y.animate.set_value(0.25))
        self.play(y.animate.set_value(2.7))

        log_y = MathTex('\log y', font_size=30, color=green).move_to(x_label)
        self.play(ReplacementTransform(x_label, log_y))

        homo = Text('homomorphism', **fancy, font_size=35, color=blue, stroke_color=blue)
        homo_desc = Tex('converts one operation\\\\into another', font_size=35, color=blue).next_to(homo, DOWN, buff=0.25)
        VGroup(homo, homo_desc).to_corner(UR, 1.25).shift(RIGHT * 0.3)
        self.play(Write(homo), FadeIn(homo_desc))

        prop1_alt = Tex('``$\exp$ is a homomorphism from addition\\\\to multiplication"', tex_environment='flushleft', font_size=35, color=blue)
        prop1_alt.next_to(prop1, DOWN, buff=0.25, aligned_edge=LEFT).shift(RIGHT * 0.6)
        self.play(FadeIn(prop1_alt))

        bijn = Text('bijection', **fancy, font_size=35, color=green, stroke_color=green).move_to(homo)
        bijn_desc = Tex('one-to-one\\\\correspondence', font_size=35, color=green).next_to(bijn, DOWN, buff=0.25)
        VGroup(bijn, bijn_desc).to_edge(DOWN, 1.25)
        self.play(FadeOut(axes, curve, y_pt, x_pt, y_label, log_y, hori, vert))
        self.play(Write(bijn), FadeIn(bijn_desc))

        prop2_alt = Tex('``$\exp$ is a bijection from real numbers\\\\to positive numbers"', tex_environment='flushleft', font_size=35, color=green)
        prop2_alt.next_to(prop2, DOWN, buff=0.25, aligned_edge=LEFT).shift(RIGHT * 0.6)
        self.play(FadeIn(prop2_alt))
        
        iso = Text('isomorphism', **fancy, font_size=35).move_to(VGroup(homo, bijn_desc))
        arr_top = Arrow(homo_desc.get_bottom(), iso.get_top(), buff=0.25)
        arr_bottom = Arrow(bijn.get_top(), iso.get_bottom(), buff=0.25)
        self.play(Write(iso), GrowArrow(arr_top, point_color=BLACK), GrowArrow(arr_bottom, point_color=BLACK))

        conj = Tex('``$\exp$ is an isomorphism from {{addition}}\\\\of {{real numbers}} to {{multiplication}} of\\\\{{positive numbers}}"', tex_environment='flushleft', font_size=35)
        conj[1].set_color(blue)
        conj[3].set_color(green)
        conj[5].set_color(blue)
        conj[7].set_color(green)
        conj.next_to(prop2_alt, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(conj))
        
        self.fade_all(exp, prop1, prop2, homo, homo_desc, prop1_alt, bijn, bijn_desc, prop2_alt, VGroup(arr_top, arr_bottom, iso))
        return conj

    def scene3(self, exp_iso):
        line2 = Tex('isomorphic operations have \\textit{the same structure}', font_size=50)
        line1 = Tex('$+$ and $\cdot_{(\\text{pos.})}$ are isomorphic', font_size=50, color=blue).next_to(line2, UP, buff=0.5)
        
        ops = MathTex('+', '\qquad', '\cdot_{(\\text{pos.})}', font_size=50, color=blue)
        arc_UL = ops[0].get_corner(UR)
        arc_DL = ops[0].get_corner(DR)
        arc_UR = ops[2].get_corner(UL) + UP * 0.12
        arc_DR = ops[2].get_corner(DL) + UP * 0.12

        arr_top = ArcBetweenPoints(arc_UR, arc_UL, radius=1, stroke_width=2.5, color=blue).add_tip(**tip_size(0.18), at_start=True)
        arr_bottom = ArcBetweenPoints(arc_DL, arc_DR, radius=1, stroke_width=2.5, color=blue).add_tip(**tip_size(0.18), at_start=True)
        exp = MathTex('\exp', font_size=40, color=blue).next_to(arr_top, UP, buff=0.1)
        log = MathTex('\log', font_size=40, color=blue).next_to(arr_bottom, DOWN, buff=0.1)
        line3 = VGroup(ops, arr_top, arr_bottom, exp, log).next_to(line2, DOWN, buff=0.5)

        self.play(FadeIn(line1), FadeOut(exp_iso))
        self.play(FadeIn(line2))
        self.play(FadeIn(line3))

        box1 = SurroundingRectangle(ops[0], color=yellow, buff=0.1)
        box2 = SurroundingRectangle(ops[2], color=yellow, buff=0.1)
        mul = MathTex('\cdot', font_size=125, color=blue).move_to(ops[0]).shift(UP * 1.6)
        ques = MathTex('?', font_size=75, color=green).move_to(ops[2]).shift(UP * 1.75 + LEFT * 0.2)
        arr_mul = Line(mul.get_bottom(), ops[0].get_top(), buff=0.2, color=blue).add_tip(**tip_size(0.27))
        arr_ques = Line(ques.get_bottom(), ops[2].get_top() + LEFT * 0.2, buff=0.2, color=green).add_tip(**tip_size(0.27))

        self.play(FadeOut(line1, line2))
        self.play(Create(box1))
        self.play(FadeIn(mul), GrowFromPoint(arr_mul, arr_mul.get_start(), point_color=BLACK))
        self.play(ReplacementTransform(box1, box2))
        self.play(FadeIn(ques), GrowFromPoint(arr_ques, arr_ques.get_start(), point_color=BLACK))
        self.play(FadeOut(box2))

        homo1 = MathTex('\exp(x + y) = \exp x \cdot \exp y', font_size=50, color=blue).to_edge(UP, 1)
        homo2 = MathTex('\exp({{x}} \cdot {{y}}) = \exp {{x}} {{\, ?}} \exp {{y}}', font_size=50, color=blue).next_to(homo1, DOWN, 0.5)
        homo2_star = MathTex('\exp({{x}} \cdot {{y}}) = \exp {{x}} {{\star}} \exp {{y}}', font_size=50, color=blue).move_to(homo2)
        homo2.get_part_by_tex('?').set_color(green)
        homo2_star.get_part_by_tex('\star').set_color(green)

        exp_copy = VGroup(exp, arr_top).copy()

        star = MathTex('\star', font_size=75, color=green).move_to(ques)
        arr_star = Line(star.get_bottom(), ops[2].get_top() + LEFT * 0.2, buff=0.2, color=green).add_tip(**tip_size(0.27))

        self.play(FadeIn(homo1))
        self.play(FadeIn(homo2), exp_copy.animate.move_to(VGroup(mul, ques).get_center() + UP * 0.4 + LEFT * 0.1))
        self.play(ReplacementTransform(homo2, homo2_star), ReplacementTransform(ques, star), ReplacementTransform(arr_ques, arr_star))

        star_def1 = MathTex('\exp({{\log x}} \cdot {{\log y}}) = \exp {{(\log x)}} {{\star}} \exp {{(\log y)}}', font_size=50, color=blue).move_to(homo2)
        star_def2 = MathTex('\exp(\log x \cdot \log y) =', '\exp (\log {{a}}) {{\star}} \exp (\log {{b}})', font_size=50, color=blue).move_to(homo2)
        star_def3 = MathTex('\exp(\log x \cdot \log y) =', 'a', '\star', 'b', font_size=50, color=blue).move_to(homo2)
        star_def4 = MathTex('\exp(\log x \cdot \log y)', '=', 'a \star b', font_size=50, color=blue).move_to(homo2)
        star_def5 = MathTex('a \star b', '=', '\exp(\log x \cdot \log y)', font_size=50, color=blue).move_to(homo2)

        self.play(ReplacementTransform(homo2_star, star_def1))
        self.add(star_def2); self.remove(star_def1)
        self.play(FadeOut(star_def2[1::2]))
        self.play(*[ ReplacementTransform(star_def2[i * 2], star_def3[i]) for i in range(4) ])
        self.add(star_def4); self.remove(*star_def3)
        self.play(*[ ReplacementTransform(star_def4[2 - i], star_def5[i]) for i in range(3)])

        self.fade_all(line3, mul, arr_mul, star, arr_star, exp_copy, homo1)
        return star_def5

    def scene4(self, star_def):
        self.play(star_def.animate.set_font_size(60).to_edge(UP, buff=1))

        proof1_tex = """
         & a \star (x \cdot y) \\\\
        =& \exp (\log a \cdot \log (x \cdot y)) \\\\
        =& \exp (\log a \cdot (\log x + \log y)) \\\\
        =& \exp ((\log a \cdot \log x) + (\log a \cdot \log y)) \\\\
        =& \exp (\log a \cdot \log x) \cdot \exp (\log a \cdot \log y) \\\\
        =& (a \star x) \cdot (a \star y)
        """

        proof2_tex = """
         & (a \cdot b) \star x \\\\
        =& \exp (\log (a \cdot b) \cdot \log x) \\\\
        =& \exp ((\log a + \log b) \cdot \log x) \\\\
        =& \exp ((\log a \cdot \log x) + (\log b \cdot \log x)) \\\\
        =& \exp (\log a \cdot \log x) \cdot \exp (\log b \cdot \log x) \\\\
        =& (a \star x) \cdot (b \star x)
        """

        proof1 = MathTex(proof1_tex, font_size=35).to_corner(DL, buff=1)
        proof2 = MathTex(proof2_tex, font_size=35).to_corner(DR, buff=1)
        self.play(FadeIn(proof1, proof2))

        arc = ArcBetweenPoints(star_def[0].get_bottom() + DR * 0.1, star_def[2].get_bottom() + RIGHT * 0.4 + UP * 0.1, radius=3, color=green).add_tip().add_tip(at_start=True)
        same = Text('same properties', **fancy, font_size=40, color=green, stroke_color=green).next_to(arc, DOWN, buff=0.1)
        self.play(FadeIn(arc))
        self.play(Write(same))

        self.fade_all(VGroup(proof1, proof2), same, arc)

        prop_fs = 40
        prop_dy1 = DOWN * 0.75
        prop_dy2 = DOWN * 1

        # TODO: use table class
        hori_r = 4
        hori = Line(LEFT * hori_r, RIGHT * hori_r)
        vert = Line(UP, DOWN * 5)
        table = VGroup(hori, vert).shift(UP * 1)

        mul_head = MathTex('\cdot', font_size=125, color=blue)
        star_head = MathTex('\star', font_size=75, color=blue)
        mul_head.move_to((hori.get_center() + hori.get_left()) / 2).shift(UP * 0.5)
        star_head.move_to((hori.get_center() + hori.get_right()) / 2).shift(UP * 0.5)

        mul_comm = Tex('commutative, associative', font_size=prop_fs, color=blue)
        star_comm = Tex('commutative, associative', font_size=prop_fs, color=blue)
        mul_comm.next_to(hori, DOWN, buff=0.5, aligned_edge=RIGHT).shift(LEFT * (hori_r + 0.5))
        star_comm.next_to(hori, DOWN, buff=0.5, aligned_edge=LEFT).shift(RIGHT * (hori_r + 0.5))

        mul_zero = MathTex('x \cdot {{0}} = {{0}}', font_size=prop_fs, color=blue).next_to(mul_comm, ORIGIN, buff=0, aligned_edge=RIGHT).shift(prop_dy1)
        star_zero = MathTex('x \star {{1}} = {{1}}', font_size=prop_fs, color=blue).next_to(star_comm, ORIGIN, buff=0, aligned_edge=LEFT).shift(prop_dy1)
        mul_zero.get_parts_by_tex('0').set_color(red)
        star_zero.get_parts_by_tex('1').set_color(red)

        mul_one = MathTex('x \cdot {{1}} = x', font_size=prop_fs, color=blue).next_to(mul_zero, ORIGIN, buff=0, aligned_edge=RIGHT).shift(prop_dy1)
        star_one = MathTex('x \star {{e}} = x', font_size=prop_fs, color=blue).next_to(star_zero, ORIGIN, buff=0, aligned_edge=LEFT).shift(prop_dy1)
        mul_one.get_parts_by_tex('1').set_color(red)
        star_one.get_parts_by_tex('e').set_color(red)

        mul_inv = MathTex('x \cdot {{\\frac{1}{a}}} = {{1}} \ (x \\neq {{0}})', font_size=prop_fs, color=blue).next_to(mul_one, ORIGIN, buff=0, aligned_edge=RIGHT).shift(prop_dy2)
        star_inv = MathTex('x \star {{\exp \\frac{1}{\log x}}} = {{e}} \ (x \\neq {{1}})', font_size=prop_fs, color=blue).next_to(star_one, ORIGIN, buff=0, aligned_edge=LEFT).shift(prop_dy2)
        mul_inv.get_parts_by_tex('1').set_color(red)
        mul_inv.get_parts_by_tex('0').set_color(red)
        star_inv.get_parts_by_tex('e', substring=False).set_color(red)
        star_inv.get_parts_by_tex('1').set_color(red)

        mul_root = MathTex('{{\sqrt{x}}} \cdot {{\sqrt{x}}} = x', '\ (x \geq {{0}})', font_size=prop_fs, color=blue).next_to(mul_inv, ORIGIN, buff=0, aligned_edge=RIGHT).shift(prop_dy2)
        star_root = MathTex('{{y}} \star {{y}} = x', '\ (x \geq {{1}})', font_size=prop_fs, color=blue).next_to(star_inv, ORIGIN, buff=0, aligned_edge=LEFT).shift(prop_dy2)
        mul_root.get_parts_by_tex('sqrt').set_color(red)
        mul_root.get_parts_by_tex('0').set_color(red)
        star_root.get_parts_by_tex('y').set_color(red)
        star_root.get_parts_by_tex('1').set_color(red)

        star_root2 = MathTex('{{(\exp \sqrt{\log x})}} \star {{(\exp \sqrt{\log x})}} = x', '\ (x \geq {{1}})', font_size=prop_fs, color=blue).next_to(star_inv, ORIGIN, buff=0, aligned_edge=LEFT).shift(prop_dy2)
        star_root2.get_parts_by_tex('sqrt').set_color(red)
        star_root2[4:].set_color(BLACK)

        self.play(FadeIn(table, mul_head, star_head))
        self.play(FadeIn(mul_comm))
        self.play(FadeIn(star_comm))
        self.play(FadeIn(mul_zero))
        self.play(FadeIn(star_zero))
        self.play(FadeIn(mul_one))
        self.play(FadeIn(star_one))
        self.play(FadeIn(mul_inv))
        self.play(FadeIn(star_inv))
        self.play(FadeIn(mul_root))
        self.play(FadeIn(star_root))
        self.play(ReplacementTransform(star_root, star_root2))

        self.fade_all(
            VGroup(mul_root, star_root2), VGroup(mul_inv, star_inv), 
            VGroup(mul_one, star_one), VGroup(mul_zero, star_zero), 
            VGroup(mul_comm, star_comm), VGroup(mul_head, star_head), table)
    
    def scene5(self, star_def):
        eq = MathTex('y = x \star a', '= x^z', color=red, font_size=50)
        eq.shift(-eq[0].get_center() + UP * 1.5)

        a = Variable(1.80, 'a').scale(40 / 48).next_to(eq[0], DOWN, 0.4)
        axes = Axes(x_range=(0, 10), y_range=(0, 5), x_length=(8 * 1), y_length=(5 * 1)).shift(DOWN * 0.7)
        curve = always_redraw(lambda: axes.plot(lambda x: x ** math.log(a.tracker.get_value()), x_range=(0.1, 10)).set_color(red)) 

        self.play(FadeIn(eq[0], a, axes, curve))
        self.play(a.tracker.animate.set_value(7.20))
        self.play(a.tracker.animate.set_value(1 / math.e))

        a_inv = MathTex('=', '1/e', font_size=40).next_to(a, RIGHT, buff=0.2)
        a_0 = MathTex('=', '1', font_size=40).next_to(a, RIGHT, buff=0.2)
        a_1 = MathTex('=', 'e', font_size=40).next_to(a, RIGHT, buff=0.2)
        a_2 = MathTex('=', 'e^2', font_size=40).next_to(a, RIGHT, buff=0.2)
        a_z = MathTex('=', 'e^z', font_size=40).next_to(a, RIGHT, buff=0.2)

        for m in [ a_inv, a_0, a_1, a_2, a_z ]:
            a_y = a.label.get_y() 
            m_y = m[0].get_y()
            m.shift(UP * (a_y - m_y))

        eq_inv = MathTex('1/x', color=red, font_size=50)
        eq_0 = MathTex('1', color=red, font_size=50)
        eq_1 = MathTex('x', color=red, font_size=50)
        eq_2 = MathTex('x^2', color=red, font_size=50)

        self.play(FadeIn(a_inv))
        self.play(FadeIn(eq_inv.move_to(axes.coords_to_point(3, 1/3) + UP * 0.5)))

        half1 = squish_rate_func(smooth, 0, 0.5)
        half2 = squish_rate_func(smooth, 0.5, 1)

        self.play(a.tracker.animate.set_value(1), FadeOut(a_inv, eq_inv, rate_func=half1), FadeIn(a_0, rate_func=half2))
        self.play(FadeIn(eq_0.move_to(axes.coords_to_point(3, 1) + UP * 0.5)))
        self.play(a.tracker.animate.set_value(math.e), FadeOut(a_0, eq_0, rate_func=half1), FadeIn(a_1, rate_func=half2))
        self.play(FadeIn(eq_1.move_to(axes.coords_to_point(2.3, 2.3) + DR * 0.35)))
        self.play(a.tracker.animate.set_value(math.e ** 2), FadeOut(a_1, eq_1, rate_func=half1), FadeIn(a_2, rate_func=half2))
        self.play(FadeIn(eq_2.move_to(axes.coords_to_point(1.6, 1.6 ** 2) + RIGHT * 0.5)))

        self.play(FadeOut(a_2, eq_2))

        exp_def = MathTex('x^y = \exp(\log x \cdot y)', font_size=50).shift(DOWN + RIGHT * 2)
        star_def2 = MathTex('x \star a =', '\exp(\log x \cdot \log a)', font_size=50).next_to(exp_def, DOWN, 0.4)
        star_exp = MathTex('x \star a =', 'x^{\log a}', font_size=50).move_to(star_def2)

        self.play(FadeIn(exp_def))
        self.play(FadeIn(star_def2))
        self.play(ReplacementTransform(star_def2, star_exp))

        self.play(FadeIn(a_z))
        self.play(FadeIn(eq[1]))
        self.fade_all(star_def, VGroup(axes, curve), eq, VGroup(a, a_z), exp_def, star_exp)
    
    def scene6(self):
        add = MathTex('+', font_size=75, color=green)
        mul = MathTex('\cdot', font_size=125, color=green)
        star = MathTex('\star', font_size=75, color=green)
        VGroup(add, mul, star).arrange(direction=DOWN, buff=1)

        self.play(FadeIn(add, mul))
        self.play(FadeIn(star))

        c1 = Text('op', **fancy, font_size=50)
        c2 = Text('defined for:', **fancy, font_size=50)
        real1 = Tex('all numbers', font_size=50, color=BLACK)
        real2 = real1.copy()
        pos = Tex('positive numbers', font_size=50, color=BLACK)
        [ add_t, mul_t, star_t ] = [ m.copy() for m in [ add, mul, star ] ]
        
        table = MobjectTable(
            [ [ c1, c2 ],
              [ add_t, real1 ],
              [ mul_t, real2 ],
              [ star_t, pos ] ])
        self.play(Transform(add, add_t), Transform(mul, mul_t), Transform(star, star_t))
        self.play(FadeIn(table))
        self.remove(add, mul, star)
        
        self.play(real1.animate.set_color(WHITE), real2.animate.set_color(WHITE))
        self.play(pos.animate.set_color(WHITE))

        arr_x = add_t.get_x() - 0.28
        between = lambda m1, m2: [ RIGHT * arr_x + UP * (m1.get_y() - 0.1), RIGHT * arr_x + UP * (m2.get_y() + 0.1) ]

        arr_mul = ArcBetweenPoints(*between(add_t, mul_t), color=yellow).add_tip(**tip_size(0.27), at_start=True)
        arr_star = ArcBetweenPoints(*between(mul_t, star_t), color=yellow).add_tip(**tip_size(0.27), at_start=True)
        self.play(FadeIn(arr_mul))
        self.play(FadeIn(arr_star))

        self.play(VGroup(table, arr_mul, arr_star).animate.to_edge(UP, buff=0.2))

        hori = table.get_horizontal_lines()
        line_height1 = hori[2].get_center() - hori[1].get_center()
        line_height2 = UP * table.get_bottom()[1] - hori[2].get_center()
        new_lines = [ hori[2].copy().shift(line_height2 + line_height1 * i) for i in range(3) ]
        new_lines.append(table.get_vertical_lines()[0].copy().shift(DOWN * 3))
        self.play(FadeIn(*new_lines))

        dia = MathTex('\diamond', font_size=75, color=green).move_to(star_t).shift((line_height1 + line_height2) / 2)
        gt_1 = Tex('numbers $> 1$', font_size=50, fill_opacity=0).move_to(pos).shift((line_height1 + line_height2) / 2)
        arr_dia = ArcBetweenPoints(*between(star_t, dia), color=yellow).add_tip(**tip_size(0.27), at_start=True)
        self.play(FadeIn(dia, arr_dia))

        table_ext = VGroup(table, *new_lines, dia, gt_1, arr_mul, arr_star, arr_dia)
        self.play(table_ext.animate.to_edge(LEFT, buff=0.2))

        star_def = MathTex('x \star y = \exp (\log x \cdot \log y)', font_size=50, color=blue)
        dia_def = MathTex('x \diamond y = \exp {{(\log x \star \log y)}}', font_size=50, color=blue)
        dia_def2 = MathTex('x \diamond y = \exp {{\exp (\log \log x \cdot \log \log y)}}', font_size=40, color=blue)
        center_right = RIGHT * (table_ext.get_right()[0] + config['frame_x_radius']) / 2
        VGroup(star_def, dia_def).arrange(DOWN, buff=0.75).move_to(center_right)

        self.play(FadeIn(star_def))
        self.play(FadeIn(dia_def))
        self.play(ReplacementTransform(dia_def, dia_def2.move_to(dia_def)))
        self.play(gt_1.animate.set_opacity(1))

        dia_zero = MathTex('x \diamond e = e', font_size=50, color=red)
        dia_one = MathTex('x \diamond e^e = x', font_size=50, color=red)
        VGroup(dia_zero, dia_one).arrange(DOWN, buff=0.75).next_to(dia_def2, DOWN, buff=0.8)
        self.play(FadeIn(dia_zero))
        self.play(FadeIn(dia_one))

        ops = VGroup(add_t.copy(), mul_t.copy(), star_t.copy(), dia.copy())
        self.add(ops)
        self.fade_all(table_ext, star_def, dia_def2, dia_zero, dia_one)
        self.play(ops.animate.arrange(DOWN, buff=0.75))
        return ops
    
    def scene7(self, ops):
        dot_n = MathTex('\cdot', '_n', font_size=125, color=blue).shift(LEFT * 3.5)
        self.play(FadeIn(dot_n[0]))
        self.play(FadeIn(dot_n[1]))
        
        dot_0 = MathTex('{{=}} \cdot_0', font_size=75, color=blue)
        dot_1 = MathTex('{{=}} \cdot_1', font_size=75, color=blue)
        dot_2 = MathTex('{{=}} \cdot_2', font_size=75, color=blue)
        dot_0.shift(RIGHT * (0.75 - dot_0[0].get_x()) + UP * (ops[1].get_y() - dot_0[0].get_y()))
        dot_1.shift(RIGHT * (0.75 - dot_1[0].get_x()) + UP * (ops[2].get_y() - dot_1[0].get_y()))
        dot_2.shift(RIGHT * (0.75 - dot_2[0].get_x()) + UP * (ops[3].get_y() - dot_2[0].get_y()))
        self.play(FadeIn(dot_0))
        self.play(FadeIn(dot_1))
        self.play(FadeIn(dot_2))

        log_n = MathTex('{{\log}}^n =', '{{\log}} \dots {{\log}}', font_size=50, color=blue)
        log_2 = MathTex('{{\log}}^2 x = {{\log}} {{\log}} x', font_size=50, color=blue)
        log_3 = MathTex('{{\log}}^3 x = {{\log}} {{\log}} {{\log}} x', font_size=50, color=blue)
        VGroup(log_n, log_2, log_3).arrange(DOWN, buff=0.6).move_to(dot_n)
        self.play(FadeOut(dot_n))
        self.play(FadeIn(log_n[2:]))
        self.play(FadeIn(log_n[0:2]))
        self.play(FadeIn(log_2))
        self.play(FadeIn(log_3))

        exp_n = MathTex('{{\exp}}^n =', '{{\exp}} \dots {{\exp}}', font_size=50, color=blue).move_to(log_n)
        exp_2 = MathTex('{{\exp}}^2 x = {{\exp}} {{\exp}} x', font_size=50, color=blue).move_to(log_2)
        exp_3 = MathTex('{{\exp}}^3 x = {{\exp}} {{\exp}} {{\exp}} x', font_size=50, color=blue).move_to(log_3)
        self.play(ReplacementTransform(log_n, exp_n), ReplacementTransform(log_2, exp_2), ReplacementTransform(log_3, exp_3))

        dot1_def = MathTex('x \cdot_1 y = \exp^1 (\log^1 x \cdot \log^1 y)', font_size=45, color=blue)
        dot2_def = MathTex('x \cdot_2 y = \exp^2 (\log^2 x \cdot \log^2 y)', font_size=45, color=blue)
        dot1_def.shift(dot_1[0].get_left() - dot1_def.get_left() + RIGHT * 0.25)
        dot2_def.shift(dot_2[0].get_left() - dot2_def.get_left() + RIGHT * 0.25)
        self.play(FadeOut(dot_0, dot_1, dot_2))
        self.play(FadeIn(dot1_def, dot2_def))

        dotn_def = MathTex('x \cdot_n y = {{\exp^n}} ({{\log^n x}} {{\cdot}} {{\log^n y}})', font_size=50, color=red).to_edge(UP, buff=0.9)
        self.play(FadeIn(dotn_def))

        self.fade_all(exp_n, exp_2, exp_3, ops, dot1_def, dot2_def)
        dom = Text('domain?', **fancy, font_size=50).next_to(dotn_def, DOWN, buff=0.75)
        self.play(Write(dom))

        box = lambda m: SurroundingRectangle(m, color=yellow, buff=0.1)
        boxes1 = VGroup(*[ box(m) for m in dotn_def.get_parts_by_tex('log') ])
        boxes2 = VGroup(*[ box(m) for m in [ dotn_def.get_part_by_tex('exp'), dotn_def.get_part_by_tex('\cdot', substring=False) ] ])
        self.play(Create(boxes1))
        self.play(ReplacementTransform(boxes1, boxes2))
        self.play(FadeOut(boxes2))
        
        doms = MathTex('\mathrm{dom}(\cdot_n) = \mathrm{dom}(\log^n)', font_size=50, color=blue).next_to(dom, DOWN, buff=0.75)
        self.play(FadeIn(doms))

        log0 = MathTex('\log^0 x = x', font_size=50, color=blue).next_to(doms, DOWN, buff=0.4)
        dom_log0 = MathTex('\mathrm{dom}({{\log^0}}) = \\text{anything}', font_size=50, color=blue).next_to(log0, DOWN, buff=0.4)
        self.play(FadeIn(log0))
        self.play(FadeIn(dom_log0))

        self.play(FadeOut(log0), dom_log0.animate.to_corner(DL, buff=0.9))

        log_exp = MathTex('\mathrm{dom}(\cdot_n) = \mathrm{dom}(\log^n)', '= \mathrm{range}(\exp^n)', font_size=50, color=blue).move_to(doms)
        self.play(ReplacementTransform(doms[0], log_exp[0]), FadeIn(log_exp[1]))

        line = NumberLine(x_range=(-5, 6), length=8, include_numbers=True, include_tip=True).shift(DOWN * 1.2).to_edge(LEFT, buff=0.8)
        dots = [ Dot(point=line.number_to_point(x), radius=0.05, color=red) for x in frange(-5, 5.5, 0.25) ]
        self.play(FadeIn(line, *dots))

        def animate_dot(dot):
            x = line.point_to_number(dot.get_center())
            if x > 5.5: return Wait()
            ex = math.exp(x)
            diff = ex - x
            end_point = line.number_to_point(ex)
            angle = -PI / diff
            if ex > 5.5:
                return ApplyFunction(lambda m: m.move_to(end_point).set_opacity(0), dot, path_arc=angle)
            return ApplyFunction(lambda m: m.move_to(end_point), dot, path_arc=angle)

        range1 = MathTex('{{\mathrm{range}(\exp^1)}} = \{x > 0\}', font_size=40, color=blue).shift(DOWN * 0.75).to_edge(RIGHT, buff=0.8)
        range2 = MathTex('{{\mathrm{range}(\exp^2)}} = \{x > 1\}', font_size=40, color=blue).next_to(range1, DOWN, buff=0.3)
        range3 = MathTex('{{\mathrm{range}(\exp^3)}} = \{x > {{\exp 1}}\}', font_size=40, color=blue).next_to(range2, DOWN, buff=0.3)
        range4 = MathTex('{{\mathrm{range}(\exp^4)}} = \{x > {{\exp^2 1}}\}', font_size=40, color=blue).next_to(range3, DOWN, buff=0.3)
    
        self.play(*[ animate_dot(dot) for dot in dots ])
        self.play(FadeIn(range1))
        self.play(*[ animate_dot(dot) for dot in dots ])
        self.play(FadeIn(range2))
        self.play(*[ animate_dot(dot) for dot in dots ])
        self.play(FadeIn(range3))
        self.play(*[ animate_dot(dot) for dot in dots ])
        self.play(FadeIn(range4))

        self.remove(*dots)

        dom0 = MathTex('\mathrm{dom}({{\log^0}}) = \\text{anything}', font_size=50, color=blue)
        dom1 = MathTex('{{\mathrm{range}(\exp^1)}} = \{x > 0\}', font_size=50, color=blue)
        dom2 = MathTex('{{\mathrm{range}(\exp^2)}} = \{x > 1\}', font_size=50, color=blue)
        dom3 = MathTex('{{\mathrm{range}(\exp^3)}} = \{x > {{\exp 1}}\}', font_size=50, color=blue)
        dom4 = MathTex('{{\mathrm{range}(\exp^4)}} = \{x > {{\exp^2 1}}\}', font_size=50, color=blue)
        vdots = MathTex('\\vdots', font_size=50, color=blue)
        VGroup(dom0, dom1, dom2, dom3, dom4, vdots).arrange(DOWN, buff=0.4)

        self.play(
            FadeOut(dotn_def, dom, log_exp, line), 
            ReplacementTransform(dom_log0, dom0), ReplacementTransform(range1, dom1), 
            ReplacementTransform(range2, dom2), ReplacementTransform(range3, dom3), 
            ReplacementTransform(range4, dom4), FadeIn(vdots))
    
        self.play(VGroup(dom3[2], dom4[2]).animate.set_color(red))
        dom3_e = MathTex('{{\mathrm{range}(\exp^3)}} = \{x > {{e}}\}', font_size=50, color=blue).move_to(dom3)
        dom4_e = MathTex('{{\mathrm{range}(\exp^4)}} = \{x > {{e^e}}\}', font_size=50, color=blue).move_to(dom4)
        dom3_e[2].set_color(red)
        dom4_e[2].set_color(red)
        self.play(ReplacementTransform(dom3, dom3_e), ReplacementTransform(dom4, dom4_e))

        dom5 = MathTex('{{\mathrm{range}(\exp^5)}} = \{x > {{e^{e^e}}}\}', font_size=50, color=blue)
        dom5[2].set_color(red)
        doms = VGroup(dom0.copy(), dom1.copy(), dom2.copy(), dom3_e.copy(), dom4_e.copy(), dom5, vdots.copy())
        doms.arrange(DOWN, buff=0.4)
        self.play(
            ReplacementTransform(dom0, doms[0]), 
            ReplacementTransform(dom1, doms[1]),
            ReplacementTransform(dom2, doms[2]),
            ReplacementTransform(dom3_e, doms[3]),
            ReplacementTransform(dom4_e, doms[4]),
            ReplacementTransform(vdots, doms[6]),
            FadeIn(doms[5]))
    
        mil = MathTex('\\approx 3.81 \\text{ million}', font_size=50, color=red)
        mil.next_to(dom5[-1], RIGHT, buff=0.25)
        self.play(FadeIn(mil))

        dom6 = MathTex('{{\mathrm{range}(\exp^6)}} = \{x > {{e^{e^{e^e}}}}\}', font_size=50, color=blue).next_to(dom5, DOWN, buff=0.3)
        dom6[2].set_color(red)
        self.play(FadeIn(dom6), doms[6].animate.shift(DOWN * 2))

        digits = Tex('1.65 million digits!}', font_size=40)
        digits.next_to(dom6[-1], RIGHT, buff=0.25)
        self.play(FadeIn(digits))

        self.play(FadeOut(mil, digits))
        dot_dom = [
            MathTex('\mathrm{dom}({{\cdot_0}}) = \\text{anything}', '= {{K_0}}', font_size=50, color=blue).move_to(doms[0]),
            MathTex('{{\mathrm{dom}(\cdot_1)}} = \{x > 0\}', '= {{K_1}}', font_size=50, color=blue).move_to(doms[1]),
            MathTex('{{\mathrm{dom}(\cdot_2)}} = \{x > 1\}', '= {{K_2}}', font_size=50, color=blue).move_to(doms[2]),
            MathTex('{{\mathrm{dom}(\cdot_3)}} = \{x > {{e}}\}', '= {{K_3}}', font_size=50, color=blue).move_to(doms[3]),
            MathTex('{{\mathrm{dom}(\cdot_4)}} = \{x > {{e^e}}\}', '= {{K_4}}', font_size=50, color=blue).move_to(doms[4]),
            MathTex('{{\mathrm{dom}(\cdot_5)}} = \{x > {{e^{e^e}}}\}', '= {{K_5}}', font_size=50, color=blue).move_to(dom5),
            MathTex('{{\mathrm{dom}(\cdot_6)}} = \{x > {{e^{e^{e^e}}}}\}', '= {{K_6}}', font_size=50, color=blue).move_to(dom6),
        ]
        for m in dot_dom:
            m[-2:].set_color(green)

        to_transform = [ doms[i] for i in range(6) ]
        to_transform.append(dom6)
        self.play(*[ ReplacementTransform(to_transform[i], dot_dom[i][0:-2]) for i in range(7) ])
        
        k_n = MathTex('K_n', font_size=75, color=green).to_edge(RIGHT, buff=2)
        self.play(FadeIn(k_n))
        self.play(FadeIn(dot_dom[0][-2:]))
        self.play(FadeIn(dot_dom[1][-2:]))
        self.fadein_all(*[ m[-2:] for m in dot_dom[2:] ])

        self.play(FadeOut(k_n), AnimationGroup(*[ m.animate.to_edge(LEFT, 1) for m in dot_dom ], lag_ratio=0.05))

        dot_def = Tex('$x \cdot_n y =$ \\\\ $\exp^n (\log^n x \cdot \log^n y)$', font_size=50)
        plus_def = Tex('$x +_n y =$ \\\\ $\exp^n (\log^n x + \log^n y)$', font_size=50)

        plus_dot = MathTex('+_n', '= \cdot_{n - 1}', font_size=50, color=blue)
        plus_dot[0].set_color(green)
        restricted = Tex('(smaller domain)', font_size=40, color=green)
        plus_dot_group = VGroup(plus_dot, restricted).arrange(DOWN, buff=0.2)

        plus1_dot = MathTex('x +_1 y', '= x \cdot y', font_size=50, color=blue)
        plus1_dot[0].set_color(green)
        positive = MathTex('(x, y > 0)', font_size=40, color=green)
        plus1_dot_group = VGroup(plus1_dot, positive).arrange(DOWN, buff=0.2)

        right = VGroup(dot_def, plus_def, plus_dot_group, plus1_dot_group).arrange(DOWN, buff=0.6).to_edge(RIGHT, buff=1.25)

        self.play(FadeIn(dot_def))
        self.play(FadeIn(plus_def))
        self.play(FadeIn(plus_dot_group))
        self.play(FadeIn(plus1_dot_group))

        fields = [ m[-1].copy() for m in dot_dom[0:5] ]
        fields.append(MathTex('\\vdots', font_size=50, color=green))

        VGroup(*fields).arrange(DOWN, buff=0.8).to_edge(LEFT, buff=2)

        self.play(AnimationGroup(
            FadeOut(*[ m[0:-1] for m in dot_dom[0:5] ], *dot_dom[5:]),
            AnimationGroup(*[ ReplacementTransform(dot_dom[i][-1], fields[i]) for i in range(5) ]),
            *[ FadeOut(m) for m in right ],
            FadeIn(fields[-1]),
            lag_ratio=0.075))
    
        return fields

    def scene8(self, fields):
        plus = [ MathTex('+_' + str(i), font_size=50, color=blue) for i in range(5) ]
        dots = [ MathTex('\cdot_' + str(i), font_size=50, color=blue) for i in range(5) ]
        plus.append(MathTex('\\vdots', font_size=50, color=blue))
        dots.append(MathTex('\\vdots', font_size=50, color=blue))
        
        plus[0].next_to(fields[0], RIGHT, buff=1.2)
        dots[0].next_to(plus[0], RIGHT, buff=0.8)

        for i in range(1, 6):
            plus[i].set_x(plus[0].get_x()).set_y(fields[i].get_y())
            dots[i].set_x(dots[0].get_x()).set_y(fields[i].get_y())
        
        for m in dots[0:-1]:
            m.shift(DOWN * 0.06)
        
        self.play(FadeIn(*plus))
        self.play(FadeIn(*dots))

        properties = [
            MathTex(txt, font_size=44, color=blue) 
            for txt in [
                'a \cdot_n (x +_n y) = (a \cdot_n x) +_n (a \cdot_n y)',
                'x +_n y = y +_n x',
                'x \cdot_n y = y \cdot_n x',
                '(x +_n y) +_n z = x +_n (y +_n z)',
                '(x \cdot_n y) \cdot_n z = x \cdot_n (y \cdot_n z)',
                'x +_n {{\exp^n 0}} = x',
                'x \cdot_n {{\exp^n 1}} = x',
                'x \cdot_n {{\exp^n 0}} = {{\exp^n 0}}',
            ]
        ]
        pgroup = VGroup(*properties).arrange(DOWN, buff=0.5).to_edge(RIGHT, buff=1)
        self.play(FadeIn(pgroup))

        boxes0 = [
            SurroundingRectangle(m, color=yellow, buff=0.1)
            for m in [ properties[5][1], properties[7][1], properties[7][3] ]
        ]
        box1 = SurroundingRectangle(properties[6][1], color=yellow, buff=0.1)
        self.play(*[ Create(m) for m in boxes0 ])
        self.play(AnimationGroup(FadeOut(*boxes0[1:]), ReplacementTransform(boxes0[0], box1), lag_ratio=0.2))
        self.play(FadeOut(box1))

        start = VGroup(plus[1], dots[0]).get_center() + UR * 0.08
        step = dots[1].get_center() - dots[0].get_center()
        
        eqs = [
            MathTex('=', font_size=75, color=purple).rotate(PI * 0.25).move_to(start + step * i)
            for i in range(5)
        ]
        self.fadein_all(*eqs)

        # gap: 0.25
        exp_arrow = ArcBetweenPoints(fields[1].get_right() + RIGHT * 0.05 + UP * 0.1, fields[0].get_right() + RIGHT * 0.12 + DOWN * 0.15, angle=(TAU / 5), color=purple)
        log_arrow = ArcBetweenPoints(fields[0].get_left() + LEFT * 0.07 + DOWN * 0.14, fields[1].get_left() + LEFT * 0.07 + UP * 0.08, angle=(TAU / 5), color=purple)
        exp_arrow.add_tip(**tip_size(0.27), at_start=True)
        log_arrow.add_tip(**tip_size(0.27), at_start=True)

        exp_arrs = [ exp_arrow.copy().shift(step * i) for i in range(5) ]
        log_arrs = [ log_arrow.copy().shift(step * i) for i in range(5) ]
        exp = MathTex('\exp', font_size=40, color=purple).next_to(exp_arrs[0], RIGHT, buff=0.15)
        log = MathTex('\log', font_size=40, color=purple).next_to(log_arrs[4], LEFT, buff=0.15)
        self.fadein_all(exp, *exp_arrs)
        self.fadein_all(log, *reversed(log_arrs))

        plus_boxes = [ SurroundingRectangle(m, color=yellow, buff=0.1) for m in plus[1:5] ] 
        self.play(*[ Create(m) for m in plus_boxes ])
        self.play(*[ plus_boxes[i].animate.move_to(dots[i]) for i in range(4) ])
        self.play(FadeOut(*plus_boxes))
        
        plus0_box = SurroundingRectangle(plus[0], color=yellow, buff=0.1)
        self.play(Create(plus0_box))

        self.play(*[ m.animate.shift(DOWN * 3.25) for m in self.get_top_level_mobjects() ], plus0_box.animate.shift(DOWN * 3.25).set_opacity(0))

        neg_fields = [ 
            MathTex('K_{-1}', font_size=50, color=green).move_to(fields[0].get_center() - step),
            MathTex('K_{-2}', font_size=50, color=green).move_to(fields[0].get_center() - step * 2),
            MathTex('\\vdots', font_size=50, color=green).move_to(fields[0].get_center() - step * 3),
        ]

        neg_plus = [ 
            MathTex('+_{-1}', font_size=50, color=blue).move_to(plus[0].get_center() - step),
            MathTex('+_{-2}', font_size=50, color=blue).move_to(plus[0].get_center() - step * 2),
            MathTex('\\vdots', font_size=50, color=blue).move_to(plus[0].get_center() - step * 3),
        ]

        neg_dots = [ 
            MathTex('\cdot_{-1}', font_size=50, color=blue).move_to(dots[0].get_center() - step),
            MathTex('\cdot_{-2}', font_size=50, color=blue).move_to(dots[0].get_center() - step * 2),
            MathTex('\\vdots', font_size=50, color=blue).move_to(dots[-1].get_center() - step * 8),
        ]

        self.play(FadeIn(neg_fields[0], neg_plus[0], neg_dots[0]))
        self.play(FadeIn(*neg_fields[1:], *neg_plus[1:], *neg_dots[1:]))

        expo = Text('exponential numbers', **fancy, font_size=50).next_to(properties[0], UP, buff=1.5)
        self.play(Write(expo))

        log_arr1 = log_arrs[0].copy().shift(-step)
        self.play(FadeIn(log_arr1))

        self.play(FadeOut(expo, *properties))
        
        K_1 = MathTex('K_{-1}', font_size=60).move_to(expo)
        top = NumberLine(x_range=(-4, 4), length=6).next_to(K_1, DOWN, buff=1.2)
        log0 = Dot().next_to(top, DOWN, buff=1)
        log0_label = MathTex('\log 0', font_size=40, color=purple).next_to(log0, RIGHT, buff=0.15)
        bottom = top.copy().next_to(log0, DOWN, buff=1)

        top_tips = VGroup(
            ArrowTriangleFilledTip(color=WHITE).move_to(top.get_left() + LEFT * 0.15), 
            ArrowTriangleFilledTip(color=WHITE).rotate(PI).move_to(top.get_right() + RIGHT * 0.15))
        bottom_tips = VGroup(
            ArrowTriangleFilledTip(color=WHITE).move_to(bottom.get_left() + LEFT * 0.15), 
            ArrowTriangleFilledTip(color=WHITE).rotate(PI).move_to(bottom.get_right() + RIGHT * 0.15))

        self.play(FadeIn(K_1, top, top_tips))
        self.fadein_all(log0, log0_label)
        self.play(FadeIn(bottom, bottom_tips))

        pstart = log0.get_center() + LEFT * 1.5
        pointer1 = Line(pstart, pstart + UR, color=yellow,).add_tip(**tip_size(0.27))
        pointer2 = Line(pstart, pstart + RIGHT * 1.25, color=yellow,).add_tip(**tip_size(0.27))
        pointer3 = Line(pstart, pstart + DR, color=yellow,).add_tip(**tip_size(0.27))
        self.play(FadeIn(pointer1))
        self.play(ReplacementTransform(pointer1, pointer2))
        self.play(ReplacementTransform(pointer2, pointer3))
        
        log_x = Dot(point=top.number_to_point(0.5), color=green)
        log_x_label = MathTex('\log(x)', font_size=40, color=green).next_to(log_x, UP, 0.15)
        log_nx = Dot(point=bottom.number_to_point(0.5), color=green)
        log_nx_label = MathTex('\log(-x)', font_size=40, color=green).next_to(log_nx, DOWN, 0.15)

        log_1 = log_x.copy().move_to(top.number_to_point(0))
        log_1_label = MathTex('\log(1)', font_size=40, color=green).next_to(log_1, UP, 0.15)
        log_n1 = log_nx.copy().move_to(bottom.number_to_point(0))
        log_n1_label = MathTex('\log(-1)', font_size=40, color=green).next_to(log_n1, DOWN, 0.15)

        log_e = log_x.copy().move_to(top.number_to_point(1))
        log_e_label = MathTex('\log(e)', font_size=40, color=green).next_to(log_e, UP, 0.15)
        log_ne = log_nx.copy().move_to(bottom.number_to_point(1))
        log_ne_label = MathTex('\log(-e)', font_size=40, color=green).next_to(log_ne, DOWN, 0.15)

        self.play(FadeIn(log_nx, log_nx_label))
        self.play(FadeIn(log_x, log_x_label), FadeOut(pointer3))
        self.play(ReplacementTransform(log_x, log_1), FadeOut(log_x_label))
        self.play(FadeIn(log_1_label))
        self.play(ReplacementTransform(log_nx, log_n1), FadeOut(log_nx_label))
        self.play(FadeIn(log_n1_label))
        self.play(ReplacementTransform(log_1, log_e), FadeOut(log_1_label))
        self.play(FadeIn(log_e_label))
        self.play(ReplacementTransform(log_n1, log_ne), FadeOut(log_n1_label))
        self.play(FadeIn(log_ne_label))

        self.play(FadeOut(
            log_e, log_e_label, log_ne, log_ne_label, 
            *fields, *plus, *dots, *neg_fields, *neg_plus, *neg_dots,
            *eqs, exp, log, *exp_arrs, *log_arrs, log_arr1))
        
        sf = 1.4
        self.play(VGroup(K_1, top, top_tips, bottom, bottom_tips, log0, log0_label).animate.scale(sf).move_to(ORIGIN))

        new_top = NumberLine(x_range=(-8, 8), length=12).scale(sf).move_to(top)
        new_bottom = NumberLine(x_range=(-8, 8), length=12).scale(sf).move_to(bottom)
        self.play(FadeOut(top_tips, bottom_tips), FadeIn(new_top, new_bottom))

        self.remove(top, bottom)
        top = new_top
        bottom = new_bottom

        def log_ext(x):
            if x > 0: return top.number_to_point(math.log(x))
            if x < 0: return bottom.number_to_point(math.log(-x))
            return log0.get_center()
        
        x = ValueTracker(5)
        x_dot = always_redraw(lambda: Dot(point=top.number_to_point(x.get_value()), color=red).scale(sf))
        l_dot = always_redraw(lambda: Dot(point=log_ext(x.get_value()), color=blue).scale(sf))
        x_label = always_redraw(lambda: MathTex('x', font_size=(40 * sf), color=red).next_to(x_dot, UP, 0.15 * sf))

        self.play(FadeIn(x_dot))
        self.play(FadeIn(x_label))
        self.play(FadeIn(l_dot))
        self.play(x.animate.set_value(0))
        self.wait()
        self.play(x.animate.set_value(-5))

        minf = MathTex('-\infty', font_size=(40 * sf), color=purple).next_to(log0, RIGHT, 0.15 * sf)
        self.play(ReplacementTransform(log0_label, minf))

        new_pstart = log0.get_center() + LEFT * 1.5 * sf
        new_pointer3 = Line(new_pstart, new_pstart + DR * sf, color=yellow).add_tip(**tip_size(0.27))
        self.play(FadeIn(new_pointer3))
        self.play(FadeOut(x_dot, l_dot, x_label, new_pointer3))

        x.set_value(1)
        x_dot.update()
        x_label.update()
        s_dot = always_redraw(lambda: Dot(point=bottom.number_to_point(x.get_value()), color=blue).scale(sf))
        s_label = MathTex('{\sim} x', font_size=(40 * sf), color=blue).next_to(s_dot, UP, buff=(0.15 * sf))
        self.play(FadeIn(x_dot, x_label, s_dot, s_label))

        x_label.clear_updaters()
        self.play(FadeOut(x_label, s_label), x.animate.set_value(0))
        
        new_x_label = MathTex('0', font_size=(40 * sf), color=red).next_to(x_dot, UP, 0.15 * sf)
        new_s_label = MathTex('\log(-1) = {\sim} 0', font_size=(40 * sf), color=blue).next_to(s_dot, UP, buff=(0.15 * sf))
        self.play(FadeIn(new_x_label, new_s_label))

        sq_def = MathTex('{\sim} x = \log(-\exp x)', font_size=(40 * sf)).next_to(log0, LEFT, buff=0.7).shift(UL * 0.3)
        self.play(FadeIn(sq_def))

        addition = Text('addition', **fancy, font_size=(40 * sf)).next_to(minf, RIGHT, buff=0.7).shift(UR * 0.3)
        self.play(Write(addition))
        self.fade_all(K_1, VGroup(x_dot, new_x_label), top, sq_def, VGroup(log0, minf), addition, VGroup(s_dot, new_s_label), bottom)

    def scene9(self):
        ext = MathTex(
            'x \cdot y =' +
            '\\begin{cases} x, y > 0 & x \cdot y \\\\' +
            'x < 0 \\text{ and } y > 0 & -(-x \cdot y) \\\\ x > 0 \\text{ and } y < 0 & -(x \cdot -y) \\\\' +
            'x, y < 0 & -x \cdot -y \\\\' +
            'x = 0 \\text{ or } y = 0 & 0 \\end{cases}',
            font_size=50) 

        rect = Rectangle(fill_opacity=1, stroke_width=1, fill_color=BLACK).set_z_index(1)
        
        self.add(rect)
        self.play(FadeIn(ext))
