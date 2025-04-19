# config.py
import time

# Configurações iniciais da janela e jogo
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRAVITY = -0.9
JUMP_STRENGTH = 0.5
PIPE_WIDTH = 0.15 # Largura para COLISÃO e posicionamento horizontal
PIPE_GAP = 0.4 # The NORMAL gap size
PIPE_SPEED = 0.5 # Horizontal speed
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
BIRD_COLS = 12; BIRD_ROWS = 1; BIRD_ANIMATION_SPEED = 0.1

POWERUP_SPRITE_PATH = "sprites/powerups.png"
POWERUP_COLS = 5; POWERUP_ROWS = 1
POWERUP_TYPES = ['life', 'speed', 'chainsaw', 'heavy_jump', 'shrink']

# --- Tree Trunk Sprite (Single Image) ---
TRUNK_SPRITE_PATH = "sprites/tree_trunk.png" # <<< SEU ARQUIVO DE TRONCO ÚNICO

# --- Root Base Sprite ---
ROOT_SPRITE_PATH = "sprites/tree_roots.png" # <<< SEU ARQUIVO DE RAÍZES
ROOT_SPRITE_WIDTH_PX = 52 # Original pixel width (used for aspect calc)
ROOT_SPRITE_HEIGHT_PX = 21 # Original pixel height (used for height calc)
# Escala da Largura da Raiz (opcional)
# Multiplicador aplicado à largura PROPORCIONAL da raiz. > 1.0 torna mais largo.
ROOT_DRAW_WIDTH_SCALE = 1.3 # Ex: Raiz 20% mais larga que sua proporção original

# Tamanhos para Desenho
BIRD_DRAW_WIDTH = 0.15; BIRD_DRAW_HEIGHT = 0.15 # Ajustada por aspect ratio
POWERUP_DRAW_SIZE = 0.08

# Tamanho para Colisão
BIRD_COLLISION_SCALE_W = 0.85; BIRD_COLLISION_SCALE_H = 0.75
POWERUP_COLLISION_SIZE = 0.04

# Configurações para Powerups Específicos
POWERUP_Y_RANGE_AROUND_PATH = 0.5
CHAINSAW_GAP_INCREASE = 0.2; CHAINSAW_DURATION_PIPES = 3
HEAVYJUMP_GRAVITY_MULTIPLIER = 1.8; HEAVYJUMP_JUMP_MULTIPLIER = 1.6; HEAVYJUMP_DURATION_SECONDS = 6.0
SHRINK_SCALE_FACTOR = 0.6; SHRINK_DURATION_SECONDS = 7.0

# Variáveis Globais de Jogo
bird_velocity = 0.0; game_started = False; game_over = False
lives = INITIAL_LIVES; score = 0; last_pipe_time = 0.0
pipes = [] # Dicionário NÃO terá tree_frame_index
powerups = []; speed_multiplier = 1.0
invulnerable = False; invulnerable_time = 0.0
chainsaw_active = False; chainsaw_pipes_remaining = 0
chainsaw_deactivation_pending = False; chainsaw_last_pipe_ref = None
heavy_jump_active = False; heavy_jump_end_time = 0.0
shrink_active = False; shrink_end_time = 0.0

# Posição inicial do pássaro
BIRD_X = -0.5; BIRD_Y = 0.0

# Variáveis Globais para Sprites
bird_texture_id = None; bird_frames_uv = []; bird_frame_aspect = 1.0
bird_current_frame = 0; last_frame_time = 0.0

powerup_texture_id = None; powerup_uvs = {}; powerup_frame_aspect = 1.0

# --- Trunk Sprite ---
trunk_texture_id = None
trunk_image_width = 0 # Largura px real
trunk_image_height = 0 # Altura px real

# --- Root Sprite ---
root_texture_id = None
root_image_width = 0 # Largura px real
root_image_height = 0 # Altura px real
root_aspect_ratio = 1.0 # Calculado em main.py (largura_px / altura_px)
# --- FIM Root Sprite ---