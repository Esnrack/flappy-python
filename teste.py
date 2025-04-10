from OpenGL.GL import *
from OpenGL.GLUT import *  # <-- Import necessário para texto
import glfw
import numpy as np
import time
import random

# Configurações iniciais
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
BIRD_X, BIRD_Y = -0.5, 0.0
BIRD_SIZE = 0.05
GRAVITY = -0.9
JUMP_STRENGTH = 0.5
PIPE_WIDTH = 0.1
PIPE_GAP = 0.35
PIPE_SPEED = 0.5
INITIAL_LIVES = 3
PIPE_SPAWN_INTERVAL = 1.5

# Variáveis globais
bird_velocity = 0.0
game_started = False
game_over = False
lives = INITIAL_LIVES
score = 0
last_pipe_time = 0
pipes = []
powerups = []
speed_multiplier = 1.0
invulnerable = False
invulnerable_time = 0

class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.size = 0.05
        self.collected = False

def draw_bird():
    if invulnerable and int(time.time() * 2) % 2 == 0:
        return

    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(BIRD_X, BIRD_Y)
    for i in range(9):
        angle = i * 2 * np.pi / 8
        glVertex2f(BIRD_X + np.cos(angle) * BIRD_SIZE, BIRD_Y + np.sin(angle) * BIRD_SIZE)
    glEnd()

    glColor3f(0.0, 0.0, 0.0)
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(BIRD_X + BIRD_SIZE * 0.3, BIRD_Y + BIRD_SIZE * 0.2)
    glEnd()

def draw_pipes():
    for pipe in pipes:
        glColor3f(0.0, 0.8, 0.0)
        glBegin(GL_QUADS)
        glVertex2f(pipe['x'], 1.0)
        glVertex2f(pipe['x'] + PIPE_WIDTH, 1.0)
        glVertex2f(pipe['x'] + PIPE_WIDTH, pipe['top_height'])
        glVertex2f(pipe['x'], pipe['top_height'])
        glEnd()

        glBegin(GL_QUADS)
        glVertex2f(pipe['x'], pipe['bottom_height'])
        glVertex2f(pipe['x'] + PIPE_WIDTH, pipe['bottom_height'])
        glVertex2f(pipe['x'] + PIPE_WIDTH, -1.0)
        glVertex2f(pipe['x'], -1.0)
        glEnd()

def draw_powerups():
    for powerup in powerups:
        if not powerup.collected:
            glColor3f(1.0, 0.0, 0.0) if powerup.type == 'life' else glColor3f(0.0, 0.0, 1.0)
            glBegin(GL_QUADS)
            glVertex2f(powerup.x - powerup.size, powerup.y - powerup.size)
            glVertex2f(powerup.x + powerup.size, powerup.y - powerup.size)
            glVertex2f(powerup.x + powerup.size, powerup.y + powerup.size)
            glVertex2f(powerup.x - powerup.size, powerup.y + powerup.size)
            glEnd()

def draw_ground():
    glColor3f(0.6, 0.3, 0.1)
    glBegin(GL_QUADS)
    glVertex2f(-1.0, -0.9)
    glVertex2f(1.0, -0.9)
    glVertex2f(1.0, -1.0)
    glVertex2f(-1.0, -1.0)
    glEnd()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(0.0, 0.0, 0.0)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))

def check_collision():
    global lives, game_over, invulnerable, invulnerable_time, speed_multiplier

    if BIRD_Y - BIRD_SIZE < -0.9 or BIRD_Y + BIRD_SIZE > 1.0:
        if not invulnerable:
            handle_collision()
        return

    for pipe in pipes:
        if (pipe['x'] < BIRD_X + BIRD_SIZE and
            pipe['x'] + PIPE_WIDTH > BIRD_X - BIRD_SIZE and
            (BIRD_Y - BIRD_SIZE < pipe['bottom_height'] or
             BIRD_Y + BIRD_SIZE > pipe['top_height'])):
            if not invulnerable:
                handle_collision()
            return

    for powerup in powerups:
        if (not powerup.collected and
            abs(BIRD_X - powerup.x) < (BIRD_SIZE + powerup.size) and
            abs(BIRD_Y - powerup.y) < (BIRD_SIZE + powerup.size)):

            powerup.collected = True
            if powerup.type == 'life':
                lives = min(lives + 1, INITIAL_LIVES * 2)
            else:
                speed_multiplier = 2.0
                invulnerable = True
                invulnerable_time = time.time() + 3

