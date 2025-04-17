# config.py
import time

# Configurações iniciais da janela e jogo
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRAVITY = -0.9
JUMP_STRENGTH = 0.5
PIPE_WIDTH = 0.15
PIPE_GAP = 0.4
PIPE_SPEED = 0.5 # Horizontal speed
INITIAL_LIVES = 3
PIPE_SPAWN_INTERVAL = 1.4

# Limita a mudança vertical baseada na POSIÇÃO ESTIMADA FUTURA do cano anterior
MAX_PIPE_HEIGHT_CHANGE = 0.4
MAX_PIPE_HEIGHT_CHANGE_AFTER_MOVING = 0.60

# Configurações para movimento vertical dos canos
PIPE_MOVE_CHANCE = 0.35
MIN_PIPE_MOVE_SPEED = 0.15
MAX_PIPE_MOVE_SPEED = 0.30

# --- Configurações para Sprites ---
BIRD_SPRITE_PATH = "sprites/bird_sheet.png"
BIRD_COLS = 12
BIRD_ROWS = 1
BIRD_ANIMATION_SPEED = 0.1

POWERUP_SPRITE_PATH = "sprites/powerups.png"
POWERUP_COLS = 2
POWERUP_ROWS = 1
POWERUP_TYPES = ['life', 'speed']

# Tamanhos para Desenho
BIRD_DRAW_WIDTH = 0.12
BIRD_DRAW_HEIGHT = 0.12 # Será ajustada pelo aspect ratio em main.py
POWERUP_DRAW_SIZE = 0.08

# --- Tamanho para Colisão ---
# REMOVIDO: BIRD_COLLISION_RADIUS
# Fatores de escala para a hitbox AABB relativa ao tamanho de desenho.
# Valores < 1.0 tornam a hitbox menor (mais forgiving).
BIRD_COLLISION_SCALE_W = 0.85 # Ex: 85% da largura de desenho
BIRD_COLLISION_SCALE_H = 0.75 # Ex: 75% da altura de desenho

# Power-up ainda usa um raio/metade do tamanho para colisão (mais simples)
POWERUP_COLLISION_SIZE = 0.04

# Variáveis Globais de Jogo
bird_velocity = 0.0
game_started = False
game_over = False
lives = INITIAL_LIVES
score = 0
last_pipe_time = 0.0
pipes = []
powerups = []
speed_multiplier = 1.0
invulnerable = False
invulnerable_time = 0.0

# Posição inicial do pássaro
BIRD_X = -0.5
BIRD_Y = 0.0

# Variáveis Globais para Sprites
bird_texture_id = None
bird_frames_uv = []
bird_frame_aspect = 1.0 # Calculado em main.py
bird_current_frame = 0
last_frame_time = 0.0

powerup_texture_id = None
powerup_uvs = {}
powerup_frame_aspect = 1.0