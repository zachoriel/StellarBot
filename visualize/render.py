import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from simulation.stellarbot_env import StellarBotEnv

def draw_frame(env: StellarBotEnv, ax_sim, ax_graph):
    ax_sim.clear()
    ax_graph.clear()
    
    ax_sim.set_aspect('equal')
    ax_sim.set_xlim(-7000, 7000)
    ax_sim.set_ylim(-7000, 7000)
    ax_sim.set_title(f"StellarBot Simulation — Step {env.step_count}")
    
    # Plot grid tiles
    tiles = env.grid.all_tile_positions()
    covered = set()
    for sat in env.satellites:
        covered.update(sat.covered_tiles(env.grid))
        
    for row in range(env.grid.height):
        for col in range(env.grid.width):
            x, y = tiles[row, col]
            color = 'blue' if (row, col) in covered else 'lightgray'
            ax_sim.plot(x, y, '.', color=color, markersize=2)
            
    # Plot satellites and coverage circles
    for sat in env.satellites:
        x, y = sat.position()
        ax_sim.plot(x, y, 'ro', markersize=6)
        ax_sim.text(x + 150, y + 150, f"S{sat.id}", fontsize=8, color='black')
        
        coverage_circle = patches.Circle(
            (x, y), radius=sat.coverage_radius,
            color='blue', alpha=0.1
        )
        ax_sim.add_patch(coverage_circle)
        
    # Add legend
    legend_elements = [
        patches.Patch(color='lightgray', label='Uncovered Tile'),
        patches.Patch(color='blue', label='Covered Tile'),
        patches.Patch(color='red', label='Satellite'),
        patches.Patch(color='blue', alpha=0.1, label='Coverage Radius')
    ]
    ax_sim.legend(handles=legend_elements, loc='lower left', fontsize=8)
    
    # Plot coverage %
    steps = list(range(1, env.step_count + 1))
    ax_graph.plot(steps, env.coverage_log, color='green')
    ax_graph.set_ylim(0, 100)
    ax_graph.set_xlim(0, max(50, env.step_count + 1))
    ax_graph.set_xlabel("Step")
    ax_graph.set_ylabel("Coverage (%)")
    ax_graph.set_title("Earth Coverage Over Time")
    ax_graph.grid(True)
        
def run_animation(steps=50, delay=0.01):
    env = StellarBotEnv(num_sats=6)
    
    fig, (ax_sim, ax_graph) = plt.subplots(1, 2, figsize=(14, 7))
    
    for _ in range(steps):
        draw_frame(env, ax_sim, ax_graph)
        env.step()
        plt.pause(delay)
        
    plt.show()
    
if __name__ == "__main__":
    run_animation()
