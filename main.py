import numpy as np
from graphics import *
import random


factor = 10


def main():
    rand = generate_maze(150, 80, (1, 1), (149, 1))
    draw_maze(rand)
    path = []
    solve(rand, rand.start, path)
    print(path)
    rand.win.getMouse()  # Pause to view result
    rand.win.close()  # Close window when done


def generate_maze(length, width, start, end):
    maze = Maze(np.zeros((width + 1, length + 1), dtype=bool), start, end)
    maze.set_free((1, 1))
    walls = []
    maze.visit((1, 1))
    add_walls(maze, walls, (1, 1))

    while len(walls) > 0:
        # draw_maze(maze)
        wall_ind = int(random.randrange(0, len(walls)))
        wall = walls[wall_ind]
        diff = (wall[0][0] - wall[1][0], wall[0][1] - wall[1][1])
        passage = (wall[0][0] + diff[0], wall[0][1] + diff[1])
        if maze.in_matrix(passage):
            if maze.is_free(wall[1]) ^ (maze.is_free(passage)):
                maze.set_free(wall[0])
                maze.set_free(passage)
                add_walls(maze, walls, passage)
        walls.pop(wall_ind)

    maze.set_free((maze.width - 2, maze.length - 2))
    maze.reset_visited()
    return maze


def add_walls(maze, wall_list, point):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i != j and (i == 0 or j == 0):
                check = (point[0] + i, point[1] + j)
                if maze.in_matrix(check) and not maze.is_free(check):
                    wall_list.append(((point[0] + i, point[1] + j), point))


def draw_maze(maze):
    if maze.win is None:
        maze.win = GraphWin("Maze", factor * maze.width, factor * maze.length)
    for i in range(0, maze.width):
        for j in range(0, maze.length):
            r = Rectangle(Point(factor * i, factor * j), Point(factor * (i + 1), factor * (j + 1)))
            if maze.is_free((i, j)):
                r.setFill("white")
                r.setOutline("white")
            else:
                r.setFill("black")
                r.setOutline("black")
            r.draw(maze.win)
    # maze.win.getMouse()  # Pause to view result
    # maze.win.close()  # Close window when done


def draw_square(maze, pos, colour):
    if maze.win is None:
        maze.win = GraphWin("Maze", factor * maze.width, factor * maze.length)
    r = Rectangle(Point(factor * pos[0], factor * pos[1]), Point(factor * (pos[0] + 1) - 1, factor * (pos[1] + 1) - 1))
    r.setFill(colour)
    r.setOutline(colour)
    r.draw(maze.win)


def solve(maze, curr, path):
    maze.visit(curr)
    draw_square(maze, curr, "red")
    if curr == maze.end:
        path.insert(0, curr)
        return True
    else:
        for i in range(-1, 2):
            for j in range(-1, 2):
                check = (curr[0] + i, curr[1] + j)
                if check[0] == curr[0] or check[1] == curr[1]:
                    good = False
                    if maze.in_matrix(check) and maze.is_free(check) and not maze.is_visited(check):
                        good = solve(maze, check, path)
                    if good:
                        path.insert(0, curr)
                        return True
    draw_square(maze, curr, "blue")


class Maze:

    def __init__(self, matrix, start, end):
        self.matrix = matrix
        self.length = len(matrix)
        self.width = len(matrix[0])
        self.start = start
        self.end = end
        self.visited = np.zeros((len(matrix), len(matrix[0])), dtype=bool)
        self.win = None

    def is_free(self, pos):
        return self.matrix[pos[1]][pos[0]]

    def set_free(self, pos):
        self.matrix[pos[1]][pos[0]] = True

    def set_wall(self, pos):
        self.matrix[pos[1]][pos[0]] = False

    def is_visited(self, pos):
        return self.visited[pos[1]][pos[0]]

    def visit(self, pos):
        self.visited[pos[1]][pos[0]] = True

    def in_matrix(self, pos):
        return 0 <= pos[1] < self.length and 0 <= pos[0] < self.width

    def reset_visited(self):
        self.visited = np.zeros((len(self.matrix), len(self.matrix[0])), dtype=bool)


if __name__ == '__main__':
    main()
