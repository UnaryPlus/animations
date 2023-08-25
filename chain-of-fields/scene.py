# WARNING: bad code ahead!

from manim import *
from manim_voiceover import VoiceoverScene
# from manim_voiceover.services.azure import AzureService
# from manim_voiceover.services.recorder import RecorderService
from manim_voiceover.services.base import SpeechService
from pathlib import Path
from pydub import AudioSegment
import shutil
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
sf = 1.4

FADEIN_T = 0.6
FADEOUT_T = 0.6
FADEALL_T = 1
TRANSFORM_T = 0.8
GROWARROW_T = 1
WRITE_T = 1.5
MOVE_T = 1
BOX_T = 1

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

def fadein_shift(mobject, vec):
    shifted_copy = mobject.copy().shift(vec)
    mobject.fade(1) 
    return Transform(mobject, shifted_copy)

def double_arrow(m1, m2):
    c = VGroup(Line(m1, m2, buff=0.1, color=yellow))
    c += c[0].copy()
    c[0].add_tip(**tip_size(0.27))
    c[1].add_tip(**tip_size(0.27), at_start=True)
    return c

class FileReaderService(SpeechService):
    def __init__(self, audio_dir):
        self.audio_dir = Path().resolve() / Path(audio_dir)
        self.copy_dir = Path().resolve() / Path('media') / Path('voiceovers')
        self.index = 0
        SpeechService.__init__(self, transcription_model='base')
    
    def generate_from_text(self, text, cache_dir=None, path=None):
        audio_file = self.audio_dir / Path('a' + str(self.index) + '.m4a')
        copy_file = self.copy_dir / Path('a' + str(self.index) + '.mp3')
        
        m4a = AudioSegment.from_file(audio_file, format='m4a')
        m4a.export(copy_file, format='mp3')

        print('>>>', 'copied to', copy_file)
    
        json_dict = {
            'input_text': text,
            'original_audio': 'a' + str(self.index) + '.mp3',
        }

        self.index += 1
        return json_dict 

class ChainOfFields(VoiceoverScene):
    def setup(self):
        # self.set_speech_service(AzureService(voice="en-US-GuyNeural", style="newscast"))
        # self.set_speech_service(RecorderService())
        self.set_speech_service(FileReaderService(self.audio_dir))

    def fade_all(self, *mobjects, reverse=False, lag_ratio=0.05, **kwargs):
        fade_iter = reversed(mobjects) if reverse else mobjects
        self.play(AnimationGroup(*[ FadeOut(m) for m in fade_iter ], lag_ratio=lag_ratio), **kwargs)
    
    def fadein_all(self, *mobjects, reverse=False, lag_ratio=0.05, **kwargs):
        fade_iter = reversed(mobjects) if reverse else mobjects
        self.play(AnimationGroup(*[ FadeIn(m) for m in fade_iter ], lag_ratio=lag_ratio), **kwargs)

class Scene1(ChainOfFields):
    audio_dir = 'assets/audio/Scene1'

    def construct(self):

        ###############
        ### SCENE 1 ###
        ###############

        text = add_bookmarks("""
        This story began some years ago when I was pondering a question concerning {bin} binary operations, 
        {ops} operations that {two} take two inputs and {one} produce one output. The two basic binary operations 
        in math are {add} addition and {mul} multiplication, and together these satisfy the distributive property, namely 
        {distr1} A times X plus Y equals A X plus A Y and {distr2} A plus B times X equals A X plus B X. I wondered 
        whether it was possible to define {ques} a third operation that distributes over multiplication just as multiplication 
        distributes over addition. Specifically, if one denotes this hypothetical operation with a {star} star, the goal is to define 
        it such that {props} these two properties hold.
        """)

        with self.voiceover(text) as tracker:

            owen = SVGMobject('assets/images/owen.svg').scale(2.5).to_corner(DL, buff=0)
            me = Text('me', **fancy, font_size=50, color=blue).shift(UP * 2.4 + LEFT * 4.4)
            arrow = Arrow(me.get_bottom(), owen.get_top(), buff=0.2, color=blue)

            c_start = owen.get_corner(UR) + DOWN * 0.6 + LEFT * 0.95
            c_direction = UP * 0.25 + RIGHT
            circles = circle_chain(start=c_start, direction=c_direction, buff=0.3, start_radius=0.2, delta_radius=0.1, n=3, color=red)
            circles.append(Ellipse(width=6, height=4, color=red).next_to(circles[-1], RIGHT, buff=0.3))
    
            t = tracker.time_until_bookmark('bin')
            self.play(DrawBorderThenFill(owen), run_time=(t * 0.45))
            self.play(FadeIn(me), GrowArrow(arrow, point_color=BLACK), run_time=(t * 0.2))
            self.play(AnimationGroup(*[ FadeIn(c) for c in circles ], lag_ratio=0.2), run_time=tracker.time_until_bookmark('bin'))

            bop = Text('binary operations', **fancy, font_size=50, color=red, stroke_color=red).move_to(circles[-1])
            self.play(Write(bop), run_time=tracker.time_until_bookmark('ops', limit=WRITE_T))
            self.wait_until_bookmark('ops')

            node = Circle(radius=0.15, color=blue).next_to(bop, UP, buff=0.5).shift(RIGHT * 0.3)
            input1 = Arrow(node.get_corner(UL) + LEFT + UP * 0.3, node.get_corner(UL), buff=0.1, color=blue)
            input2 = Arrow(node.get_corner(DL) + LEFT + DOWN * 0.3, node.get_corner(DL), buff=0.1, color=blue)
            output = Arrow(node.get_right(), node.get_right() + RIGHT * 1.1, buff=0.15, color=blue)

            self.play(FadeIn(node), run_time=tracker.time_until_bookmark('two', limit=FADEIN_T))
            self.wait_until_bookmark('two')
            self.play(GrowArrow(input1, point_color=BLACK), GrowArrow(input2, point_color=BLACK), run_time=tracker.time_until_bookmark('one', limit=GROWARROW_T))
            self.wait_until_bookmark('one')
            self.play(GrowArrow(output, point_color=BLACK), run_time=GROWARROW_T)

            mul = MathTex('\cdot', font_size=125, color=blue).next_to(bop, DOWN, buff=0.45)
            add = MathTex('+', font_size=75, color=blue).next_to(mul, LEFT, buff=1)
            self.wait_until_bookmark('add')
            self.play(FadeIn(add), run_time=tracker.time_until_bookmark('mul', limit=FADEIN_T))
            self.wait_until_bookmark('mul')
            self.play(FadeIn(mul), run_time=FADEIN_T)

            distr1 = MathTex('a {{\cdot}} (x {{+}} y) = (a {{\cdot}} x) {{+}} (a {{\cdot}} y)', font_size=50, color=blue).next_to(circles[-1], DOWN, buff=0.5).shift(LEFT * 1.2)
            distr2 = MathTex('(a {{+}} b) {{\cdot}} x = (a {{\cdot}} x) {{+}} (b {{\cdot}} x)', font_size=50, color=blue).next_to(distr1, DOWN, buff=0.5)
            self.wait_until_bookmark('distr1')
            self.play(FadeIn(distr1), run_time=tracker.time_until_bookmark('distr2', limit=FADEIN_T))
            self.wait_until_bookmark('distr2')
            self.play(FadeIn(distr2), run_time=FADEIN_T)

            ques = MathTex('?', font_size=75, color=green).next_to(mul, RIGHT, buff=1)
            star = MathTex('\star', font_size=75, color=green).move_to(ques)
            self.wait_until_bookmark('ques')
            self.play(FadeIn(ques), run_time=FADEIN_T)
            self.wait_until_bookmark('star')
            self.play(ReplacementTransform(ques, star), run_time=TRANSFORM_T)

            distr1_star = MathTex('a {{\star}} (x {{\cdot}} y) = (a {{\star}} x) {{\cdot}} (a {{\star}} y)', font_size=50, color=blue).move_to(distr1)
            distr2_star = MathTex('(a {{\cdot}} b) {{\star}} x = (a {{\star}} x) {{\cdot}} (b {{\star}} x)', font_size=50, color=blue).move_to(distr2)
            distr1_star.get_parts_by_tex('\star').set_color(green)
            distr2_star.get_parts_by_tex('\star').set_color(green)
            self.wait_until_bookmark('props')
            self.play(ReplacementTransform(distr1, distr1_star), ReplacementTransform(distr2, distr2_star), run_time=TRANSFORM_T)

        self.fade_all(owen, me, arrow, *circles, bop, node, input1, input2, output, add, mul, star, reverse=True, run_time=FADEALL_T)
        
        text = add_bookmarks("""
        An obvious first candidate is {exp} exponentiation, since there's a way in which the relationship between exponentiation 
        and multiplication is the same as that between multiplication and addition, namely when one of the inputs is {nat} a 
        natural number, then {radd} multiplication is the same as repeated addition and {rmul} exponentiation is repeated multiplication. {end}
        And exponentiation does satisfy {p1} this property, since {i1} A B to the X equals A to the X times B to the X. But it doesn't satisfy {p2} the other 
        property, since {i2} A to the X Y is not usually equal to A to the X times A to the Y. {strike} I wanted an operation that satisfied both distributive 
        properties.
        """)

        with self.voiceover(text) as tracker:

            star_exp = MathTex('x {{\star}} y = x^y?', font_size=50, color=blue).to_edge(UP, buff=1)
            star_exp.get_parts_by_tex('\star').set_color(green)
            self.wait_until_bookmark('exp')
            self.play(FadeIn(star_exp), run_time=FADEIN_T)            

            rep_add = MathTex('x \cdot n', '= \\underbrace{x + \dots + x}_{n \\text{ copies}}', color=red).to_edge(LEFT, buff=2).shift(UP, 0.15)
            rep_mul = MathTex('x^n', '= \\underbrace{x \cdot \dots \cdot x}_{n \\text{ copies}}', color=red).next_to(rep_add, DOWN, buff=0.25)
            self.wait_until_bookmark('nat')
            self.play(FadeIn(rep_add[0], rep_mul[0]), run_time=tracker.time_until_bookmark('radd', limit=FADEIN_T))
            self.wait_until_bookmark('radd')
            self.play(FadeIn(rep_add[1]), run_time=tracker.time_until_bookmark('rmul', limit=FADEIN_T))
            self.wait_until_bookmark('rmul')
            self.play(FadeIn(rep_mul[1]), run_time=FADEIN_T)
            self.wait_until_bookmark('end')

            self.play(FadeOut(rep_add, rep_mul), run_time=FADEOUT_T)

            box1 = SurroundingRectangle(distr1_star, color=yellow, buff=0.1)
            box2 = SurroundingRectangle(distr2_star, color=yellow, buff=0.1)
            distr1_exp = MathTex('a^{xy}', '\\neq', 'a^x a^y', font_size=50, color=blue).next_to(star_exp, DOWN, buff=0.5)
            distr2_exp = MathTex('(ab)^x = a^x b^x', font_size=50, color=blue).next_to(distr1_exp, DOWN, buff=0.5)
            distr1_exp[1].set_color(red)

            self.wait_until_bookmark('p1')
            self.play(Create(box2), run_time=tracker.time_until_bookmark('i1', limit=BOX_T))
            self.wait_until_bookmark('i1')
            self.play(FadeIn(distr2_exp), run_time=tracker.time_until_bookmark('p2', limit=FADEIN_T))
            self.wait_until_bookmark('p2')
            self.play(ReplacementTransform(box2, box1), run_time=tracker.time_until_bookmark('i2', limit=MOVE_T))
            self.wait_until_bookmark('i2')
            self.play(FadeIn(distr1_exp), run_time=FADEIN_T)

            strike = Line(star_exp.get_left(), star_exp.get_right(), color=red)
            self.wait_until_bookmark('strike')
            self.play(GrowFromPoint(strike, strike.get_start()), run_time=GROWARROW_T)

        self.fade_all(box1, distr2_exp, distr1_exp, star_exp, strike, run_time=FADEALL_T)
    
        text = add_bookmarks("If you'd like, you can pause the video and {try} try to find a solution yourself.")

        with self.voiceover(text) as tracker:
            
            chal = Text('Try it yourself:', **fancy, font_size=50).shift(UP)
            laws = VGroup(distr1_star, distr2_star)
            self.wait_until_bookmark('try')
            self.play(FadeIn(chal), laws.animate.next_to(chal, DOWN, buff=0.5), run_time=MOVE_T)

        self.wait(1)
        self.play(FadeOut(chal, laws), run_time=FADEALL_T)
    
