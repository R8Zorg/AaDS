import random
import tkinter as tk

PLAYER = 2


def load_maze(filename):
    maze = []
    with open(filename, "r") as file:
        for line in file:
            maze.append([int(x) for x in line.strip()])
    return maze


def find_player(maze):
    for y, row in enumerate(maze):
        for x, value in enumerate(row):
            if value == PLAYER:
                return x, y
    return None


def find_accessible_exit(maze, start: tuple[int, int]):
    exits = []
    width, height = len(maze[0]), len(maze)

    exit_candidates: list[tuple[int, int]] = []
    for x in range(width):
        if maze[0][x] == 0:
            exit_candidates.append((x, 0))
        if maze[height - 1][x] == 0:
            exit_candidates.append((x, height - 1))
    for y in range(height):
        if maze[y][0] == 0:
            exit_candidates.append((0, y))
        if maze[y][width - 1] == 0:
            exit_candidates.append((width - 1, y))

    for exit_pos in exit_candidates:
        path = dfs(maze, start, exit_pos)
        if path:
            exits.append(exit_pos)

    return exits


def dfs(maze, start: tuple[int, int], exit: tuple[int, int]) -> list[tuple[int, int]]:
    stack = [(start, [start])]
    visited = set()

    while stack:
        (x, y), path = stack.pop()
        if (x, y) == exit:
            return path
        if (x, y) in visited:
            continue
        visited.add((x, y))
        left, right, up, down = (-1, 0), (1, 0), (0, -1), (0, 1)
        for x_move, y_move in [left, right, up, down]:
            next_x, next_y = x + x_move, y + y_move
            if (
                0 <= next_y < len(maze)
                and 0 <= next_x < len(maze[0])
                and maze[next_y][next_x] != 1
            ):
                stack.append(((next_x, next_y), path + [(next_x, next_y)]))
    return []


def animate_path(canvas, path: list[tuple[int, int]], size: int) -> None:
    for x, y in path[1:]:
        canvas.after(150)
        canvas.move(
            player_rect,
            (x - canvas.coords(player_rect)[0] // size) * size,
            (y - canvas.coords(player_rect)[1] // size) * size,
        )
        canvas.update()


def draw_maze(canvas, maze, size: int):
    for y, row in enumerate(maze):
        for x, val in enumerate(row):
            color = "white"
            if val == 1:
                color = "black"
            elif val == 2:
                color = "blue"
            elif val == 0:
                color = "white"
            canvas.create_rectangle(
                x * size,
                y * size,
                (x + 1) * size,
                (y + 1) * size,
                fill=color,
                outline="gray",
            )


maze = load_maze("maze.txt")
player_position = find_player(maze)
accessible_exits = find_accessible_exit(maze, player_position)
if not accessible_exits:
    raise ValueError("Нет доступных выходов!")

chosen_exit = random.choice(accessible_exits)
path = dfs(maze, player_position, chosen_exit)
root = tk.Tk()
size = 50
canvas = tk.Canvas(root, width=len(maze[0]) * size, height=len(maze) * size)
canvas.pack()
draw_maze(canvas, maze, size)

x, y = player_position
player_rect = canvas.create_rectangle(
    x * size, y * size, (x + 1) * size, (y + 1) * size, fill="red"
)

root.after(500, lambda: animate_path(canvas, path, size))
root.mainloop()
