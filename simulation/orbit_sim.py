import numpy as np
import time

class Satellite:
    def __init__(self, altitude_km: float, angular_speed_deg_per_sec: float, phase_deg: float = 0.0, start_time: float = 0.0):
        """       
        Represents a satellite in circular 2D orbit.
        
        :param altitude_km: Distance from Earth's center (in km)
        :param angular_speed_deg_per_sec: Orbital speed in degrees per second
        :param phase_deg: Initial angle (0-360 degrees)
        """
        self.altitude = altitude_km
        self.speed = angular_speed_deg_per_sec
        self.phase = phase_deg % 360
        self.start_time = start_time if start_time is not None else time.perf_counter()
        
        # Stepped logic state (for RL training)
        self.angle_sim = self.phase
                
    def step(self, dt: float):
        """
        Step-based angle update (for physics/training use only).
        """
        self.angle_sim = (self.angle_sim + self.speed * dt) % 360
        
    def position(self) -> tuple[float, float]:
        """
        Real-time position based on wall clock (for rendering).
        """
        elapsed = time.perf_counter() - self.start_time
        angle = (self.phase + self.speed * elapsed) % 360
        theta = np.radians(angle)
        x = self.altitude * np.cos(theta)
        y = self.altitude * np.sin(theta)
        return x, y
    
    def stepped_position(self) -> tuple[float, float]:
        """
        Return the stepped angle position (used only during RL).
        """
        theta = np.radians(self.angle_sim)
        x = self.altitude * np.cos(theta)
        y = self.altitude * np.sin(theta)
        return x, y
