# maze.py
START = "S"
GOAL = "G"
WALL = "#"
EMPTY = "."

maze = [
    ["S", ".", ".", ".", ".", ".", ".", "."],
    [".", "#", "#", ".", "#", "#", "#", "."],
    [".", "#", ".", ".", ".", ".", "#", "."],
    [".", "#", ".", "#", "#", ".", "#", "."],
    [".", ".", ".", "#", ".", ".", ".", "."],
    [".", "#", "#", ".", "#", "#", "#", "."],
    [".", ".", ".", ".", ".", ".", "#", "G"]
]

MOVES = [
    (-1, 0),  # Up
    (1, 0),   # Down
    (0, -1),  # Left
    (0, 1),   # Right
]

def find_tile(tile):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == tile:
                return (r, c)

def valid(pos):
    r, c = pos
    if r < 0 or c < 0 or r >= len(maze) or c >= len(maze[0]):
        return False
    return maze[r][c] != WALL