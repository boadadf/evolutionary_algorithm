# better_view.py
import pygame

CELL = 40
PADDING = 20
EA_COUNT = 4

COLORS = {
    "bg": (25, 25, 35),
    "wall": (70, 70, 90),
    "path": (220, 220, 220),
    "start": (120, 200, 255),
    "goal": (255, 200, 120),
    "ea": (120, 255, 120),
    "ai": (255, 120, 120),
    "text": (255, 255, 255),
    "highlight": (255, 255, 0)
}

# Map integer moves to letters for display
MOVES_LETTERS = ['U','D','L','R']

class MazeViewer:
    def __init__(self, maze):
        self.pygame = pygame
        pygame.init()
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])

        width = EA_COUNT * (self.cols * CELL + PADDING) + 500
        height = 900

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("EA vs AI Arcade Battle")

        self.bg_image = pygame.image.load("background.jpg").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (width, height))

        # Fonts
        self.font = pygame.font.SysFont("consolas", 28, bold=True)
        self.small = pygame.font.SysFont("consolas", 22, bold=True)
        self.big = pygame.font.SysFont("consolas", 50, bold=True)

    def draw_start_screen(self):
        self.screen.blit(self.bg_image, (0, 0))

        title = self.big.render("EA vs AI", True, (255, 255, 255))
        subtitle = self.font.render("Press SPACE to start the match", True, (255, 255, 255))

        rect = title.get_rect(center=(self.screen.get_width()//2, 200))
        rect2 = subtitle.get_rect(center=(self.screen.get_width()//2, 260))

        self.screen.blit(title, rect)
        self.screen.blit(subtitle, rect2)

        pygame.display.flip()

    def draw_maze(self, offset_x, offset_y, agent_pos, agent_type):
        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(offset_x + c*CELL, offset_y + r*CELL, CELL, CELL)
                tile = self.maze[r][c]
                if tile == "#":
                    color = COLORS["wall"]
                elif tile == "S":
                    color = COLORS["start"]
                elif tile == "G":
                    color = COLORS["goal"]
                else:
                    color = COLORS["path"]
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (50,50,60), rect,1)

        if agent_pos:
            r, c = agent_pos
            center = (offset_x + c*CELL + CELL//2, offset_y + r*CELL + CELL//2)
            color = COLORS["ea"] if agent_type=="EA" else COLORS["ai"]
            pygame.draw.circle(self.screen, color, center, CELL//3)

    def draw_battle(self, ea_positions, ai_position, generation, ea_score, ai_score,
                    ea_genomes=None, ai_params=None, winner=None):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Draw background first
        self.screen.blit(self.bg_image, (0,0))

        offset_y = 100

        # Player labels
        title_ea = self.big.render("PLAYER EA", True, COLORS["text"])
        title_ai = self.big.render("PLAYER AI", True, COLORS["text"])
        self.screen.blit(title_ea, (PADDING, 10))
        self.screen.blit(title_ai, (self.cols*CELL*EA_COUNT + PADDING + 100, 10))

        # Draw mazes
        for i, pos in enumerate(ea_positions):
            offset_x = PADDING + i*(self.cols*CELL + PADDING)
            self.draw_maze(offset_x, offset_y, pos, "EA")

        ai_x = EA_COUNT*(self.cols*CELL+PADDING)+150
        self.draw_maze(ai_x, offset_y, ai_position, "AI")

        # Distance texts
        ea_text = self.font.render(f"DISTANCE: {ea_score}", True, COLORS["ea"])
        ai_text = self.font.render(f"DISTANCE: {ai_score}", True, COLORS["ai"])
        self.screen.blit(ea_text, (PADDING, offset_y + self.rows*CELL + 20))
        self.screen.blit(ai_text, (ai_x, offset_y + self.rows*CELL + 20))

        # Draw EA genome paths below each maze
        if ea_genomes:
            for i, genome in enumerate(ea_genomes):
                offset_x = PADDING + i*(self.cols*CELL + PADDING)
                for j, move in enumerate(genome):
                    letter = MOVES_LETTERS[move] if isinstance(move,int) else str(move)
                    genome_text = self.small.render(letter, True, COLORS["text"])
                    self.screen.blit(genome_text, (offset_x, offset_y + self.rows*CELL + 60 + j*20))

        # Draw AI parameters
        if ai_params:
            eps_text = self.small.render(f"EPSILON: {ai_params.get('epsilon', '-')}", True, COLORS["text"])
            lr_text = self.small.render(f"ALPHA: {ai_params.get('alpha', '-')}", True, COLORS["text"])
            self.screen.blit(eps_text, (ai_x, offset_y + self.rows*CELL + 60))
            self.screen.blit(lr_text, (ai_x, offset_y + self.rows*CELL + 90))

        # Iteration
        iter_text = self.small.render(f"Iteration: {generation}", True, COLORS["text"])
        self.screen.blit(iter_text, (self.screen.get_width()//2 - 80, 60))

        # Winner overlay
        if winner:
            if winner == "EA":
                msg = "EA WINS"
            elif winner == "AI":
                msg = "AI WINS"
            elif winner == "EA+AI":
                msg = "COOPERATION WIN"
            msg_text = self.big.render(msg, True, COLORS["highlight"])
            self.screen.blit(msg_text, (
                self.screen.get_width()//2 - msg_text.get_width()//2,
                20 + offset_y + self.rows*CELL + 120
            ))

        pygame.display.flip()