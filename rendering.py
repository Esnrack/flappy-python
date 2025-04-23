# rendering.py
from OpenGL.GL import *
from OpenGL.GLUT import *
import config
import time

# --- draw_background RESTAURADA ---
def draw_background(x_min, x_max, y_min, y_max):
    """Desenha a textura de background esticada para cobrir a área visível."""
    # A textura já deve estar vinculada por render()
    # Wrap mode CLAMP_TO_EDGE já foi setado
    U0, V0 = 0.0, 0.0 # UV: v=0 é base da imagem
    U1, V1 = 1.0, 1.0 # UV: v=1 é topo da imagem

    glBegin(GL_QUADS)
    # Mapeamento UV com V invertido
    glTexCoord2f(U0, V1); glVertex2f(x_min, y_min) # Bottom-Left Vert -> Top-Left Tex UV (V=1)
    glTexCoord2f(U1, V1); glVertex2f(x_max, y_min) # Bottom-Right Vert -> Top-Right Tex UV (V=1)
    glTexCoord2f(U1, V0); glVertex2f(x_max, y_max) # Top-Right Vert -> Bottom-Right Tex UV (V=0)
    glTexCoord2f(U0, V0); glVertex2f(x_min, y_max) # Top-Left Vert -> Bottom-Left Tex UV (V=0)
    glEnd()
# --- FIM draw_background ---

# --- draw_clouds RESTAURADA ---
def draw_clouds():
    """Desenha todas as nuvens ativas."""
    # Itera sobre a lista de nuvens em config
    # A classe Cloud deve estar definida em clouds.py e importada onde é usada (update.py)
    for cloud in config.clouds:
        # O objeto cloud tem seu próprio método draw que lida com textura e fallback
        cloud.draw()
# --- FIM draw_clouds ---


# --- draw_ground ---
def draw_ground(world_x_min=-1.5, world_x_max=1.5, use_fallback_color=False):
    """Desenha o chão com textura repetida cobrindo a largura visível ou cor sólida."""

    x_min, x_max = world_x_min, world_x_max
    y_min, y_max = -1.0, -0.9 # Posição Y fixa do chão

    if use_fallback_color or not config.ground_texture_id:
        glColor3f(0.6, 0.3, 0.1) # Marrom
        glBegin(GL_QUADS)
        glVertex2f(x_min, y_max); glVertex2f(x_max, y_max)
        glVertex2f(x_max, y_min); glVertex2f(x_min, y_min)
        glEnd()
        if not use_fallback_color: glColor3f(1.0, 1.0, 1.0)
    else:
        quad_width = x_max - x_min
        tile_world_width = config.GROUND_TILE_WORLD_WIDTH
        horizontal_repeats = quad_width / tile_world_width if tile_world_width > 0 else 1.0
        quad_height = y_max - y_min
        tile_world_height = tile_world_width
        vertical_repeats = quad_height / tile_world_height if tile_world_height > 0 else 1.0
        U0_offset = config.ground_offset_x
        U_REPEAT_offset = config.ground_offset_x + horizontal_repeats
        V0_base = 0.0; V_REPEAT = vertical_repeats

        glBegin(GL_QUADS)
        glTexCoord2f(U0_offset,       V0_base);   glVertex2f(x_min, y_max)
        glTexCoord2f(U_REPEAT_offset, V0_base);   glVertex2f(x_max, y_max)
        glTexCoord2f(U_REPEAT_offset, V_REPEAT);  glVertex2f(x_max, y_min)
        glTexCoord2f(U0_offset,       V_REPEAT);  glVertex2f(x_min, y_min)
        glEnd()

# --- draw_text ---
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    """Desenha texto na tela usando GLUT."""
    glColor3f(0.0, 0.0, 0.0) # Preto
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))