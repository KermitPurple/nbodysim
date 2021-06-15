import random
from pycoord import Coord
from pygame_tools import *

class Body:
    MAX_TAIL_LENGTH = 100

    def __init__(self, mass: float, pos: Coord = None, vel: Coord = None):
        self.mass = mass
        if pos is None:
            pos = Coord()
        self.pos = pos
        if vel is None:
            vel = Coord()
        self.vel = vel
        self.dead = False
        self.tail = []

    @staticmethod
    def random(size: Coord) -> 'Body':
        return Body(
                random.random() * 10,
                Coord(random.random() * size.x, random.random() * size.y),
                Coord.from_polar(random.random() * 5, random.random() * math.pi * 2),
                )

    def update(self, bodies: ['Body', ...], size: Coord):
        # G = 6.67 * 10 ** -11 # gravitational contant
        G = 0.1
        prev = tuple(self.pos)
        self.pos += self.vel
        self.tail.append((prev, tuple(self.pos)))
        if len(self.tail) > self.MAX_TAIL_LENGTH:
            self.tail.pop(0)
        if self.pos.x >= size.x + self.mass:
            self.pos.x = -self.mass
        if self.pos.x < -self.mass:
            self.pos.x = size.x + self.mass
        if self.pos.y >= size.y + self.mass:
            self.pos.y = -self.mass
        if self.pos.y < -self.mass:
            self.pos.y = size.y + self.mass
        a = Coord()
        for body in bodies:
            if self is body:
                continue
            # TODO: do mass calculations
            dpos = body.pos - self.pos
            a += self.mass * body.mass / (dpos.r ** 2) * dpos
            # # COLISIONS
            # if self.collides_with(body):
            #     if self.mass > body.mass:
            #         self.absorb(body)
            #     else:
            #         body.absorb(self)
        self.vel += G / self.mass * a


    def absorb(self, body: 'Body'):
        body.dead = True
        self.vel += body.mass / self.mass * body.vel
        self.mass += body.mass
        body.mass = 0
        body.vel.r = 0

    def collides_with(self, other: 'Body') -> bool:
        if other.dead or self.dead:
            return False
        return self.pos.dist(other.pos) < self.mass + other.mass

    def draw(self, screen):
        pygame.draw.circle(screen, 'white', tuple(math.floor(self.pos)), int(self.mass))
        for line in self.tail:
            pygame.draw.line(screen, 'white', *line)

class NBodySim(GameScreen):
    def __init__(self):
        pygame.init()
        size = Point(800, 600)
        super().__init__(pygame.display.set_mode(size), size)
        self.bodies = [Body.random(size) for _ in range(50)]
        self.run()

    def update(self):
        self.screen.fill('black')
        i = 0
        while i < len(self.bodies):
            body = self.bodies[i]
            body.draw(self.screen)
            body.update(self.bodies, self.window_size)
            if body.dead:
                self.bodies.pop(i)
            else:
                i += 1

if __name__ == '__main__':
    NBodySim()

