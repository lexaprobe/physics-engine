import math

from vector import Vector


class Atom:
    # unchanging
    _mass: float
    _radius: float

    # dynamic
    pos: Vector
    prev_pos: Vector
    _force: Vector = Vector((0, 0))
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
        self.pos = Vector(pos)
        self.prev_pos = self.pos - Vector(vel)

    def step(self, dt: float):
        vel = self.velocity()
        self.prev_pos = self.pos.copy()
        self.pos = self.pos + vel + self._force * dt * dt

    def apply_force(self, values: tuple[float, float]):
        self._force.set(values)

    def distance_from(self, atom) -> float:
        if not isinstance(atom, Atom):
            raise TypeError
        x1, y1 = self.position()
        x2, y2 = atom.position()
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return dist

    def position(self) -> tuple[float, float]:
        return self.pos.vector()

    def velocity(self) -> Vector:
        return self.pos - self.prev_pos

    def force(self) -> tuple[float, float]:
        return self._force.vector()

    def radius(self) -> float:
        return self._radius

    def mass(self) -> float:
        return self._mass

    def colour(self) -> tuple[int, int, int]:
        return self._colour

    def paint(self, rgb: tuple[int, int, int]):
        for val in rgb:
            if val > 255 or val < 0:
                raise ValueError
        self._colour = rgb
