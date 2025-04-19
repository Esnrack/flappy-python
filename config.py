# config.py
import time

# Configurações iniciais da janela e jogo
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRAVITY = -0.9 # Gravidade normal
JUMP_STRENGTH = 0.5 # Força do pulo normal
PIPE_WIDTH = 0.15
PIPE_GAP = 0.4 # Gap normal
PIPE_SPEED = 0.5
INITIAL_LIVES = 3
PIPE_SPAWN_INTERVAL = 1.4

# Limita a mudança vertical
MAX_PIPE_HEIGHT_CHANGE = 0.4
MAX_PIPE_HEIGHT_CHANGE_AFTER_MOVING = 0.5

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
# !! IMPORTANTE: Atualize para 5 se você adicionou o sprite Shrink !!
POWERUP_COLS = 5 # vida, velocidade, motosserra, heavy_jump, shrink
POWERUP_ROWS = 1
# Adiciona 'shrink' à lista
POWERUP_TYPES = ['life', 'speed', 'chainsaw', 'heavy_jump', 'shrink']

# Tamanhos para Desenho
BIRD_DRAW_WIDTH = 0.15 # Valor atualizado
BIRD_DRAW_HEIGHT = 0.15 # Valor atualizado
POWERUP_DRAW_SIZE = 0.08

# Tamanho para Colisão
BIRD_COLLISION_SCALE_W = 0.85 # Escala base da hitbox W
BIRD_COLLISION_SCALE_H = 0.75 # Escala base da hitbox H
POWERUP_COLLISION_SIZE = 0.04

# --- Configurações para Powerups Específicos ---
POWERUP_Y_RANGE_AROUND_PATH = 0.5

# Chainsaw
CHAINSAW_GAP_INCREASE = 0.2
CHAINSAW_DURATION_PIPES = 3

# Heavy Jump
HEAVYJUMP_GRAVITY_MULTIPLIER = 1.8
HEAVYJUMP_JUMP_MULTIPLIER = 1.6
HEAVYJUMP_DURATION_SECONDS = 6.0

# --- Shrink ---
SHRINK_SCALE_FACTOR = 0.6 # Para qual fração do tamanho normal o pássaro encolhe (Ex: 60%)
SHRINK_DURATION_SECONDS = 7.0 # Duração do efeito em segundos

# Variáveis Globais de Jogo
bird_velocity = 0.0
game_started = False
game_over = False
lives = INITIAL_LIVES
score = 0
last_pipe_time = 0.0
pipes = []
powerups = []
speed_multiplier = 1.0 # Do powerup 'speed'
invulnerable = False
invulnerable_time = 0.0

# Estado Chainsaw
chainsaw_active = False
chainsaw_pipes_remaining = 0
chainsaw_deactivation_pending = False
chainsaw_last_pipe_ref = None

# Estado Heavy Jump
heavy_jump_active = False
heavy_jump_end_time = 0.0

# --- Estado Shrink ---
shrink_active = False
shrink_end_time = 0.0

# Posição inicial do pássaro
BIRD_X = -0.5
BIRD_Y = 0.0

# Variáveis Globais para Sprites
bird_texture_id = None
bird_frames_uv = []
bird_frame_aspect = 1.0
bird_current_frame = 0
last_frame_time = 0.0

powerup_texture_id = None
powerup_uvs = {} # Dicionário: {'life':(uv), 'speed':(uv), ...}
powerup_frame_aspect = 1.0