class Scene2_5(ChainOfFields):
    audio_dir = 'assets/audio/Scene2_5'

    def construct(self):

        ###############
        ### SCENE 2 ###
        ###############

        text = add_bookmarks("""
        At the time, I couldn't think of a solution, and I forgot about the problem for a while. But when I returned to it a few months later, 
        I realized that the solution lies with that {func} all-powerful function, the {exp} exponential function. This is often denoted as {not1} 
        E to the X, but I'm going to write it as {not2} exp of X instead. This function {slide} has two crucial properties: first, {prop1} exp 
        of X plus Y equals exp of X times exp of Y, and {prop2} second, it creates a one-to-one correspondence between {real} real numbers and 
        {pos} positive numbers. {out} Every positive {y} number Y has a unique {x} number X such that {lines} exp of X equals Y, and this is 
        called the natural logarithm of Y , or {log} log of Y. 
        """)

        with self.voiceover(text) as tracker:
        
            exp = Text('exponential function', **fancy, font_size=50).to_edge(UP, buff=1)
            nots = MathTex('e^x', '\quad \exp x', font_size=60, color=blue).next_to(exp, DOWN, buff=0.5)
            strike = Line(nots[0].get_left(), nots[0].get_right(), color=red).shift(DOWN * 0.1 + LEFT * 0.05)
            nots[1].set_color(red)

            axes = Axes(x_range=(-3, 3), y_range=(-1, 4)).scale(0.5).to_edge(DOWN, buff=0.75)
            curve = axes.plot(lambda x: math.exp(x), x_range=(-3, 1.5), color=red)

            self.wait_until_bookmark('func')
            self.play(FadeIn(axes), run_time=tracker.time_until_bookmark('exp', limit=FADEIN_T))
            self.wait_until_bookmark('exp')
            self.play(AnimationGroup(Write(exp), Create(curve), lag_ratio=0.3), run_time=tracker.time_until_bookmark('not1', limit=WRITE_T))
            self.wait_until_bookmark('not1')
            self.play(FadeIn(nots[0]), run_time=FADEIN_T)
            self.wait_until_bookmark('not2')
            self.play(GrowFromPoint(strike, strike.get_start()), FadeIn(nots[1]), run_time=FADEIN_T)

            self.wait_until_bookmark('slide')
            self.play(AnimationGroup(
                FadeOut(nots, strike), 
                AnimationGroup(exp.animate.to_corner(UL, buff=1), VGroup(axes, curve).animate.to_corner(DR, buff=0.75)), 
                lag_ratio=0.3), run_time=1.5)

            prop1 = Tex('1. $ \exp(x + y) = \exp x \cdot \exp y $', font_size=50, color=blue).next_to(exp, DOWN, buff=0.5, aligned_edge=LEFT)        
            prop2 = Tex('2. ', 'real numbers ', '$\longleftrightarrow$ positive numbers', font_size=50, color=green).next_to(prop1, DOWN, buff=1.5, aligned_edge=LEFT)
            
            pos_axis = Line(axes[1].number_to_point(0), axes[1].get_end())
            real_brace = Brace(axes[0], DOWN, color=green)
            pos_brace = Brace(pos_axis, RIGHT, color=green)

            self.wait_until_bookmark('prop1')
            self.play(FadeIn(prop1), run_time=FADEIN_T)
            self.wait_until_bookmark('prop2')
            self.play(FadeIn(prop2[0]), run_time=FADEIN_T)
            self.wait_until_bookmark('real')
            self.play(FadeIn(prop2[1], real_brace), run_time=tracker.time_until_bookmark('pos', limit=FADEIN_T))
            self.wait_until_bookmark('pos')
            self.play(FadeIn(prop2[2]), ReplacementTransform(real_brace, pos_brace), run_time=tracker.time_until_bookmark('out', limit=TRANSFORM_T))
            self.wait_until_bookmark('out')
            self.play(FadeOut(pos_brace), run_time=tracker.time_until_bookmark('y', limit=FADEOUT_T))

            y = ValueTracker(2.7)

            y_pt = always_redraw(lambda: Dot(axes[1].number_to_point(y.get_value()), radius=0.07, color=green))
            x_pt = always_redraw(lambda: Dot(axes[0].number_to_point(math.log(y.get_value())), radius=0.07, color=green))
            y_label = always_redraw(lambda: MathTex('y', font_size=35, color=green).next_to(y_pt, LEFT, buff=0.1))
            x_label = always_redraw(lambda: MathTex('x', font_size=35, color=green).next_to(x_pt, DOWN, buff=0.1))
            
            hori = always_redraw(lambda: Line(y_pt.get_center(), axes.coords_to_point(math.log(y.get_value()), y.get_value()), stroke_width=2.5, color=green))
            vert = always_redraw(lambda: Line(x_pt.get_center(), axes.coords_to_point(math.log(y.get_value()), y.get_value()), stroke_width=2.5, color=green))

            self.wait_until_bookmark('y')
            self.play(FadeIn(y_pt, y_label), run_time=tracker.time_until_bookmark('x', limit=FADEIN_T))
            self.wait_until_bookmark('x')
            self.play(FadeIn(x_pt, x_label), run_time=tracker.time_until_bookmark('lines', limit=FADEIN_T))
            self.wait_until_bookmark('lines')
            self.play(GrowFromPoint(hori, hori.get_start()), GrowFromPoint(vert, vert.get_start()), run_time=GROWARROW_T)

            self.wait(1)
            self.play(y.animate.set_value(0.25))
            self.play(y.animate.set_value(2.7))

            log_y = MathTex('\log y', font_size=30, color=green).move_to(x_label)
            self.wait_until_bookmark('log')
            self.play(ReplacementTransform(x_label, log_y), run_time=TRANSFORM_T)
        
        text = add_bookmarks("""
        Mathematicians have specific terminology for properties like these. A function that converts one operation into another is called a 
        {homo} “homomorphism,” so property 1 could be restated as {alt1} “exp is a homomorphism from addition to multiplication.” {out} And 
        a function that creates a one-to-one correspondence is called a {bijn} bijection, so property 2 could be stated as {alt2} “exp is a 
        bijection from real numbers to positive numbers.” Lastly, a bijective homomorphism is called an {iso} isomorphism, so these two 
        properties taken together say that {conj} “exp is an isomorphism from addition of real numbers to multiplication of positive numbers.”
        """)

        with self.voiceover(text) as tracker:

            homo = Text('homomorphism', **fancy, font_size=35, color=blue, stroke_color=blue)
            homo_desc = Tex('converts one operation\\\\into another', font_size=35, color=blue).next_to(homo, DOWN, buff=0.25)
            VGroup(homo, homo_desc).to_corner(UR, 1.25).shift(RIGHT * 0.3)
            self.wait_until_bookmark('homo')
            self.play(Write(homo), FadeIn(homo_desc), run_time=WRITE_T)

            prop1_alt = Tex('``$\exp$ is a homomorphism from addition\\\\to multiplication"', tex_environment='flushleft', font_size=35, color=blue)
            prop1_alt.next_to(prop1, DOWN, buff=0.25, aligned_edge=LEFT).shift(RIGHT * 0.6)
            self.wait_until_bookmark('alt1')
            self.play(FadeIn(prop1_alt), run_time=FADEIN_T)

            bijn = Text('bijection', **fancy, font_size=35, color=green, stroke_color=green).move_to(homo)
            bijn_desc = Tex('one-to-one\\\\correspondence', font_size=35, color=green).next_to(bijn, DOWN, buff=0.25)
            VGroup(bijn, bijn_desc).to_edge(DOWN, 1.25)
            self.wait_until_bookmark('out')
            self.play(FadeOut(axes, curve, y_pt, x_pt, y_label, log_y, hori, vert), run_time=FADEOUT_T)
            self.wait_until_bookmark('bijn')
            self.play(Write(bijn), FadeIn(bijn_desc), run_time=WRITE_T)

            prop2_alt = Tex('``$\exp$ is a bijection from real numbers\\\\to positive numbers"', tex_environment='flushleft', font_size=35, color=green)
            prop2_alt.next_to(prop2, DOWN, buff=0.25, aligned_edge=LEFT).shift(RIGHT * 0.6)
            self.wait_until_bookmark('alt2')
            self.play(FadeIn(prop2_alt), run_time=FADEIN_T)
            
            iso = Text('isomorphism', **fancy, font_size=35).move_to(VGroup(homo, bijn_desc))
            arr_top = Arrow(homo_desc.get_bottom(), iso.get_top(), buff=0.25)
            arr_bottom = Arrow(bijn.get_top(), iso.get_bottom(), buff=0.25)
            self.wait_until_bookmark('iso')
            self.play(Write(iso), GrowArrow(arr_top, point_color=BLACK), GrowArrow(arr_bottom, point_color=BLACK), run_time=WRITE_T)

            conj = Tex('``$\exp$ is an isomorphism from {{addition}}\\\\of {{real numbers}} to {{multiplication}} of\\\\{{positive numbers}}"', tex_environment='flushleft', font_size=35)
            conj[1].set_color(blue)
            conj[3].set_color(green)
            conj[5].set_color(blue)
            conj[7].set_color(green)
            conj.next_to(prop2_alt, DOWN, buff=0.25, aligned_edge=LEFT)
            self.wait_until_bookmark('conj')
            self.play(FadeIn(conj), run_time=FADEIN_T)
        
        self.fade_all(exp, prop1, prop2, homo, homo_desc, prop1_alt, bijn, bijn_desc, prop2_alt, VGroup(arr_top, arr_bottom, iso), run_time=FADEALL_T)
        self.exp_iso = conj
    
        ###############
        ### SCENE 3 ###
        ###############

        exp_iso = self.exp_iso

        text = add_bookmarks("""
        Whenever you have an isomorphism between two operations, they're called {iso} isomorphic. And isomorphic operations have essentially 
        {same} the same structure, because you can go back and forth between them using the isomorphisms while preserving all of their 
        properties. In our case, you can go back and forth between {cycle} addition of real numbers and multiplication of positive numbers 
        using exp and log, so any property that holds for one operation must also hold for the other. {fade}

        One of these operations, {addbox} addition, has another operation that distributes over it, namely {arrmul} multiplication. And 
        this means that {mulbox} multiplication (of positive numbers), being isomorphic to addition, must also have {arrques} an operation 
        that distributes over it. {fbox} Just as exp {homo1} converts addition into multiplication (of positive numbers), it will {homo2} 
        convert multiplication into this new operation, which I'll call {star} star. We can get a formula for star by replacing X and Y 
        with log of X and log of Y {subst}. The exp and log cancel out since they're inverses {cancel}, and we get that {final} X star 
        Y equals exp of log of x times log of y.
        """)

        with self.voiceover(text) as tracker:

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

            self.wait_until_bookmark('iso')
            self.play(FadeIn(line1), FadeOut(exp_iso), run_time=FADEIN_T)
            self.wait_until_bookmark('same')
            self.play(FadeIn(line2), run_time=FADEIN_T)
            self.wait_until_bookmark('cycle')
            self.play(FadeIn(line3), run_time=FADEIN_T)

            box1 = SurroundingRectangle(ops[0], color=yellow, buff=0.1)
            box2 = SurroundingRectangle(ops[2], color=yellow, buff=0.1)
            mul = MathTex('\cdot', font_size=125, color=blue).move_to(ops[0]).shift(UP * 1.6)
            ques = MathTex('?', font_size=75, color=green).move_to(ops[2]).shift(UP * 1.75 + LEFT * 0.2)
            arr_mul = Line(mul.get_bottom(), ops[0].get_top(), buff=0.2, color=blue).add_tip(**tip_size(0.27))
            arr_ques = Line(ques.get_bottom(), ops[2].get_top() + LEFT * 0.2, buff=0.2, color=green).add_tip(**tip_size(0.27))

            self.wait_until_bookmark('fade')
            self.play(FadeOut(line1, line2), run_time=tracker.time_until_bookmark('addbox', limit=FADEOUT_T))
            self.wait_until_bookmark('addbox')
            self.play(Create(box1), run_time=BOX_T)
            self.wait_until_bookmark('arrmul')
            self.play(FadeIn(mul), GrowFromPoint(arr_mul, arr_mul.get_start(), point_color=BLACK), run_time=GROWARROW_T)
            self.wait_until_bookmark('mulbox')
            self.play(ReplacementTransform(box1, box2), run_time=MOVE_T)
            self.wait_until_bookmark('arrques')
            self.play(FadeIn(ques), GrowFromPoint(arr_ques, arr_ques.get_start(), point_color=BLACK), run_time=GROWARROW_T)
            self.wait_until_bookmark('fbox')
            self.play(FadeOut(box2), run_time=FADEOUT_T)

            homo1 = MathTex('\exp(x + y) = \exp x \cdot \exp y', font_size=50, color=blue).to_edge(UP, 1)
            homo2 = MathTex('\exp({{x}} \cdot {{y}}) = \exp {{x}} {{\, ?}} \exp {{y}}', font_size=50, color=blue).next_to(homo1, DOWN, 0.5)
            homo2_star = MathTex('\exp({{x}} \cdot {{y}}) = \exp {{x}} {{\star}} \exp {{y}}', font_size=50, color=blue).move_to(homo2)
            homo2.get_part_by_tex('?').set_color(green)
            homo2_star.get_part_by_tex('\star').set_color(green)

            exp_copy = VGroup(exp, arr_top).copy()

            star = MathTex('\star', font_size=75, color=green).move_to(ques)
            arr_star = Line(star.get_bottom(), ops[2].get_top() + LEFT * 0.2, buff=0.2, color=green).add_tip(**tip_size(0.27))

            self.wait_until_bookmark('homo1')
            self.play(FadeIn(homo1), run_time=FADEIN_T)
            self.wait_until_bookmark('homo2')
            self.play(FadeIn(homo2), exp_copy.animate.move_to(VGroup(mul, ques).get_center() + UP * 0.4 + LEFT * 0.1), run_time=MOVE_T)
            self.wait_until_bookmark('star')
            self.play(ReplacementTransform(homo2, homo2_star), ReplacementTransform(ques, star), ReplacementTransform(arr_ques, arr_star), run_time=TRANSFORM_T)

            star_def1 = MathTex('\exp({{\log x}} \cdot {{\log y}}) = \exp {{(\log x)}} {{\star}} \exp {{(\log y)}}', font_size=50, color=blue).move_to(homo2)
            star_def2 = MathTex('\exp(\log x \cdot \log y) =', '\exp (\log {{x}}) {{\star}} \exp (\log {{y}})', font_size=50, color=blue).move_to(homo2)
            star_def3 = MathTex('\exp(\log x \cdot \log y) =', 'x', '\star', 'y', font_size=50, color=blue).move_to(homo2)
            star_def4 = MathTex('\exp(\log x \cdot \log y)', '=', 'x \star y', font_size=50, color=blue).move_to(homo2)
            star_def5 = MathTex('x \star y', '=', '\exp(\log x \cdot \log y)', font_size=50, color=blue).move_to(homo2)

            self.wait_until_bookmark('subst')
            self.play(ReplacementTransform(homo2_star, star_def1), run_time=MOVE_T)
            self.add(star_def2); self.remove(star_def1)
            self.wait_until_bookmark('cancel')
            self.play(FadeOut(star_def2[1::2]), run_time=FADEOUT_T)
            self.play(*[ ReplacementTransform(star_def2[i * 2], star_def3[i]) for i in range(4) ], run_time=MOVE_T)
            self.add(star_def4); self.remove(*star_def3)
            self.wait_until_bookmark('final')
            self.play(*[ ReplacementTransform(star_def4[2 - i], star_def5[i]) for i in range(3)], run_time=MOVE_T)

        self.fade_all(line3, mul, arr_mul, star, arr_star, exp_copy, homo1, run_time=FADEALL_T)
        self.star_def = star_def5
    
        ###############
        ### SCENE 4 ###
        ###############

        star_def = self.star_def

        text = add_bookmarks("""
        Star does indeed distribute over multiplication; {proof} a direct proof of this is on the screen right now. And star is {iso} isomorphic 
        to multiplication by construction, so it {same} shares all of the properties of multiplication. {out} Multiplication is commutative and 
        associative, therefore {starcomm} star is commutative and associative. And just as {mulzero} anything times 0 is 0, {starzero} anything 
        star exp of 0 is exp of 0. And just as {mulone} X times 1 equals X, {starone} X star exp of 1 equals X. And just as {mulinv} every nonzero 
        number has a multiplicative inverse, {starinv} every positive number except 1 has a star-inverse. Lastly, just as {mulroot} every positive 
        number has a square root, {starroot} every number X greater than 1 has a number Y such that Y star Y equals X. You can find Y by {formula} 
        this formula.
        """)

        with self.voiceover(text) as tracker:

            self.play(star_def.animate.set_font_size(60).to_edge(UP, buff=1), run_time=MOVE_T)

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
            self.wait_until_bookmark('proof')
            self.play(FadeIn(proof1, proof2), run_time=FADEIN_T)

            arc = ArcBetweenPoints(star_def[0].get_bottom() + DR * 0.1, star_def[2].get_bottom() + RIGHT * 0.4 + UP * 0.1, radius=3, color=green).add_tip().add_tip(at_start=True)
            same = Text('same properties', **fancy, font_size=40, color=green, stroke_color=green).next_to(arc, DOWN, buff=0.1)
            self.wait_until_bookmark('iso')
            self.play(FadeIn(arc), run_time=FADEIN_T)
            self.wait_until_bookmark('same')
            self.play(Write(same), run_time=WRITE_T)

            self.wait_until_bookmark('out')
            self.play(FadeOut(proof1, proof2, same, arc), run_time=FADEOUT_T)

            prop_fs = 40
            prop_dy1 = DOWN * 0.75
            prop_dy2 = DOWN * 1

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

            mul_inv = MathTex('x \cdot {{\\frac{1}{x}}} = {{1}} \ (x \\neq {{0}})', font_size=prop_fs, color=blue).next_to(mul_one, ORIGIN, buff=0, aligned_edge=RIGHT).shift(prop_dy2)
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

            self.play(FadeIn(table, mul_head, star_head, mul_comm), run_time=FADEIN_T)
            self.wait_until_bookmark('starcomm')
            self.play(FadeIn(star_comm), run_time=FADEIN_T)
            self.wait_until_bookmark('mulzero')
            self.play(FadeIn(mul_zero), run_time=FADEIN_T)
            self.wait_until_bookmark('starzero')
            self.play(FadeIn(star_zero), run_time=FADEIN_T)
            self.wait_until_bookmark('mulone')
            self.play(FadeIn(mul_one), run_time=FADEIN_T)
            self.wait_until_bookmark('starone')
            self.play(FadeIn(star_one), run_time=FADEIN_T)
            self.wait_until_bookmark('mulinv')
            self.play(FadeIn(mul_inv), run_time=FADEIN_T)
            self.wait_until_bookmark('starinv')
            self.play(FadeIn(star_inv), run_time=FADEIN_T)
            self.wait_until_bookmark('mulroot')
            self.play(FadeIn(mul_root), run_time=FADEIN_T)
            self.wait_until_bookmark('starroot')
            self.play(FadeIn(star_root), run_time=FADEIN_T)
            self.wait_until_bookmark('formula')
            self.play(ReplacementTransform(star_root, star_root2), run_time=MOVE_T)

        self.fade_all(
            VGroup(mul_root, star_root2), VGroup(mul_inv, star_inv), 
            VGroup(mul_one, star_one), VGroup(mul_zero, star_zero), 
            VGroup(mul_comm, star_comm), VGroup(mul_head, star_head), table, run_time=FADEALL_T)
            
        ###############
        ### SCENE 5 ###
        ###############

        star_def = self.star_def

        text = add_bookmarks("""
        If you want to see what the star operation looks like on a graph, 
        {graph} here is a graph of X star A, {vary} with A varying over time. 
        You can see that when {ainv} A is 1 over E, the function {xinv} is 1 over X, 
        {a0} when A is 1, the function {x0} is just 1, {a1} when A is E {x1} it's X, 
        and {a2} when A is E squared {x2} it's X squared. Why is this? {out} 
        Well, in calculus, it's common to define exponentiation as {expdef} 
        X to the Y equals exp of log X times Y. If you compare this definition to
        {stardef} the definition of star, you can see that X star A is equal to X 
        to the log of A. {new} So if A equals {aez} E to the Z, then X star A equals 
        {sxz} X to the Z.
        """)

        with self.voiceover(text) as tracker:

            eq = MathTex('y = x \star a', '= x^z', color=red, font_size=50)
            eq.shift(-eq[0].get_center() + UP * 1.5)

            a = Variable(1.80, 'a').scale(40 / 48).next_to(eq[0], DOWN, 0.4)
            axes = Axes(x_range=(0, 10), y_range=(0, 5), x_length=(8 * 1), y_length=(5 * 1)).shift(DOWN * 0.7)
            curve = always_redraw(lambda: axes.plot(lambda x: x ** math.log(a.tracker.get_value()), x_range=(0.1, 10)).set_color(red)) 

            self.wait_until_bookmark('graph')
            self.play(FadeIn(eq[0], a, axes, curve), run_time=FADEIN_T)
            self.wait_until_bookmark('vary')
            self.play(a.tracker.animate.set_value(7.20), run_time=1.25)
            self.play(a.tracker.animate.set_value(1 / math.e), run_time=1.25)

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

            self.wait_until_bookmark('ainv')
            self.play(FadeIn(a_inv), run_time=FADEIN_T)
            self.wait_until_bookmark('xinv')
            self.play(FadeIn(eq_inv.move_to(axes.coords_to_point(3, 1/3) + UP * 0.5)))

            half1 = squish_rate_func(smooth, 0, 0.5)
            half2 = squish_rate_func(smooth, 0.5, 1)

            self.wait_until_bookmark('a0')
            self.play(a.tracker.animate.set_value(1), FadeOut(a_inv, eq_inv, rate_func=half1), FadeIn(a_0, rate_func=half2), run_time=(FADEIN_T * 2))
            self.wait_until_bookmark('x0')
            self.play(FadeIn(eq_0.move_to(axes.coords_to_point(3, 1) + UP * 0.5)), run_time=FADEIN_T)
            self.wait_until_bookmark('a1')
            self.play(a.tracker.animate.set_value(math.e), FadeOut(a_0, eq_0, rate_func=half1), FadeIn(a_1, rate_func=half2), run_time=(FADEIN_T * 2))
            self.wait_until_bookmark('x1')
            self.play(FadeIn(eq_1.move_to(axes.coords_to_point(2.3, 2.3) + DR * 0.35)), run_time=FADEIN_T)
            self.wait_until_bookmark('a2')
            self.play(a.tracker.animate.set_value(math.e ** 2), FadeOut(a_1, eq_1, rate_func=half1), FadeIn(a_2, rate_func=half2), run_time=(FADEIN_T * 2))
            self.wait_until_bookmark('x2')
            self.play(FadeIn(eq_2.move_to(axes.coords_to_point(1.6, 1.6 ** 2) + RIGHT * 0.5)), run_time=FADEIN_T)

            self.wait_until_bookmark('out')
            self.play(FadeOut(a_2, eq_2), run_time=FADEOUT_T)

            exp_def = MathTex('x^y = \exp(\log x \cdot y)', font_size=50).shift(DOWN + RIGHT * 2)
            star_def2 = MathTex('x \star a =', '\exp(\log x \cdot \log a)', font_size=50).next_to(exp_def, DOWN, 0.4)
            star_exp = MathTex('x \star a =', 'x^{\log a}', font_size=50).move_to(star_def2)

            self.wait_until_bookmark('expdef')
            self.play(FadeIn(exp_def), run_time=FADEIN_T)
            self.wait_until_bookmark('stardef')
            self.play(FadeIn(star_def2), run_time=FADEIN_T)
            self.wait_until_bookmark('new')
            self.play(ReplacementTransform(star_def2, star_exp), run_time=TRANSFORM_T)
            
            self.wait_until_bookmark('aez')
            self.play(FadeIn(a_z), run_time=FADEIN_T)
            self.wait_until_bookmark('sxz')
            self.play(FadeIn(eq[1]), run_time=FADEIN_T)
            
        self.fade_all(star_def, VGroup(axes, curve), eq, VGroup(a, a_z), exp_def, star_exp, run_time=FADEALL_T)

