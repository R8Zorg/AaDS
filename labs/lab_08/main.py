import tkinter as tk

from main_window import MainWindow


def print_hello():
    print("Hello!")


def main():
    root = tk.Tk()
    window = MainWindow(root)
    window.btn_load_data.configure(command=print_hello)
    root.mainloop()


if __name__ == "__main__":
    main()
