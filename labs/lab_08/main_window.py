import math
import tkinter as tk
from functools import partial
from typing import Literal

from circle import Circle


# TODO: исправить circle_ids на circles[id: Circle]
class MainWindow:
    def __init__(self, root=None):
        root.geometry("924x730")
        # root.minsize(1, 1)
        # root.maxsize(2545, 1410)
        root.resizable(1, 1)
        root.title("My program")

        self.root = root
        self.circles = {}
        self.selected_circle_number = tk.IntVar(value=0)
        self.selected_circle: Circle = None

        self.user_point: Circle = Circle(-10, -10, 5, "Black")

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

        self.btn_color_black = tk.Button(
            text="",
            background="Black",
            activebackground="Black",
            command=partial(self.paint_circle, "Black"),
        )
        self.btn_color_black.place(relx=0.797, rely=0.125, height=33, width=71)

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
        self.draw_field.bind("<Button-1>", self.draw_user_point)
        self.draw_field.place(relx=0.044, rely=0.253, relheight=0.732, relwidth=0.896)

        self.draw_field.create_oval(
            self.get_coordinates(
                self.user_point.get_x(), self.user_point.get_y, self.user_point.get_r()
            ),
            fill=self.user_point.get_color(),
        )

        self.lb_check_entry = tk.Label(text="Вхождение не найдено", anchor="center")
        self.lb_check_entry.place(relx=0.043, rely=0.221, height=19, width=163)

        self.lb_choose_color = tk.Label(text="Выбрать цвет")
        self.lb_choose_color.place(relx=0.793, rely=0.054, height=18, width=145)

        self.btn_turn_left = tk.Button(text="Повернуть влево", command=self.rotate_left)
        self.btn_turn_left.place(relx=0.368, rely=0.204, height=33, width=131)

        self.btn_turn_right = tk.Button(
            text="Повернуть вправо", command=self.rotate_right
        )
        self.btn_turn_right.place(relx=0.507, rely=0.204, height=33, width=131)

        self.entry_turn_degree = tk.Entry()
        self.entry_turn_degree.place(relx=0.478, rely=0.164, height=25, relwidth=0.06)

        self.lb_enter_turn_degree = tk.Label(text="Введите угол поворота (гр.)")
        self.lb_enter_turn_degree.place(relx=0.368, rely=0.137, height=23, width=264)

        self.rb_first_circle = tk.Radiobutton(
            text="1й кр.",
            anchor="w",
            value=0,
            variable=self.selected_circle_number,
        )
        self.rb_first_circle.place(
            relx=0.424, rely=0.094, relheight=0.034, relwidth=0.075
        )
        self.rb_second_circle = tk.Radiobutton(
            text="2й кр.",
            anchor="w",
            value=1,
            variable=self.selected_circle_number,
        )
        self.rb_second_circle.place(
            relx=0.511, rely=0.094, relheight=0.034, relwidth=0.075
        )

        self.lb_choose_circle = tk.Label(text="Выбор круга")
        self.lb_choose_circle.place(relx=0.37, rely=0.067, height=23, width=261)

    def check_circles(self):
        if len(self.circles) != 2:
            tk.messagebox.showerror("Ошибка проверки", "Кругов на поле должно быть 2")
            return
        is_include = Circle.contains(self.circles[0], self.circles[1])
        if is_include:
            self.lb_check_entry.configure(text="Вхождение найдено", foreground="Green")
        else:
            self.lb_check_entry.configure(text="Вхождение не найдено", foreground="Red")

    def load_and_draw_circles(self):
        circles_num = 2
        self.circles = []
        with open("input.txt", "r") as f:
            lines = f.readlines()[:circles_num]
            for line in lines:
                try:
                    x, y, r, color = line.split()
                    circle_id = self.draw_field.create_oval(
                        self.get_coordinates(x, y, r), color
                    )
                    self.circles[circle_id] = Circle(int(x), int(y), int(r), color)
                except ValueError:
                    tk.messagebox.showerror(
                        "Ошибка чтения данных", "Ожидаемый ввод: int int int str"
                    )
                    return
        self.draw_circles()

    def get_coordinates(self, x, y, r) -> tuple[int, int, int, int]:
        x1 = x - r
        y1 = y - r
        x2 = x + r
        y2 = y + r
        return x1, y1, x2, y2

    def draw_circles(self):
        for circle in self.circles:
            cid = self.draw_field.create_oval(
                self.get_coordinates(circle.get_x(), circle.get_y(), circle.get_r()),
                outline=circle.get_color(),
                width=5,
            )
            self.circle_ids.append(cid)

    def paint_circle(self, color: str):
        self.circles[self.selected_circle_number.get()].set_color(color)
        self.draw_field.itemconfigure(
            self.circle_ids[self.selected_circle_number.get()], outline=color
        )

    def move_to(self, x, y, circle):
        circle.set_position(x, y)
        r = circle.get_r()
        self.draw_field.coords(
            self.circle_ids[self.selected_circle_number.get()],
            x - r,
            y - r,
            x + r,
            y + r,
        )

    def draw_user_point(self, event):
        self.user_point.set_position(event.x, event.y)
        self.draw_field.coords()

    def rotate_circle(self, sign: Literal[1, -1]):
        self.selected_circle: Circle = self.circles[self.selected_circle_number.get()]
        rotation_center = [250, 250]  # TODO: сделать на клик мыши, нарисовать точку
        if self.entry_turn_degree.get() == "":
            return
        degree = int(self.entry_turn_degree.get()) * sign
        cx = rotation_center[0]
        cy = rotation_center[1]

        angle_rad = math.radians(degree)
        dx = self.selected_circle.get_x() - cx
        dy = self.selected_circle.get_y() - cy
        new_x = cx + math.cos(angle_rad) * dx - math.sin(angle_rad) * dy
        new_y = cy + math.sin(angle_rad) * dx + math.cos(angle_rad) * dy
        self.move_to(new_x, new_y, self.selected_circle)

    def rotate_left(self):
        self.rotate_circle(1)

    def rotate_right(self):
        self.rotate_circle(-1)