def handle_collision():
    global lives, game_over, BIRD_Y, bird_velocity, invulnerable, invulnerable_time

    lives -= 1
    if lives <= 0:
        game_over = True
    else:
        BIRD_Y = 0.0
        bird_velocity = 0.0
        invulnerable = True
        invulnerable_time = time.time() + 2

def update_pipes(delta_time):
    global pipes, score, last_pipe_time, powerups

    for pipe in pipes:
        pipe['x'] -= PIPE_SPEED * speed_multiplier * delta_time

    pipes = [pipe for pipe in pipes if pipe['x'] + PIPE_WIDTH > -1.0]

    current_time = time.time()
    if current_time - last_pipe_time > PIPE_SPAWN_INTERVAL / speed_multiplier and game_started and not game_over:
        height = random.uniform(0.2, 0.6)
        pipes.append({
            'x': 1.0,
            'top_height': height + PIPE_GAP,
            'bottom_height': height
        })

        if random.random() < 0.2:
            powerups.append(PowerUp(
                1.0,
                random.uniform(-0.7, 0.7),
                'life' if random.random() < 0.7 else 'speed'
            ))

        last_pipe_time = current_time
        score += 1

    for powerup in powerups:
        powerup.x -= PIPE_SPEED * speed_multiplier * delta_time

    powerups = [p for p in powerups if not (p.x + p.size < -1.0 or p.collected)]

def update(delta_time):
    global BIRD_Y, bird_velocity, invulnerable, speed_multiplier

    if not game_started or game_over:
        return

    bird_velocity += GRAVITY * delta_time
    BIRD_Y += bird_velocity * delta_time
    update_pipes(delta_time)
    check_collision()

    current_time = time.time()
    if invulnerable and current_time > invulnerable_time:
        invulnerable = False
        if speed_multiplier > 1.0:
            speed_multiplier = 1.0

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.53, 0.81, 0.92, 1.0)

    draw_pipes()
    draw_powerups()
    draw_ground()
    draw_bird()

    draw_text(-0.95, 0.9, f"Score: {score}")
    draw_text(-0.95, 0.8, f"Lives: {lives}")
    if speed_multiplier > 1:
        draw_text(-0.95, 0.7, f"SPEED BOOST: {int(invulnerable_time - time.time())}s")

    if game_over:
        draw_text(-0.4, 0.0, "GAME OVER! Pressione R para reiniciar")

    glfw.swap_buffers(window)

def key_callback(window, key, scancode, action, mods):
    global bird_velocity, game_started, game_over, lives, score, pipes, powerups, last_pipe_time
    global BIRD_Y, invulnerable, speed_multiplier

    if action == glfw.PRESS:
        if key == glfw.KEY_SPACE:
            if not game_started:
                game_started = True
                last_pipe_time = time.time()
            if not game_over:
                bird_velocity = JUMP_STRENGTH

        if key == glfw.KEY_R and game_over:
            game_over = False
            game_started = False
            lives = INITIAL_LIVES
            score = 0
            pipes.clear()
            powerups.clear()
            BIRD_Y = 0.0
            bird_velocity = 0.0
            invulnerable = False
            speed_multiplier = 1.0
            last_pipe_time = 0

def main():
    global window

    if not glfw.init():
        return

    glutInit()  # Necessário para funções GLUT

    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Flappy Bird", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    glOrtho(-1, 1, -1, 1, -1, 1)
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
