import colorsys
import random

import pygame
from atom import Atom
from environment import PhysicsBox, PhysicsCircle


class Engine:
    # engine configuration
    win_width: int
    win_height: int
    win_colour: tuple[int, int, int]
    circular_env: bool = False
    fps: int

    # engine settings
    obj_limit: int | None
    auto: bool = False
    cycle_colours: bool = False
    random_radius: bool = False
    constant_velocity: bool = False

    # private attributes
    _env: PhysicsCircle | PhysicsBox
    _obj_hue = 0
    _spawn_angle = 0
    _vmax: int = 500
    _default_radius: float = 15
    _default_velocity: tuple[float, float]

    def __init__(
        self,
        size: tuple[int, int] = (1000, 1000),
        background: tuple[int, int, int] = (0, 0, 0),
        obj_limit: int | None = None,
        fps: int = 60,
    ):
        self.win_width, self.win_height = size
        self.win_colour = background
        self.obj_limit = obj_limit
        self.fps = fps

    def simulate(self, caption: str = "Physics Engine"):
        pygame.init()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 18)
        window = pygame.display.set_mode(self.window_size())
        pygame.display.set_caption(caption)
        clock = pygame.time.Clock()
        if self.circular_env:
            self._env = PhysicsCircle(self.window_size(), self.win_width / 2.5)
        else:
            self._env = PhysicsBox(self.window_size())
        obj_count = 0
        frames = 0
        pause = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self._manual_valid(obj_count, pause):
                        coords = pygame.mouse.get_pos()
                        radius = self.get_object_radius()
                        if not self.circular_env or (
                            self.circular_env
                            and isinstance(self._env, PhysicsCircle)
                            and self._env.in_bounds(coords, radius)
                        ):
                            self.spawn_object(coords, radius)
                            obj_count += 1
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self._env.clear()
                        obj_count = 0
                    elif event.key == pygame.K_p:
                        pause = not pause
                        continue
            if self._auto_valid(obj_count, frames, pause):
                self.spawn_object(self.centre(), self.get_object_radius())
                obj_count += 1
            if not pause:
                self._env.update(1 / self.fps, sub_steps=2)
            if self.circular_env and isinstance(self._env, PhysicsCircle):
                window.fill(pygame.Color("GRAY"))
                pygame.draw.circle(
                    window,
                    self.win_colour,
                    self._env.centre().vector(),
                    self._env.radius(),
                )
            else:
                window.fill(self.win_colour)
            self.draw_objects(window)
            fps = f"FPS: {int(clock.get_fps())}"
            fps_text = font.render(fps, 1, pygame.Color("BLACK"))
            obj_text = font.render(f"Objects: {obj_count}", 1, pygame.Color("BLACK"))
            window.blit(fps_text, (6, 5))
            window.blit(obj_text, (95, 5))
            if pause:
                pause_text = font.render("PAUSED", 1, pygame.Color("BLACK"))
                window.blit(pause_text, (self.win_width - 78, 5))
            pygame.display.update()
            clock.tick(self.fps)
            frames += 1

    def spawn_object(
        self,
        pos: tuple[float, float],
        radius: float,
        vel: tuple[float, float] | None = None,
        mass: float = 1,
    ):
        if self._env is None:
            return
        if vel is None:
            atom = Atom(mass, radius, pos, self.spawn_velocity())
        else:
            atom = Atom(mass, radius, pos, self.scale(vel))
        if self.cycle_colours:
            atom.paint(self.get_next_hue())
        self._env.add(atom)

    def draw_objects(self, surface: pygame.Surface):
        if self._env is None:
            return
        for atom in self._env.get_objects():
            pygame.draw.circle(surface, atom.colour(), atom.position(), atom.radius())

    def get_next_hue(self):
        self._obj_hue += 0.05 % 1
        rgb = colorsys.hsv_to_rgb(self._obj_hue, 1, 1)
        return (rgb[0] * 255, rgb[1] * 255, rgb[2] * 255)

    def centre(self) -> tuple[float, float]:
        return (self.win_width / 2, self.win_height / 2)

    def window_size(self) -> tuple[int, int]:
        return (self.win_width, self.win_height)

    def spawn_velocity(self) -> tuple[float, float]:
        if self.constant_velocity:
            x_vel, y_vel = self._default_velocity
        else:
            x_vel, y_vel = self.random_velocity(self._vmax)
        return self.scale((x_vel, y_vel))

    def set_obj_limit(self, limit: int):
        self.obj_limit = limit

    def scale(self, vel: tuple[float, float]) -> tuple[float, float]:
        dt = 1 / self.fps
        return (vel[0] * dt, vel[1] * dt)

    def auto_spawn(self, auto: bool):
        self.auto = auto

    def circular_environment(self, circle: bool):
        self.circular_env = circle

    def change_colours(self, cycle: bool):
        self.cycle_colours = cycle

    def random_obj_radius(self, random: bool):
        self.random_radius = random

    def set_default_radius(self, value: float):
        self._default_radius = value

    def set_vmax(self, value: int):
        self._vmax = value

    def constrain_velocity(self, value: tuple[float, float]):
        self.constant_velocity = True
        self._default_velocity = value

    def release_velocity(self):
        self.constant_velocity = False

    def random_velocity(self, maximum: int) -> tuple[float, float]:
        x = random.randint(-maximum, maximum)
        y = random.randint(-maximum, maximum)
        return (x, y)

    def get_object_radius(self) -> float:
        if self.random_radius:
            r = int(self._default_radius * 100)
            return random.randint(r - 1000, r + 1000) / 100
        else:
            return self._default_radius

    def _auto_valid(self, obj_count: int, frames: int, pause: bool) -> bool:
        return (
            not pause
            and self.auto
            and (self.obj_limit is None or obj_count < self.obj_limit)
            and frames % 24 == 0
        )

    def _manual_valid(self, obj_count: int, pause: bool) -> bool:
        return (
            not pause
            and not self.auto
            and (self.obj_limit is None or obj_count < self.obj_limit)
        )
