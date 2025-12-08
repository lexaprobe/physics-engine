import math


class Vector:
    x: float
    y: float

    def __init__(self, components: tuple[float, float]):
        self.x, self.y = components

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def vector(self) -> tuple[float, float]:
        return (self.x, self.y)

    def set(self, components: tuple[float, float]):
        self.x, self.y = components

    def add(self, vector):
        if not isinstance(vector, Vector):
            return None
        # add this vector to another vector
        self.x += vector.x
        self.y += vector.y

    def scale(self, value: float):
        # scale this vector by some value
        self.x = self.x * value
        self.y = self.y * value

    def dot(self, vector):
        if not isinstance(vector, Vector):
            return None
        # compute the dot product of two vectors
        return self.x * vector.x + self.y * vector.y


class Atom:
    # unchanging
    _mass: float
    _radius: float

    # dynamic
    prev_pos: Vector
    pos: Vector
    vel: Vector
    acc: Vector = Vector((0, 0))
    collided = False
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
        self.vel = Vector(vel)

    def step(self, dt: float):
        x, y = self.position()
        x_vel, y_vel = self.velocity()
        x_acc, y_acc = self.acceleration()
        x += x_vel * dt + 0.5 * x_acc * dt**2
        y += y_vel * dt + 0.5 * y_acc * dt**2
        x_vel += x_acc * dt
        y_vel += y_acc * dt
        self.pos.set((x, y))
        self.vel.set((x_vel, y_vel))

    def accelerate(self, values: tuple[float, float]):
        self.acc.set(values)

    def distance_from(self, atom) -> float:
        if not isinstance(atom, Atom):
            raise TypeError
        x1, y1 = self.position()
        x2, y2 = atom.position()
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return dist

    def position(self) -> tuple[float, float]:
        return self.pos.vector()

    def velocity(self) -> tuple[float, float]:
        return self.vel.vector()

    def acceleration(self) -> tuple[float, float]:
        return self.acc.vector()

    def radius(self) -> float:
        return self._radius

    def mass(self) -> float:
        return self._mass

    def momentum(self) -> float:
        return self.vel.magnitude() * self._mass

    def kinetic_energy(self) -> float:
        return 0.5 * self._mass * self.vel.magnitude()

    def colour(self) -> tuple[int, int, int]:
        return self._colour

    def paint(self, rgb: tuple[int, int, int]):
        for val in rgb:
            if val > 255 or val < 0:
                raise ValueError
        self._colour = rgb
