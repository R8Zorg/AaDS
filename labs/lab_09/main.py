import math
import tkinter as tk
from tkinter import messagebox


class TickTacToe:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.GRID_SIZE = 3
        self.header = tk.Frame(root, height=100, bg="lightgray")
        self.header.pack(fill="x", side="top")
        self.current_player = "X"

        tk.Button(
            self.header, text="Перезапустить", font=("Arial", 14), command=self.reset
        ).pack(fill="both", padx=20)

        self.game_field = tk.Frame(root, width=500, height=500)
        self.game_field.pack(fill="both", expand=True)

        self.buttons = [
            [None for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)
        ]

        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                btn = tk.Button(
                    self.game_field,
                    text="",
                    font=("Arial", 32),
                    width=3,
                    height=1,
                    command=lambda row=row, col=col: self.on_click(row, col),
                )
                btn.grid(row=row, column=col, sticky="nsew")
                self.buttons[row][col] = btn

        for i in range(self.GRID_SIZE):
            self.game_field.grid_rowconfigure(i, weight=1)
            self.game_field.grid_columnconfigure(i, weight=1)

    def reset(self):
        self.current_player = "X"
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                self.buttons[row][col].config(text="", state="normal")

    def on_click(self, row, col):
        button = self.buttons[row][col]
        if button["text"] == "":
            button["text"] = "X"
            if self.check_winner("X"):
                self.end_game("Вы победили!")
                return
            if self.is_draw():
                self.end_game("Ничья!")
                return
            self.bot_move()

    def bot_move(self):
        best_score = -math.inf
        move = None
        for row in range(self.GRID_SIZE):
            for column in range(self.GRID_SIZE):
                if self.buttons[row][column]["text"] == "":
                    self.buttons[row][column]["text"] = "O"
                    score = self.minimax(False)
                    self.buttons[row][column]["text"] = ""
                    if score > best_score:
                        best_score = score
                        move = (row, column)
        if move:
            self.buttons[move[0]][move[1]]["text"] = "O"
        if self.check_winner("O"):
            self.end_game("Вы проиграли")
            return
        if self.is_draw():
            self.end_game("Ничья!")

    def minimax(self, is_maximizing):
        if self.check_winner("O"):
            return 1
        if self.check_winner("X"):
            return -1
        if self.is_draw():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for row in range(self.GRID_SIZE):
                for col in range(self.GRID_SIZE):
                    if self.buttons[row][col]["text"] == "":
                        self.buttons[row][col]["text"] = "O"
                        score = self.minimax(False)
                        self.buttons[row][col]["text"] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for row in range(self.GRID_SIZE):
                for col in range(self.GRID_SIZE):
                    if self.buttons[row][col]["text"] == "":
                        self.buttons[row][col]["text"] = "X"
                        score = self.minimax(True)
                        self.buttons[row][col]["text"] = ""
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        for row in range(self.GRID_SIZE):
            if all(
                self.buttons[row][column]["text"] == player
                for column in range(self.GRID_SIZE)
            ):
                return True
        for column in range(self.GRID_SIZE):
            if all(
                self.buttons[row][column]["text"] == player
                for row in range(self.GRID_SIZE)
            ):
                return True
        if all(
            self.buttons[i][i]["text"] == player  # текст-заглушка для форматирования
            for i in range(self.GRID_SIZE)
        ):
            return True
        if all(
            self.buttons[i][self.GRID_SIZE - 1 - i]["text"] == player
            for i in range(self.GRID_SIZE)
        ):
            return True
        return False

    def is_draw(self):
        return all(
            self.buttons[row][column]["text"] != ""
            for row in range(self.GRID_SIZE)
            for column in range(self.GRID_SIZE)
        )

    def end_game(self, message):
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                self.buttons[row][col].config(state="disabled")
        messagebox.showinfo("Игра окончена", message)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Крестики-нолики")
    root.geometry("650x600")
    root.resizable(0, 0)
    game = TickTacToe(root)
    root.mainloop()
