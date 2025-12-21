import tkinter as tk

from battleship_gui import BattleshipGUI


def main():
    root = tk.Tk()
    app = BattleshipGUI(root)
    app.start()
    root.mainloop()


if __name__ == "__main__":
    main()
