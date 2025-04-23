 # main.py
import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image
import time
import numpy as np
import random
import config # Importa config primeiro
from player import draw_bird
from game_pipes import draw_pipes
from powerup import draw_powerups
from rendering import draw_ground, draw_text, draw_background, draw_clouds
from update import update # update importa config
from input import key_callback
from high_score import load_high_score
from clouds import Cloud

# --- Função para Carregar Textura ---
def load_texture(path):
    try:
        img = Image.open(path).convert("RGBA")
        img_data = np.array(list(img.getdata()), np.uint8)
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glBindTexture(GL_TEXTURE_2D, 0)
        print(f"Textura carregada: {path}, ID: {texture_id}, Dimensões: {img.width}x{img.height}")
        return texture_id, img.width, img.height
    except FileNotFoundError: print(f"Erro Crítico: Arquivo não encontrado {path}"); return None, 0, 0
    except Exception as e: print(f"Erro ao carregar textura {path}: {e}"); return None, 0, 0

# --- Função para Calcular Coordenadas UV dos Frames ---
def calculate_sprite_uvs(sheet_width, sheet_height, cols, rows):
    uvs = []; aspect_ratio = 1.0
    if cols <= 0 or rows <= 0 or sheet_width <= 0 or sheet_height <= 0: return uvs, aspect_ratio
    frame_width = sheet_width / cols; frame_height = sheet_height / rows
    if frame_height > 0: aspect_ratio = frame_width / frame_height
    for r in range(rows):
        for c in range(cols):
            u0 = c / cols; v0 = 1.0 - (r + 1) / rows; u1 = (c + 1) / cols; v1 = 1.0 - r / rows
            uvs.append((u0, v0, u1, v1))
    return uvs, aspect_ratio

window = None
# --- REMOVIDO Variáveis Globais Ortho daqui ---

