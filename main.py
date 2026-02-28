# main.py
import time
from better_view import MazeViewer
from evolution import random_genome, evolve
from ai_agent import ai_reset, ai_step
from maze import maze, find_tile, MOVES, valid

EA_POP = 4
POP_SIZE = 20

# Initialize EA population
population = [random_genome() for _ in range(POP_SIZE)]
viewer = MazeViewer(maze)
generation = 0
goal = find_tile("G")

# Initialize EA positions once, clones stop at goal
ea_positions = [find_tile("S")] * EA_POP
finished = [False] * EA_POP

# Reset AI
ai_pos = ai_reset()
ai_done = False
ai_params = {"epsilon": 0.3, "alpha": 0.5}  # example parameters

# Store EA genome paths for display
ea_genomes_display = [[] for _ in range(EA_POP)]

goal_reached = False

# Wait for SPACE to start (good for recording)
waiting = True
while waiting:
    viewer.draw_start_screen()   # new function in viewer

    for event in viewer.pygame.event.get():
        if event.type == viewer.pygame.QUIT:
            viewer.pygame.quit()
            exit()
        if event.type == viewer.pygame.KEYDOWN and event.key == viewer.pygame.K_SPACE:
            waiting = False

while not goal_reached:
    generation += 1

    # Evolve EA population
    population, best = evolve(population)
    score, genome, best_pos = best

    # Copy best genome to all EA clones
    ea_genomes = [list(genome) for _ in range(EA_POP)]
    ea_genomes_display = [[] for _ in range(EA_POP)]  # reset displayed path

    # Animate genome step by step
    for step in range(len(genome)):
        for i in range(EA_POP):
            if not finished[i]:
                move = genome[step]
                dr, dc = MOVES[move]
                r, c = ea_positions[i]
                nr, nc = r + dr, c + dc
                if valid((nr, nc)):
                    ea_positions[i] = (nr, nc)
                    ea_genomes_display[i].append(move)
                if ea_positions[i] == goal:
                    finished[i] = True  # stop clone at goal

        # AI moves ONE step (persistent)
        ai_score, ai_pos, ai_done = ai_step()

        # Check for winner
        ea_goal_reached = any(pos == goal for pos in ea_positions)
        ai_goal_reached = ai_pos == goal or ai_done

        if ea_goal_reached:
            winner = "EA"
            goal_reached = True
        elif ai_goal_reached:
            winner = "AI"
            goal_reached = True
        else:
            winner = None

        # Draw arcade battle
        viewer.draw_battle(
            ea_positions,
            ai_pos,
            generation,
            score,
            ai_score,
            ea_genomes=ea_genomes_display,
            ai_params=ai_params,
            winner=winner
        )

        time.sleep(0.08)  # animation speed

# Keep Pygame window open after match
running = True
while running:
    for event in viewer.pygame.event.get():
        if event.type == viewer.pygame.QUIT:
            running = False