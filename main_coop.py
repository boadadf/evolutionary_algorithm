import time
import sys
from better_view import MazeViewer
from maze import maze
from ea_ai import coop_reset, coop_step

EA_POP = 4

viewer = MazeViewer(maze)

# Reset cooperative system
state = coop_reset()

goal_reached = False
generation = 0

# Wait for SPACE before starting (good for recording)
waiting = True
while waiting:
    viewer.draw_start_screen()

    for event in viewer.pygame.event.get():
        if event.type == viewer.pygame.QUIT:
            viewer.pygame.quit()
            exit()
        if event.type == viewer.pygame.KEYDOWN and event.key == viewer.pygame.K_SPACE:
            waiting = False

# Main loop
while not goal_reached:
    generation += 1

    # Run one cooperative step
    (
        ea_positions,
        ai_pos,
        ea_score,
        ai_score,
        ea_genomes_display,
        ai_params,
        winner,
        done
    ) = coop_step(state)

    viewer.draw_battle(
        ea_positions,
        ai_pos,
        generation,
        ea_score,
        ai_score,
        ea_genomes=ea_genomes_display,
        ai_params=ai_params,
        winner=winner
    )

    time.sleep(0.08)

    if done:
        goal_reached = True

# Keep window open
running = True
while running:
    for event in viewer.pygame.event.get():
        if event.type == viewer.pygame.QUIT:
            running = False