def main():
    global window
    if not glfw.init(): print("Falha GLFW"); return
    glutInit()

    config.high_score = load_high_score()
    print(f"Recorde carregado: {config.high_score}")

    window = glfw.create_window(config.WINDOW_WIDTH, config.WINDOW_HEIGHT, "Flappy Bird com Sprites", None, None)
    if not window: glfw.terminate(); print("Falha janela GLFW"); return
    glfw.make_context_current(window); glfw.set_key_callback(window, key_callback); glfw.set_window_size_callback(window, window_size_callback)

    glEnable(GL_TEXTURE_2D); glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    print("Carregando texturas...")
    # Pássaro
    config.bird_texture_id, sheet_w, sheet_h = load_texture(config.BIRD_SPRITE_PATH)
    if config.bird_texture_id and sheet_w > 0 and sheet_h > 0:
        config.bird_frames_uv, config.bird_frame_aspect = calculate_sprite_uvs(sheet_w, sheet_h, config.BIRD_COLS, config.BIRD_ROWS)
        config.BIRD_DRAW_HEIGHT = config.BIRD_DRAW_WIDTH / config.bird_frame_aspect if config.bird_frame_aspect > 0 else config.BIRD_DRAW_WIDTH
        config.last_frame_time = time.time()
        print(f"Frames pássaro: {len(config.bird_frames_uv)}, Aspect: {config.bird_frame_aspect:.2f}, Draw H: {config.BIRD_DRAW_HEIGHT:.2f}")
    else: print("Falha textura pássaro.")
    # Power-ups
    loaded_powerup_textures = []
    print("Carregando power-ups individuais...")
    for pu_config in config.POWERUP_CONFIG:
        pu_type = pu_config['type']; pu_path = pu_config['path']
        pu_cols = pu_config.get('cols', 1); pu_rows = pu_config.get('rows', 1)
        pu_ping_pong = pu_config.get('ping_pong', False)
        tex_id, w, h = load_texture(pu_path)
        if tex_id and w > 0 and h > 0:
            uvs, aspect = calculate_sprite_uvs(w, h, pu_cols, pu_rows)
            if not uvs: print(f"Aviso: Falha ao calcular UVs para '{pu_type}'"); continue
            config.powerup_data[pu_type] = {'id': tex_id, 'uvs': uvs, 'aspect': aspect, 'ping_pong': pu_ping_pong}
            loaded_powerup_textures.append(tex_id)
            print(f"  - '{pu_type}' carregado (Frames: {len(uvs)}, Aspect: {aspect:.2f}, PingPong: {pu_ping_pong})")
        else: print(f"Aviso: Falha ao carregar textura para '{pu_type}' em {pu_path}")

    # Tronco
    config.trunk_texture_id, config.trunk_image_width, config.trunk_image_height = load_texture(config.TRUNK_SPRITE_PATH)
    if config.trunk_texture_id:
        glBindTexture(GL_TEXTURE_2D, config.trunk_texture_id); glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT); glBindTexture(GL_TEXTURE_2D, 0)
        print(f"Textura do tronco carregada.")
    else: print("Falha ao carregar textura do tronco.")
    # Raízes
    config.root_texture_id, config.root_image_width, config.root_image_height = load_texture(config.ROOT_SPRITE_PATH)
    if config.root_texture_id and config.root_image_height > 0:
        config.root_aspect_ratio = config.root_image_width / config.root_image_height
        glBindTexture(GL_TEXTURE_2D, config.root_texture_id); glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE); glBindTexture(GL_TEXTURE_2D, 0)
        print(f"Textura das raízes carregada, Aspect Ratio: {config.root_aspect_ratio:.2f}")
    else: print("Falha ao carregar textura das raízes.")
    # Chão
    config.ground_texture_id, config.ground_image_width, config.ground_image_height = load_texture(config.GROUND_SPRITE_PATH)
    if config.ground_texture_id:
        glBindTexture(GL_TEXTURE_2D, config.ground_texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT); glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT); glBindTexture(GL_TEXTURE_2D, 0)
        print("Textura do chão carregada.")
    else: print("Falha ao carregar textura do chão.")
    # Nuvens
    loaded_cloud_textures = []
    print("Carregando nuvens...")
    if not config.CLOUD_CONFIG: print("  - Nenhuma nuvem configurada, usando fallback (quadrados).")
    else:
        for cloud_conf in config.CLOUD_CONFIG:
            path = cloud_conf['path']; cols = cloud_conf.get('cols', 1); rows = cloud_conf.get('rows', 1)
            tex_id, w, h = load_texture(path)
            if tex_id and w > 0 and h > 0:
                uvs, aspect = calculate_sprite_uvs(w, h, cols, rows)
                if uvs:
                    config.cloud_data[path] = {'id': tex_id, 'uvs': uvs, 'aspect': aspect}
                    loaded_cloud_textures.append(tex_id)
                    print(f"  - Nuvem '{path}' carregada (Frames: {len(uvs)}, Aspect: {aspect:.2f})")
                else: print(f"Aviso: Falha ao calcular UVs para nuvem '{path}'")
            else: print(f"Aviso: Falha ao carregar textura para nuvem '{path}'")

    fb_width, fb_height = glfw.get_framebuffer_size(window); window_size_callback(window, fb_width, fb_height)

    last_time = time.time(); print("Iniciando loop principal...")
    config.next_cloud_spawn_interval = random.uniform(config.CLOUD_SPAWN_INTERVAL_MIN, config.CLOUD_SPAWN_INTERVAL_MAX)
    while not glfw.window_should_close(window):
        current_time = time.time(); delta_time = current_time - last_time; last_time = current_time
        delta_time = min(delta_time, 0.1)
        update(delta_time); render(); glfw.poll_events()

    print("Encerrando..."); textures_to_delete = []
    if config.bird_texture_id: textures_to_delete.append(config.bird_texture_id)
    textures_to_delete.extend(loaded_powerup_textures)
    if config.trunk_texture_id: textures_to_delete.append(config.trunk_texture_id)
    if config.root_texture_id: textures_to_delete.append(config.root_texture_id)
    if config.ground_texture_id: textures_to_delete.append(config.ground_texture_id)
    textures_to_delete.extend(loaded_cloud_textures)
    if textures_to_delete:
        glfw.make_context_current(window)
        try: glDeleteTextures(textures_to_delete); print(f"Texturas deletadas: {textures_to_delete}")
        except Exception as e: print(f"Erro ao deletar texturas: {e}")
    glfw.terminate(); print("Aplicação encerrada.")

