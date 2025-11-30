import math


class Atom:
    # unchanging
    _mass: float
    _radius: float

    # dynamic
    x: float
    y: float
    x_vel: float
    y_vel: float
    _colour = (255, 255, 255)

    def __init__(
        self,
        mass: float,
        radius: float,
        pos: tuple[float, float],
        vel: tuple[float, float] = (0, 0),
    ):
        self._mass = mass
        self._radius = radius
        self.x = pos[0]
        self.y = pos[1]
        self.x_vel = vel[0]
        self.y_vel = vel[1]

    def pos(self) -> tuple[float, float]:
        return (self.x, self.y)

    def vel(self) -> tuple[float, float]:
        return (self.x_vel, self.y_vel)

    def mass(self) -> float:
        return self._mass

    def radius(self) -> float:
        return self._radius

    def get_normalised_vector(self) -> tuple[float, float]:
        magnitude = math.sqrt((self.x_vel**2) + (self.y_vel**2))
        return (self.x_vel / magnitude, self.y_vel / magnitude)

    def colour(self) -> tuple[int, int, int]:
        return self._colour

    def paint(self, rgb: tuple[int, int, int]):
        for val in rgb:
            if val > 255 or val < 0:
                raise ValueError
        self._colour = rgb
