from simulation.orbit_sim import Satellite as OrbitSatellite
from simulation.coverage_grid import EarthGrid

class SatelliteAgent:
    def __init__(self, sat_id: int, altitude_km: float, angular_speed_deg_per_sec: float, phase_deg: float, coverage_radius_km: float, start_time: float):
        """
        A satellite agent with unique ID and coverage logic.
        
        :param sat_id: Unique identifier
        :param altitude_km: Orbit radius
        :param angular_speed_deg_per_sec: Speed in deg/second
        :param phase_deg: Initial angle
        :param coverage_radius_km: Radius of Earth surface covered
        """
        self.id = sat_id
        self.coverage_radius = coverage_radius_km
        self.orbit = OrbitSatellite(altitude_km, angular_speed_deg_per_sec, phase_deg, start_time)
                
    def step(self, dt: float = 1.0):
        """
        Advance satellite in its orbit.
        """
        self.orbit.step(dt)
        
    def position(self):
        """
        Current (x, y) position in orbit.
        """
        return self.orbit.position()
    
    def stepped_position(self):
        return self.orbit.stepped_position()
    