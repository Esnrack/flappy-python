import time

# Configurações iniciais
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
BIRD_X = -0.5
BIRD_Y = 0.0
BIRD_SIZE = 0.05
GRAVITY = -0.9
JUMP_STRENGTH = 0.5
PIPE_WIDTH = 0.1
PIPE_GAP = 0.35
PIPE_SPEED = 0.5
INITIAL_LIVES = 3
PIPE_SPAWN_INTERVAL = 1.5

# Variáveis globais
bird_velocity = 0.0
game_started = False
game_over = False
lives = INITIAL_LIVES
score = 0
last_pipe_time = 0
pipes = []
powerups = []
speed_multiplier = 1.0
invulnerable = False
invulnerable_time = 0
