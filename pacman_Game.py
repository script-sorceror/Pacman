import pygame
import sys
import random
from easyAI import AI_Player, Negamax, TwoPlayerGame

pygame.init()

SCREEN_WIDTH = 560
SCREEN_HEIGHT = 620
CELL_SIZE = 20
FPS = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

font = pygame.font.SysFont('Arial', 18)

board = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o####.#####.##.#####.####o#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "######.##### ## #####.######",
    "######.##          ##.######",
    "######.## ###--### ##.######",
    "######.## #      # ##.######",
    "       ## #      # ##       ",
    "######.## #      # ##.######",
    "######.## ######## ##.######",
    "######.##          ##.######",
    "######.## ######## ##.######",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#o..##................##..o#",
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################"
]

pacman_img = pygame.image.load('assets/pacman.png')
ghost_imgs = [
    pygame.image.load('assets/yellow.png'),
    pygame.image.load('assets/red.png'),
    pygame.image.load('assets/blue.png'),
    pygame.image.load('assets/green.png')
]

pacman_img = pygame.transform.scale(pacman_img, (CELL_SIZE, CELL_SIZE))
for i in range(len(ghost_imgs)):
    ghost_imgs[i] = pygame.transform.scale(ghost_imgs[i], (CELL_SIZE, CELL_SIZE))


def draw_board():
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == '#':
                pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif cell == '.':
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 3)
            elif cell == 'o':
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 7)


def draw_pacman():
    screen.blit(pacman_img, (pacman_x * CELL_SIZE, pacman_y * CELL_SIZE))

def draw_ghosts():
    for i, ghost in enumerate(ghosts):
        screen.blit(ghost_imgs[i], (ghost['x'] * CELL_SIZE, ghost['y'] * CELL_SIZE))


# AI Player Class for Ghosts
class GhostAI(TwoPlayerGame):
    def __init__(self, players, ghost):
        self.players = players
        self.current_player = 1
        self.ghost = ghost
        self.pacman_pos = (pacman_x, pacman_y)

    def possible_moves(self):
        moves = []
        if board[self.ghost['y']][self.ghost['x'] - 1] != '#':
            moves.append('LEFT')
        if board[self.ghost['y']][self.ghost['x'] + 1] != '#':
            moves.append('RIGHT')
        if board[self.ghost['y'] - 1][self.ghost['x']] != '#':
            moves.append('UP')
        if board[self.ghost['y'] + 1][self.ghost['x']] != '#':
            moves.append('DOWN')
        return moves

    def make_move(self, move):
        if move == 'LEFT':
            self.ghost['x'] -= 1
        elif move == 'RIGHT':
            self.ghost['x'] += 1
        elif move == 'UP':
            self.ghost['y'] -= 1
        elif move == 'DOWN':
            self.ghost['y'] += 1

    def unmake_move(self, move):
        if move == 'LEFT':
            self.ghost['x'] += 1
        elif move == 'RIGHT':
            self.ghost['x'] -= 1
        elif move == 'UP':
            self.ghost['y'] += 1
        elif move == 'DOWN':
            self.ghost['y'] -= 1

    def lose(self):
        return self.ghost['x'] == pacman_x and self.ghost['y'] == pacman_y

    def is_over(self):
        return self.lose()

    def scoring(self):
        # Heuristic: Ghost tries to get as close as possible to Pac-Man
        return -((self.ghost['x'] - pacman_x) ** 2 + (self.ghost['y'] - pacman_y) ** 2)


# Move Pacman Function
def move_pacman():
    global pacman_x, pacman_y, score
    if pacman_direction == 'LEFT' and board[pacman_y][pacman_x - 1] != '#':
        pacman_x -= 1
    elif pacman_direction == 'RIGHT' and board[pacman_y][pacman_x + 1] != '#':
        pacman_x += 1
    elif pacman_direction == 'UP' and board[pacman_y - 1][pacman_x] != '#':
        pacman_y -= 1
    elif pacman_direction == 'DOWN' and board[pacman_y + 1][pacman_x] != '#':
        pacman_y += 1
    
    if board[pacman_y][pacman_x] == '.':
        board[pacman_y] = board[pacman_y][:pacman_x] + ' ' + board[pacman_y][pacman_x + 1:]
        score += 10
    elif board[pacman_y][pacman_x] == 'o':
        board[pacman_y] = board[pacman_y][:pacman_x] + ' ' + board[pacman_y][pacman_x + 1:]
        score += 50


# Move Ghosts using AI
def move_ghosts():
    for i, ghost in enumerate(ghosts):
        game = GhostAI([AI_Player(Negamax(2))], ghost)
        move = game.get_move()
        game.make_move(move)


def check_collisions():
    for ghost in ghosts:
        if ghost['x'] == pacman_x and ghost['y'] == pacman_y:
            return True
    return False


def check_all_pellets_eaten():
    for row in board:
        if '.' in row or 'o' in row:
            return False
    return True


# Initialize game state variables
pacman_x = 14  # Pac-Man starting X position (adjust based on your board layout)
pacman_y = 23  # Pac-Man starting Y position (adjust based on your board layout)
pacman_direction = 'LEFT'  # Pac-Man starting direction
score = 0  # Initial score

# Initialize ghosts
ghosts = [
    {'x': 13, 'y': 11},  # Yellow ghost initial position
    {'x': 14, 'y': 11},  # Red ghost initial position
    {'x': 15, 'y': 11},  # Blue ghost initial position
    {'x': 16, 'y': 11}   # Green ghost initial position
]


lock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                pacman_direction = 'RIGHT'
            elif event.key == pygame.K_UP:
                pacman_direction = 'UP'
            elif event.key == pygame.K_DOWN:
                pacman_direction = 'DOWN'

    move_pacman()
    move_ghosts()

    if check_collisions():
        print("Game Over!")
        running = False

    if check_all_pellets_eaten():
        print("You Win!")
        running = False

    screen.fill(BLACK)
    draw_board()
    draw_pacman()
    draw_ghosts()

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, SCREEN_HEIGHT - 30))

    pygame.display.flip()
    lock.tick(FPS)

pygame.quit()
sys.exit()