class Scene6_11(ChainOfFields):
    audio_dir = 'assets/audio/Scene6_11'

    def construct(self):
            
        ###############
        ### SCENE 6 ###
        ###############

        # bookmarks messed up because of weird transcription
        text = add_bookmarks(""" 
        As of yet, we have three binary operations: the standard operations of {addmul} addition and multiplication, 
        and this new {star} star operation. {table} The first two are defined for {real} all numbers, 
        but the last is only defined for {pos} positive numbers. And these operations form a kind of 
        chain where {distrmul} multiplication distributes over addition, and {distrstar} star distributes 
        over multiplication. {up} It turns out that we can extend this chain into an {inf} infinite 
        sequence of binary operations, with each distributing over the one before it. I'll call the next 
        operation in this {dia} sequence diamond. {left} Just as {stardef} X star Y is exp of log of X times 
        log of {diadef} Y, X diamond Y is defined as exp of log of X star log of Y, which you can {expand} expand to 
        exp exp of log log of X times log log of Y. This is defined for {domain} all numbers greater 
        than 1, distributes over star, and, just like star, inherits all the properties of multiplication. 
        {dia0} For example, X diamond E equals E and {dia1} X diamond E to the E equals X, so E acts like 
        0 and E to the E acts like 1.
        """)

        with self.voiceover(text) as tracker:

            add = MathTex('+', font_size=75, color=green)
            mul = MathTex('\cdot', font_size=125, color=green)
            star = MathTex('\star', font_size=75, color=green)
            VGroup(add, mul, star).arrange(direction=DOWN, buff=1)

            self.wait_until_bookmark('addmul')
            self.play(FadeIn(add, mul), run_time=FADEIN_T)
            self.wait_until_bookmark('star')
            self.play(FadeIn(star), run_time=FADEIN_T)

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
            self.wait_until_bookmark('table')
            self.play(Transform(add, add_t), Transform(mul, mul_t), Transform(star, star_t), run_time=MOVE_T)
            self.play(FadeIn(table), run_time=FADEIN_T)
            self.remove(add, mul, star)
            
            self.wait_until_bookmark('real')
            self.play(real1.animate.set_color(WHITE), real2.animate.set_color(WHITE), run_time=FADEIN_T)
            self.wait_until_bookmark('pos')
            self.play(pos.animate.set_color(WHITE), run_time=FADEIN_T)

            arr_x = add_t.get_x() - 0.28
            between = lambda m1, m2: [ RIGHT * arr_x + UP * (m1.get_y() - 0.1), RIGHT * arr_x + UP * (m2.get_y() + 0.1) ]

            arr_mul = ArcBetweenPoints(*between(add_t, mul_t), color=yellow).add_tip(**tip_size(0.27), at_start=True)
            arr_star = ArcBetweenPoints(*between(mul_t, star_t), color=yellow).add_tip(**tip_size(0.27), at_start=True)
            self.wait_until_bookmark('distrmul')
            self.play(FadeIn(arr_mul), run_time=FADEIN_T)
            self.wait_until_bookmark('distrstar')
            self.play(FadeIn(arr_star), run_time=FADEIN_T)

            self.wait_until_bookmark('up')
            self.play(VGroup(table, arr_mul, arr_star).animate.to_edge(UP, buff=0.2), run_time=MOVE_T)

            hori = table.get_horizontal_lines()
            line_height1 = hori[2].get_center() - hori[1].get_center()
            line_height2 = UP * table.get_bottom()[1] - hori[2].get_center()
            new_lines = [ hori[2].copy().shift(line_height2 + line_height1 * i) for i in range(3) ]
            new_lines.append(table.get_vertical_lines()[0].copy().shift(DOWN * 3))
            self.wait_until_bookmark('inf')
            self.play(FadeIn(*new_lines), run_time=FADEIN_T)

            dia = MathTex('\diamond', font_size=75, color=green).move_to(star_t).shift((line_height1 + line_height2) / 2)
            gt_1 = Tex('numbers $> 1$', font_size=50, fill_opacity=0).move_to(pos).shift((line_height1 + line_height2) / 2)
            arr_dia = ArcBetweenPoints(*between(star_t, dia), color=yellow).add_tip(**tip_size(0.27), at_start=True)
            self.wait_until_bookmark('dia')
            self.play(FadeIn(dia, arr_dia), run_time=FADEIN_T)

            table_ext = VGroup(table, *new_lines, dia, gt_1, arr_mul, arr_star, arr_dia)
            self.wait_until_bookmark('left')
            self.play(table_ext.animate.to_edge(LEFT, buff=0.2), run_time=MOVE_T)

            star_def = MathTex('x \star y = \exp (\log x \cdot \log y)', font_size=50, color=blue)
            dia_def = MathTex('x \diamond y = \exp {{(\log x \star \log y)}}', font_size=50, color=blue)
            dia_def2 = MathTex('x \diamond y = \exp {{\exp (\log \log x \cdot \log \log y)}}', font_size=40, color=blue)
            center_right = RIGHT * (table_ext.get_right()[0] + config['frame_x_radius']) / 2
            VGroup(star_def, dia_def).arrange(DOWN, buff=0.75).move_to(center_right)

            self.wait_until_bookmark('stardef')
            self.play(FadeIn(star_def), run_time=FADEIN_T)
            self.wait_until_bookmark('diadef')
            self.play(FadeIn(dia_def), run_time=FADEIN_T)
            self.wait_until_bookmark('expand')
            self.play(ReplacementTransform(dia_def, dia_def2.move_to(dia_def)), run_time=MOVE_T)
            self.wait_until_bookmark('domain')
            self.play(gt_1.animate.set_opacity(1), run_time=FADEIN_T)

            dia_zero = MathTex('x \diamond e = e', font_size=50, color=red)
            dia_one = MathTex('x \diamond e^e = x', font_size=50, color=red)
            VGroup(dia_zero, dia_one).arrange(DOWN, buff=0.75).next_to(dia_def2, DOWN, buff=0.8)
            self.wait_until_bookmark('dia0')
            self.play(FadeIn(dia_zero), run_time=FADEIN_T)
            self.wait_until_bookmark('dia1')
            self.play(FadeIn(dia_one), run_time=FADEIN_T)

        ops = VGroup(add_t.copy(), mul_t.copy(), star_t.copy(), dia.copy())
        self.add(ops)
        self.fade_all(table_ext, star_def, dia_def2, dia_zero, dia_one, run_time=FADEALL_T)
        self.play(ops.animate.arrange(DOWN, buff=0.75), run_time=MOVE_T)
        self.ops = ops
    
        ###############
        ### SCENE 7 ###
        ###############

        ops = self.ops

        text = add_bookmarks("""
        Before we continue, it's a good idea to systematically name these operations. I'll use a {dot} dot symbol, 
        like I've been using for multiplication, but with a {sub} subscript added. {dot0} So dot 0 means multiplication, 
        {dot1} dot 1 is the same as star, {dot2} dot 2 is diamond, and so on. {out} And to avoid having to write {many} 
        log so many times in a row, I'll use {sup} superscripts for repeated application, so {log2} log 2 of X means log 
        of log of X, {log3} log 3 of X means log of log of log of X, and so on. And I'll do the {exp} same with exp. 
        Here are {out2} the definitions of {defs} star and diamond written in this new notation. Now we can define the 
        rest of the operations all at once. {dotn} The dot N operation takes two numbers X and Y, applies log N times, 
        multiplies the results, and then applies exp N times. {fade}

        Whenever you define a new operation, it's important to know what its {dom} domain is, what inputs it accepts. 
        In the case of dot N, the only thing that could restrict the domain is this {logbox} repeated application of 
        log, because {movebox} exp and multiplication both have unrestricted domains, they can work with any real 
        numbers, so we don't need to worry about them. {outbox} So the domain of {domeq} dot N is the same as the 
        domain of log N.
        """)

        with self.voiceover(text) as tracker:

            dot_n = MathTex('\cdot', '_n', font_size=125, color=blue).shift(LEFT * 3.5)
            self.wait_until_bookmark('dot')
            self.play(FadeIn(dot_n[0]), run_time=FADEIN_T)
            self.wait_until_bookmark('sub')
            self.play(FadeIn(dot_n[1]), run_time=FADEIN_T)
            
            dot_0 = MathTex('{{=}} \cdot_0', font_size=75, color=blue)
            dot_1 = MathTex('{{=}} \cdot_1', font_size=75, color=blue)
            dot_2 = MathTex('{{=}} \cdot_2', font_size=75, color=blue)
            dot_0.shift(RIGHT * (0.75 - dot_0[0].get_x()) + UP * (ops[1].get_y() - dot_0[0].get_y()))
            dot_1.shift(RIGHT * (0.75 - dot_1[0].get_x()) + UP * (ops[2].get_y() - dot_1[0].get_y()))
            dot_2.shift(RIGHT * (0.75 - dot_2[0].get_x()) + UP * (ops[3].get_y() - dot_2[0].get_y()))
            self.wait_until_bookmark('dot0')
            self.play(FadeIn(dot_0), run_time=FADEIN_T)
            self.wait_until_bookmark('dot1')
            self.play(FadeIn(dot_1), run_time=FADEIN_T)
            self.wait_until_bookmark('dot2')
            self.play(FadeIn(dot_2), run_time=FADEIN_T)

            log_n = MathTex('{{\log}}^n =', '{{\log}} \dots {{\log}}', font_size=50, color=blue)
            log_2 = MathTex('{{\log}}^2 x = {{\log}} {{\log}} x', font_size=50, color=blue)
            log_3 = MathTex('{{\log}}^3 x = {{\log}} {{\log}} {{\log}} x', font_size=50, color=blue)
            VGroup(log_n, log_2, log_3).arrange(DOWN, buff=0.6).move_to(dot_n)
            self.wait_until_bookmark('out')
            self.play(FadeOut(dot_n), run_time=FADEOUT_T)
            self.wait_until_bookmark('many')
            self.play(FadeIn(log_n[2:]), run_time=FADEIN_T)
            self.wait_until_bookmark('sup')
            self.play(FadeIn(log_n[0:2]), run_time=FADEIN_T)
            self.wait_until_bookmark('log2')
            self.play(FadeIn(log_2), run_time=FADEIN_T)
            self.wait_until_bookmark('log3')
            self.play(FadeIn(log_3), run_time=FADEIN_T)

            exp_n = MathTex('{{\exp}}^n =', '{{\exp}} \dots {{\exp}}', font_size=50, color=blue).move_to(log_n)
            exp_2 = MathTex('{{\exp}}^2 x = {{\exp}} {{\exp}} x', font_size=50, color=blue).move_to(log_2)
            exp_3 = MathTex('{{\exp}}^3 x = {{\exp}} {{\exp}} {{\exp}} x', font_size=50, color=blue).move_to(log_3)
            self.wait_until_bookmark('exp')
            self.play(ReplacementTransform(log_n, exp_n), ReplacementTransform(log_2, exp_2), ReplacementTransform(log_3, exp_3), run_time=TRANSFORM_T)

            dot1_def = MathTex('x \cdot_1 y = \exp^1 (\log^1 x \cdot \log^1 y)', font_size=45, color=blue)
            dot2_def = MathTex('x \cdot_2 y = \exp^2 (\log^2 x \cdot \log^2 y)', font_size=45, color=blue)
            dot1_def.shift(dot_1[0].get_left() - dot1_def.get_left() + RIGHT * 0.25)
            dot2_def.shift(dot_2[0].get_left() - dot2_def.get_left() + RIGHT * 0.25)
            self.wait_until_bookmark('out2')
            self.play(FadeOut(dot_0, dot_1, dot_2), run_time=FADEOUT_T)
            self.wait_until_bookmark('defs')
            self.play(FadeIn(dot1_def, dot2_def), run_time=FADEIN_T)

            dotn_def = MathTex('x \cdot_n y = {{\exp^n}} ({{\log^n x}} {{\cdot}} {{\log^n y}})', font_size=50, color=red).to_edge(UP, buff=0.9)
            self.wait_until_bookmark('dotn')
            self.play(FadeIn(dotn_def), run_time=FADEIN_T)

            self.wait_until_bookmark('fade')
            self.fade_all(exp_n, exp_2, exp_3, ops, dot1_def, dot2_def, run_time=FADEALL_T)

            dom = Text('domain?', **fancy, font_size=50).next_to(dotn_def, DOWN, buff=0.75)
            self.wait_until_bookmark('dom')
            self.play(Write(dom), run_time=WRITE_T)

            box = lambda m: SurroundingRectangle(m, color=yellow, buff=0.1)
            boxes1 = VGroup(*[ box(m) for m in dotn_def.get_parts_by_tex('log') ])
            boxes2 = VGroup(*[ box(m) for m in [ dotn_def.get_part_by_tex('exp'), dotn_def.get_part_by_tex('\cdot', substring=False) ] ])
            self.wait_until_bookmark('logbox')
            self.play(Create(boxes1), run_time=BOX_T)
            self.wait_until_bookmark('movebox')
            self.play(ReplacementTransform(boxes1, boxes2), run_time=MOVE_T)
            self.wait_until_bookmark('outbox')
            self.play(FadeOut(boxes2), run_time=FADEOUT_T)
            
            doms = MathTex('\mathrm{dom}(\cdot_n) = \mathrm{dom}(\log^n)', font_size=50, color=blue).next_to(dom, DOWN, buff=0.75)
            self.wait_until_bookmark('domeq')
            self.play(FadeIn(doms), run_time=FADEIN_T)
        
        # bookmarks messed up because of weird transcription
        text = add_bookmarks("""
        Log 0 does nothing with its input, it applies log zero times, 
        so {dom0} its domain is the entire number line. 
        {out} To work out the rest, we can use the fact that log and exp are inverses, 
        which implies that the {domrange} domain of log N is the same as the range of exp N, 
        the set of possible outputs of exp N. {line} If we apply exp {apply1} once the outputs are 
        {range1} all numbers greater than 0. If we apply it {apply2} again, 0 gets mapped to 1, 
        and since exp is an increasing function, anything greater than 0 will map to something
        greater than 1, so the range of exp 2 consists of {range2} all numbers greater than 1. 
        Likewise, the {apply3} range of exp 3 is {range3} all numbers greater than exp of 1, 
        the {apply4} range of exp 4 is {range4} all numbers greater than exp of exp of 1 
        or exp 2 of 1, and so on. {move} If we write these {bounds} lower bounds using 
        the e notation, we find they're equal to {e} E, E to the E, {eee} E to the E to the E, 
        and so on. As you might imagine, this sequence grows very, very quickly. 
        E to the E to the E is {mil} approximately 4 million, and the {eeee} next value in the sequence is too 
        large to represent on a computer, but I worked out that it's {digits} about 1.65 million 
        digits long to the left of the decimal point. This means that the dot 6 operation only 
        works on numbers with more than 1.65 million digits. Not very practical, I must admit.
        """)

        with self.voiceover(text) as tracker:
            
            log0 = MathTex('\log^0 x = x', font_size=50, color=blue).next_to(doms, DOWN, buff=0.4)
            dom_log0 = MathTex('\mathrm{dom}({{\log^0}}) = \\text{anything}', font_size=50, color=blue).next_to(log0, DOWN, buff=0.4)
            self.play(FadeIn(log0), run_time=FADEIN_T)
            self.wait_until_bookmark('dom0')
            self.play(FadeIn(dom_log0), run_time=FADEIN_T)
            self.wait_until_bookmark('out')
            self.play(FadeOut(log0), dom_log0.animate.to_corner(DL, buff=0.9), run_time=MOVE_T)

            log_exp = MathTex('\mathrm{dom}(\cdot_n) = \mathrm{dom}(\log^n)', '= \mathrm{range}(\exp^n)', font_size=50, color=blue).move_to(doms)
            self.wait_until_bookmark('domrange')
            self.play(ReplacementTransform(doms[0], log_exp[0]), FadeIn(log_exp[1]), run_time=MOVE_T)

            line = NumberLine(x_range=(-5, 6), length=8, include_numbers=True, include_tip=True).shift(DOWN * 1.2).to_edge(LEFT, buff=0.8)
            dots = [ Dot(point=line.number_to_point(x), radius=0.05, color=red) for x in frange(-5, 5.5, 0.25) ]
            self.wait_until_bookmark('line')
            self.play(FadeIn(line, *dots), run_time=FADEIN_T)

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
            
            self.wait_until_bookmark('apply1')
            self.play(*[ animate_dot(dot) for dot in dots ], run_time=MOVE_T)
            self.wait_until_bookmark('range1')
            self.play(FadeIn(range1), run_time=FADEIN_T)
            self.wait_until_bookmark('apply2')
            self.play(*[ animate_dot(dot) for dot in dots ], run_time=MOVE_T)
            self.wait_until_bookmark('range2')
            self.play(FadeIn(range2), run_time=FADEIN_T)
            self.wait_until_bookmark('apply3')
            self.play(*[ animate_dot(dot) for dot in dots ], run_time=MOVE_T)
            self.wait_until_bookmark('range3')
            self.play(FadeIn(range3), run_time=FADEIN_T)
            self.wait_until_bookmark('apply4')
            self.play(*[ animate_dot(dot) for dot in dots ], run_time=MOVE_T)
            self.wait_until_bookmark('range4')
            self.play(FadeIn(range4), run_time=FADEIN_T)

            self.remove(*dots)

            dom0 = MathTex('\mathrm{dom}({{\log^0}}) = \\text{anything}', font_size=50, color=blue)
            dom1 = MathTex('{{\mathrm{range}(\exp^1)}} = \{x > 0\}', font_size=50, color=blue)
            dom2 = MathTex('{{\mathrm{range}(\exp^2)}} = \{x > 1\}', font_size=50, color=blue)
            dom3 = MathTex('{{\mathrm{range}(\exp^3)}} = \{x > {{\exp 1}}\}', font_size=50, color=blue)
            dom4 = MathTex('{{\mathrm{range}(\exp^4)}} = \{x > {{\exp^2 1}}\}', font_size=50, color=blue)
            vdots = MathTex('\\vdots', font_size=50, color=blue)
            VGroup(dom0, dom1, dom2, dom3, dom4, vdots).arrange(DOWN, buff=0.4)

            self.wait(3.5) # self.wait_until_bookmark('move')
            self.play( 
                FadeOut(dotn_def, dom, log_exp, line), 
                ReplacementTransform(dom_log0, dom0), ReplacementTransform(range1, dom1), 
                ReplacementTransform(range2, dom2), ReplacementTransform(range3, dom3), 
                ReplacementTransform(range4, dom4), FadeIn(vdots), run_time=MOVE_T)

            # self.wait_until_bookmark('bounds')
            self.play(VGroup(dom3[2], dom4[2]).animate.set_color(red), run_time=FADEIN_T)
            dom3_e = MathTex('{{\mathrm{range}(\exp^3)}} = \{x > {{e}}\}', font_size=50, color=blue).move_to(dom3)
            dom4_e = MathTex('{{\mathrm{range}(\exp^4)}} = \{x > {{e^e}}\}', font_size=50, color=blue).move_to(dom4)
            dom3_e[2].set_color(red)
            dom4_e[2].set_color(red)
            self.wait(2.5) # self.wait_until_bookmark('e')
            self.play(ReplacementTransform(dom3, dom3_e), ReplacementTransform(dom4, dom4_e), run_time=TRANSFORM_T)

            dom5 = MathTex('{{\mathrm{range}(\exp^5)}} = \{x > {{e^{e^e}}}\}', font_size=50, color=blue)
            dom5[2].set_color(red)
            doms = VGroup(dom0.copy(), dom1.copy(), dom2.copy(), dom3_e.copy(), dom4_e.copy(), dom5, vdots.copy())
            doms.arrange(DOWN, buff=0.4)
            self.wait(0.5) # self.wait_until_bookmark('eee')
            self.play(
                ReplacementTransform(dom0, doms[0]), 
                ReplacementTransform(dom1, doms[1]),
                ReplacementTransform(dom2, doms[2]),
                ReplacementTransform(dom3_e, doms[3]),
                ReplacementTransform(dom4_e, doms[4]),
                ReplacementTransform(vdots, doms[6]),
                FadeIn(doms[5]), run_time=MOVE_T)
        
            mil = MathTex('\\approx 3.81 \\text{ million}', font_size=50, color=red)
            mil.next_to(dom5[-1], RIGHT, buff=0.25)
            self.wait(7.5) # self.wait_until_bookmark('mil')
            self.play(FadeIn(mil), run_time=FADEIN_T)

            dom6 = MathTex('{{\mathrm{range}(\exp^6)}} = \{x > {{e^{e^{e^e}}}}\}', font_size=50, color=blue).next_to(dom5, DOWN, buff=0.3)
            dom6[2].set_color(red)
            self.wait(0.75) # self.wait_until_bookmark('eeee')
            self.play(FadeIn(dom6), doms[6].animate.shift(DOWN * 2), run_time=MOVE_T)

            digits = Tex('1.65 million digits!}', font_size=40)
            digits.next_to(dom6[-1], RIGHT, buff=0.25)
            self.wait_until_bookmark('digits')
            self.play(FadeIn(digits), run_time=FADEIN_T)
        
        self.play(FadeOut(mil, digits), run_time=FADEOUT_T)
    
        text = add_bookmarks("""
        So we've worked out the {dotdom} domains of all the dot N operations. 
        I'll write these as {kn} K N, so {k0} K 0 is the entire number line, {k1} K 1 is the set of 
        positive numbers, {etc} and so on. And I'm going to introduce {left} another notation as well. 
        Just as we defined {dotn} X dot N Y as exp N of log N of X times log N of Y, I'm going to define 
        {plusn} X plus N Y as exp N of log N of X plus log N of Y. This doesn't really add anything new, 
        because {restr} plus N is just a more restricted version of dot N minus 1. For example, 
        {plus1} plus 1 is the same as multiplication, but only works on positive numbers. 
        Nevertheless, this can be a useful notation to have.
        """)

        with self.voiceover(text) as tracker:

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

            self.wait_until_bookmark('dotdom')
            self.play(*[ ReplacementTransform(to_transform[i], dot_dom[i][0:-2]) for i in range(7) ], run_time=MOVE_T)
            
            k_n = MathTex('K_n', font_size=75, color=green).to_edge(RIGHT, buff=2)
            self.wait_until_bookmark('kn')
            self.play(FadeIn(k_n), run_time=FADEIN_T)
            self.wait_until_bookmark('k0')
            self.play(FadeIn(dot_dom[0][-2:]), run_time=FADEIN_T)
            self.wait_until_bookmark('k1')
            self.play(FadeIn(dot_dom[1][-2:]), run_time=FADEIN_T)
            self.wait_until_bookmark('etc')
            self.fadein_all(*[ m[-2:] for m in dot_dom[2:] ], run_time=1)
            
            self.wait_until_bookmark('left')
            self.play(FadeOut(k_n), AnimationGroup(*[ m.animate.to_edge(LEFT, 1) for m in dot_dom ], lag_ratio=0.05), run_time=1)

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

            self.wait_until_bookmark('dotn')
            self.play(FadeIn(dot_def), run_time=FADEIN_T)
            self.wait_until_bookmark('plusn')
            self.play(FadeIn(plus_def), run_time=FADEIN_T)
            self.wait_until_bookmark('restr')
            self.play(FadeIn(plus_dot_group), run_time=FADEIN_T)
            self.wait_until_bookmark('plus1')
            self.play(FadeIn(plus1_dot_group), run_time=FADEIN_T)

            fields = [ m[-1].copy() for m in dot_dom[0:5] ]
            fields.append(MathTex('\\vdots', font_size=50, color=green))

            VGroup(*fields).arrange(DOWN, buff=0.8).to_edge(LEFT, buff=2)

        self.play(AnimationGroup(
            FadeOut(*[ m[0:-1] for m in dot_dom[0:5] ], *dot_dom[5:]),
            AnimationGroup(*[ ReplacementTransform(dot_dom[i][-1], fields[i]) for i in range(5) ]),
            *[ FadeOut(m) for m in right ],
            FadeIn(fields[-1]),
            lag_ratio=0.075))
    
        self.fields = fields

        ###############
        ### SCENE 8 ###
        ###############

        fields = self.fields

        text = add_bookmarks("""
        You can think of K N as a smaller copy of the real numbers hidden within the real numbers. 
        It has two operations defined on it, {plus} plus N and {dot} dot N, and these operations obey 
        {props} all the properties of normal addition and multiplication, but with {0box} 0 replaced by 
        exp N of 0 and {1box} 1 replaced by exp N of 1. {outbox1} And these smaller copies of the real 
        numbers are related to each other in two ways. First of all, {eqs} the dot operation of one copy 
        is the same as the plus operation of the next, and second of all, you can go from {exp} K N to K N 
        plus 1 using exp and go the {log} other way using log, and these two functions are isomorphisms.
                             
        So {plusbox} plus N is a more restricted version of {dotbox} dot N minus 1. {outbox2} 
        But this is not true for {plus0} plus 0, because there's no such thing as dot negative 1, 
        and if there were, its domain, K negative 1, would have to be larger than the real numbers. 
        But we {shift} shouldn't let that stop us. The rest of this video will be devoted to defining 
        {kg1} K negative 1 as well as {kgn} K N for all negative integers N, resulting in a new number 
        system which I call the {expnum} exponential numbers.
        """)

        with self.voiceover(text) as tracker:

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
            
            self.wait_until_bookmark('plus')
            self.play(FadeIn(*plus), run_time=FADEIN_T)
            self.wait_until_bookmark('dot')
            self.play(FadeIn(*dots), run_time=FADEIN_T)

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
            self.wait_until_bookmark('props')
            self.play(FadeIn(pgroup), run_time=FADEIN_T)

            boxes0 = [
                SurroundingRectangle(m, color=yellow, buff=0.1)
                for m in [ properties[5][1], properties[7][1], properties[7][3] ]
            ]
            box1 = SurroundingRectangle(properties[6][1], color=yellow, buff=0.1)
            self.wait_until_bookmark('0box')
            self.play(*[ Create(m) for m in boxes0 ], run_time=BOX_T)
            self.wait_until_bookmark('1box')
            self.play(AnimationGroup(FadeOut(*boxes0[1:]), ReplacementTransform(boxes0[0], box1), lag_ratio=0.2), run_time=MOVE_T)
            self.wait_until_bookmark('outbox1')
            self.play(FadeOut(box1), run_time=FADEOUT_T)

            start = VGroup(plus[1], dots[0]).get_center() + UR * 0.08
            step = dots[1].get_center() - dots[0].get_center()
            
            eqs = [
                MathTex('=', font_size=75, color=purple).rotate(PI * 0.25).move_to(start + step * i)
                for i in range(5)
            ]
            self.wait_until_bookmark('eqs')
            self.fadein_all(*eqs, run_time=FADEALL_T)

            # gap: 0.25
            exp_arrow = ArcBetweenPoints(fields[1].get_right() + RIGHT * 0.05 + UP * 0.1, fields[0].get_right() + RIGHT * 0.12 + DOWN * 0.15, angle=(TAU / 5), color=purple)
            log_arrow = ArcBetweenPoints(fields[0].get_left() + LEFT * 0.07 + DOWN * 0.14, fields[1].get_left() + LEFT * 0.07 + UP * 0.08, angle=(TAU / 5), color=purple)
            exp_arrow.add_tip(**tip_size(0.27), at_start=True)
            log_arrow.add_tip(**tip_size(0.27), at_start=True)

            exp_arrs = [ exp_arrow.copy().shift(step * i) for i in range(5) ]
            log_arrs = [ log_arrow.copy().shift(step * i) for i in range(5) ]
            exp = MathTex('\exp', font_size=40, color=purple).next_to(exp_arrs[0], RIGHT, buff=0.15)
            log = MathTex('\log', font_size=40, color=purple).next_to(log_arrs[4], LEFT, buff=0.15)
            self.wait_until_bookmark('exp')
            self.fadein_all(exp, *exp_arrs, run_time=FADEALL_T)
            self.wait_until_bookmark('log')
            self.fadein_all(log, *reversed(log_arrs), run_time=FADEALL_T)

            plus_boxes = [ SurroundingRectangle(m, color=yellow, buff=0.1) for m in plus[1:5] ]
            self.wait_until_bookmark('plusbox')
            self.play(*[ Create(m) for m in plus_boxes ], run_time=BOX_T)
            self.wait_until_bookmark('dotbox')
            self.play(*[ plus_boxes[i].animate.move_to(dots[i]) for i in range(4) ], run_time=MOVE_T)
            self.wait_until_bookmark('outbox2')
            self.play(FadeOut(*plus_boxes), run_time=FADEOUT_T)
            
            plus0_box = SurroundingRectangle(plus[0], color=yellow, buff=0.1)
            self.wait_until_bookmark('plus0')
            self.play(Create(plus0_box), run_time=BOX_T)

            self.wait_until_bookmark('shift')
            self.play(*[ m.animate.shift(DOWN * 3.25) for m in self.get_top_level_mobjects() ], plus0_box.animate.shift(DOWN * 3.25).set_opacity(0), run_time=MOVE_T)

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

            self.wait_until_bookmark('kg1')
            self.play(FadeIn(neg_fields[0], neg_plus[0], neg_dots[0]), run_time=FADEIN_T)
            self.wait_until_bookmark('kgn')
            self.play(FadeIn(*neg_fields[1:], *neg_plus[1:], *neg_dots[1:]), run_time=FADEALL_T)

            expo = Text('exponential numbers', **fancy, font_size=50).next_to(properties[0], UP, buff=1.5)
            self.wait_until_bookmark('expnum')
            self.play(Write(expo), run_time=WRITE_T)
        
        text = add_bookmarks("""
        Since log maps each K N to K N minus 1, it should map {log} K 0 to K negative 1. 
        This means {out} that K negative 1 will contain the {kg1} real numbers, 
        as well as log of 0 and a logarithm for each negative number. 
        For now, I'll draw this set as two lines with a point in the middle. 
        The {p1} top line represents the real numbers, the {p2} central point is log of 0, 
        and the {p3} bottom line consists of logs of negative numbers, with {lmx} 
        log of minus X placed directly below {lx} log of X. For example, {shift0} 
        0 is {l1} log of 1, so the {shifts0} point below 0 is {lm1} log of minus 1. 
        {shift1} 1 is {le} log of E, so the point {shifts1} below 1 is {lme} log of minus E.
        """)

        with self.voiceover(text) as tracker:

            log_arr1 = log_arrs[0].copy().shift(-step)
            self.wait_until_bookmark('log')
            self.play(FadeIn(log_arr1), run_time=FADEIN_T)

            self.wait_until_bookmark('out')
            self.play(FadeOut(expo, *properties), run_time=FADEOUT_T)
            
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

            self.wait_until_bookmark('kg1')
            self.play(FadeIn(K_1, top, top_tips, log0, log0_label, bottom, bottom_tips), run_time=FADEIN_T)

            pstart = log0.get_center() + LEFT * 1.5
            pointer1 = Line(pstart, pstart + UR, color=yellow,).add_tip(**tip_size(0.27))
            pointer2 = Line(pstart, pstart + RIGHT * 1.25, color=yellow,).add_tip(**tip_size(0.27))
            pointer3 = Line(pstart, pstart + DR, color=yellow,).add_tip(**tip_size(0.27))
            self.wait_until_bookmark('p1')
            self.play(FadeIn(pointer1), run_time=FADEIN_T)
            self.wait_until_bookmark('p2')
            self.play(ReplacementTransform(pointer1, pointer2), run_time=MOVE_T)
            self.wait_until_bookmark('p3')
            self.play(ReplacementTransform(pointer2, pointer3), run_time=MOVE_T)
            
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

            self.wait_until_bookmark('lmx')
            self.play(FadeIn(log_nx, log_nx_label), run_time=FADEIN_T)
            self.wait_until_bookmark('lx')
            self.play(FadeIn(log_x, log_x_label), FadeOut(pointer3), run_time=FADEIN_T)
            self.wait_until_bookmark('shift0')
            self.play(ReplacementTransform(log_x, log_1), FadeOut(log_x_label), run_time=MOVE_T)
            self.wait_until_bookmark('l1')
            self.play(FadeIn(log_1_label), run_time=FADEIN_T)
            self.wait_until_bookmark('shifts0')
            self.play(ReplacementTransform(log_nx, log_n1), FadeOut(log_nx_label), run_time=MOVE_T)
            self.wait_until_bookmark('lm1')
            self.play(FadeIn(log_n1_label), run_time=FADEIN_T)
            self.wait_until_bookmark('shift1')
            self.play(ReplacementTransform(log_1, log_e), FadeOut(log_1_label), run_time=MOVE_T)
            self.wait_until_bookmark('le')
            self.play(FadeIn(log_e_label), run_time=FADEIN_T)
            self.wait_until_bookmark('shifts1')
            self.play(ReplacementTransform(log_n1, log_ne), FadeOut(log_n1_label), run_time=MOVE_T)
            self.wait_until_bookmark('lme')
            self.play(FadeIn(log_ne_label), run_time=FADEIN_T)

        self.play(FadeOut(
            log_e, log_e_label, log_ne, log_ne_label, 
            *fields, *plus, *dots, *neg_fields, *neg_plus, *neg_dots,
            *eqs, exp, log, *exp_arrs, *log_arrs, log_arr1), run_time=FADEOUT_T)
            
        self.play(VGroup(K_1, top, top_tips, bottom, bottom_tips, log0, log0_label).animate.scale(sf).move_to(ORIGIN), run_time=MOVE_T)

        new_top = NumberLine(x_range=(-8, 8), length=12).scale(sf).move_to(top)
        new_bottom = NumberLine(x_range=(-8, 8), length=12).scale(sf).move_to(bottom)
        self.play(FadeOut(top_tips, bottom_tips), FadeIn(new_top, new_bottom), run_time=FADEIN_T)

        self.remove(top, bottom)
        top = new_top
        bottom = new_bottom

        text = add_bookmarks("""
        To help you visualize how this extended logarithm works, 
        I'll draw a {rdot} red dot here, call this number {x} X, 
        and draw a {bdot} blue dot at the point log of X. {approach} As X approaches 0, 
        its logarithm shoots off to the left. At {exact} exactly 0, its logarithm is the center point, 
        and as it {below} decreases further, the logarithm shoots in from the left, {end} but now on the bottom line. 
        Because of this behavior, I think it's accurate to call this center point {minf} minus infinity, 
        and to say that {arr} these lower points are less than minus infinity.
        """)

        with self.voiceover(text) as tracker:

            def log_ext(x):
                if x > 0: return top.number_to_point(math.log(x))
                if x < 0: return bottom.number_to_point(math.log(-x))
                return log0.get_center()
            
            x = ValueTracker(5)
            x_dot = always_redraw(lambda: Dot(point=top.number_to_point(x.get_value()), color=red).scale(sf))
            l_dot = always_redraw(lambda: Dot(point=log_ext(x.get_value()), color=blue).scale(sf))
            x_label = always_redraw(lambda: MathTex('x', font_size=(40 * sf), color=red).next_to(x_dot, UP, 0.15 * sf))

            self.wait_until_bookmark('rdot')
            self.play(FadeIn(x_dot), run_time=FADEIN_T)
            self.wait_until_bookmark('x')
            self.play(FadeIn(x_label), run_time=FADEIN_T)
            self.wait_until_bookmark('bdot')
            self.play(FadeIn(l_dot), run_time=FADEIN_T)
            self.wait_until_bookmark('approach')
            self.play(x.animate.set_value(0), run_time=tracker.time_until_bookmark('exact'))
            self.wait_until_bookmark('below')
            self.play(x.animate.set_value(-5), run_time=tracker.time_until_bookmark('end'))

            minf = MathTex('-\infty', font_size=(40 * sf), color=purple).next_to(log0, RIGHT, 0.15 * sf)
            self.wait_until_bookmark('minf')
            self.play(ReplacementTransform(log0_label, minf), run_time=TRANSFORM_T)

            new_pstart = log0.get_center() + LEFT * 1.5 * sf
            new_pointer3 = Line(new_pstart, new_pstart + DR * sf, color=yellow).add_tip(**tip_size(0.27))
            self.wait_until_bookmark('arr')
            self.play(FadeIn(new_pointer3), run_time=FADEIN_T)
        
        self.play(FadeOut(x_dot, l_dot, x_label, new_pointer3), run_time=FADEOUT_T)

        text = add_bookmarks("""
        I'll introduce a new notation for these numbers. I'll denote the point directly {xsx} across from X as squiggle X, 
        {shift0} so log of minus 1 {sq0} can also be referred to as squiggle 0. Applying the squiggle function is the same 
        as reflecting across {hori} this horizontal line. {out} An explicit definition is given by {sqdef} 
        squiggle X = log of minus exp of X.
        """)

        with self.voiceover(text) as tracker:

            x.set_value(1)
            x_dot.update()
            x_label.update()
            s_dot = always_redraw(lambda: Dot(point=bottom.number_to_point(x.get_value()), color=blue).scale(sf))
            s_label = MathTex('{\sim} x', font_size=(40 * sf), color=blue).next_to(s_dot, UP, buff=(0.15 * sf))
            self.wait_until_bookmark('xsx')
            self.play(FadeIn(x_dot, x_label, s_dot, s_label), run_time=FADEIN_T)

            x_label.clear_updaters()
            self.wait_until_bookmark('shift0')
            self.play(FadeOut(x_label, s_label), x.animate.set_value(0), run_time=MOVE_T)
            
            new_x_label = MathTex('0', font_size=(40 * sf), color=red).next_to(x_dot, UP, 0.15 * sf)
            new_s_label = MathTex('\log(-1) = {\sim} 0', font_size=(40 * sf), color=blue).next_to(s_dot, UP, buff=(0.15 * sf))
            self.wait_until_bookmark('sq0')
            self.play(FadeIn(new_x_label, new_s_label), run_time=FADEIN_T)

            hori = DashedLine(log0.get_center() + LEFT * 8 , log0.get_center() + RIGHT * 8, dash_length=0.2, color=green)
            self.wait_until_bookmark('hori')
            self.play(FadeIn(hori), run_time=FADEIN_T)
            self.wait_until_bookmark('out')
            self.play(FadeOut(hori), run_time=FADEOUT_T)

            sq_def = MathTex('{\sim} x = \log(-\exp x)', font_size=(40 * sf)).next_to(log0, LEFT, buff=0.7).shift(UL * 0.3)
            self.wait_until_bookmark('sqdef')
            self.play(FadeIn(sq_def), run_time=FADEIN_T)
        
        ###############
        ### SCENE 9 ###
        ###############

        text = add_bookmarks("""
        To see how we can extend {add} addition to this number system, 
        we'll first look at how multiplication extends from the positive numbers to the {out} real numbers. 
        In other words, how can we define {mul} real-number multiplication in terms of positive number multiplication. 
        Well, {pos2} if both of the inputs happen to be positive, we simply multiply them. {posneg} 
        If exactly one of the inputs is negative, we negate it to get two positive numbers, then multiply, 
        and then negate the result. {neg2} If both are negative, we negate both of them and multiply, 
        but we don't negate the result because negative times negative is positive. 
        The only remaining case is {zero} where one or both of the inputs are zero, 
        and in this case we just return zero.

        Now we'll repeat this construction, but instead of extending multiplication from positive numbers to reals, 
        we'll extend addition from K 0 to K negative 1. All we need to do is replace {rep1} multiplication with addition, 
        {rep2} 0 with minus infinity, and {rep3} minus with squiggle. {switch} 
        For example, if you want to add {nums} these two numbers, you apply {sq1} squiggle to make them both real, 
        then {sum} add them together, and then {sq2} squiggle the result.
        """)

        with self.voiceover(text) as tracker:

            addition = Text('addition?', **fancy, font_size=(40 * sf)).next_to(minf, RIGHT, buff=0.7).shift(UR * 0.3)
            self.wait_until_bookmark('add')
            self.play(Write(addition), run_time=WRITE_T)
            self.wait_until_bookmark('out')
            self.fade_all(K_1, VGroup(x_dot, new_x_label), top, sq_def, VGroup(log0, minf), addition, VGroup(s_dot, new_s_label), bottom, run_time=FADEALL_T)
            self.K_1 = (K_1, top, log0, minf, bottom)

            lhs = MathTex('x {{\cdot}} y =', font_size=50)
            
            rhs_tex = [ 
                'x, y > 0:', 'x \cdot y',
                'x < 0 \\text{ and } y > 0:', '-(-x \cdot y)',
                'x > 0 \\text{ and } y < 0:', '-(x \cdot -y)',
                'x, y < 0:', '-x \cdot -y', 
                'x = 0 \\text{ or } y = 0:', '0', 
            ]
            
            rhs = VGroup(*[ MathTex(t, substrings_to_isolate=['\cdot', '0', '-'], font_size=50) for t in rhs_tex ]).arrange_in_grid(cols=2, buff=0.5, cell_alignment=LEFT)
            brace = Brace(rhs, LEFT)
            VGroup(lhs, VGroup(brace, rhs)).arrange(RIGHT, buff=0.25)

            self.wait_until_bookmark('mul')
            self.play(FadeIn(lhs), run_time=FADEIN_T)
            self.wait_until_bookmark('pos2')
            self.play(FadeIn(brace, rhs[0:2]), run_time=FADEIN_T)
            self.wait_until_bookmark('posneg')
            self.play(FadeIn(rhs[2:6]), run_time=FADEIN_T)
            self.wait_until_bookmark('neg2')
            self.play(FadeIn(rhs[6:8]), run_time=FADEIN_T)
            self.wait_until_bookmark('zero')
            self.play(FadeIn(rhs[8:]), run_time=FADEIN_T)

            rhs2_tex = [ s.replace('\cdot', '+') for s in rhs_tex ]
            rhs3_tex = [ s.replace('0', '-\infty') for s in rhs2_tex ]
            rhs4_tex = [ (s.replace('-', '{\sim}') if i in [3,5,7] else s) for (i, s) in enumerate(rhs3_tex) ]
            rhs2 = VGroup(*[ MathTex(t, substrings_to_isolate=['+', '0', '-'], font_size=50) for t in rhs2_tex ]).arrange_in_grid(cols=2, buff=0.5, cell_alignment=LEFT)
            rhs3 = VGroup(*[ MathTex(t, substrings_to_isolate=['+', '-\infty', '-'], font_size=50) for t in rhs3_tex ]).arrange_in_grid(cols=2, buff=0.5, cell_alignment=LEFT)
            rhs4 = VGroup(*[ MathTex(t, substrings_to_isolate=['+', '-\infty', '{\sim}'], font_size=50) for t in rhs4_tex ]).arrange_in_grid(cols=2, buff=0.5, cell_alignment=LEFT)
            for m in [rhs2, rhs3, rhs4]:
                m.shift(rhs.get_left() - m.get_left())
            
            lhs2 = MathTex('x {{+}} y =', font_size=50)
            lhs2.shift(lhs.get_right() - lhs2.get_right())

            self.wait_until_bookmark('rep1')
            self.play(Transform(rhs, rhs2), Transform(lhs, lhs2), run_time=MOVE_T)
            self.wait_until_bookmark('rep2')
            self.play(Transform(rhs, rhs3), run_time=MOVE_T)
            self.wait_until_bookmark('rep3')
            self.play(Transform(rhs, rhs4), run_time=MOVE_T)

            self.wait_until_bookmark('switch')
            self.play(FadeOut(*self.get_top_level_mobjects()), run_time=FADEOUT_T)
            self.play(FadeIn(K_1, top, log0, minf, bottom), run_time=FADEIN_T)

            x = Dot(point=top.number_to_point(1), color=red).scale(sf)
            y = Dot(point=bottom.number_to_point(3), color=blue).scale(sf)
            y2 = Dot(point=top.number_to_point(3), color=blue).scale(sf)
            z = Dot(point=top.number_to_point(4), color=green).scale(sf)
            z2 = Dot(point=bottom.number_to_point(4), color=green).scale(sf)

            self.wait_until_bookmark('nums')
            self.play(FadeIn(x, y))
            self.wait_until_bookmark('sq1')
            self.play(Transform(y, y2))
            self.wait_until_bookmark('sum')
            self.play(Transform(y, z, path_arc=(-TAU / 4)), ReplacementTransform(x, z, path_arc=(-TAU / 4)))
            self.remove(y)
            self.wait_until_bookmark('sq2')
            self.play(Transform(z, z2))

        text = add_bookmarks("""
        This is the best way to visualize the extended addition operation, 
        {out} but there's a simpler way to {in} define it. If you {new} replace squiggle X with log of minus exp of X, 
        replace the remaining occurrences of X with log of exp of X, do likewise with Y, and then expand the remaining squiggles, 
        you get these horrific expressions. If we simplify them using the rules for log and exp, the minuses all cancel out, 
        and in each case {simplify} we're left with log of exp of X times exp of Y. 
        The case where one of the inputs is minus infinity also fits {formula} this formula, 
        because if we {subst} plug in minus infinity, we get {log0} log of 0 times something, 
        which is {minf} minus infinity. Therefore, our extended addition operation can be defined with {unify} this one formula.

        If you replace exp with {log1} log negative 1 and log with {exp1} exp negative 1, 
        {out2} and recall how we {dotdef} defined all those dot operations, 
        you can see that what I've been calling “extended addition” could also be called {dot1} dot negative 1. 
        We can define {plus1} plus negative 1 in a similar fashion. {fade} 
        So we've succeeded in {tower} extending this tower of operations in the negative direction.
        """)

        with self.voiceover(text) as tracker:
            self.wait_until_bookmark('out')
            self.fade_all(K_1, top, VGroup(log0, minf), VGroup(bottom, z), run_time=FADEALL_T)

            VGroup(lhs, brace, rhs).move_to(ORIGIN)

            rhs5_tex = [
                rhs4_tex[0], '{{ x }} + {{ y }}',
                rhs4_tex[2], '{{ {\sim} }} ( {{ {\sim} x }} + {{ y }} )',
                rhs4_tex[4], '{{ {\sim} }} ( {{ x }} + {{ {\sim} y }} )',
                rhs4_tex[6], '{{ {\sim} x }} + {{ {\sim} y }}',
                rhs4_tex[8], '-\infty',
            ]
            rhs5 = VGroup(*[ MathTex(t, font_size=50) for t in rhs5_tex ]).arrange_in_grid(cols=2, buff=0.5, cell_alignment=LEFT).move_to(rhs)
            rhs5[1][0].set_color(blue); rhs5[1][2].set_color(blue)
            rhs5[3][0].set_color(blue); rhs5[3][2].set_color(blue); rhs5[3][4].set_color(blue)
            rhs5[5][0].set_color(blue); rhs5[5][2].set_color(blue); rhs5[5][4].set_color(blue)
            rhs5[7][0].set_color(blue); rhs5[7][2].set_color(blue)
            top_def = VGroup(lhs.copy(), brace.copy(), rhs5).scale(0.65).to_edge(UP, buff=0.8)

            rhs6_tex = [
                rhs4_tex[0], '{{ \log (\exp x) }} + {{ \log (\exp y) }}',
                rhs4_tex[2], '{{ \log (-\exp }} \,( {{ \log (-\exp x) }} + {{ \log (\exp y) }} ) {{ ) }}',
                rhs4_tex[4], '{{ \log (-\exp }} \,( {{ \log (\exp x) }} + {{ \log (-\exp y) }} ) {{ ) }}',
                rhs4_tex[6], '{{ \log (-\exp x) }} + {{ \log (-\exp y) }}',
                rhs4_tex[8], '-\infty',
            ]
            rhs6 = VGroup(*[ MathTex(t, font_size=50) for t in rhs6_tex ]).arrange_in_grid(cols=2, buff=0.5, cell_alignment=LEFT)
            rhs6.shift(rhs.get_left() - rhs6.get_left())
            rhs6[1][0].set_color(blue); rhs6[1][2].set_color(blue)
            rhs6[3][0].set_color(blue); rhs6[3][2].set_color(blue); rhs6[3][4].set_color(blue); rhs6[3][6].set_color(blue)
            rhs6[5][0].set_color(blue); rhs6[5][2].set_color(blue); rhs6[5][4].set_color(blue); rhs6[5][6].set_color(blue)
            rhs6[7][0].set_color(blue); rhs6[7][2].set_color(blue)
            bottom_def = VGroup(lhs.copy(), brace.copy(), rhs6).scale(0.65).move_to(ORIGIN).to_edge(DOWN, buff=0.8)

            self.wait_until_bookmark('in')
            self.play(FadeIn(top_def), run_time=FADEIN_T)
            self.wait_until_bookmark('new')
            self.play(FadeIn(bottom_def), run_time=FADEIN_T)

            final = MathTex('{{\log}} ({{\exp}} x \cdot {{\exp}} y)', font_size=50, color=green).scale(0.65)
            finals = [ final.copy().shift(rhs6[i].get_left() - final.get_left()) for i in range(1, 8, 2) ]
            self.wait_until_bookmark('simplify')
            self.play(*[ ReplacementTransform(rhs6[2 * i + 1], finals[i]) for i in range(4) ], run_time=MOVE_T)
            self.play(FadeOut(top_def), bottom_def.animate.set_x(-0.25), run_time=MOVE_T)

            y = 1.5
            eq1 = MathTex('\log (\exp {{x}} \cdot \exp y)', font_size=50, color=green).shift(UP * y)
            eq2 = MathTex('\log (\exp {{(-\infty)}} \cdot \exp y)', font_size=50, color=green).shift(UP * y)
            eq3 = MathTex('\log ({{\exp (-\infty)}} \cdot \exp y)', font_size=50, color=green).shift(UP * y)
            eq4 = MathTex('\log ({{0}} \cdot \exp y)', font_size=50, color=green).shift(UP * y)
            eq5 = MathTex('-\infty', font_size=50, color=green).shift(UP * y)
            self.wait_until_bookmark('formula')
            self.play(FadeIn(eq1), run_time=FADEIN_T)
            self.wait_until_bookmark('subst')
            self.play(ReplacementTransform(eq1, eq2), run_time=MOVE_T)
            self.add(eq3); self.remove(eq2)
            self.wait_until_bookmark('log0')
            self.play(ReplacementTransform(eq3, eq4), run_time=MOVE_T)
            self.wait_until_bookmark('minf')
            self.play(ReplacementTransform(eq4, eq5), run_time=TRANSFORM_T)

            lhs_final = MathTex('x {{+}} y =', font_size=50)
            rhs_final = MathTex('{{\log}} ({{\exp}} x \cdot {{\exp}} y)', font_size=50, color=green)
            VGroup(lhs_final, rhs_final).arrange(RIGHT, buff=0.15).shift(DOWN * y)
            self.wait_until_bookmark('unify')
            self.play(ReplacementTransform(bottom_def[0], lhs_final), FadeOut(bottom_def[1], bottom_def[2][0], bottom_def[2][2:]), ReplacementTransform(finals[0], rhs_final), run_time=MOVE_T)
            
            rhs2 = MathTex('{{\log}} ({{\log^{-1}}} x \cdot {{\log^{-1}}} y)', font_size=50, color=green)
            rhs3 = MathTex('{{\exp^{-1}}} ({{\log^{-1}}} x \cdot {{\log^{-1}}} y)', font_size=50, color=green)
            rhs2.shift(rhs_final.get_left() - rhs2.get_left()).shift(UP * 0.065)
            rhs3.shift(rhs_final.get_left() - rhs3.get_left()).shift(UP * 0.065)

            dotn_def = MathTex('x \cdot_n y = \exp^n(\log^n x \cdot \log^n y)', font_size=50, color=blue).move_to(eq5)

            self.wait_until_bookmark('log1')
            self.play(ReplacementTransform(rhs_final, rhs2), run_time=MOVE_T)
            self.wait_until_bookmark('exp1')
            self.play(ReplacementTransform(rhs2, rhs3), run_time=MOVE_T)
            self.wait_until_bookmark('out2')
            self.play(FadeOut(eq5), VGroup(lhs_final, rhs3).animate.set_x(0), run_time=MOVE_T)
            self.wait_until_bookmark('dotdef')
            self.play(FadeIn(dotn_def), run_time=FADEIN_T)

            lhs2 = MathTex('x {{\cdot_{-1}}} y =', font_size=50)
            lhs2.shift(lhs_final[-1].get_right() - lhs2[-1].get_right())
            self.wait_until_bookmark('dot1')
            self.play(ReplacementTransform(lhs_final, lhs2), run_time=TRANSFORM_T)

            plus_1 = MathTex('x +_{-1} y =', '\exp^{-1} (\log^{-1} x + \log^{-1} y)', font_size=50)
            plus_1[1].set_color(green)
            plus_1.move_to(VGroup(lhs2, rhs3, dotn_def))
            self.wait_until_bookmark('plus1')
            self.play(FadeIn(plus_1), run_time=FADEIN_T)

            self.wait_until_bookmark('fade')
            self.fade_all(dotn_def, plus_1, VGroup(lhs2, rhs3), run_time=FADEALL_T)

            table = VGroup(
                MathTex('K_{-1}', font_size=50, color=green), MathTex('+_{-1}', font_size=50, color=blue), MathTex('\cdot_{-1}', font_size=50, color=blue),
                MathTex('K_0', font_size=50, color=green), MathTex('+_0', font_size=50, color=blue), MathTex('\cdot_0', font_size=50, color=blue),
                MathTex('K_1', font_size=50, color=green), MathTex('+_1', font_size=50, color=blue), MathTex('\cdot_1', font_size=50, color=blue),
                MathTex('K_2', font_size=50, color=green), MathTex('+_2', font_size=50, color=blue), MathTex('\cdot_2', font_size=50, color=blue),
                MathTex('K_3', font_size=50, color=green), MathTex('+_3', font_size=50, color=blue), MathTex('\cdot_3', font_size=50, color=blue),
                MathTex('\\vdots', font_size=50, color=green), MathTex('\\vdots', font_size=50, color=blue), MathTex('\\vdots', font_size=50, color=blue),
            )
            table.arrange_in_grid(cols=3, buff=0.75)
            for m in table[2:15:3]: m.shift(DOWN * 0.06)

            eq = MathTex('=', font_size=75, color=red).rotate(PI / 4)
            eqs = [ eq.copy().move_to(VGroup(table[i], table[i + 2])).shift(UR * 0.06) for i in range(2, 15, 3) ]
            center = VGroup(*eqs).get_x()
            for m in eqs: m.set_x(center)

            self.wait_until_bookmark('tower')
            self.play(FadeIn(table, *eqs), run_time=FADEIN_T)
    
        ################
        ### SCENE 10 ###
        ################

        # bookmarks messed up because of weird transcription
        text = add_bookmarks("""
        But we have the same problem now as we had before. Unlike all the other plus operations, 
        {plusbox} plus negative 1 has no generalization. {outbox} And the problem runs deeper than that. 
        K negative 1 is isomorphic to K 0, because one can go {iso} back and forth between them using exp 
        and log while preserving the structure of the dot and plus operations. 
        K negative 1 might seem like a crazy new number system containing values less than minus infinity, 
        {same} but it's structure is the same as that of the real numbers, it's the real numbers in disguise. 
        K negative 1 is best thought of not as a new number system, but as a relabeling, or alternative presentation, 
        of the reals. Nevertheless, this alternative presentation can give us insight into how we can extend things further. 
        Once we've defined dot N and plus N for {ext} all integers N, we really will have a new number system.
        """)

        with self.voiceover(text) as tracker:

            plus_box = SurroundingRectangle(table[1], color=yellow, buff=0.1)
            self.wait(5.5) # self.wait_until_bookmark('plusbox')
            self.play(Create(plus_box), run_time=BOX_T)
            self.wait(2) # self.wait_until_bookmark('outbox')
            self.play(FadeOut(plus_box), run_time=FADEOUT_T)

            log_arr = ArcBetweenPoints(table[3].get_corner(UR) + DOWN * 0.135, table[0].get_corner(DR) + DL * 0.05 + DOWN * 0.02, angle=(TAU / 7), color=purple).add_tip(**tip_size(0.27))
            exp_arr = ArcBetweenPoints(table[0].get_corner(DL), table[3].get_corner(UL) + DOWN * 0.18, angle=(TAU / 6), color=purple).add_tip(**tip_size(0.27))
            log = MathTex('\log', font_size=40, color=purple).next_to(log_arr, RIGHT, 0.1)
            exp = MathTex('\exp', font_size=40, color=purple).next_to(exp_arr, LEFT, 0.1)
            self.wait(5) # self.wait_until_bookmark('iso')
            self.play(FadeIn(log_arr, exp_arr, log, exp), run_time=FADEIN_T)

            left = VGroup(table, *eqs, log_arr, exp_arr, log, exp)
            iso = Tex('$K_{-1}$', ' and ', '$K_0$', ' have \\\\ the same structure', font_size=50).shift(RIGHT * 3)
            iso.get_parts_by_tex('K').set_color(green)
            self.wait(12) # self.wait_until_bookmark('same')
            self.play(FadeIn(iso), left.animate.shift(LEFT * 2.5), run_time=MOVE_T)

            top_dots = table[15:].copy().set_opacity(0).next_to(table, UP, buff=0.75)
            self.wait(18) # self.wait_until_bookmark('ext')
            self.play(left.animate.shift(DOWN * 0.87), top_dots.animate.set_opacity(1).shift(DOWN * 0.87), run_time=MOVE_T)
    
        self.play(FadeOut(*self.get_top_level_mobjects()), run_time=FADEOUT_T)

        ################
        ### SCENE 11 ###
        ################

        (K_1, top, log0, minf, bottom) = self.K_1

        text = add_bookmarks("""
        To make this easier, I'm going to change how I depict {in} K negative 1. 
        Instead of putting {cur} log of minus X directly below log of X, 
        I'm going to {shift} put it below {m1} minus X. And similarly, log of 0 will go {log0} directly below 0. 
        {outl} This arrangement is less symmetric, but it's more obvious now how we're extending K 0 to K negative 1; 
        we're just {arr} adding logs of non-positive numbers. And we can {etc} keep going.
        """)

        with self.voiceover(text) as tracker:

            minf = MathTex('\log(0)', color=purple).next_to(log0, RIGHT, buff=(0.15 * sf))
            self.wait_until_bookmark('in')
            self.play(FadeIn(K_1, top, log0, minf, bottom), run_time=FADEIN_T)

            log_1 = Dot(top.number_to_point(0), color=red).scale(sf)
            log_n1 = Dot(bottom.number_to_point(0), color=blue).scale(sf).set_z_index(1)
            log_1_label = MathTex('\log(1)', color=red).next_to(log_1, UP, buff=(0.15 * sf))
            log_n1_label = MathTex('\log(-1)', color=blue).next_to(log_n1, UP, buff=(0.15 * sf))
            self.wait_until_bookmark('cur')
            self.play(FadeIn(log_1, log_n1, log_1_label, log_n1_label), run_time=FADEIN_T)

            left = NumberLine(x_range=(-8, 0), length=6).scale(sf)
            left.move_to(bottom.get_center() - left.get_right())
            self.add(left)

            self.wait_until_bookmark('shift')
            self.play(
                log_n1.animate.move_to(bottom.number_to_point(-1)), 
                log_n1_label.animate.shift(bottom.number_to_point(-1) - bottom.number_to_point(0)),
                FadeOut(log_1, log_1_label, bottom),
                run_time=MOVE_T
            )

            n1 = log_1.move_to(top.number_to_point(-1))
            n1_label = MathTex('-1', color=red).next_to(n1, UP, buff=(0.15 * sf))
            self.wait_until_bookmark('m1')
            self.play(FadeIn(n1, n1_label), run_time=FADEIN_T)

            self.wait_until_bookmark('log0')
            self.play(log0.animate.move_to(left.number_to_point(0)), minf.animate.shift(left.number_to_point(0) - log0.get_center()), run_time=MOVE_T)

            self.wait_until_bookmark('outl')
            self.play(FadeOut(n1, n1_label, log_n1, log_n1_label, log0, minf), run_time=FADEOUT_T)

            arr = Arrow(top.number_to_point(-2.5), left.number_to_point(-2.5), color=purple, buff=0.5)
            log = MathTex('\log', font_size=(40 * sf), color=purple).next_to(arr, RIGHT, buff=(0.15 * sf))
            self.wait_until_bookmark('arr')
            self.play(GrowArrow(arr, point_color=BLACK), FadeIn(log), run_time=GROWARROW_T)

            lines = VGroup(left)
            diff = left.number_to_point(0) - top.number_to_point(0)
            for i in range(1, 4):
                lines += left.copy().shift(diff * i)
            vdots = MathTex('\\vdots', font_size=50).move_to(left).shift(diff * 4)

            top_target = top.copy().to_edge(UP, buff=1)
            lines_target = lines.copy().arrange(DOWN, buff=1).next_to(top_target, DOWN, buff=1, aligned_edge=LEFT)
            vdots_target = vdots.copy().next_to(lines_target, DOWN, buff=0.5).set_x(lines[-1].number_to_point(-3.5)[0])

            self.wait_until_bookmark('etc')
            self.play(FadeOut(arr, log, K_1), Transform(top, top_target), Transform(lines, lines_target), Transform(vdots, vdots_target), run_time=1.5)

        text = add_bookmarks("""
        So now we have a line at the top, representing the {real} real numbers, 
        and infinitely many half-lines below it, representing {log1} logs of non-positive numbers, 
        {log2} logs of those numbers, {etc} and so on. I'll call this whole set {e} E, and call its elements 
        {expo} exponential numbers. {total} Every exponential number has a logarithm, which is itself an exponential number. 
        This property makes E unique among all of the sets we've seen so far. 
        """)

        with self.voiceover(text) as tracker:
    
            R = MathTex('\mathbb{R}', font_size=60).next_to(top, DOWN, buff=0.25).set_x(top.number_to_point(1.5)[0])
            self.wait_until_bookmark('real')
            self.play(FadeIn(R), run_time=FADEIN_T)

            logs = VGroup(*[ 
                Arrow((top if i == 0 else lines[i - 1]).number_to_point(-3.5), lines[i].number_to_point(-3.5), buff=0.2, color=purple)
                for i in range(len(lines))
            ])
            log = MathTex('\log', font_size=40, color=purple).next_to(logs[0], RIGHT, buff=0.2)
            self.wait_until_bookmark('log1')
            self.play(FadeIn(logs[0], log), run_time=FADEIN_T)
            self.wait_until_bookmark('log2')
            self.play(FadeIn(logs[1]), run_time=FADEIN_T)
            self.wait_until_bookmark('etc')
            self.play(FadeIn(*logs[2:]), run_time=FADEIN_T)

            E = MathTex('\mathrm{E}', font_size=100).next_to(top, DOWN, buff=2).set_x(top.number_to_point(3.5)[0])
            expo = Text('exponential numbers', **fancy, font_size=50).next_to(E, DOWN, buff=0.5)
            self.wait_until_bookmark('e')
            self.play(FadeIn(E), run_time=FADEIN_T)
            self.wait_until_bookmark('expo')
            self.play(Write(expo), run_time=WRITE_T)

            total = MathTex('\log : \mathrm{E} \\to \mathrm{E}', font_size=50).next_to(expo, DOWN, buff=0.5)
            self.wait_until_bookmark('total')
            self.play(FadeIn(total), run_time=FADEIN_T)
        
        text = add_bookmarks("""
        We can now define K N for all integers N. {k0} K 0 is the top line, 
        {kg1} K negative 1 is the top two lines, {kg2} K negative 2 is the top three lines, 
        {kg3} K negative 3 is the top four lines, and so on. 
        {out} And the {def} definitions of plus N and dot N now make sense for all negative indices. 
        For example, {dotg3} dot negative 3 takes two inputs, {xy} X and Y, 
        applies {exp3} exp three times to each of them, {mul} multiplies the results, 
        and then applies {log3} log three times. The domain of this operation is {dom} K negative 3, 
        because the formula only works if applying exp three times gets you to the real numbers, 
        so the input has to be somewhere in the top four lines.
        """)
        
        with self.voiceover(text) as tracker:

            diff = lines[1].number_to_point(0) - lines[0].number_to_point(0)
            start = top.number_to_point(0) - diff/2
            braces = [ Brace(Line(start, start + diff * i), RIGHT, buff=0.1, color=blue) for i in range(1, 5) ]
            ks = [ 
                MathTex('K', '_{' + str(-i) + '}', font_size=60, color=blue).next_to(braces[0], RIGHT, buff=0.1).shift(-diff/2 + DOWN * 0.1)
                for i in range(0, 4) 
            ]

            self.wait_until_bookmark('k0')
            self.play(FadeIn(braces[0], ks[0]), run_time=FADEIN_T)
            self.wait_until_bookmark('kg1')
            self.play(ReplacementTransform(braces[0], braces[1]), ReplacementTransform(ks[0], ks[1]), run_time=MOVE_T)
            self.wait_until_bookmark('kg2')
            self.play(ReplacementTransform(braces[1], braces[2]), ReplacementTransform(ks[1], ks[2]), run_time=MOVE_T)
            self.wait_until_bookmark('kg3')
            self.play(ReplacementTransform(braces[2], braces[3]), ReplacementTransform(ks[2], ks[3]), run_time=MOVE_T)
            
            dotn_def = MathTex('x \cdot{{_n}} y = \exp{{^n}}(\log{{^n}} x \cdot \log{{^n}} y)', font_size=50, color=blue).next_to(E, UP, buff=1)
            dot3_def = MathTex('x \cdot{{_{-3}}} y = \exp{{^{-3}}}(\log{{^{-3}}} x \cdot \log{{^{-3}}} y)', font_size=40, color=blue).move_to(dotn_def)
            self.wait_until_bookmark('out')
            self.play(FadeOut(braces[3], ks[3], R), run_time=FADEOUT_T)
            self.wait_until_bookmark('def')
            self.play(FadeIn(dotn_def), run_time=FADEIN_T)
            self.wait_until_bookmark('dotg3')
            self.play(ReplacementTransform(dotn_def, dot3_def), run_time=TRANSFORM_T)

            x = Dot(lines[2].number_to_point(-1.75), color=blue).scale(sf)
            y = Dot(lines[0].number_to_point(-0.25), color=red).scale(sf)
            xl = MathTex('x', font_size=50, color=blue).next_to(x, DOWN, buff=0.2)
            yl = MathTex('y', font_size=50, color=red).next_to(y, DOWN, buff=0.2)
            self.wait_until_bookmark('xy')
            self.play(FadeIn(x, y, xl, yl), run_time=FADEIN_T)
        
            yn = math.exp(math.exp(-0.25))
            self.wait_until_bookmark('exp3')
            self.play(x.animate.move_to(lines[1].number_to_point(-1.75)), y.animate.move_to(top.number_to_point(-0.25)), FadeOut(xl, yl), run_time=0.6)
            self.play(x.animate.move_to(lines[0].number_to_point(-1.75)), y.animate.move_to(top.number_to_point(math.exp(-0.25))), run_time=0.6)
            self.play(x.animate.move_to(top.number_to_point(-1.75)), y.animate.move_to(top.number_to_point(yn)), run_time=0.6)

            prod = -1.75 * yn
            arc = TAU / 6
            z = Dot(top.number_to_point(prod), color=green).scale(sf)
            self.wait_until_bookmark('mul')
            self.play(ReplacementTransform(x, z, path_arc=arc), ReplacementTransform(y, z, path_arc=arc), run_time=MOVE_T)
            self.wait_until_bookmark('log3')
            self.play(z.animate.move_to(lines[0].number_to_point(prod)), run_time=0.6)
            self.play(z.animate.move_to(lines[1].number_to_point(prod)), run_time=0.6)
            self.play(z.animate.move_to(lines[2].number_to_point(prod)), run_time=0.6)

            self.wait_until_bookmark('dom')
            self.play(FadeIn(braces[3], ks[3]), run_time=FADEIN_T)

        self.fade_all(
            VGroup(braces[3], ks[3]), 
            VGroup(log, logs[0], dot3_def), 
            VGroup(logs[1], E),
            VGroup(logs[2], z, expo),
            VGroup(logs[3], total),
        )

        text = add_bookmarks("""
        There's an easier way to visualize these operations. 
        First, we extend each of these half-lines into a {full} full line. Each point is the log of the point above it, 
        so {lx1} this is the log of {x} this. But {lx2} this is also the log of the red point, so {corr} 
        these two points are equivalent, they represent the same exponential number. {out} 
        There is no longer a one-to-one correspondence between numbers and points; in fact, 
        each number is represented by {inf} infinitely many points. To give you an idea of which points are equivalent, 
        {out2} I'll draw {guides} these guidelines.
        """)

        with self.voiceover(text) as tracker:

            ks = [ top ]
            for m in lines:
                ks.append(top.copy().move_to(m.number_to_point(0)))
            self.wait_until_bookmark('full')
            self.play(FadeIn(*ks[1:]), vdots.animate.set_x(0), run_time=MOVE_T)
            self.remove(*lines)

            x = Dot(ks[0].number_to_point(0.5), color=red).scale(sf)
            lx1 = Dot(ks[1].number_to_point(0.5), color=blue).scale(sf)
            lx2 = Dot(ks[0].number_to_point(math.log(0.5)), color=blue).scale(sf)

            log1 = Line(x, lx1, buff=0.1, color=purple).add_tip(**tip_size(0.27))
            log2 = ArcBetweenPoints(x.get_corner(UL) + UL * 0.05, lx2.get_corner(UR) + UR * 0.05, angle=TAU/6, color=purple).add_tip(**tip_size(0.27))
            log_label = MathTex('\log', font_size=50, color=purple).next_to(log1, RIGHT, buff=0.175)
            corr = double_arrow(lx1, lx2)
            
            self.wait_until_bookmark('lx1')
            self.play(FadeIn(lx1), run_time=FADEIN_T)
            self.wait_until_bookmark('x')
            self.play(FadeIn(x, log1, log_label), run_time=FADEIN_T)
            self.wait_until_bookmark('lx2')
            self.play(FadeIn(lx2, log2), run_time=FADEIN_T)
            self.wait_until_bookmark('corr')
            self.play(FadeIn(corr), run_time=FADEIN_T)
            self.wait_until_bookmark('out')
            self.play(FadeOut(x, log1, log2, log_label), run_time=FADEOUT_T)

            lx3 = Dot(ks[2].number_to_point(math.exp(0.5)), color=blue).scale(sf)
            lx4 = Dot(ks[3].number_to_point(math.exp(math.exp(0.5))), color=blue).scale(sf)
            lx5 = Dot(ks[4].number_to_point(25), color=blue).scale(sf)
            corr3 = double_arrow(lx1, lx3)
            corr4 = double_arrow(lx3, lx4)
            corr5 = double_arrow(lx4, lx5)
            self.wait_until_bookmark('inf')
            self.fadein_all(VGroup(lx3, corr3), VGroup(lx4, corr4), corr5)

            scale_x = ks[0].number_to_point(1)[0] - ks[0].number_to_point(0)[0]
            scale_y = ks[1].get_y() - ks[0].get_y()
            f0 = lambda i: lambda t: ks[i].number_to_point(0) + RIGHT * scale_x * (-1/t + 1) + UP * scale_y * t
            f1 = lambda i: lambda t: ks[i].number_to_point(0) + RIGHT * scale_x * t + UP * scale_y * t
            f2 = lambda i: lambda t: ks[i].number_to_point(0) + RIGHT * scale_x * math.exp(t) + UP * scale_y * t
            f3 = lambda i: lambda t: ks[i].number_to_point(0) + RIGHT * scale_x * math.exp(math.exp(t)) + UP * scale_y * t

            guides = VGroup(
                *[ ParametricFunction(f0(i), t_range=(0.1, 1), stroke_width=2, color=yellow) for i in range(4) ],
                *[ ParametricFunction(f1(i), t_range=(0, 1), stroke_width=2, color=yellow) for i in range(4) ],
                *[ ParametricFunction(f2(i), t_range=(0, 1), stroke_width=2, color=yellow) for i in range(4) ],
                *[ ParametricFunction(f3(i), t_range=(0, 1), stroke_width=2, color=yellow) for i in range(4) ],
            )
            self.wait_until_bookmark('out2')
            self.play(FadeOut(lx1, lx2, lx3, lx4, corr, corr3, corr4, corr5), run_time=FADEOUT_T)
            self.wait_until_bookmark('guides')
            self.play(FadeIn(guides), run_time=FADEIN_T)
        
        self.wait(0.75)
        
        text = add_bookmarks("""
        Earlier I said that K negative 2 consists of the top three lines. 
        But now we can think of the third line on its own as {kg2} K negative 2, 
        since all of the {points} points above this line have {equiv} equivalent points within it. 
        So each of these lines corresponds to {kn} K N for some non-positive N. We can extend this to positive N as well, 
        {shift} by drawing K 1 on its own line above the real numbers, and so on. To be clear, 
        we aren't adding any new values by doing this, but it makes the presentation more symmetrical.
        """)

        with self.voiceover(text) as tracker:

            K_2 = MathTex('K_{-2}', font_size=40, color=green).next_to(ks[2], UP, buff=0.1).set_x(ks[2].number_to_point(-3.5)[0])
            self.wait_until_bookmark('kg2')
            self.play(FadeIn(K_2), run_time=FADEIN_T)

            points = [ ks[1].number_to_point(-2.5), ks[0].number_to_point(-1.5), ks[1].number_to_point(1.5)]
            targets = [ ks[2].number_to_point(math.exp(-2.5)), ks[2].number_to_point(math.exp(math.exp(-1.5))), ks[2].number_to_point(math.exp(1.5)) ]
            dots = [ Dot(p, color=blue).scale(sf) for p in points ]
            self.wait_until_bookmark('points')
            self.play(FadeIn(*dots), run_time=FADEIN_T)
            self.wait_until_bookmark('equiv')
            self.play(*[ dots[i].animate.move_to(targets[i]) for i in range(3) ], run_time=MOVE_T)

            kls = [ MathTex('K_{' + str(-i) + '}', font_size=40, color=green).next_to(ks[i], UP, buff=0.1).set_x(ks[i].number_to_point(-3.5)[0]) for i in range(5) ]
            self.wait_until_bookmark('kn')
            self.play(FadeIn(*kls), FadeOut(*dots), run_time=FADEIN_T)
            self.remove(K_2)

            diff = ks[0].get_center() - ks[1].get_center()
            pks = [ ks[0].copy().shift(diff * i) for i in range(1, 3) ]
            pkls = [ MathTex('K_{' + str(i) + '}', font_size=40, color=green).next_to(pks[i - 1], UP, buff=0.1).set_x(ks[0].number_to_point(-3.5)[0]) for i in range(1, 3) ]
            pguides = guides.copy().shift(diff * 4)

            self.wait_until_bookmark('shift')
            self.play(
                *[ m.animate.shift(DOWN * 2.5) for m in self.get_top_level_mobjects() ],
                *[ fadein_shift(m, DOWN * 2.5) for m in [ *pks, *pkls, pguides ] ],
                run_time=MOVE_T
            )

        text = add_bookmarks("""
        So here's how to visualize the dot and plus operations. Say we want to apply plus negative 2 to {xy} these two values, 
        X and Y. Each is represented by {sev} several points on the screen. 
        We look at the {box} points which are on the K negative 2 line, and {add} add them as if it were the real number line. 
        The result is {res} X plus negative 2 Y. For another example, {out} suppose we want to apply dot 2 to {xy2} these two values. 
        {sev2} We look at their {box2} representations on the K 2 line, 
        and then {mul} multiply them as if this were the real number line.
        """)

        with self.voiceover(text) as tracker:

            xd = Dot(ks[3].number_to_point(0.25), color=red).scale(sf)
            yd = Dot(ks[0].number_to_point(0.25), color=blue).scale(sf)
            xl = MathTex('x', font_size=50, color=red).next_to(xd, UP, buff=0.2)
            yl = MathTex('y', font_size=50, color=blue).next_to(yd, UP, buff=0.2)
            x = VGroup(xd, xl)
            y = VGroup(yd, yl)
            self.wait_until_bookmark('xy')
            self.play(FadeIn(x, y), run_time=FADEIN_T)

            xs = x.copy().shift(ks[2].number_to_point(math.log(0.25)) - xd.get_center())
            ys = VGroup(
                y.copy().shift(pks[0].number_to_point(math.log(0.25)) - yd.get_center()),
                y.copy().shift(ks[1].number_to_point(math.exp(0.25)) - yd.get_center()),
                y.copy().shift(ks[2].number_to_point(math.exp(math.exp(0.25))) - yd.get_center()))
            self.wait_until_bookmark('sev')
            self.play(FadeIn(xs, ys), run_time=FADEIN_T)

            xbox = SurroundingRectangle(xs[0], buff=0.1, color=yellow)
            ybox = SurroundingRectangle(ys[2][0], buff=0.1, color=yellow)
            self.wait_until_bookmark('box')
            self.play(Create(xbox), Create(ybox), run_time=BOX_T)

            sumd = Dot(ks[2].number_to_point(math.exp(math.exp(0.25)) + math.log(0.25)), color=green).scale(sf)
            suml = MathTex('x +_{-2} y', font_size=40, color=green).next_to(sumd, DOWN, buff=0.2).shift(RIGHT * 0.3)
            self.wait_until_bookmark('add')
            self.play(FadeIn(sumd), run_time=FADEIN_T)
            self.wait_until_bookmark('res')
            self.play(FadeIn(suml), run_time=FADEIN_T)

            self.wait_until_bookmark('out')
            self.play(FadeOut(x, y, xs, ys, xbox, ybox, sumd, suml), run_time=FADEOUT_T)

            yl.next_to(yd, DOWN, buff=0.2)
            xs = VGroup(
                x.copy().shift(pks[1].number_to_point(-2.5) - xd.get_center()),
                x.copy().shift(pks[0].number_to_point(math.exp(-2.5)) - xd.get_center()),
                x.copy().shift(ks[0].number_to_point(math.exp(math.exp(-2.5))) - xd.get_center()),
                x.copy().shift(ks[1].number_to_point(math.exp(math.exp(math.exp(-2.5)))) - xd.get_center()))
            ys = y.copy().shift(pks[1].number_to_point(2.2) - yd.get_center())
            self.wait_until_bookmark('xy2')
            self.play(FadeIn(xs[1], ys), run_time=FADEIN_T)
            self.wait_until_bookmark('sev2')
            self.play(FadeIn(xs[0], xs[2:]), run_time=FADEIN_T)

            xbox.move_to(xs[0][0])
            ybox.move_to(ys[0])
            self.wait_until_bookmark('box2')
            self.play(Create(xbox), Create(ybox), run_time=BOX_T)

            prodd = Dot(pks[1].number_to_point(-2.5 * 2.2), color=green).scale(sf)
            prodl = MathTex('x \cdot_2 y', font_size=40, color=green).next_to(prodd, UP, buff=0.2)
            self.wait_until_bookmark('mul')
            self.play(FadeIn(prodd, prodl), run_time=FADEIN_T)

        self.fade_all(
            VGroup(xs, ys, prodd, prodl, xbox, ybox), 
            VGroup(guides, pguides),
            VGroup(pks[1], pkls[1]),
            VGroup(pks[0], pkls[0]),
            *[ VGroup(ks[i], kls[i]) for i in range(len(ks)) ], 
            run_time=FADEALL_T)

