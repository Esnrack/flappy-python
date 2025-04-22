# config.py
import time

# Configurações iniciais da janela e jogo
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRAVITY = -0.9
JUMP_STRENGTH = 0.5
PIPE_WIDTH = 0.15
PIPE_GAP = 0.4
PIPE_SPEED = 0.5
INITIAL_LIVES = 3
PIPE_SPAWN_INTERVAL = 1.4
MAX_PIPE_HEIGHT_CHANGE = 0.4
MAX_PIPE_HEIGHT_CHANGE_AFTER_MOVING = 0.4
PIPE_MOVE_CHANCE = 0.35
MIN_PIPE_MOVE_SPEED = 0.15
MAX_PIPE_MOVE_SPEED = 0.30

# --- Configurações para Sprites ---
BIRD_SPRITE_PATH = "sprites/bird_sheet.png"
BIRD_COLS = 24
BIRD_ROWS = 1
BIRD_ANIMATION_SPEED = 0.1

# --- Tree Trunk Sprite (Single Image) ---
TRUNK_SPRITE_PATH = "sprites/tree_trunk.png"

# --- Root Base Sprite ---
ROOT_SPRITE_PATH = "sprites/tree_roots.png"
ROOT_SPRITE_WIDTH_PX = 52
ROOT_SPRITE_HEIGHT_PX = 21
ROOT_DRAW_WIDTH_SCALE = 1.3

# --- Configuração INDIVIDUAL dos Power-ups ---
POWERUP_CONFIG = [
    {'type': 'life',       'path': 'sprites/pu_life.png',       'cols': 1, 'rows': 1, 'ping_pong': False},
    {'type': 'speed',      'path': 'sprites/speed.png',         'cols': 4, 'rows': 1, 'ping_pong': True},
    {'type': 'chainsaw',   'path': 'sprites/chainsaw.png',   'cols': 12, 'rows': 1, 'ping_pong': False},
    {'type': 'heavy_jump', 'path': 'sprites/heavy_jump.png', 'cols': 2, 'rows': 1, 'ping_pong': False},
    {'type': 'shrink',     'path': 'sprites/shrink.png',     'cols': 5, 'rows': 1, 'ping_pong': False},
]
POWERUP_ANIMATION_SPEED = 0.15 # Segundos por frame

# Tamanhos para Desenho
BIRD_DRAW_WIDTH = 0.15
BIRD_DRAW_HEIGHT = 0.15 # Ajustada por aspect ratio
# POWERUP_DRAW_SIZE agora define a LARGURA de desenho desejada
POWERUP_DRAW_SIZE = 0.10 # Ajuste conforme necessário para o tamanho desejado

# Tamanho para Colisão
BIRD_COLLISION_SCALE_W = 0.75
BIRD_COLLISION_SCALE_H = 0.75
POWERUP_COLLISION_SIZE = 0.04 # Raio/Metade do tamanho para colisão

# Configurações para Powerups Específicos (Efeitos)
POWERUP_Y_RANGE_AROUND_PATH = 0.5
CHAINSAW_GAP_INCREASE = 0.2
CHAINSAW_DURATION_PIPES = 3
HEAVYJUMP_GRAVITY_MULTIPLIER = 1.8
HEAVYJUMP_JUMP_MULTIPLIER = 1.6
HEAVYJUMP_DURATION_SECONDS = 6.0
SHRINK_SCALE_FACTOR = 0.6
SHRINK_DURATION_SECONDS = 7.0

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
chainsaw_active = False
chainsaw_pipes_remaining = 0
chainsaw_deactivation_pending = False
chainsaw_last_pipe_ref = None
heavy_jump_active = False
heavy_jump_end_time = 0.0
shrink_active = False
shrink_end_time = 0.0

# Posição inicial do pássaro
BIRD_X = -0.5
BIRD_Y = 0.0

# High Score
high_score = 0
HIGH_SCORE_FILE = "high_score.txt"

# --- Variáveis Globais para Sprites ---
bird_texture_id = None
bird_frames_uv = []
bird_frame_aspect = 1.0
bird_current_frame = 0
last_frame_time = 0.0

# Dicionário para armazenar dados carregados dos powerups
powerup_data = {}

# Trunk Sprite
trunk_texture_id = None
trunk_image_width = 0
trunk_image_height = 0

# Root Sprite
root_texture_id = None
root_image_width = 0
root_image_height = 0
root_aspect_ratio = 1.0