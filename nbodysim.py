import random
from pycoord import Coord
from pygame_tools import *

class Body:
    MAX_TAIL_LENGTH = 100

    def __init__(self, size: Coord):
        self.mass = random.random() * 10
        self.pos = Coord(random.random() * size.x, random.random() * size.y)
        self.vel = Coord.from_polar(random.random() * 5, random.random() * math.pi * 2)
        self.dead = False
        self.tail = []

    def update(self, bodies: ['Body', ...], size: Coord):
        G = 6.67 * 10 ** -11 # gravitational contant
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
            a += body.mass * ((1 / dpos) ** 3) * dpos
            # COLISIONS
            # if self.collides_with(body):
            #     if self.mass > body.mass:
            #         self.absorb(body)
            #     else:
            #         body.absorb(self)
        self.vel += a * 10


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
        self.bodies = [Body(size) for _ in range(50)]
        super().__init__(pygame.display.set_mode(size), size)
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