class Scene12_13(ChainOfFields):
    audio_dir = 'assets/audio/Scene12_13'

    def construct(self):

        ################
        ### SCENE 12 ###
        ################

        text = add_bookmarks("""
        So to summarize, we've constructed this set {e} E by extending the real numbers with logs of non-positive numbers, 
        logs of those values, and so on. E contains a subset {kn} K N for each integer N, and these subsets form an {chain} 
        infinite descending chain, with K N plus 1 contained inside K N. K 0 {k0} is the real number line we started with, 
        and {kndef} K N is defined as the set exp N of X for all real numbers X. For example, {kg2def} K negative 2 is 
        the set of logs of logs of real numbers, since exp negative 2 is the same as log 2. {out} Each K N has its own 
        versions of addition and multiplication, {plusn} denoted {plusn} plus N {dotn} and dot N, and these are {def} defined as shown. 
        {rel} Plus N is the same as dot N minus 1, when both are defined, and this means that {distr} dot N distributes 
        over dot N minus 1. In other words, we have a {opchain} chain of binary operations, with each distributing over 
        the one before it, and this chain extends infinitely in both directions.
        """)

        with self.voiceover(text) as tracker:

            eq1 = MathTex('\mathrm{E}', '\supset K_n', font_size=50)
            eq2 = MathTex('\cdots \supset K_{-2} \supset K_{-1} \supset K_0 \supset K_1 \supset K_2 \supset \cdots', font_size=50)
            eq3 = MathTex('K_0 = \mathbb{R}', '\qquad K_n = \{ \exp^n x \ |\  x \in \mathbb{R} \}', font_size=50)
            eq4 = MathTex('K_{-2} = \{ \exp^{-2} x \} = \{ \log (\log x) \}', font_size=50)
            VGroup(eq1, eq2, eq3, eq4).arrange(DOWN, buff=0.65)

            self.wait_until_bookmark('e')
            self.play(FadeIn(eq1[0]), run_time=FADEIN_T)
            self.wait_until_bookmark('kn')
            self.play(FadeIn(eq1[1]), run_time=FADEIN_T)
            self.wait_until_bookmark('chain')
            self.play(FadeIn(eq2), run_time=FADEIN_T)
            self.wait_until_bookmark('k0')
            self.play(FadeIn(eq3[0]), run_time=FADEIN_T)
            self.wait_until_bookmark('kndef')
            self.play(FadeIn(eq3[1]), run_time=FADEIN_T)
            self.wait_until_bookmark('kg2def')
            self.play(FadeIn(eq4), run_time=FADEIN_T)
            self.wait_until_bookmark('out')
            self.fade_all(eq1, eq2, eq3, eq4, run_time=FADEALL_T)

            plusn_def = MathTex('x +_n y', '= \exp^n(\log^n x + \log^n y)', font_size=50, color=blue)
            dotn_def = MathTex('x \cdot_n y', '= \exp^n(\log^n x \cdot \log^n y)', font_size=50, color=green)
            plus_dot = MathTex('x +_n y', '=', 'x \cdot_{n-1} y', font_size=50)
            distr = MathTex('\cdot_n', '\\text{ distributes over }', '\cdot_{n - 1}', font_size=50)
            chain = MathTex('\cdots \leftarrow {{\cdot_{-2}}} \leftarrow {{\cdot_{-1}}} \leftarrow {{\cdot_0}} \leftarrow {{\cdot_1}} \leftarrow {{\cdot_2}} \leftarrow \cdots', font_size=50)
            VGroup(plusn_def, dotn_def, plus_dot, distr, chain).arrange(DOWN, buff=0.65)
            
            plus_dot[0].set_color(blue) 
            plus_dot[2].set_color(green)
            distr[0].set_color(green)
            distr[2].set_color(green)
            chain[1:10:2].set_color(green)
            
            self.wait_until_bookmark('plusn')
            self.play(FadeIn(plusn_def[0]), run_time=FADEIN_T)
            self.wait_until_bookmark('dotn')
            self.play(FadeIn(dotn_def[0]), run_time=FADEIN_T)
            self.wait_until_bookmark('def')
            self.play(FadeIn(plusn_def[1], dotn_def[1]), run_time=FADEIN_T)
            self.wait_until_bookmark('rel')
            self.play(FadeIn(plus_dot), run_time=FADEIN_T)
            self.wait_until_bookmark('distr')
            self.play(FadeIn(distr), run_time=FADEIN_T)
            self.wait_until_bookmark('opchain')
            self.play(FadeIn(chain), run_time=FADEIN_T)
        
        self.fade_all(plusn_def, dotn_def, plus_dot, distr, chain, run_time=FADEALL_T)
    
        ################
        ### SCENE 13 ###
        ################

        text = add_bookmarks("""
        I'll end this video with two exercises for the viewer. 
        First, there is a natural {f} bijection between the exponential numbers and the reals, 
        {map0} mapping 0 to 0, {map1} 1 to 1, {mape} E to 2, {maplog0} log of 0 to minus 1, and in general, 
        {gen} mapping exp N of 0 to N for all integers N. {q1} Find this bijection. 
        {q2} Second, show how E can be defined as a colimit. Leave your answers in the comments, 
        and of course, {sub} subscribe to my channel. I'll be posting {more} more videos like this in the future.
        """)

        with self.voiceover(text) as tracker:

            f = MathTex('f : \mathrm{E} \\to \mathbb{R}', font_size=50, color=blue)
            map_0 = MathTex('f(0) = 0', font_size=50, color=blue) 
            map_1 = MathTex('f(1) = 1', font_size=50, color=blue)
            map_e = MathTex('f(e) = 2', font_size=50, color=blue)
            map_log0 = MathTex('f(\log 0) = -1', font_size=50, color=blue)
            gen = MathTex('f(\exp^n 0) = n', font_size=50, color=blue)
            VGroup(f, map_0, map_1, map_e, map_log0).arrange(DOWN, buff=0.65)
            gen.move_to(VGroup(map_1, map_e))

            self.wait_until_bookmark('f')
            self.play(FadeIn(f), run_time=FADEIN_T)
            self.wait_until_bookmark('map0')
            self.play(FadeIn(map_0), run_time=FADEIN_T)
            self.wait_until_bookmark('map1')
            self.play(FadeIn(map_1), run_time=FADEIN_T)
            self.wait_until_bookmark('mape')
            self.play(FadeIn(map_e), run_time=FADEIN_T)
            self.wait_until_bookmark('maplog0')
            self.play(FadeIn(map_log0), run_time=FADEIN_T)
            self.wait_until_bookmark('gen')
            self.play(*[ ReplacementTransform(m, gen) for m in [ map_0, map_1, map_e, map_log0 ]], run_time=MOVE_T)

            ex1 = Tex(
                '1. Find a ``natural" bijection \\\\ {{$f : \mathrm{E} \\to \mathbb{R}$}} such that \\\\ {{$f(\exp^n 0) = n$}} for all integers n.',
                font_size=50)
            ex2 = Tex(
                '2. Construct $\mathrm{E}$ as a colimit (in $\mathbf{Set}$).',
                font_size=50)
            VGroup(ex1, ex2).arrange(DOWN, buff=0.65)
            ex1[1:4:2].set_color(blue)

            self.wait_until_bookmark('q1')
            self.play(FadeIn(ex1[0], ex1[2], ex1[4]), f.animate.move_to(ex1[1]), gen.animate.move_to(ex1[3]), run_time=MOVE_T)
            self.wait_until_bookmark('q2')
            self.play(FadeIn(ex2), run_time=FADEIN_T)

            sub = Text('Subscribe', **fancy, font_size=50).next_to(ex1, UP, buff=0.65)
            vid = Text('for more videos', **fancy, font_size=50).next_to(ex2, DOWN, buff=0.65)

            self.wait_until_bookmark('sub')
            self.play(Write(sub), run_time=WRITE_T)
            self.wait_until_bookmark('more')
            self.play(Write(vid), run_time=WRITE_T)