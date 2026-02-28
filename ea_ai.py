from evolution import random_genome, evolve
from ai_agent import ai_reset, ai_step
from maze import find_tile, MOVES, valid

EA_POP = 4
POP_SIZE = 20


def coop_reset():
    start = find_tile("S")
    goal = find_tile("G")

    state = {
        "population": [random_genome() for _ in range(POP_SIZE)],
        "start": start,
        "goal": goal,
        "ai_pos": ai_reset(),
        "ai_done": False,
        "ea_positions": [start] * EA_POP,
        "finished": [False] * EA_POP,
        "ea_genomes_display": [[] for _ in range(EA_POP)],
        "genome": None,
        "genome_step": 0,
        "ai_params": {
            "epsilon": 0.3,
            "alpha": 0.5
        }
    }

    return state


def coop_step(state):
    goal = state["goal"]

    # --- AI moves first ---
    ai_score, ai_pos, ai_done = ai_step()
    state["ai_pos"] = ai_pos
    state["ai_done"] = ai_done

    # --- If genome finished, evolve a new one ---
    if state["genome"] is None or state["genome_step"] >= len(state["genome"]):
        state["population"], best = evolve(state["population"])
        ea_score, genome, best_pos = best

        state["genome"] = genome
        state["genome_step"] = 0
    else:
        ea_score = 999  # just placeholder distance

    genome = state["genome"]
    step = state["genome_step"]

    # --- EA executes next move ---
    if step < len(genome):
        move = genome[step]

        for i in range(EA_POP):
            if not state["finished"][i]:
                dr, dc = MOVES[move]
                r, c = state["ea_positions"][i]
                nr, nc = r + dr, c + dc

                if valid((nr, nc)):
                    state["ea_positions"][i] = (nr, nc)
                    state["ea_genomes_display"][i].append(move)

                if state["ea_positions"][i] == goal:
                    state["finished"][i] = True

        state["genome_step"] += 1

    # Winner detection
    ea_goal = any(pos == goal for pos in state["ea_positions"])
    ai_goal = ai_pos == goal or ai_done

    winner = None
    done = False

    if ea_goal or ai_goal:
        winner = "EA+AI"
        done = True
        # Snap BOTH to the goal for visualization
        state["ea_positions"] = [goal] * EA_POP
        state["ai_pos"] = goal

    return (
        state["ea_positions"],
        state["ai_pos"],
        ea_score,
        ai_score,
        state["ea_genomes_display"],
        state["ai_params"],
        winner,
        done
    )