# ai_agent.py
import random
from maze import MOVES, valid, find_tile, maze

ALPHA = 0.3
GAMMA = 0.9
EPSILON = 0.2

start = find_tile("S")
goal = find_tile("G")

Q = {}
ai_state = start  # persistent state

def get_q(state):
    if state not in Q:
        Q[state] = [0.0, 0.0, 0.0, 0.0]
    return Q[state]

def choose_action(state):
    if random.random() < EPSILON:
        return random.randint(0, 3)
    q = get_q(state)
    return max(range(4), key=lambda a: q[a])

def step(state, action):
    r, c = state
    dr, dc = MOVES[action]
    nr, nc = r + dr, c + dc
    if valid((nr, nc)):
        new_state = (nr, nc)
    else:
        new_state = state

    reward = -1
    done = False
    if new_state == goal:
        reward = 100
        done = True
    return new_state, reward, done

def ai_reset():
    global ai_state
    ai_state = start
    return ai_state

def ai_step():
    global ai_state
    action = choose_action(ai_state)
    new_state, reward, done = step(ai_state, action)

    q = get_q(ai_state)
    next_q = get_q(new_state)
    q[action] = q[action] + ALPHA * (reward + GAMMA*max(next_q) - q[action])

    ai_state = new_state
    dist = abs(goal[0]-ai_state[0]) + abs(goal[1]-ai_state[1])
    return dist, ai_state, done