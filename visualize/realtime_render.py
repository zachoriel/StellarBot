import pygame
import sys
import time
import math
from simulation.stellarbot_env import StellarBotEnv

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
SCALE = 0.05  # km to pixels (adjust to fit 7000 km radius on screen)
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
BLUE = (50, 100, 255)
LIGHT_BLUE = (100, 150, 255)

# Initialize PyGame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("StellarBot Real-Time Visualization")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Simulation Environment
env = StellarBotEnv(num_sats=6)
sim_start = time.perf_counter()
running = True
paused = False
show_ids = True
show_coverage_percent = True

# Buttons
button_font = pygame.font.SysFont(None, 24)
pause_button = pygame.Rect(20, 20, 100, 30)

# Main Loop
while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pause_button.collidepoint(event.pos):
                paused = not paused
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                show_ids = not show_ids
            if event.key == pygame.K_c:
                show_coverage_percent = not show_coverage_percent

    if paused:
        continue

    elapsed = time.perf_counter() - sim_start
    screen.fill(BLACK)

    # Draw Earth boundary
    earth_radius_px = int(env.grid.radius * SCALE)
    pygame.draw.circle(screen, GRAY, (CENTER_X, CENTER_Y), earth_radius_px, width=1)

    # Determine coverage
    tiles = env.grid.all_tile_positions()
    covered = set()
    for sat in env.satellites:
        pos = sat.position()
        covered.update(env.grid.covered_tiles(pos, sat.coverage_radius))

    # Draw tiles
    for row in range(env.grid.height):
        for col in range(env.grid.width):
            x_km, y_km = tiles[row, col]
            x_px = int(CENTER_X + x_km * SCALE)
            y_px = int(CENTER_Y - y_km * SCALE)
            color = LIGHT_BLUE if (row, col) in covered else GRAY
            dist = math.sqrt(x_km**2 + y_km**2)
            if dist <= env.grid.radius:
                pygame.draw.circle(screen, color, (x_px, y_px), 2)

    # Draw satellites
    for sat in env.satellites:
        x_km, y_km = sat.position()
        x_px = int(CENTER_X + x_km * SCALE)
        y_px = int(CENTER_Y - y_km * SCALE)

        pygame.draw.circle(screen, RED, (x_px, y_px), 4)

        if show_ids:
            label = font.render(f"S{sat.id}", True, WHITE)
            screen.blit(label, (x_px + 6, y_px - 6))

        radius_px = int(sat.coverage_radius * SCALE)
        pygame.draw.circle(screen, BLUE, (x_px, y_px), radius_px, width=1)

    # Draw overlays
    if show_coverage_percent:
        coverage_percent = 100 * len(covered) / (env.grid.width * env.grid.height)
        coverage_text = font.render(f"Coverage: {coverage_percent:.1f}%", True, WHITE)
        screen.blit(coverage_text, (SCREEN_WIDTH - 200, 20))

    # Draw buttons
    pygame.draw.rect(screen, GRAY, pause_button)
    pause_label = button_font.render("Pause" if not paused else "Resume", True, BLACK)
    screen.blit(pause_label, (pause_button.x + 10, pause_button.y + 5))

    pygame.display.flip()

pygame.quit()
sys.exit()
