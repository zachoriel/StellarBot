import pygame
import sys
import time
import math
from collections import deque, defaultdict
from simulation.stellarbot_env import StellarBotEnv

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
SCALE = 0.05
FPS = 60
MAX_TRAIL_LENGTH = 120

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
BLUE = (50, 100, 255)
LIGHT_BLUE = (100, 150, 255)
HEAT_COLOR = (255, 165, 0)

HEAT_GAIN = 0.1
HEAT_DECAY = 0.98

# Setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("StellarBot Real-Time Visualization")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Slider class for the control panel UI
class Slider:
    def __init__(self, x, y, width, min_val, max_val, value):
        self.rect = pygame.Rect(x, y, width, 10)
        self.min_val = min_val
        self.max_val = max_val
        self.value = value
        self.knob_radius = 8
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.get_knob_rect().collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel_x = event.pos[0] - self.rect.x
            pct = min(1.0, max(0.0, rel_x / self.rect.width))
            self.value = self.min_val + pct * (self.max_val - self.min_val)

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        knob_x = self.rect.x + (self.rect.width * (self.value - self.min_val) / (self.max_val - self.min_val))
        knob_y = self.rect.y + self.rect.height // 2
        pygame.draw.circle(surface, WHITE, (int(knob_x), int(knob_y)), self.knob_radius)

    def get_knob_rect(self):
        knob_x = self.rect.x + (self.rect.width * (self.value - self.min_val) / (self.max_val - self.min_val))
        knob_y = self.rect.y + self.rect.height // 2
        return pygame.Rect(knob_x - self.knob_radius, knob_y - self.knob_radius, self.knob_radius * 2, self.knob_radius * 2)
    
# Buttons
toggle_button = pygame.Rect(20, 10, 130, 25)
trail_button = pygame.Rect(60, 220, 100, 30)
heatmap_button = pygame.Rect(180, 220, 100, 30)

# Sliders
alt_slider = Slider(60, 70, 200, 5000, 10000, 7000)
cov_slider = Slider(60, 120, 200, 1000, 4000, 2500)

# Simulation Environment
def create_env(num_sats):
    env = StellarBotEnv(num_sats=num_sats)
    for sat in env.satellites.values():
        sat.orbit.altitude = int(alt_slider.value)
        sat.coverage_radius = int(cov_slider.value)
        sat.trail = deque(maxlen=MAX_TRAIL_LENGTH)
    return env

env = create_env(num_sats=6)
sim_start = time.perf_counter()
running = True
paused = False
show_ids = True
show_coverage_percent = True
show_trails = True
use_heatmap = False
show_controls = True

coverage_intensity = defaultdict(float)

