import math

from atom import Atom


class Container:
    """
    This class defines the physical laws for a PhysicsEngine.
    """

    _width: int
    _height: int
    _atoms: list[Atom]
    _gravity = 9.81

    def __init__(self, size: tuple[int, int]):
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

    def step(self, dt: float):
        for atom in self._atoms:
            # vel = v + a * dt
            # pos = p + v * dt
            atom.x += atom.x_vel * dt
            atom.y += atom.y_vel * dt
            atom.y_vel += self._gravity * dt
            r = atom.radius()
            if atom.x + r >= self._width:
                atom.x = self._width - r
                atom.x_vel = -atom.x_vel
            elif atom.x - r <= 0:
                atom.x = r
                atom.x_vel = -atom.x_vel
            elif atom.y + r >= self._height:
                atom.y = self._height - r
                atom.y_vel = -atom.y_vel
            elif atom.y - r <= 0:
                atom.y = r
                atom.y_vel = -atom.y_vel

    def resolve(self):
        for a1 in self._atoms:
            r1 = a1.radius()
            for a2 in self._atoms:
                if a1 == a2:
                    continue
                r2 = a2.radius()
                distance = math.sqrt((a2.x - a1.x) ** 2 + (a2.y - a1.y) ** 2)
                overlap = distance - (r1 + r2)
                if overlap > 0:
                    a1_norm_x, a1_norm_y = a1.get_normalised_vector()
                    a1.x -= a1_norm_x * (overlap / 2)
                    a1.y -= a1_norm_y * (overlap / 2)
                    a1.x_vel = -a1.x_vel
                    a1.y_vel = -a1.y_vel
                    a2_norm_x, a2_norm_y = a2.get_normalised_vector()
                    a2.x -= a2_norm_x * (overlap / 2)
                    a2.y -= a2_norm_y * (overlap / 2)
                    a2.x_vel = -a2.x_vel
                    a2.y_vel = -a2.y_vel

    def set_gravity(self, gravity: float):
        self._gravity = gravity
