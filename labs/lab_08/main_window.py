import tkinter as tk

from shapes.circle import Circle


class MainWindow:
    def __init__(self, root=None):
        root.geometry("1100x1000")
        # root.minsize(1, 1)
        # root.maxsize(2545, 1410)
        root.resizable(1, 1)
        root.title("My program")

        self.root = root
        self.circles = []
        self.circle_ids = []

        self.btn_load_data = tk.Button(text="Загрузить данные", command=self.load_data)
        self.btn_load_data.place(relx=0.064, rely=0.055, height=33, width=130)

        self.btn_color_red = tk.Button(text="", background="Red")
        self.btn_color_red.place(relx=0.718, rely=0.055, height=33, width=71)

        self.btn_color_blue = tk.Button(text="", background="Blue")
        self.btn_color_blue.place(relx=0.782, rely=0.055, height=33, width=71)

        self.btn_color_gren = tk.Button(text="", background="Green")
        self.btn_color_gren.place(relx=0.718, rely=0.088, height=33, width=71)

        self.btn_color_yellow = tk.Button(text="", background="Yellow")
        self.btn_color_yellow.place(relx=0.782, rely=0.088, height=33, width=71)

        self.btn_color_black = tk.Button(text="", background="Black")
        self.btn_color_black.place(relx=0.718, rely=0.121, height=33, width=71)

        self.btn_color_white = tk.Button(text="", background="White")
        self.btn_color_white.place(relx=0.782, rely=0.121, height=33, width=71)

        self.btn_check_entry = tk.Button(
            text="Проверка включения", activebackground="#d9d9d9"
        )
        self.btn_check_entry.place(relx=0.064, rely=0.121, height=33, width=150)

        self.draw_field = tk.Canvas(
            background="#d2d8d7",
            borderwidth="2",
            relief="ridge",
            selectbackground="#d9d9d5",
        )
        self.draw_field.place(relx=0.046, rely=0.254, relheight=0.731, relwidth=0.885)

        self.label1 = tk.Label(text="Проверка включения", anchor="w")
        self.label1.place(relx=0.064, rely=0.221, height=23, width=249)

        self.label2 = tk.Label(text="Выбрать цвет")
        self.label2.place(relx=0.727, rely=0.022, height=23, width=130)

    def load_data(self):
        with open("input.txt", "r") as f:
            for line in f:
                x, y, r, color = map(float, line.strip().split())
                self.circles.append(Circle(x, y, r, color))

    def draw_circles(self):
        for circle in self.circles:
            x0 = circle.get_x() - circle.get_r()
            y0 = circle.get_y() - circle.get_r()
            x1 = circle.get_x() + circle.get_r()
            y1 = circle.get_y() + circle.get_r()
            cid = self.draw_field.create_oval(x0, y0, x1, y1, outline="blue")
            self.circle_ids.append(cid)
