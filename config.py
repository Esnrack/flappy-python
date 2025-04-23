# config.py
import time

# Configurações iniciais da janela e jogo
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRAVITY = -0.9
JUMP_STRENGTH = 0.5
PIPE_WIDTH = 0.15
PIPE_GAP = 0.4
PIPE_SPEED = 0.5 # Velocidade horizontal principal (canos, chão)
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

TRUNK_SPRITE_PATH = "sprites/tree_trunk.png"

ROOT_SPRITE_PATH = "sprites/tree_roots.png"
ROOT_SPRITE_WIDTH_PX = 52
ROOT_SPRITE_HEIGHT_PX = 21
ROOT_DRAW_WIDTH_SCALE = 1.3

GROUND_SPRITE_PATH = "sprites/ground.png"
GROUND_TILE_WORLD_WIDTH = 0.1

# --- Configuração das Nuvens ---
CLOUD_CONFIG = [
    {'path': 'sprites/cloud.png',  'cols': 2, 'rows': 1}
]
CLOUD_SPAWN_INTERVAL_MIN = 2.5
CLOUD_SPAWN_INTERVAL_MAX = 5.0
CLOUD_SPEED_MIN = 0.1
CLOUD_SPEED_MAX = 0.25
CLOUD_Y_MIN = 0.3
CLOUD_Y_MAX = 0.8
CLOUD_SCALE_MIN = 0.8
CLOUD_SCALE_MAX = 1.3
CLOUD_BASE_DRAW_WIDTH = 0.2
CLOUD_ANIMATION_SPEED = 0.5 # Segundos por frame

# Configuração INDIVIDUAL dos Power-ups
POWERUP_CONFIG = [
    {'type': 'life',       'path': 'sprites/life.png',       'cols': 12, 'rows': 1, 'ping_pong': False},
    {'type': 'speed',      'path': 'sprites/speed.png',      'cols': 4, 'rows': 1, 'ping_pong': True},
    {'type': 'chainsaw',   'path': 'sprites/chainsaw.png',   'cols': 12, 'rows': 1, 'ping_pong': False},
    {'type': 'heavy_jump', 'path': 'sprites/heavy_jump.png', 'cols': 2, 'rows': 1, 'ping_pong': False},
    {'type': 'shrink',     'path': 'sprites/shrink.png',     'cols': 5, 'rows': 1, 'ping_pong': False},
]
POWERUP_ANIMATION_SPEED = 0.15

# Tamanhos para Desenho
BIRD_DRAW_WIDTH = 0.12
BIRD_DRAW_HEIGHT = 0.12 # Ajustada por aspect ratio
POWERUP_DRAW_SIZE = 0.10

# Tamanho para Colisão
BIRD_COLLISION_SCALE_W = 0.65
BIRD_COLLISION_SCALE_H = 0.65
POWERUP_COLLISION_SIZE = 0.04

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
ground_offset_x = 0.0

# --- Variáveis de Pausa ---
game_paused = False # Controla se o jogo está pausado
pause_start_time = 0.0 # Momento em que o jogo foi pausado
total_pause_duration = 0.0 # Tempo acumulado em pausa (RENOMEADO de total_pause_time)
# --- FIM Pausa ---


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

powerup_data = {}

trunk_texture_id = None
trunk_image_width = 0
trunk_image_height = 0
root_texture_id = None
root_image_width = 0
root_image_height = 0
root_aspect_ratio = 1.0
ground_texture_id = None
ground_image_width = 0
ground_image_height = 0

cloud_data = {}
clouds = []
last_cloud_spawn_time = 0.0
next_cloud_spawn_interval = 0.0

# --- Variáveis Globais para limites do Ortho ---
world_x_min = -1.0 * (WINDOW_WIDTH / WINDOW_HEIGHT) if WINDOW_WIDTH >= WINDOW_HEIGHT else -1.0
world_x_max = 1.0 * (WINDOW_WIDTH / WINDOW_HEIGHT) if WINDOW_WIDTH >= WINDOW_HEIGHT else 1.0
world_y_min = -1.0 if WINDOW_WIDTH >= WINDOW_HEIGHT else -1.0 / (WINDOW_WIDTH / WINDOW_HEIGHT)
world_y_max = 1.0 if WINDOW_WIDTH >= WINDOW_HEIGHT else 1.0 / (WINDOW_WIDTH / WINDOW_HEIGHT)