import numpy as np
from graphics import *
import random


square_size = 10
delays_on = False


def main():
    random.seed()
    rand = generate_maze(100, 60, (1, 1), (99, 59))
    path = []
    solve(rand, rand.start, path)
    print(path)
    rand.win.getMouse()  # Pause to view result
    rand.win.close()  # Close window when done


def generate_maze(length, width, start, end):
    maze = Maze(np.zeros((width + 1, length + 1), dtype=bool), start, end)
    draw_blank_maze(maze)
    maze.set_free((1, 1))
    draw_square(maze,(1,1),"white")
    walls = []
    add_walls(maze, walls, (1, 1))
    last = None

    while len(walls) > 0:
        if delays_on:
            time.sleep(0.003)
        wall_ind = int(random.randrange(0, len(walls)))
        wall = walls[wall_ind]
        diff = (wall[0][0] - wall[1][0], wall[0][1] - wall[1][1])
        passage = (wall[0][0] + diff[0], wall[0][1] + diff[1])
        if maze.in_matrix(passage):
            if maze.is_free(wall[1]) ^ (maze.is_free(passage)):
                if last is not None:
                    draw_square(maze, last, "white")
                maze.set_free(wall[0])
                draw_square(maze, wall[0], "white")
                maze.set_free(passage)
                draw_square(maze, passage, "red")
                add_walls(maze, walls, passage)
                last = passage
        walls.pop(wall_ind)
    draw_square(maze, last, "white")
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
        maze.win = GraphWin("Maze", square_size * maze.width, square_size * maze.length)
    for i in range(0, maze.width):
        for j in range(0, maze.length):
            r = Rectangle(Point(square_size * i, square_size * j), Point(square_size * (i + 1), square_size * (j + 1)))
            if maze.is_free((i, j)):
                r.setFill("white")
                r.setOutline("white")
            else:
                r.setFill("black")
                r.setOutline("black")
            r.draw(maze.win)


def draw_blank_maze(maze):
    if maze.win is None:
        maze.win = GraphWin("Maze", square_size * maze.width, square_size * maze.length)
    r = Rectangle(Point(0,0), Point(square_size * maze.width, square_size * maze.length))
    r.setFill("black")
    r.setOutline("black")
    r.draw(maze.win)


def draw_square(maze, pos, colour):
    if maze.win is None:
        maze.win = GraphWin("Maze", square_size * maze.width, square_size * maze.length)
    r = Rectangle(Point(square_size * pos[0], square_size * pos[1]), Point(square_size * (pos[0] + 1) - 1, square_size * (pos[1] + 1) - 1))
    r.setFill(colour)
    r.setOutline(colour)
    r.draw(maze.win)


def solve(maze, curr, path):
    if delays_on:
        time.sleep(0.03)
    maze.visit(curr)
    draw_square(maze, curr, "red")
    if curr == maze.end:
        path.insert(0, curr)
        return True
    else:
        index_offset = [(-1,0), (0,-1), (1,0), (0,1)]
        random.shuffle(index_offset)
        for offset in index_offset:
            check = (curr[0] + offset[0], curr[1] + offset[1])
            good = False
            if maze.in_matrix(check) and maze.is_free(check) and not maze.is_visited(check):
                good = solve(maze, check, path)
            if good:
                path.insert(0, curr)
                return True
    if delays_on:
        time.sleep(0.03)
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
