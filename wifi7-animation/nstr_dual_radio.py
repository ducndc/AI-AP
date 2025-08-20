from manim import *

class STRDualRadio(Scene):
    def construct(self):
        # ==== Helpers ====
        def pkt(label, color):
            box = Rectangle(width=1.5, height=0.4, color=color, fill_opacity=1)
            txt = Text(label, font_size=18, color=BLACK).move_to(box.get_center())
            return VGroup(box, txt)

        def run_packet(group, path, t=1.6):
            return AnimationGroup(
                FadeIn(group),
                MoveAlongPath(group, path),
                FadeOut(group),
                lag_ratio=0.9, run_time=t
            )

        # ==== Nodes (dual-radio AP/STA) ====
        ap = RoundedRectangle(width=1.8, height=1.0, corner_radius=0.15, color=BLUE, fill_opacity=0.4).shift(LEFT*4)
        sta = RoundedRectangle(width=1.8, height=1.0, corner_radius=0.15, color=GREEN, fill_opacity=0.4).shift(RIGHT*4)
        ap_lbl = Text("AP MLD (dual-radio)", font_size=22).next_to(ap, UP*1.2)
        sta_lbl = Text("STA MLD (dual-radio)", font_size=22).next_to(sta, UP*1.2)
        self.play(Create(ap), Create(sta), Write(ap_lbl), Write(sta_lbl))

        # ==== Two links (top=Link1, bottom=Link2) ====
        link1 = Line(ap.get_right()+UP*1.2, sta.get_left()+UP*1.2, color=GRAY)
        link2 = Line(ap.get_right()+DOWN*1.2, sta.get_left()+DOWN*1.2, color=GRAY)
        l1_txt = Text("Link 1", font_size=18).next_to(link1, UP*0.7)
        l2_txt = Text("Link 2", font_size=18).next_to(link2, DOWN*0.7)
        self.play(Create(link1), Create(link2), Write(l1_txt), Write(l2_txt))

        # Convenience reversed paths
        path1_AP2STA = link1
        path1_STA2AP = link1.copy().reverse_direction()
        path2_AP2STA = link2
        path2_STA2AP = link2.copy().reverse_direction()

        # ==== Phase A: Listening on enabled links ====
        listen1 = Text("Listening (CCA)", font_size=16, color=YELLOW).move_to(link1.get_center()).shift(DOWN*0.4)
        listen2 = Text("Listening (CCA)", font_size=16, color=YELLOW).move_to(link2.get_center()).shift(UP*0.4)
        self.play(
            link1.animate.set_color(YELLOW),
            link2.animate.set_color(YELLOW),
            FadeIn(listen1), FadeIn(listen2)
        )
        self.wait(1)
        self.play(FadeOut(listen1), FadeOut(listen2))

        # ==== Phase C: STR frame exchanges happen concurrently ====
        # Link 1 (UL): STA -> AP PPDU + ACK
        ack_ul1  = pkt("ACK", YELLOW).move_to(ap.get_right()+UP*1.2)
        ack_ul2  = pkt("ACK", YELLOW).move_to(ap.get_right()+DOWN*1.2)
        ppdu_ul1 = pkt("UL PPDU", ORANGE).move_to(sta.get_left()+UP*1.2)
        ppdu_ul2 = pkt("UL PPDU", ORANGE).move_to(sta.get_left()+DOWN*1.2)

        # Link 2 (DL): AP -> STA PPDU + ACK
        ppdu_dl1 = pkt("DL PPDU", TEAL).move_to(ap.get_right()+UP*1.2)
        ppdu_dl2 = pkt("DL PPDU", TEAL).move_to(ap.get_right()+DOWN*1.2)
        ack_dl1  = pkt("ACK", YELLOW).move_to(sta.get_left()+UP*1.2)
        ack_dl2  = pkt("ACK", YELLOW).move_to(sta.get_left()+DOWN*1.2)

        # Tô màu trạng thái hoạt động đồng thời
        self.play(link1.animate.set_color(GREEN), link2.animate.set_color(TEAL))

        # Chạy đồng thời UL (Link1) và DL (Link2)
        self.play(
            run_packet(ppdu_ul1, path1_STA2AP, t=4.0),
            run_packet(ppdu_ul2, path2_STA2AP, t=4.0)
        )

        # ACK đồng thời ngược chiều
        self.play(
            run_packet(ack_ul1,  path1_AP2STA, t=4.0),
            run_packet(ack_ul2,  path2_AP2STA, t=4.0)
        )

        # Chạy đồng thời DL (Link1) và DL (Link2)
        self.play(
            run_packet(ppdu_dl1, path1_AP2STA, t=4.0),
            run_packet(ppdu_dl2, path2_AP2STA, t=4.0)
        )

        # ACK đồng thời ngược chiều
        self.play(
            run_packet(ack_dl1,  path1_STA2AP, t=4.0),
            run_packet(ack_dl2,  path2_STA2AP, t=4.0)
        )

        self.wait(2)