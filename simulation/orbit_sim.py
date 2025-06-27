import numpy as np

class Satellite:
    def __init__(self, altitude_km: float, angular_speed_deg: float, phase_deg: float = 0.0):
        """       
        Represents a satellite in circular 2D orbit.
        
        :param altitude_km: Distance from Earth's center (in km)
        :param angular_speed_deg: Orbital speed in degrees per timestep
        :param phase_deg: Initial angle (0-360 degrees)
        """
        self.altitude = altitude_km
        self.angle = phase_deg % 360
        self.speed = angular_speed_deg
        
    def step(self):
        """
        Advance the satellite's position by one timestep.
        """
        self.angle = (self.angle + self.speed) % 360
        
    def position(self) -> tuple[float, float]:
        """
        Return (x, y) position in 2D Cartesian space.
        """
        theta = np.radians(self.angle)
        x = self.altitude * np.cos(theta)
        y = self.altitude * np.sin(theta)
        return x, y
    
    def __repr__(self):
        return f"Satellite(alt={self.altitude}km, angle={self.angle:.2f} deg, speed={self.speed} deg/step)"
    
# TEST
# if __name__ == "__main__":
#     sats = [
#         Satellite(altitude_km=7000, angular_speed_deg=10, phase_deg=0),
#         Satellite(altitude_km=7000, angular_speed_deg=10, phase_deg=120),
#         Satellite(altitude_km=7000, angular_speed_deg=10, phase_deg=240)
#     ]
    
#     for t in range(5):
#         print(f"Time step {t}")
#         for s in sats:
#             print(f"  {s} -> Position: {s.position()}")
#             s.step()