# Simulation loop
while running:
    dt = clock.tick(FPS) / 1000.0
    
    # UI handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if toggle_button.collidepoint(event.pos):
                show_controls = not show_controls
            elif show_controls:
                if trail_button.collidepoint(event.pos):
                    show_trails = not show_trails
                elif heatmap_button.collidepoint(event.pos):
                    use_heatmap = not use_heatmap
        if show_controls:
            alt_slider.handle_event(event)
            cov_slider.handle_event(event)

    if paused:
        continue

    screen.fill(BLACK)

    # Draw Earth boundary
    earth_radius_px = int(env.grid.radius * SCALE)
    pygame.draw.circle(screen, GRAY, (CENTER_X, CENTER_Y), earth_radius_px, width=1)

    # Update satellite orbit data
    covered = set()
    for sat in env.satellites.values():
        pos = sat.position()
        sat.orbit.altitude = int(alt_slider.value)
        sat.coverage_radius = int(cov_slider.value)
        covered.update(env.grid.covered_tiles(pos, sat.coverage_radius))

    # Update heatmap coverage data
    for row in range(env.grid.height):
        for col in range(env.grid.width):
            key = (row, col)
            if key in covered:
                coverage_intensity[key] = min(1.0, coverage_intensity[key] + HEAT_GAIN)
            else:
                coverage_intensity[key] *= HEAT_DECAY

    # Draw tiles
    tiles = env.grid.all_tile_positions()
    for row in range(env.grid.height):
        for col in range(env.grid.width):
            x_km, y_km = tiles[row, col]
            dist = math.sqrt(x_km**2 + y_km**2)
            if dist > env.grid.radius:
                continue
            x_px = int(CENTER_X + x_km * SCALE)
            y_px = int(CENTER_Y - y_km * SCALE)
            if use_heatmap:
                intensity = coverage_intensity[(row, col)]
                color = (
                    int(HEAT_COLOR[0] * intensity),
                    int(HEAT_COLOR[1] * intensity),
                    int(HEAT_COLOR[2] * intensity)
                )
            else:
                color = LIGHT_BLUE if (row, col) in covered else GRAY
            pygame.draw.circle(screen, color, (x_px, y_px), 2)

    # Draw satellites
    for sat in env.satellites.values():
        x_km, y_km = sat.position()
        x_px = int(CENTER_X + x_km * SCALE)
        y_px = int(CENTER_Y - y_km * SCALE)
        sat.trail.append((x_px, y_px))
        if show_trails and len(sat.trail) > 1:
            pygame.draw.lines(screen, RED, False, list(sat.trail), width=1)
        pygame.draw.circle(screen, RED, (x_px, y_px), 4)
        if show_ids:
            label = font.render(f"S{sat.id}", True, WHITE)
            screen.blit(label, (x_px + 6, y_px - 6))
        radius_px = int(sat.coverage_radius * SCALE)
        pygame.draw.circle(screen, BLUE, (x_px, y_px), radius_px, width=1)

    # Update coverage percentage text
    if show_coverage_percent:
        coverage_percent = 100 * len(covered) / (env.grid.width * env.grid.height)
        coverage_text = font.render(f"Coverage: {coverage_percent:.1f}%", True, WHITE)
        screen.blit(coverage_text, (SCREEN_WIDTH - 200, 20))

    # Control Panel
    pygame.draw.rect(screen, GRAY, toggle_button)
    toggle_label = font.render("Control Panel", True, BLACK)
    toggle_rect = toggle_label.get_rect(center=toggle_button.center)
    screen.blit(toggle_label, toggle_rect)

    if show_controls:
        pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(10, 40, 300, 220))

        # Altitude slider
        altitude_label = font.render(f"Altitude: {int(alt_slider.value)} km", True, WHITE)
        altitude_rect = altitude_label.get_rect(centerx=alt_slider.rect.centerx)
        altitude_rect.top = alt_slider.rect.top - 20
        screen.blit(font.render(f"Altitude: {int(alt_slider.value)} km", True, WHITE), altitude_rect)
        
        # Coverage radius slider
        coverage_label = font.render(f"Coverage: {int(cov_slider.value)} km", True, WHITE)
        coverage_rect = coverage_label.get_rect(centerx=cov_slider.rect.centerx)
        coverage_rect.top = cov_slider.rect.top - 20
        screen.blit(font.render(f"Coverage: {int(cov_slider.value)} km", True, WHITE), coverage_rect)
        
        alt_slider.draw(screen)
        cov_slider.draw(screen)
        
        # Trails toggle button
        pygame.draw.rect(screen, GRAY, trail_button)
        trail_label = font.render("Trails", True, BLACK)
        trail_rect = trail_label.get_rect(center=trail_button.center)
        screen.blit(trail_label, trail_rect)
        
        # Heatmap toggle button
        pygame.draw.rect(screen, GRAY, heatmap_button)
        heatmap_label = font.render("Heatmap", True, BLACK)
        heatmap_rect = heatmap_label.get_rect(center=heatmap_button.center)
        screen.blit(heatmap_label, heatmap_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
