from simulation.orbit_sim import Satellite as OrbitSatellite
from simulation.coverage_grid import EarthGrid

class SatelliteAgent:
    def __init__(self, sat_id: int, altitude_km: float, angular_speed_deg: float, phase_deg: float, coverage_radius_km: float):
        """
        A satellite agent with unique ID and coverage logic.
        
        :param sat_id: Unique identifier
        :param altitude_km: Orbit radius
        :param angular_speed_deg: SPeed in deg/timestep
        :param phase_deg: Initial angle
        :param coverage_radius_km: Radius of Earth surface covered
        """
        self.id = sat_id
        self.coverage_radius = coverage_radius_km
        self.orbit = OrbitSatellite(altitude_km, angular_speed_deg, phase_deg)
        
    def step(self):
        """
        Advance satellite in its orbit.
        """
        self.orbit.step()
        
    def position(self):
        """
        Current (x, y) position in orbit.
        """
        return self.orbit.position()
    
    def covered_tiles(self, earth_grid: EarthGrid):
        """
        Returns list of (row, col) tiles currently covered on the grid.
        """
        pos = self.position()
        return earth_grid.covered_tiles(pos, self.coverage_radius)
    
    def __repr__(self):
        pos = self.position()
        return f"Satellite {self.id} at ({pos[0]:.1f}, {pos[1]:.1f})"
  
# TEST  
# if __name__ == "__main__":
#     from coverage_grid import EarthGrid
    
#     grid = EarthGrid(width=36, height=18)
#     sat = SatelliteAgent(sat_id=1, altitude_km=7000, angular_speed_deg=15, phase_deg=90, coverage_radius_km=2500)
    
#     for t in range(3):
#         print(f"Time {t}: {sat}")
#         covered = sat.covered_tiles(grid)
#         print(f"  Covers {len(covered)} tiles")
#         sat.step()
    