# config.py
import time

# Configurações iniciais da janela e jogo
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRAVITY = -0.9
JUMP_STRENGTH = 0.5
PIPE_WIDTH = 0.15
PIPE_GAP = 0.4 # The NORMAL gap size
PIPE_SPEED = 0.5 # Horizontal speed
INITIAL_LIVES = 3
PIPE_SPAWN_INTERVAL = 1.4

# Limita a mudança vertical baseada na POSIÇÃO ESTIMADA FUTURA do cano anterior
MAX_PIPE_HEIGHT_CHANGE = 0.4
MAX_PIPE_HEIGHT_CHANGE_AFTER_MOVING = 0.5 # Valor atualizado

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
POWERUP_COLS = 3 # vida, velocidade, motosserra
POWERUP_ROWS = 1
POWERUP_TYPES = ['chainsaw']

# Tamanhos para Desenho
BIRD_DRAW_WIDTH = 0.15 # Valor atualizado
BIRD_DRAW_HEIGHT = 0.15 # Valor atualizado
POWERUP_DRAW_SIZE = 0.08

# Tamanho para Colisão
BIRD_COLLISION_SCALE_W = 0.85
BIRD_COLLISION_SCALE_H = 0.75
POWERUP_COLLISION_SIZE = 0.04

# --- Configurações para Powerups Específicos ---
POWERUP_Y_RANGE_AROUND_PATH = 0.5
CHAINSAW_GAP_INCREASE = 0.2
CHAINSAW_DURATION_PIPES = 3

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

# Estado do Power-up Chainsaw
chainsaw_active = False
chainsaw_pipes_remaining = 0
# --- NOVAS VARIÁVEIS GLOBAIS ---
chainsaw_deactivation_pending = False # Flag para indicar que a desativação está aguardando
chainsaw_last_pipe_ref = None       # Referência ao último cano afetado

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