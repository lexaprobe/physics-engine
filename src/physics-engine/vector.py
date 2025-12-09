import math


class Vector:
    x: float
    y: float

    def __init__(self, components: tuple[float, float]):
        self.x, self.y = components

    def __add__(self, other):
        if isinstance(other, Vector):
            x = self.x + other.x
            y = self.y + other.y
            return Vector((x, y))
        elif isinstance(other, (int, float)):
            return Vector((self.x + other, self.y + other))
        else:
            raise TypeError

    def __addi__(self, other):
        if isinstance(other, Vector):
            self.x += other.x
            self.y += other.y
        elif isinstance(other, (int, float)):
            self.x += other
            self.y += other
        else:
            raise TypeError

    def __sub__(self, other):
        if isinstance(other, Vector):
            x = self.x - other.x
            y = self.y - other.y
            return Vector((x, y))
        elif isinstance(other, (int, float)):
            return Vector((self.x - other, self.y - other))
        else:
            raise TypeError

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, (int, float)):
            return Vector((self.x * other, self.y * other))
        else:
            raise TypeError

    def __rmul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, (int, float)):
            return Vector((self.x * other, self.y * other))
        else:
            raise TypeError

    def __repr__(self):
        return f"{self.vector()}"

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def normalise(self):
        length = self.magnitude()
        if not length:
            return self.copy()
        return Vector((self.x / length, self.y / length))

    def vector(self) -> tuple[float, float]:
        return (self.x, self.y)

    def set(self, components: tuple[float, float]):
        self.x, self.y = components

    def copy(self):
        return Vector(self.vector())

    def add(self, vector):
        if not isinstance(vector, Vector):
            return None
        # add another vector to this vector
        self.x += vector.x
        self.y += vector.y

    def sub(self, vector):
        if not isinstance(vector, Vector):
            return None
        # subtract a vector from this vector
        self.x -= vector.x
        self.y -= vector.y

    def scale(self, value: int | float):
        # scale this vector by some value
        self.x = self.x * value
        self.y = self.y * value

    def dot(self, vector):
        if not isinstance(vector, Vector):
            return None
        # compute the dot product of two vectors
        return self.x * vector.x + self.y * vector.y
