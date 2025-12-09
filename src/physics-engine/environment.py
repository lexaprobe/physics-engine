from atom import Atom
from vector import Vector


class PhysicsBox:
    """
    Define the physical laws for a PhysicsEngine.
    """

    _width: float
    _height: float
    _atoms: list[Atom]
    _gravity = (0.0, 500.0)
    _damping = 0.9

    def __init__(self, size: tuple[float, float]):
        self._width, self._height = size
        self._atoms = []

    def get_objects(self) -> list[Atom]:
        return self._atoms

    def add(self, atom: Atom):
        if atom is None:
            return
        self._atoms.append(atom)

    def remove(self, atom: Atom) -> bool:
        if atom is None or atom not in self._atoms:
            return False
        self._atoms.remove(atom)
        return True

    def clear(self):
        self._atoms = []

    def update(self, dt: float, sub_steps: int = 1):
        sub_dt = dt / sub_steps
        for _ in range(sub_steps):
            self.apply_gravity()
            self.update_atoms(sub_dt)
            self.resolve_collisions()
            self.apply_constraint()

    def apply_gravity(self):
        for atom in self._atoms:
            atom.apply_force(self._gravity)

    def update_atoms(self, dt: float):
        for atom in self._atoms:
            atom.step(dt)

    def resolve_collisions(self):
        for a1 in self._atoms:
            for a2 in self._atoms:
                if a2 is a1:
                    continue
                # check if they collide
                delta = a2.pos - a1.pos
                distance = delta.magnitude()
                overlap = (a1.radius() + a2.radius()) - distance
                if overlap > 0:
                    correction = delta.normalise() * (overlap / 2)
                    a1.pos -= correction
                    a2.pos += correction

    def apply_constraint(self):
        for atom in self._atoms:
            if not isinstance(atom, Atom):
                continue
            x, y, r = atom.pos.x, atom.pos.y, atom.radius()
            if x + r > self._width:
                vel = atom.velocity()
                atom.pos.set((self._width - r, y))
                vel.x *= -self._damping
                atom.prev_pos = atom.pos - vel
            elif x - r < 0:
                vel = atom.velocity()
                atom.pos.set((r, y))
                vel.x *= -self._damping
                atom.prev_pos = atom.pos - vel
            if y + r > self._height:
                vel = atom.velocity()
                atom.pos.set((x, self._height - r))
                vel.y *= -self._damping
                atom.prev_pos = atom.pos - vel
            elif y - r < 0:
                vel = atom.velocity()
                atom.pos.set((x, r))
                vel.y *= -self._damping
                atom.prev_pos = atom.pos - vel

    def set_gravity(self, gravity: tuple[float, float]):
        self._gravity = gravity


class PhysicsCircle(PhysicsBox):
    _radius: float

    def __init__(self, size: tuple[float, float], radius: float):
        super().__init__(size)
        if radius > self._height / 2 or radius > self._width / 2:
            raise TypeError("radius value too large for environment size")
        self._radius = radius

    def centre(self) -> Vector:
        return Vector((self._width / 2, self._height / 2))

    def radius(self) -> float:
        return self._radius

    def in_bounds(self, pos: tuple[float, float], radius: float) -> bool:
        origin = Vector(pos) - self.centre()
        if origin.magnitude() > self._radius - radius:
            return False
        return True

    def apply_constraint(self):
        centre = self.centre()
        for atom in self._atoms:
            to_atom = atom.pos - centre
            dist = to_atom.magnitude()
            if dist > self._radius - atom.radius():
                to_atom.scale(1 / dist)
                atom.pos = centre + (to_atom * (self._radius - atom.radius()))
