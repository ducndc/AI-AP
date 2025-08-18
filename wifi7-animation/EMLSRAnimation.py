from manim import *

class EMLSRWithTimelineACK(Scene):
    def construct(self):
        # ==== Helpers ====
        def packet(label, color):
            rect = Rectangle(height=0.34, width=1.0, color=color, fill_opacity=1)
            txt = Text(label, font_size=18, color=BLACK)
            txt.move_to(rect.get_center())
            return VGroup(rect, txt)

        def inactive_tag(midpoint):
            return Text("Inactive", font_size=16, color=GRAY).move_to(midpoint)

        # ==== Nodes ====
        ap = Circle(color=BLUE).shift(LEFT*4)
        sta = Circle(color=RED).shift(RIGHT*4)
        ap_text = Text("AP MLD", font_size=22).move_to(ap.get_center())
        sta_text = Text("STA MLD", font_size=22).move_to(sta.get_center())
        self.play(Create(ap), Create(sta), Write(ap_text), Write(sta_text))

        # ==== Links ====
        link1 = Line(ap.get_right()+UP*1.0, sta.get_left()+UP*1.0, color=GRAY)   # upper
        link2 = Line(ap.get_right()+DOWN*1.0, sta.get_left()+DOWN*1.0, color=GRAY) # lower
        l1_label = Text("Link 1 (e.g., 5 GHz)", font_size=18).next_to(link1, UP)
        l2_label = Text("Link 2 (e.g., 2.4 GHz)", font_size=18).next_to(link2, DOWN)
        self.play(Create(link1), Create(link2), Write(l1_label), Write(l2_label))

        # Convenience reversed paths (for STA->AP direction)
        path1_sta_to_ap = link1.copy().reverse_direction()
        path1_ap_to_sta = link1
        path2_ap_to_sta = link2
        path2_sta_to_ap = link2.copy().reverse_direction()

        # ==== Timeline ====
        timeline = Line(LEFT*4, RIGHT*4, color=WHITE).shift(DOWN*3)
        steps = ["Listening", "Link1: PPDU+ACK", "Listening", "Link2: MU-RTS/CTS/PPDU/ACK"]
        marks = []
        for i, name in enumerate(steps):
            pos = interpolate(timeline.get_start(), timeline.get_end(), i/(len(steps)-1))
            dot = Dot(pos, color=YELLOW)
            label = Text(name, font_size=14).next_to(dot, DOWN)
            self.add(dot, label)
            marks.append(dot)
        pointer = Triangle(color=RED, fill_opacity=1).scale(0.22).next_to(timeline.get_start(), UP, buff=0.1)

        self.play(Create(timeline), FadeIn(pointer))

        # ==== Phase 1: Listening on both links (CCA + ICF) ====
        listen1 = Text("Listening (CCA + ICF)", font_size=16, color=YELLOW).move_to(link1.get_center()).shift(DOWN*0.3)
        listen2 = listen1.copy().move_to(link2.get_center()).shift(UP*0.3)
        self.play(
            link1.animate.set_color(YELLOW),
            link2.animate.set_color(YELLOW),
            FadeIn(listen1), FadeIn(listen2),
            pointer.animate.move_to(marks[0].get_top()+UP*0.18)
        )
        self.wait(0.8)
        self.play(FadeOut(listen1), FadeOut(listen2))

        # ==== Phase 2: Link 1 wins channel; STA1 -> AP1 PPDU, then AP1 -> STA1 ACK ====
        # Other link inactive
        self.play(
            link1.animate.set_color(GREEN),
            link2.animate.set_color(GRAY),
            pointer.animate.move_to(marks[1].get_top()+UP*0.18)
        )
        l2_inact = inactive_tag(link2.get_center()).shift(UP*0.3)
        self.play(FadeIn(l2_inact), run_time=0.3)

        # PPDU (STA -> AP) on Link 1
        ppdu1 = packet("PPDU", GREEN).move_to(sta.get_left()+UP*1.0)
        self.play(FadeIn(ppdu1), run_time=0.2)
        self.play(MoveAlongPath(ppdu1, path1_sta_to_ap), run_time=2.0, rate_func=linear)
        self.play(FadeOut(ppdu1), run_time=0.2)

        # ACK (AP -> STA) on Link 1
        ack1 = packet("ACK", YELLOW).move_to(ap.get_right()+UP*1.0)
        self.play(FadeIn(ack1), run_time=0.2)
        self.play(MoveAlongPath(ack1, path1_ap_to_sta), run_time=1.2, rate_func=linear)
        self.play(FadeOut(ack1), run_time=0.2)

        self.play(FadeOut(l2_inact))
        self.play(link1.animate.set_color(GRAY))

        # ==== Phase 3: Return to Listening on both links ====
        self.play(
            link1.animate.set_color(YELLOW),
            link2.animate.set_color(YELLOW),
            pointer.animate.move_to(marks[2].get_top()+UP*0.18)
        )
        listen1b = Text("Listening", font_size=16, color=YELLOW).move_to(link1.get_center()).shift(DOWN*0.3)
        listen2b = listen1b.copy().move_to(link2.get_center()).shift(UP*0.3)
        self.play(FadeIn(listen1b), FadeIn(listen2b))
        self.wait(0.6)
        self.play(FadeOut(listen1b), FadeOut(listen2b))

        # ==== Phase 4: Link 2 wins channel; AP2->STA2 MU-RTS, STA2->AP2 CTS, then PPDU + ACK ====
        self.play(
            link2.animate.set_color(ORANGE),
            link1.animate.set_color(GRAY),
            pointer.animate.move_to(marks[3].get_top()+UP*0.18)
        )
        l1_inact = inactive_tag(link1.get_center()).shift(DOWN*0.3)
        self.play(FadeIn(l1_inact), run_time=0.3)

        # MU-RTS (AP -> STA) on Link 2
        murts = packet("MU-RTS", ORANGE).move_to(ap.get_right()+DOWN*1.0)
        self.play(FadeIn(murts), run_time=0.2)
        self.play(MoveAlongPath(murts, path2_ap_to_sta), run_time=1.4, rate_func=linear)
        self.play(FadeOut(murts), run_time=0.2)

        # CTS (STA -> AP) on Link 2
        cts = packet("CTS", TEAL).move_to(sta.get_left()+DOWN*1.0)
        self.play(FadeIn(cts), run_time=0.2)
        self.play(MoveAlongPath(cts, path2_sta_to_ap), run_time=1.0, rate_func=linear)
        self.play(FadeOut(cts), run_time=0.2)

        # PPDU (AP -> STA) on Link 2
        ppdu2 = packet("PPDU", GREEN).move_to(ap.get_right()+DOWN*1.0)
        self.play(FadeIn(ppdu2), run_time=0.2)
        self.play(MoveAlongPath(ppdu2, path2_ap_to_sta), run_time=1.8, rate_func=linear)
        self.play(FadeOut(ppdu2), run_time=0.2)

        # ACK (STA -> AP) on Link 2
        ack2 = packet("ACK", YELLOW).move_to(sta.get_left()+DOWN*1.0)
        self.play(FadeIn(ack2), run_time=0.2)
        self.play(MoveAlongPath(ack2, path2_sta_to_ap), run_time=1.2, rate_func=linear)
        self.play(FadeOut(ack2), run_time=0.2)

        self.wait(2)