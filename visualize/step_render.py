import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import numpy as np
import time
from simulation.stellarbot_env import StellarBotEnv

class RealTimeSim:
    def __init__(self, physics_dt=0.1):
        self.env = StellarBotEnv(num_sats=6)
        self.fig, (self.ax_sim, self.ax_graph) = plt.subplots(1, 2, figsize=(14, 7))
        self.physics_dt = physics_dt
        self.last_physics_time = time.perf_counter()
        self.coverage_log = []
        self.phase = 0.0  # [0.0, 1.0] — how far we are between physics steps
        self.running = True
        
        self.fig.canvas.mpl_connect("key_press_event", self.on_keypress)
        
    def on_keypress(self, event):
        if event.key == "escape":
            print("Stopping simulation...")
            self.running = False
            
    def update_physics(self):
        for sat in self.env.satellites:
            sat.step(self.physics_dt)
            
    def update_frame(self, frame):
        if not self.running:
            plt.close(self.fig)
            return []
        
        # current_time = time.perf_counter()
        # elapsed = current_time - self.last_physics_time
        
        # if elapsed >= self.physics_dt:
        #     self.update_physics()
        #     self.last_physics_time = current_time
        #     self.phase = 0.0
        # else:
        #     self.phase = elapsed / self.physics_dt
            
        self.draw()
        return []
        
    def draw(self):
        self.ax_sim.clear()
        self.ax_sim.set_aspect('equal')
        self.ax_sim.set_xlim(-7000, 7000)
        self.ax_sim.set_ylim(-7000, 7000)
        self.ax_sim.set_title("StellarBot — Live Sim (ESC to stop)")
        
        tiles = self.env.grid.all_tile_positions()
        covered = set()
        for sat in self.env.satellites:
            pos = sat.position()
            covered.update(self.env.grid.covered_tiles(pos, sat.coverage_radius))
            
        # Draw tiles
        for row in range(self.env.grid.height):
            for col in range(self.env.grid.width):
                x, y = tiles[row, col]
                color = 'blue' if (row, col) in covered else 'lightgray'
                self.ax_sim.plot(x, y, '.', color=color, markersize=2)
                
        # Draw satellites
        for sat in self.env.satellites:
            x, y = sat.position()
            self.ax_sim.plot(x, y, 'ro', markersize=6)
            self.ax_sim.text(x + 150, y + 150, f"S{sat.id}", fontsize=8)
            coverage_circle = patches.Circle((x, y), radius=sat.coverage_radius, color='blue', alpha=0.1)
            self.ax_sim.add_patch(coverage_circle)
            
        # Update coverage graph
        coverage_percent = 100 * len(covered) / (self.env.grid.width * self.env.grid.height)
        self.coverage_log.append(coverage_percent)
        
        self.ax_graph.clear()
        self.ax_graph.plot(self.coverage_log, color='green')
        self.ax_graph.set_ylim(0, 100)
        self.ax_graph.set_xlim(0, max(50, len(self.coverage_log)))
        self.ax_graph.set_title("Coverage % Over Time")
        self.ax_graph.set_xlabel("Frame")
        self.ax_graph.set_ylabel("Coverage (%)")
        self.ax_graph.grid(True)
        
    def run(self):
        ani = animation.FuncAnimation(self.fig, self.update_frame, interval=16)
        plt.show()
        
if __name__ == "__main__":
    sim = RealTimeSim()
    sim.run()
