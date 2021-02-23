import pygame
from math import sqrt

FPS = 60

pygame.init()

WIN = pygame.display.set_mode((1000, 1000))

pygame.display.set_caption('lol')

clock = pygame.time.Clock()

black = 0, 0, 0
white = 255, 255, 255
G = 0.1




class Planet():
    def __init__(self, win, mass, x, y, V):
        self.win = win
        self.pos = [x, y]
        self.mass = mass
        self.radius = (mass // 3.14)**(1/2)
        if self.radius > 100:
            self.radius = 100
        self.V = V

    def draw(self):
        pygame.draw.circle(self.win, white, (self.pos[0], self.pos[1]), self.radius)

    def update(self, other):
        if self != other:
            dx = other.pos[0] - self.pos[0]
            dy = other.pos[1] - self.pos[1]
            distance = sqrt((dx)**2 + (dy)**2)
            if distance != 0:
                F = (G * self.mass + other.mass)/distance**2
                Fx = F * dx/distance
                Fy = F * dy/distance
                self.V[0] += Fx/self.mass
                self.V[1] += Fy/self.mass



class Sky():
    def __init__(self, win, planets):
        self.planets = planets
        self.win = win

    def update(self):
        for planet1 in self.planets:
            for planet2 in self.planets:
                planet1.update(planet2)

            planet1.pos[0] += planet1.V[0]
            planet1.pos[1] += planet1.V[1]


def main():
    run = True
    planet1 = Planet(WIN, 1000, 400, 400, [0, 0])
    planet2 = Planet(WIN, 1000, 600, 600, [0, 0])
    planets = [planet1, planet2]
    sky = Sky(WIN, planets)

    while run:
        WIN.fill(black)
        clock.tick(FPS)
        sky.update()
        for planet in sky.planets:
            planet.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()


if __name__ == "__main__":
    main()