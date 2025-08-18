from manim import *

CYAN = "#00FFFF"  # định nghĩa màu cyan

class MLOAnimation(Scene):
    def construct(self):
        # Vẽ AP và STA
        ap = Circle(color=BLUE).shift(LEFT*4)
        sta = Circle(color=RED).shift(RIGHT*4)
        ap_text = Text("AP", font_size=24).move_to(ap.get_center())
        sta_text = Text("STA", font_size=24).move_to(sta.get_center())

        self.play(Create(ap), Create(sta), Write(ap_text), Write(sta_text))

        # Hai link song song
        link1 = Line(ap.get_right()+UP*0.5, sta.get_left()+UP*0.5, color=GRAY)
        link2 = Line(ap.get_right()+DOWN*0.5, sta.get_left()+DOWN*0.5, color=GRAY)
        self.play(Create(link1), Create(link2))

        # Tạo danh sách packet
        packets = []
        for i in range(5):
            # Packet vàng trên link1 (dịch phải dần để tạo hiệu ứng nối tiếp)
            p1 = Dot(color=YELLOW).move_to(ap.get_right()+UP*0.5).shift(LEFT*0.5*i)
            packets.append((p1, link1))

            # Packet cyan trên link2
            p2 = Dot(color=CYAN).move_to(ap.get_right()+DOWN*0.5).shift(LEFT*0.5*i)
            packets.append((p2, link2))

        # Add vào scene
        for p, _ in packets:
            self.add(p)

        # Animation cho tất cả packet chạy song song
        animations = []
        for p, path in packets:
            animations.append(MoveAlongPath(p, path, rate_func=linear, run_time=4))

        # Phát animation đồng thời
        self.play(*animations)
        self.wait()

