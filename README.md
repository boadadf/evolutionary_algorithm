# EA vs AI – Arcade Maze Battle

Today I want to share a fun and educational demo combining **Evolutionary Algorithms (EA)** and simple **AI (Q-learning)** in a maze challenge.

This project showcases three rounds:

- **EA vs AI – Round 1:** EA (genetic algorithm) explores the maze; AI struggles.
- **AI vs EA – Round 2:** AI (reinforcement learning) adapts and wins; EA can get stuck if the path is tricky.
- **Cooperation – Round 3:** EA + AI work together to find the goal faster.

The goal is to visualize algorithmic decision-making in a fun **arcade-style** way with **Pygame**.

---

## Features

- Pygame visualization with Street-Fighter style background
- EA clones executing evolving genomes in parallel
- AI moving step by step, learning via Q-learning
- Round 3 cooperation mode: EA and AI win together
- Start screen: press **SPACE** to start the match
- Step-by-step visualization of EA genomes and AI parameters

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/ea-vs-ai.git
cd ea-vs-ai
```

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

Install requirements:

```bash
pip install pygame
```

Make sure `background.jpg` is in the same folder as `better_view.py`.

---

## How to Run

### Standard Battle Mode (Rounds 1–2)

```bash
python main.py
```

### Cooperation Mode (Round 3)

```bash
python main_coop.py
```

---

## Controls

- Press **SPACE** to start each round.
- The simulation runs automatically.
- EA and AI move step by step.
- The winner is displayed arcade-style on the screen.

---

## How It Works

### Evolutionary Algorithm (EA)

- Maintains a population of candidate solutions (genomes)

Each generation:

- Evaluate fitness – how close each genome gets to the goal
- Select parents – choose the best genomes
- Reproduce – crossover and mutate to create the next generation
- Iterates until a solution reaches the goal

Example pseudo-code:

```text
do generation = 1, max_gen
    call evaluate_fitness(population)
    call select_parents(population, fitness)
    call reproduce(parents, population_new)
    population = population_new
end do
```

### Q-Learning AI

- Moves through the maze, learning best actions from rewards
- Updates its policy after each step
- Works in tandem with EA in Round 3

---

## License

MIT License – feel free to reuse and modify for educational purposes.
