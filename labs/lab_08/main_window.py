import tkinter as tk

from shapes.circle import Circle


class MainWindow:
    def __init__(self, root=None):
        root.geometry("924x730")
        # root.minsize(1, 1)
        # root.maxsize(2545, 1410)
        root.resizable(1, 1)
        root.title("My program")

        self.root = root
        self.circles = []
        self.circle_ids = []

        self.btn_load_data = tk.Button(
            text="Загрузить данные", command=self.draw_circles
        )
        self.btn_load_data.place(relx=0.042, rely=0.086, height=33, width=161)

        self.btn_color_red = tk.Button(
            text="", background="Red", activebackground="Red"
        )
        self.btn_color_red.place(relx=0.797, rely=0.084, height=33, width=71)

        self.btn_color_blue = tk.Button(
            text="", background="Blue", activebackground="Blue"
        )
        self.btn_color_blue.place(relx=0.865, rely=0.084, height=33, width=71)

        self.btn_color_black = tk.Button(
            text="", background="Black", activebackground="Black"
        )
        self.btn_color_black.place(relx=0.797, rely=0.125, height=33, width=71)

        self.btn_color_white = tk.Button(
            text="", background="White", activebackground="White"
        )
        self.btn_color_white.place(relx=0.865, rely=0.125, height=33, width=71)

        self.btn_color_yellow = tk.Button(
            text="", background="Yellow", activebackground="Yellow"
        )
        self.btn_color_yellow.place(relx=0.797, rely=0.164, height=33, width=71)

        self.btn_color_green = tk.Button(
            text="", background="Green", activebackground="Green"
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
        self.draw_field.place(relx=0.044, rely=0.253, relheight=0.732, relwidth=0.896)

        self.lb_check_entry = tk.Label(text="Проверка включения", anchor="w")
        self.lb_check_entry.place(relx=0.043, rely=0.221, height=19, width=221)

        self.lb_choose_color = tk.Label(text="Выбрать цвет")
        self.lb_choose_color.place(relx=0.802, rely=0.044, height=18, width=124)

        self.btn_turn_left = tk.Button(text="Повернуть влево")
        self.btn_turn_left.place(relx=0.367, rely=0.163, height=33, width=131)

        self.btn_turn_right = tk.Button(text="Повернуть вправо")
        self.btn_turn_right.place(relx=0.508, rely=0.163, height=33, width=131)

    def check_circles(self):
        if len(self.circles) != 2:
            tk.messagebox.showerror("Ошибка проверки", "Кругов на поле должно быть 2")
            return
        is_include = Circle.contains(self.circles[0], self.circles[1])
        if is_include:
            self.lb_check_entry.configure(text="Найдено вхождение кругов", foreground="Green")
        else:
            self.lb_check_entry.configure(text="Вхождение не найдено", foreground="Red")

    def load_data(self):
        circles_num = 2
        self.circles = []
        with open("input.txt", "r") as f:
            lines = f.readlines()[:circles_num]
            for line in lines:
                try:
                    x, y, r, color = line.split()
                    self.circles.append(Circle(int(x), int(y), int(r), color))
                except ValueError:
                    tk.messagebox.showerror(
                        "Ошибка чтения данных", "Ожидаемый ввод: int int int str"
                    )
                    return

    def get_coordinates(self, circle: "Circle") -> tuple[int, int, int, int]:
        x1 = circle.get_x() - circle.get_r()
        y1 = circle.get_y() - circle.get_r()
        x2 = circle.get_x() + circle.get_r()
        y2 = circle.get_y() + circle.get_r()
        return x1, y1, x2, y2

    def draw_circles(self):
        self.load_data()
        for circle in self.circles:
            cid = self.draw_field.create_oval(
                self.get_coordinates(circle), outline=circle.get_color()
            )
            self.circle_ids.append(cid)
