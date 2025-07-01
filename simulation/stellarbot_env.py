from simulation.satellite import SatelliteAgent
from simulation.coverage_grid import EarthGrid
import time

class StellarBotEnv:
    def __init__(self, num_sats=3, grid_width=36, grid_height=18):
        self.grid = EarthGrid(grid_width, grid_height)
        self.satellites = self._init_satellites(num_sats)
        self.step_count = 0
        self.coverage_log = []
        
    def _init_satellites(self, num_sats):
        sats = []
        shared_start = time.perf_counter()
        for i in range(num_sats):
            phase = (360 / num_sats) * i  # Evenly spaced
            sats.append(SatelliteAgent(
                sat_id=i,
                altitude_km=7000,
                angular_speed_deg_per_sec=15,
                phase_deg=phase,
                coverage_radius_km=2500,
                start_time=shared_start
            ))
        return sats
    
    def step(self):
        """
        Advance all satellites, compute coverage, and return stats.
        """
        self.step_count += 1
        all_covered = set()
        
        for sat in self.satellites:
            sat.step()
            tiles = sat.covered_tiles(self.grid)
            all_covered.update(tiles)
            
        coverage_percent = 100 * len(all_covered) / (self.grid.height * self.grid.width)
        self.coverage_log.append(coverage_percent)
        
        return {
            "step": self.step_count,
            "coverage_tiles": len(all_covered),
            "coverage_percent": coverage_percent
        }
        
    def reset(self):
        """
        Restart the environment.
        """
        self.satellites = self._init_satellites(len(self.satellites))
        self.step_count = 0
        self.coverage_log = []
        
    def get_satellite_positions(self):
        """
        Returns current (x, y) positions of all satellites.
        """
        return [sat.position() for sat in self.satellites]
    