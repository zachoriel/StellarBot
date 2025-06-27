# StellarBot

## MVP Assumptions:
- Circular orbits
- Ignore complex perturbations
- Earth kept at origin point
- Earth is a 2D circle (flattened globe)
- We use a lat/lon-style grid, simplified into an equirectangular projection
- Coverage is a circular radius in Carestian space (not geodetic)
- Grid tiles are fixed-size, and we compute coverage by Euclidean distance in (x, y) space
