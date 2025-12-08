import math

from atom import Atom


class PhysicsEnvironment:
    """
    Define the physical laws for a PhysicsEngine.
    """

    _width: float
    _height: float
    _atoms: list[Atom]
    _gravity = 200.0
    _damping = 0.5

    def __init__(self, size: tuple[float, float]):
        self._width, self._height = size
        self._atoms = []

    def get_objects(self) -> list[Atom]:
        return self._atoms

    def add(self, atom: Atom):
        if atom is None:
            return
        self._atoms.append(atom)
        atom.accelerate((0, self._gravity))

    def remove(self, atom: Atom) -> bool:
        if atom is None or atom not in self._atoms:
            return False
        self._atoms.remove(atom)
        return True

    def update(self, dt: float, sub_steps: int = 1):
        sub_dt = dt / sub_steps
        for _ in range(sub_steps):
            self.apply_constraint()
            self.resolve_collisions()
            self.update_positions(sub_dt)

    def update_positions(self, dt: float):
        for atom in self._atoms:
            atom.step(dt)
            atom.collided = False

    def apply_constraint(self):
        for atom in self._atoms:
            r = atom.radius()
            x, y = atom.position()
            x_vel, y_vel = atom.velocity()
            collided = True
            if x + r >= self._width:
                x = self._width - r
                x_vel = -x_vel
            elif x - r <= 0:
                x = r
                x_vel = -x_vel
            elif y + r >= self._height:
                y = self._height - r
                y_vel = -y_vel
            elif y - r <= 0:
                y = r
                y_vel = -y_vel
            else:
                collided = False
            atom.pos.set((x, y))
            atom.vel.set((x_vel, y_vel))
            if collided:
                self.dampen_velocity(atom)

    def resolve_collisions(self):
        for a1 in self._atoms:
            for a2 in self._atoms:
                if a2 is a1:
                    continue
                # check if they collide
                distance = a1.distance_from(a2)
                overlap = (a1.radius() + a2.radius()) - distance
                if overlap > 0:
                    self.compute_collision(a1, a2)

    def compute_collision(self, a1: Atom, a2: Atom):
        if a1.collided or a2.collided:
            return
        n = (a2.pos.x - a1.pos.x, a2.pos.y - a1.pos.y)
        magnitude = math.sqrt(n[0] ** 2 + n[1] ** 2)
        un = (n[0] / magnitude, n[1] / magnitude)
        ut = (-un[1], un[0])
        v1n = un[0] * a1.vel.x + un[1] * a1.vel.y
        v1t = ut[0] * a1.vel.x + ut[1] * a1.vel.y
        v2n = un[0] * a2.vel.x + un[1] * a2.vel.y
        v2t = ut[0] * a2.vel.x + ut[1] * a2.vel.y
        # after collision
        v1n_prime = (v1n * (a1.mass() - a2.mass()) + (2 * a2.mass() * v2n)) / (
            a1.mass() + a2.mass()
        )
        v2n_prime = (v2n * (a2.mass() - a1.mass()) + (2 * a1.mass() * v1n)) / (
            a1.mass() + a2.mass()
        )
        a1.vel.set(
            (
                v1n_prime * un[0] + v1t * ut[0],
                v1n_prime * un[1] + v1t * ut[1],
            )
        )
        a2.vel.set(
            (
                v2n_prime * un[0] + v2t * ut[0],
                v2n_prime * un[1] + v2t * ut[1],
            )
        )
        a1.collided = True
        a2.collided = True

    def dampen_velocity(self, atom: Atom):
        atom.vel.scale(self._damping / atom.mass())

    def set_gravity(self, gravity: float):
        self._gravity = gravity