# --- Função Render ---
def render():
    glClearColor(0.53, 0.81, 0.92, 1.0); glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW); glLoadIdentity()

    # 1. Nuvens
    draw_clouds()

    # 2. Pipes
    if config.trunk_texture_id and config.root_texture_id:
         glEnable(GL_TEXTURE_2D); glColor4f(1.0, 1.0, 1.0, 1.0)
         draw_pipes(); glDisable(GL_TEXTURE_2D)
    else: glDisable(GL_TEXTURE_2D); draw_pipes(use_fallback_color=True)

    # 3. Ground
    if config.ground_texture_id:
        glEnable(GL_TEXTURE_2D); glColor4f(1.0, 1.0, 1.0, 1.0)
        glBindTexture(GL_TEXTURE_2D, config.ground_texture_id)
        # Passa os limites do config para draw_ground
        draw_ground(config.world_x_min, config.world_x_max); glBindTexture(GL_TEXTURE_2D, 0); glDisable(GL_TEXTURE_2D)
    else: glDisable(GL_TEXTURE_2D); draw_ground(use_fallback_color=True)

    # 4. Bird & Powerups
    glEnable(GL_TEXTURE_2D); glColor4f(1.0, 1.0, 1.0, 1.0)
    draw_bird(); draw_powerups(); glDisable(GL_TEXTURE_2D)

    # 5. UI
    draw_text(-0.95, 0.9, f"Score: {config.score}"); draw_text(-0.95, 0.8, f"Lives: {config.lives}")
    draw_text(-0.95, 0.7, f"High Score: {config.high_score}")
    status_y_start = 0.6; status_y_offset = -0.1; current_status_y = status_y_start
    current_time = time.time()
    if config.invulnerable:
        remaining_time = max(0, config.invulnerable_time - current_time)
        status_text = f"INVULNERABLE: {remaining_time:.1f}s";
        if config.speed_multiplier > 1.0: status_text = f"SPEED BOOST: {remaining_time:.1f}s"
        draw_text(-0.95, current_status_y, status_text); current_status_y += status_y_offset
    if config.chainsaw_active or config.chainsaw_deactivation_pending:
        pipes_left = config.chainsaw_pipes_remaining if not config.chainsaw_deactivation_pending else 0
        draw_text(-0.95, current_status_y, f"CHAINSAW: {pipes_left} pipes"); current_status_y += status_y_offset
    if config.heavy_jump_active:
        remaining_time = max(0, config.heavy_jump_end_time - current_time)
        draw_text(-0.95, current_status_y, f"HEAVY JUMP: {remaining_time:.1f}s"); current_status_y += status_y_offset
    if config.shrink_active:
        remaining_time = max(0, config.shrink_end_time - current_time)
        draw_text(-0.95, current_status_y, f"SHRUNK: {remaining_time:.1f}s")

    if config.game_over: draw_text(-0.4, 0.0, "GAME OVER! Press R to Restart")
    elif not config.game_started: draw_text(-0.5, 0.0, "Press SPACE to Start")

    glfw.swap_buffers(window)

# --- Callback de Redimensionamento ---
def window_size_callback(window, width, height):
    # --- ATUALIZA LIMITES NO CONFIG ---
    # global world_x_min, world_x_max, world_y_min, world_y_max # Não precisa mais ser global aqui
    if height == 0: height = 1
    glViewport(0, 0, width, height); glMatrixMode(GL_PROJECTION); glLoadIdentity()
    aspect_ratio = width / height
    if aspect_ratio >= 1.0: # Mais larga ou quadrada
        config.world_x_min, config.world_x_max = -aspect_ratio, aspect_ratio
        config.world_y_min, config.world_y_max = -1.0, 1.0
        glOrtho(config.world_x_min, config.world_x_max, config.world_y_min, config.world_y_max, -1.0, 1.0)
    else: # Mais alta
        config.world_x_min, config.world_x_max = -1.0, 1.0
        config.world_y_min, config.world_y_max = -1.0 / aspect_ratio, 1.0 / aspect_ratio
        glOrtho(config.world_x_min, config.world_x_max, config.world_y_min, config.world_y_max, -1.0, 1.0)
    # --- FIM ATUALIZAÇÃO ---
    print(f"Window Resized: World Coords X:({config.world_x_min:.2f}, {config.world_x_max:.2f}), Y:({config.world_y_min:.2f}, {config.world_y_max:.2f})")
    glMatrixMode(GL_MODELVIEW); glLoadIdentity()

if __name__ == "__main__": main()