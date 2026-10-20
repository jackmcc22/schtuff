import pygame
import pygame.math 
from pygame.math import Vector2
import random

WIDTH, HEIGHT = 900, 600
GRAVITY = Vector2(0, 1000)

class Particle:
    def __init__(self, x, y, radius=10, pinned=False):
        self.pos = Vector2(x, y)
        self.prev = Vector2(x, y)
        self.acc = Vector2(0, 0)
        self.radius = radius
        self.pinned = pinned
    def apply_force(self, force):
        self.acc += force

    def update(self, dt):
        if self.pinned:
            return
        velocity = (self.pos - self.prev) * 0.999
        self.prev = self.pos.copy()
        self.pos += velocity + self.acc * dt * dt
        self.acc = Vector2(0, 0)



class Stick:
    def __init__(self, a, b, length=None):
        self.a, self.b = a, b
        self.length = length if length is not None else (a.pos - b.pos).length()

    def solve(self):
        delta = self.b.pos - self.a.pos
        dist = delta.length()
        if dist == 0:
            return
        diff = (dist -self.length()) / dist

        wa = 0 if self.a.pinned else 1
        wb = 0 if self.b.pinned else 1
        total = wa + wb
        if total == 0:
            return
        correction = delta * diff

        self.a.pos += correction * (wa / total)
        self.b.pos -= correction * (wb/ total)

def constrain_to_box(p):
        r = p.radius
        p.pos.x = max(r, min(WIDTH - r, p.pos.x))
        p.pos.y = max(r, min(HEIGHT -r, p.pos.y))




def solve_collisions(particles):
    n = len(particles)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = particles[i], particles[j]
            delta = a.pos - b.pos
            dist = delta.length()
            min_dist = a.radius + b.radius
            if 0 < dist < min_dist:
                push = delta / dist * (min_dist - dist) * 0.5
                if not a.pinned:
                    a.pos += push
                if not b.pinned:
                    b.pos -= push

class World:
    def __init__(self):
        self.particles = []
        self.sticks = []
        self.substeps = 8

    def step(self, dt):
        sub_dt = dt / self.substeps
        for _ in range(self.substeps):
            for p in self.particles:
                p.apply_force(GRAVITY)
                p.update(sub_dt)
            for _ in range(2):
                for s in self.sticks:
                    s.solve()
                solve_collisions(self.particles)
                for p in self.particles:
                    constrain_to_box(p)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    world = World()
    

    prev = None
    for i in range(15):
        p = Particle(300 + i * 20, 100, radius=6, pinned=(i == 0))
        world.particles.append(p)
        if prev:
            world.sticks.append(Stick(prev, p))
        prev = p

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #print("click", event.pos)
                    x, y = event.pos
                    world.particles.append(Particle(x, y, radius=random.randint(8, 18)))
            world.step(1 / 60)

            screen.fill((20, 20, 30))

            for s in world.sticks:
                pygame.draw.line(screen, (200, 200, 200), s.a.pos, s.b.pos, 2)
            for p in world.particles:
                color = (255, 100, 100) if p.pinned else (100, 200, 255)
                pygame.draw.circle(screen, color, p.pos, p.radius)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
    
if __name__ == "__main__":
    main()
