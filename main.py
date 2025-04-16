 # main.py
import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image # Importar PIL/Pillow
import time
import numpy as np # Importar numpy
import config
from player import draw_bird
from game_pipes import draw_pipes
from powerup import draw_powerups
from rendering import draw_ground, draw_text
from update import update
from input import key_callback

# --- Função para Carregar Textura ---
def load_texture(path):
    """Carrega uma imagem e cria uma textura OpenGL."""
    try:
        img = Image.open(path).convert("RGBA") # Garante formato RGBA
        img_data = np.array(list(img.getdata()), np.uint8)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        # Configura parâmetros da textura
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST) # Bom para pixel art
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE) # Evita repetir bordas
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        # Envia dados da imagem para a GPU
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glBindTexture(GL_TEXTURE_2D, 0) # Desvincula a textura
        print(f"Textura carregada: {path}, ID: {texture_id}, Dimensões: {img.width}x{img.height}")
        return texture_id, img.width, img.height
    except FileNotFoundError:
        print(f"Erro Crítico: Arquivo de sprite não encontrado em {path}")
        # Aqui você poderia talvez carregar uma textura padrão de 'erro' ou sair
        return None, 0, 0
    except Exception as e:
        print(f"Erro ao carregar textura {path}: {e}")
        return None, 0, 0

# --- Função para Calcular Coordenadas UV dos Frames ---
def calculate_sprite_uvs(sheet_width, sheet_height, cols, rows):
    """Calcula as coordenadas de textura (UV) para cada frame em uma sprite sheet."""
    uvs = []
    if cols <= 0 or rows <= 0: return uvs, 1.0 # Evita divisão por zero

    frame_width = sheet_width / cols
    frame_height = sheet_height / rows
    aspect_ratio = frame_width / frame_height if frame_height > 0 else 1.0

    for r in range(rows):
        for c in range(cols):
            # Calcula coordenadas UV (0,0 no canto inferior esquerdo para OpenGL)
            u0 = c / cols
            v0 = 1.0 - (r + 1) / rows # V invertido (origem da imagem em cima, OpenGL embaixo)
            u1 = (c + 1) / cols
            v1 = 1.0 - r / rows     # V invertido
            uvs.append((u0, v0, u1, v1))
            # print(f"Frame ({r},{c}): UV=({u0:.2f},{v0:.2f}) a ({u1:.2f},{v1:.2f})") # Debug
    return uvs, aspect_ratio

# Variável global para a janela (se já não estiver definida assim)
window = None

def main():
    global window
    if not glfw.init():
        print("Falha ao inicializar GLFW")
        return

    # Inicializa GLUT (necessário para draw_text)
    glutInit()

    # Cria a janela
    window = glfw.create_window(config.WINDOW_WIDTH, config.WINDOW_HEIGHT, "Flappy Bird com Sprites", None, None)
    if not window:
        glfw.terminate()
        print("Falha ao criar a janela GLFW")
        return

    glfw.make_context_current(window)
    # Define callbacks
    glfw.set_key_callback(window, key_callback)
    glfw.set_window_size_callback(window, window_size_callback)

    # --- Configurações do OpenGL ---
    glEnable(GL_TEXTURE_2D) # Habilita o uso de texturas 2D
    glEnable(GL_BLEND)      # Habilita blending (para transparência)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) # Define como a transparência funciona

    # --- Carregar Texturas AQUI ---
    print("Carregando texturas...")
    # Carregar Pássaro
    config.bird_texture_id, sheet_w, sheet_h = load_texture(config.BIRD_SPRITE_PATH)
    if config.bird_texture_id and sheet_w > 0 and sheet_h > 0:
        config.bird_frames_uv, config.bird_frame_aspect = calculate_sprite_uvs(sheet_w, sheet_h, config.BIRD_COLS, config.BIRD_ROWS)
        # Ajusta a altura de desenho baseado no aspect ratio REAL do frame
        if config.bird_frame_aspect > 0:
            config.BIRD_DRAW_HEIGHT = config.BIRD_DRAW_WIDTH / config.bird_frame_aspect
        else:
             config.BIRD_DRAW_HEIGHT = config.BIRD_DRAW_WIDTH # Mantém quadrado se aspect ratio for inválido
        config.last_frame_time = time.time() # Inicia timer da animação
        print(f"Frames do pássaro calculados: {len(config.bird_frames_uv)}, Aspect Ratio: {config.bird_frame_aspect:.2f}")
    else:
        print("Falha ao carregar textura do pássaro.")


    # Carregar Power-ups
    config.powerup_texture_id, sheet_w, sheet_h = load_texture(config.POWERUP_SPRITE_PATH)
    if config.powerup_texture_id and sheet_w > 0 and sheet_h > 0:
        powerup_frame_uvs, config.powerup_frame_aspect = calculate_sprite_uvs(sheet_w, sheet_h, config.POWERUP_COLS, config.POWERUP_ROWS)
        # Mapear UVs para tipos de power-up definidos em config.POWERUP_TYPES
        for i, type_name in enumerate(config.POWERUP_TYPES):
            if i < len(powerup_frame_uvs):
                config.powerup_uvs[type_name] = powerup_frame_uvs[i]
            else:
                print(f"Aviso: Menos frames na sheet ({len(powerup_frame_uvs)}) do que tipos de power-up definidos ({len(config.POWERUP_TYPES)})")
                break # Para de mapear se acabaram os frames
        print(f"UVs dos power-ups mapeados: {config.powerup_uvs}")
    else:
        print("Falha ao carregar textura dos power-ups.")

    # --- Configuração inicial da projeção ---
    # Chama o callback uma vez para configurar a projeção inicial
    fb_width, fb_height = glfw.get_framebuffer_size(window)
    window_size_callback(window, fb_width, fb_height)

    # --- Loop Principal ---
    last_time = time.time()
    print("Iniciando loop principal...")
    while not glfw.window_should_close(window):
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time

        # Limita delta_time para evitar saltos grandes (opcional mas recomendado)
        delta_time = min(delta_time, 0.1) # Ex: não processar mais que 0.1s por frame

        update(delta_time) # Atualiza estado do jogo e animação
        render()           # Desenha o frame atual
        glfw.poll_events() # Processa eventos (teclado, janela, etc.)

    # --- Limpeza ---
    print("Encerrando...")
    # Deleta as texturas da memória da GPU
    textures_to_delete = []
    if config.bird_texture_id:
        textures_to_delete.append(config.bird_texture_id)
    if config.powerup_texture_id:
         textures_to_delete.append(config.powerup_texture_id)
    if textures_to_delete:
        glDeleteTextures(textures_to_delete)
        print(f"Texturas deletadas: {textures_to_delete}")

    glfw.terminate()
    print("Aplicação encerrada.")

