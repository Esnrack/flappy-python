import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import time
import config
from player import draw_bird
from game_pipes import draw_pipes
from powerup import draw_powerups
from rendering import draw_ground, draw_text
from update import update
from input import key_callback

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.53, 0.81, 0.92, 1.0)

    draw_pipes()
    draw_powerups()
    draw_ground()
    draw_bird()

    draw_text(-0.95, 0.9, f"Score: {config.score}")
    draw_text(-0.95, 0.8, f"Lives: {config.lives}")
    if config.speed_multiplier > 1:
        draw_text(-0.95, 0.7, f"SPEED BOOST: {int(config.invulnerable_time - time.time())}s")

    if config.game_over:
        draw_text(-0.4, 0.0, "GAME OVER! Pressione R para reiniciar")

    glfw.swap_buffers(window)

def window_size_callback(window, width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect_ratio = width / height if height != 0 else 1
    if aspect_ratio >= 1:
        glOrtho(-aspect_ratio, aspect_ratio, -1, 1, -1, 1)
    else:
        glOrtho(-1, 1, -1/aspect_ratio, 1/aspect_ratio, -1, 1)
    glMatrixMode(GL_MODELVIEW)

def main():
    global window
    if not glfw.init():
        return

    glutInit()  # Necessário para funções GLUT

    window = glfw.create_window(config.WINDOW_WIDTH, config.WINDOW_HEIGHT, "Flappy Bird", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_window_size_callback(window, window_size_callback)

    glViewport(0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect_ratio = config.WINDOW_WIDTH / config.WINDOW_HEIGHT
    if aspect_ratio >= 1:
        glOrtho(-aspect_ratio, aspect_ratio, -1, 1, -1, 1)
    else:
        glOrtho(-1, 1, -1/aspect_ratio, 1/aspect_ratio, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    last_time = time.time()

    while not glfw.window_should_close(window):
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time

        update(delta_time)
        render()
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
