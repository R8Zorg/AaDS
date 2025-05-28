import math

from circle import Circle
from circle_canvas import CircleCanvas


class CircleManager:
    def __init__(self, canvas: CircleCanvas):
        self.canvas = canvas
        self.first_circle_id: int | None = None
        self.second_circle_id: int | None = None

    def load_circles_from_file(self, path: str = "input.txt", counts: int = 2) -> None:
        self.canvas.clear_canvas()
        self.canvas.draw_user_point()
        with open(path, "r") as f:
            for i, line in enumerate(f.readlines()[:counts]):
                x, y, r, color = line.split()
                circle = Circle(int(x), int(y), int(r), color, -1)
                circle_id = self.canvas.draw_circle(circle)
                if i == 0:
                    self.first_circle_id = circle_id
                if i == 1:
                    self.second_circle_id = circle_id

    def check_inclusion(self) -> bool:
        if not self.first_circle_id and not self.second_circle_id:
            return False
        first_circle = self.canvas.circles[self.first_circle_id]  # type: ignore
        second_circle = self.canvas.circles[self.second_circle_id]  # type: ignore
        return Circle.contains(first_circle, second_circle)

    def rotate_circle(
        self, circle_id: int, angle_degree: int, center: tuple[int, int]
    ) -> None:
        circle = self.canvas.circles[circle_id]
        center_x, center_y = center
        dx = circle.get_x() - center_x
        dy = circle.get_y() - center_y
        angle_rad = math.radians(angle_degree)
        new_x = center_x + math.cos(angle_rad) * dx - math.sin(angle_rad) * dy
        new_y = center_y + math.sin(angle_rad) * dx + math.cos(angle_rad) * dy
        circle.set_position(int(new_x), int(new_y))
        self.canvas.move_circle(circle)