# --- Função Render ---
def render():
    """Desenha todos os elementos do jogo na tela."""
    # Define a cor de fundo (céu) e limpa os buffers
    glClearColor(0.53, 0.81, 0.92, 1.0) # Azul claro
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpa cor e profundidade

    # Reseta a matriz ModelView para garantir que as transformações não se acumulem
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # --- Desenhar Elementos ---
    # É uma boa prática habilitar/desabilitar estados OpenGL conforme necessário

    # 1. Elementos Não Texturizados (ou com texturas diferentes)
    glDisable(GL_TEXTURE_2D) # Garante que textura está desligada
    draw_ground()    # Desenha o chão (ainda cor sólida)
    draw_pipes()     # Desenha os canos (ainda cor sólida)

    # 2. Elementos Texturizados (Pássaro e Powerups compartilham estado)
    glEnable(GL_TEXTURE_2D)
    glColor4f(1.0, 1.0, 1.0, 1.0) # Cor branca para não tingir a textura, Alpha 1.0

    # Desenha o pássaro (usará sua própria textura internamente via glBindTexture)
    draw_bird()

    # Desenha os powerups (usará sua própria textura internamente)
    draw_powerups()

    glDisable(GL_TEXTURE_2D) # Desliga textura após desenhar todos os texturizados

    # 3. Interface do Usuário (Texto - não usa textura 2D padrão)
    # Certifique-se que o texto não é afetado pela cor branca anterior se necessário
    # draw_text já define sua própria cor (preto)
    draw_text(-0.95, 0.9, f"Score: {config.score}")
    draw_text(-0.95, 0.8, f"Lives: {config.lives}")
    if config.speed_multiplier > 1.0 and config.invulnerable:
        remaining_time = max(0, config.invulnerable_time - time.time())
        draw_text(-0.95, 0.7, f"SPEED BOOST: {remaining_time:.1f}s")
    elif config.invulnerable: # Invulnerabilidade normal (sem speed boost)
         remaining_time = max(0, config.invulnerable_time - time.time())
         draw_text(-0.95, 0.7, f"INVULNERABLE: {remaining_time:.1f}s")


    if config.game_over:
        draw_text(-0.4, 0.0, "GAME OVER! Press R to Restart")
    elif not config.game_started:
         draw_text(-0.5, 0.0, "Press SPACE to Start")


    # Troca os buffers (mostra o que foi desenhado)
    glfw.swap_buffers(window)

# --- Callback de Redimensionamento da Janela ---
def window_size_callback(window, width, height):
    """Chamado quando a janela é redimensionada."""
    if height == 0: height = 1 # Previne divisão por zero
    glViewport(0, 0, width, height) # Define a área de desenho para a janela inteira

    # Configura a projeção ortográfica para manter o aspect ratio
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect_ratio = width / height
    # Ajusta a visualização para que o eixo Y (-1 a 1) seja sempre visível
    # e o eixo X seja ajustado baseado no aspect ratio
    if aspect_ratio >= 1.0: # Janela mais larga ou quadrada
        glOrtho(-aspect_ratio, aspect_ratio, -1.0, 1.0, -1.0, 1.0)
    else: # Janela mais alta
        glOrtho(-1.0, 1.0, -1.0 / aspect_ratio, 1.0 / aspect_ratio, -1.0, 1.0)

    # Volta para a matriz ModelView para operações de desenho
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity() # Reseta a matriz ModelView também


# --- Ponto de Entrada ---
if __name__ == "__main__":
    main()