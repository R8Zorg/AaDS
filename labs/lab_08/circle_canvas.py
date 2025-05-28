import tkinter as tk

from circle import Circle


class CircleCanvas:
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.circles: dict[int, Circle] = {}
        self.user_point: Circle | None = None

    def clear_canvas(self) -> None:
        self.circles.clear()
        self.canvas.delete("all")

    def draw_circle(self, circle: Circle) -> int:
        coords = self.get_coordinates(circle.get_x(), circle.get_y(), circle.get_r())
        circle_id = self.canvas.create_oval(coords, outline=circle.get_color(), width=5)
        circle.set_id(circle_id)
        self.circles[circle_id] = circle
        return circle_id

    def draw_user_point(
        self, x: int = -10, y: int = -10, r: int = 3, color: str = "Black"
    ) -> None:
        circle = Circle(x, y, r, color, -1)
        self.draw_circle(circle)
        self.user_point = circle

    def move_circle(self, circle: Circle) -> None:
        self.canvas.coords(
            circle.get_id(),
            *self.get_coordinates(circle.get_x(), circle.get_y(), circle.get_r()),
        )

    def update_color(self, circle: Circle) -> None:
        self.canvas.itemconfigure(circle.get_id(), outline=circle.get_color())

    def get_coordinates(self, x: int, y: int, r: int) -> tuple[int, int, int, int]:
        return x - r, y - r, x + r, y + r
