import math
import tkinter as tk
from functools import partial
from tkinter import messagebox
from typing import Literal

from circle import Circle


class MainWindow:
    def __init__(self, root: tk.Tk):
        root.geometry("924x730")
        # root.minsize(1, 1)
        # root.maxsize(2545, 1410)
        root.resizable(True, True)
        root.title("My program")

        self.root = root
        self.circles: dict[int, Circle] = {}
        self.first_circle_id: int = 2
        self.second_circle_id: int = 3
        self.selected_circle_id: tk.IntVar = tk.IntVar(value=2)

        self.btn_load_data = tk.Button(
            text="Загрузить данные", command=self.load_and_draw_circles
        )
        self.btn_load_data.place(relx=0.042, rely=0.086, height=33, width=161)

        self.btn_color_red = tk.Button(
            text="",
            background="Red",
            activebackground="Red",
            command=partial(self.paint_circle, "Red"),
        )
        self.btn_color_red.place(relx=0.797, rely=0.084, height=33, width=71)

        self.btn_color_blue = tk.Button(
            text="",
            background="Blue",
            activebackground="Blue",
            command=partial(self.paint_circle, "Blue"),
        )
        self.btn_color_blue.place(relx=0.865, rely=0.084, height=33, width=71)

        self.btn_color_orange = tk.Button(
            text="",
            background="Orange",
            activebackground="Orange",
            command=partial(self.paint_circle, "Orange"),
        )
        self.btn_color_orange.place(relx=0.797, rely=0.125, height=33, width=71)

        self.btn_color_white = tk.Button(
            text="",
            background="White",
            activebackground="White",
            command=partial(self.paint_circle, "White"),
        )
        self.btn_color_white.place(relx=0.865, rely=0.125, height=33, width=71)

        self.btn_color_yellow = tk.Button(
            text="",
            background="Yellow",
            activebackground="Yellow",
            command=partial(self.paint_circle, "Yellow"),
        )
        self.btn_color_yellow.place(relx=0.797, rely=0.164, height=33, width=71)

        self.btn_color_green = tk.Button(
            text="",
            background="Green",
            activebackground="Green",
            command=partial(self.paint_circle, "Green"),
        )
        self.btn_color_green.place(relx=0.865, rely=0.164, height=33, width=71)

        self.btn_check_entry = tk.Button(
            text="Проверка включения",
            command=self.check_circles,
        )
        self.btn_check_entry.place(relx=0.043, rely=0.162, height=33, width=161)

        self.draw_field = tk.Canvas(
            background="#d2d8d7",
            borderwidth="2",
            relief="ridge",
            selectbackground="#d9d9d5",
        )
        self.draw_field.bind("<Button-1>", self.move_user_point)
        self.draw_field.place(relx=0.044, rely=0.253, relheight=0.732, relwidth=0.896)

        self.lb_check_entry = tk.Label(text="Вхождение не найдено", anchor="center")
        self.lb_check_entry.place(relx=0.043, rely=0.221, height=19, width=163)

        self.lb_choose_color = tk.Label(text="Выбрать цвет")
        self.lb_choose_color.place(relx=0.793, rely=0.054, height=18, width=145)

        self.btn_turn_left = tk.Button(text="По часовой", command=self.rotate_left)
        self.btn_turn_left.place(relx=0.368, rely=0.204, height=33, width=131)

        self.btn_turn_right = tk.Button(
            text="Против часовой", command=self.rotate_right
        )
        self.btn_turn_right.place(relx=0.507, rely=0.204, height=33, width=131)

        self.entry_turn_degree = tk.Entry()
        self.entry_turn_degree.place(relx=0.478, rely=0.164, height=25, relwidth=0.06)

        self.lb_enter_turn_degree = tk.Label(text="Введите угол поворота (гр.)")
        self.lb_enter_turn_degree.place(relx=0.368, rely=0.137, height=23, width=264)

        self.rb_first_circle = tk.Radiobutton(
            text="1й кр.",
            anchor="w",
            value=self.first_circle_id,
            variable=self.selected_circle_id,
        )
        self.rb_first_circle.place(
            relx=0.424, rely=0.094, relheight=0.034, relwidth=0.075
        )
        self.rb_second_circle = tk.Radiobutton(
            text="2й кр.",
            anchor="w",
            value=self.second_circle_id,
            variable=self.selected_circle_id,
        )
        self.rb_second_circle.place(
            relx=0.511, rely=0.094, relheight=0.034, relwidth=0.075
        )

        self.lb_choose_circle = tk.Label(text="Выбор круга")
        self.lb_choose_circle.place(relx=0.37, rely=0.067, height=23, width=261)

    def check_circles(self) -> None:
        if len(self.circles) != 2:
            messagebox.showerror(
                "Ошибка проверки", "Ошибка проверки.\nКругов на поле должно быть 2"
            )
            return
        is_include = Circle.contains(
            self.circles[self.first_circle_id], self.circles[self.second_circle_id]
        )
        if is_include:
            self.lb_check_entry.configure(text="Вхождение найдено", foreground="Green")
        else:
            self.lb_check_entry.configure(text="Вхождение не найдено", foreground="Red")

    def load_and_draw_circles(self) -> None:
        circles_num = 2
        self.clear_field()
        self.draw_user_point()
        with open("input.txt", "r") as f:
            lines = f.readlines()[:circles_num]
            for line in lines:
                try:
                    x, y, r, color = line.split()
                    circle_id = self.draw_field.create_oval(
                        self.get_coordinates(int(x), int(y), int(r)),
                        outline=color,
                        width=5,
                    )
                    self.circles[circle_id] = Circle(
                        int(x), int(y), int(r), color, circle_id
                    )
                except ValueError:
                    messagebox.showerror(
                        "Ошибка чтения данных",
                        "Ошибка чтения данных.\nОжидаемый ввод: int int int str",
                    )
                    return
        self.update_ids()

    def get_coordinates(self, x: int, y: int, r: int) -> tuple[int, int, int, int]:
        x1 = x - r
        y1 = y - r
        x2 = x + r
        y2 = y + r
        return x1, y1, x2, y2

    def paint_circle(self, color: str) -> None:
        self.circles[self.selected_circle_id.get()].set_color(color)
        self.draw_field.itemconfigure(self.selected_circle_id.get(), outline=color)

    def move_to(self, x: int, y: int, r: int, id: int) -> None:
        self.draw_field.coords(
            id,
            x - r,
            y - r,
            x + r,
            y + r,
        )

    def draw_user_point(self) -> None:
        x, y = -10, -10
        user_point_r = 3
        color = "Black"
        circle_id = self.draw_field.create_oval(
            self.get_coordinates(x, y, user_point_r),
            outline=color,
            width=3,
        )
        self.user_point = Circle(x, y, user_point_r, color, circle_id)

    def move_user_point(self, event: tk.Event) -> None:  # type: ignore[type-arg]
        try:
            self.user_point.set_position(event.x, event.y)
        except AttributeError:
            return
        self.move_to(
            event.x,
            event.y,
            self.user_point.get_r(),
            self.user_point.get_id(),
        )

    def rotate_circle(self, sign: Literal[1, -1]) -> None:
        selected_circle = self.circles[self.selected_circle_id.get()]
        rotation_center = [self.user_point.get_x(), self.user_point.get_y()]
        if self.entry_turn_degree.get() == "":
            return
        degree = int(self.entry_turn_degree.get()) * sign
        cx = rotation_center[0]
        cy = rotation_center[1]

        angle_rad = math.radians(degree)
        dx = selected_circle.get_x() - cx
        dy = selected_circle.get_y() - cy
        new_x = cx + math.cos(angle_rad) * dx - math.sin(angle_rad) * dy
        new_y = cy + math.sin(angle_rad) * dx + math.cos(angle_rad) * dy
        selected_circle.set_position(int(new_x), int(new_y))
        self.move_to(
            int(new_x),
            int(new_y),
            selected_circle.get_r(),
            selected_circle.get_id(),
        )

    def rotate_left(self) -> None:
        self.rotate_circle(1)

    def rotate_right(self) -> None:
        self.rotate_circle(-1)

    def get_objects_id(self) -> tuple[int, ...]:
        return self.draw_field.find_all()

    def update_ids(self) -> None:
        ids = self.get_objects_id()
        self.user_point.set_id(ids[0])
        self.first_circle_id = ids[1]
        self.second_circle_id = ids[2]
        self.selected_circle_id = tk.IntVar(value=self.first_circle_id)
        self.rb_first_circle.configure(
            value=self.first_circle_id, variable=self.selected_circle_id
        )
        self.rb_second_circle.configure(
            value=self.second_circle_id, variable=self.selected_circle_id
        )

    def clear_field(self) -> None:
        self.circles.clear()
        self.draw_field.delete("all")
