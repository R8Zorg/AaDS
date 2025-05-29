import tkinter as tk
from tkinter import messagebox

from circle_canvas import CircleCanvas
from circle_manager import CircleManager
from color_buttons import ColorButtons


class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.geometry("924x730")
        self.root.title("My program")

        self.selected_circle_id = tk.IntVar()

        self.draw_field = tk.Canvas(
            background="#d2d8d7", borderwidth="2", relief="ridge"
        )
        self.draw_field.place(relx=0.044, rely=0.253, relheight=0.732, relwidth=0.896)
        self.draw_field.bind("<Button-1>", self.move_user_point)

        self.canvas = CircleCanvas(self.draw_field)
        self.manager = CircleManager(self.canvas)

        tk.Button(text="Загрузить данные", command=self.load_and_draw_circles).place(
            relx=0.042, rely=0.086, height=33, width=161
        )

        tk.Button(text="Проверка включения", command=self.check_circles).place(
            relx=0.043, rely=0.162, height=33, width=161
        )

        tk.Button(text="По часовой", command=self.rotate_left).place(
            relx=0.368, rely=0.204, height=33, width=131
        )

        tk.Button(text="Против часовой", command=self.rotate_right).place(
            relx=0.507, rely=0.204, height=33, width=131
        )

        ColorButtons(
            root=self.root,
            colors=["Red", "Blue", "Orange", "White", "Yellow", "Green"],
            command=self.paint_circle,
        )

        self.lb_check_entry = tk.Label(text="Вхождение не найдено", anchor="center")
        self.lb_check_entry.place(relx=0.043, rely=0.221, height=19, width=163)

        tk.Label(text="Выбрать цвет").place(
            relx=0.793, rely=0.054, height=18, width=145
        )
        tk.Label(text="Выбор круга").place(relx=0.37, rely=0.067, height=23, width=261)
        tk.Label(text="Введите угол поворота (гр.)").place(
            relx=0.368, rely=0.137, height=23, width=264
        )

        self.rb_first_circle = tk.Radiobutton(
            text="1й кр.", anchor="w", variable=self.selected_circle_id
        )
        self.rb_first_circle.place(
            relx=0.424, rely=0.094, relheight=0.034, relwidth=0.075
        )

        self.rb_second_circle = tk.Radiobutton(
            text="2й кр.", anchor="w", variable=self.selected_circle_id
        )
        self.rb_second_circle.place(
            relx=0.511, rely=0.094, relheight=0.034, relwidth=0.075
        )

        self.entry_turn_degree = tk.Entry()
        self.entry_turn_degree.place(relx=0.478, rely=0.164, height=25, relwidth=0.06)

    def load_and_draw_circles(self) -> None:
        try:
            self.manager.load_circles_from_file()
            self.selected_circle_id.set(self.manager.first_circle_id)  # type: ignore

            self.rb_first_circle.configure(value=self.manager.first_circle_id)
            self.rb_second_circle.configure(value=self.manager.second_circle_id)

        except Exception as e:
            messagebox.showerror("Ошибка загрузки", str(e))

    def check_circles(self) -> None:
        result = self.manager.check_inclusion()
        self.lb_check_entry.configure(
            text="Вхождение найдено" if result else "Вхождение не найдено",
            foreground="Green" if result else "Red",
        )

    def rotate_circle(self, sign: int) -> None:
        try:
            degree = int(self.entry_turn_degree.get()) * sign
        except ValueError:
            return

        user_point = self.canvas.user_point
        if not user_point:
            return

        center = (user_point.get_x(), user_point.get_y())
        self.manager.rotate_circle(self.selected_circle_id.get(), degree, center)

    def rotate_left(self) -> None:
        self.rotate_circle(1)

    def rotate_right(self) -> None:
        self.rotate_circle(-1)

    def move_user_point(self, event: tk.Event) -> None:  # type: ignore[type-arg]
        user_point = self.canvas.user_point
        if not user_point:
            return
        user_point.set_position(event.x, event.y)
        self.canvas.move_circle(user_point)

    def paint_circle(self, color: str) -> None:
        circle_id = self.selected_circle_id.get()
        if circle_id in self.canvas.circles:
            circle = self.canvas.circles[circle_id]
            circle.set_color(color)
            self.canvas.update_color(circle)
