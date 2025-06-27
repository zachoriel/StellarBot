import numpy as np

class EarthGrid:
    def __init__(self, width: int, height: int, earth_radius_km: float = 6371.0):
        """
        Initializes a 2D grid over Earth's surface.

        :param width: Number of tiles along x (longitude)
        :param height: Number of tiles along y (latitude)
        :param earth_radius_km: Radius of Earth
        """
        self.width = width
        self.height = height
        self.radius = earth_radius_km
        self.tiles = self._generate_grid()
        
    def _generate_grid(self):
        """
        Generates (x, y) center points for each tile.
        Returns a 2D array of shape (height, width, 2).
        """
        xs = np.linspace(-self.radius, self.radius, self.width)
        ys = np.linspace(-self.radius, self.radius, self.height)
        grid = np.array([[(x, y) for x in xs] for y in ys])
        return grid
    
    def covered_tiles(self, sat_pos: tuple[float, float], coverage_radius_km: float) -> list[tuple[int, int]]:
        """
        Given a satellite position (x, y), return a list of (row, col) indices of tiles within coverage radius.
        """
        covered = []
        for row in range(self.height):
            for col in range(self.width):
                tile_x, tile_y = self.tiles[row, col]
                dx = tile_x - sat_pos[0]
                dy = tile_y - sat_pos[1]
                dist = np.sqrt(dx**2 + dy**2)
                if dist <= coverage_radius_km:
                    covered.append((row, col))
        return covered
    
    def all_tile_positions(self) -> np.ndarray:
        """
        Returns the full grid of tile center positions.
        """
        return self.tiles
    
    def grid_shape(self) -> tuple[int, int]:
        return (self.height, self.width)
    
# TEST
# if __name__ == "__main__":
#     grid = EarthGrid(width=36, height=18)
#     sat_x, sat_y = 2000, 1000  # Example satellite position
#     coverage_radius = 2500     # km
    
#     covered = grid.covered_tiles((sat_x, sat_y), coverage_radius)
#     print(f"Satellite at ({sat_x}, {sat_y}) covers {len(covered)} tiles.")
        