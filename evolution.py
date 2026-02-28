# evolution.py
import random
from maze import MOVES, valid, find_tile

GENOME_LENGTH = 25
POP_SIZE = 30
MUTATION_RATE = 0.1

start = find_tile("S")
goal = find_tile("G")

def random_genome():
    return [random.randint(0, 3) for _ in range(GENOME_LENGTH)]

def simulate(genome):
    pos = start
    for move in genome:
        dr, dc = MOVES[move]
        nr, nc = pos[0] + dr, pos[1] + dc
        if valid((nr, nc)):
            pos = (nr, nc)
        if pos == goal:
            break
    dist = abs(goal[0]-pos[0]) + abs(goal[1]-pos[1])
    return dist, pos

def mutate(genome):
    return [random.randint(0, 3) if random.random() < MUTATION_RATE else m for m in genome]

def evolve(population):
    scored = []
    for genome in population:
        dist, pos = simulate(genome)
        scored.append((dist, genome, pos))

    scored.sort(key=lambda x: x[0])
    best = scored[0]

    # Take top 25% as survivors
    survivors = [g for _, g, _ in scored[:POP_SIZE//4]]

    new_pop = survivors[:]
    while len(new_pop) < POP_SIZE:
        parent = random.choice(survivors)
        new_pop.append(mutate(parent))

    return new_pop, best