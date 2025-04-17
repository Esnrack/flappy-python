import glfw
from OpenGL.GL import *
from PIL import Image
import time

# Inicializa o GLFW e cria a janela
if not glfw.init():
    raise Exception("glfw não foi inicializado!")

window = glfw.create_window(800, 600, "Animação com Sprite Sheet", None, None)
if not window:
    glfw.terminate()
    raise Exception("Falha ao criar a janela!")

glfw.make_context_current(window)

# Configura a viewport e a projeção ortográfica baseada no tamanho da janela
def setup_projection():
    width, height = glfw.get_framebuffer_size(window)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    return width, height

window_width, window_height = setup_projection()

# Carrega a sprite sheet a partir da pasta 'sprites'
# Certifique-se de que o arquivo 'meu_sprite.png' está na pasta 'sprites'
sprite_sheet = Image.open("sprites/Prot-Motoserra.png").convert("RGBA")
sheet_width, sheet_height = sprite_sheet.size

# Define o número de colunas e linhas na sprite sheet
cols = 12  # quantidade de frames na largura
rows = 1  # quantidade de frames na altura

# Calcula a largura e altura de cada frame
frame_width = sheet_width // cols
frame_height = sheet_height // rows
# Aspect ratio do frame (largura/altura)
frame_aspect = frame_width / frame_height

# Extrai os frames da sprite sheet
frames = []
for row in range(rows):
    for col in range(cols):
        box = (col * frame_width, row * frame_height,
               (col + 1) * frame_width, (row + 1) * frame_height)
        frame = sprite_sheet.crop(box)
        frame_data = frame.tobytes("raw", "RGBA", 0, -1)
        frames.append((frame_data, frame_width, frame_height))

total_frames = len(frames)
print("Total de frames extraídos:", total_frames)

# Cria uma textura OpenGL e configura os parâmetros
texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

# Variáveis de controle da animação
current_frame = 0
last_time = time.time()
frame_duration = 0.1  # duração de cada frame em segundos

while not glfw.window_should_close(window):
    current_time = time.time()
    # Atualiza o frame com base no tempo decorrido
    if current_time - last_time >= frame_duration:
        current_frame = (current_frame + 1) % total_frames
        last_time = current_time
        frame_data, w, h = frames[current_frame]
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, frame_data)

    glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)

    # Atualiza projeção em caso de redimensionamento da janela
    window_width, window_height = setup_projection()

    # Calcula a área máxima para desenhar o sprite, preservando o aspect ratio
    # Se a janela for "mais larga" que o aspecto do sprite, a altura é o fator limitante.
    if (window_width / window_height) > frame_aspect:
        quad_height = window_height
        quad_width = quad_height * frame_aspect
    else:
        quad_width = window_width
        quad_height = quad_width / frame_aspect

    # Centraliza o sprite na tela
    x0 = (window_width - quad_width) / 2
    y0 = (window_height - quad_height) / 2
    x1 = x0 + quad_width
    y1 = y0 + quad_height

    # Desenha o quad com o sprite ajustado ao tamanho da tela
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(x0, y0)

    glTexCoord2f(1, 0)
    glVertex2f(x1, y0)

    glTexCoord2f(1, 1)
    glVertex2f(x1, y1)

    glTexCoord2f(0, 1)
    glVertex2f(x0, y1)
    glEnd()

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()
