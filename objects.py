from constants import WIDTH, HEIGHT, white, red, G, blue, green
from random import randint, choice
from math import cos, sin, sqrt, atan2
import pygame

class Star():
    def __init__(self, win):
        self.win = win
        self.assign_radius()
        self.get_position()
        self.colour = white

    def assign_radius(self):
        self._radius = randint(1, 2)

    def radius(self):
        return self._radius

    def get_position(self):
        self._x = randint(0, WIDTH)
        self._y = randint(0, HEIGHT)

    def draw(self):
        pygame.draw.circle(self.win, self.colour, (self._x, self._y), self.radius())


class Galaxy():
    def __init__(self, win):
        self.assign_center()
        self.assign_points()
        self.win = win

    def assign_center(self):
        self._x = randint(0, WIDTH)
        self._y = randint(0, HEIGHT)
        self.center = (self._x, self._y)

    def assign_points(self):
        points1 = []
        points2 = []
        i = 0
        radius = choice([2, 2.1, 2.05, 2.3, 2.25, 2.14])
        phi = choice([0.24, 0.25])

        while i < 20:
            x = (radius**(phi*i))*cos(i) + self._x
            y = (radius**(phi*i))*sin(i) + self._y
            points1.append((x, y))
            x2 = 2*self._x - x
            y2 = 2*self._y - y
            points2.append((x2, y2))

            i += 0.2
        self.points1 = points1
        self.points2 = points2

    def draw(self):
        start1 = self.center
        start2 = self.center
        for point1, point2 in zip(self.points1, self.points2):
            pygame.draw.line(self.win, white, start1, point1, 1)
            pygame.draw.line(self.win, white, start2, point2, 1)
            start1 = point1
            start2 = point2


class Planet():
    def __init__(self, win, mass, x, y, V, stationary):
        self.win = win
        self._x = x
        self._y = y
        self._mass = mass
        self._radius = (mass // 3.14)**(1/2)
        if self._radius > 50:
            self._radius = 50
        elif self._radius < 2:
            self._radius = 2
        self.V = V
        self.stationary = stationary

    def change_stationary(self, change):
        self.stationary = change

    def Fg(self, other):
        if not self.stationary:
            if self == other:
                Fx = Fy = 0
            else:
                d = sqrt((self._x - other._x)**2 + (self._y - other._y)**2)
                dx = (self._x - other._x)
                dy = (self._y - other._y)
                if d == 0:
                    Fx = Fy = 0
                else:
                    if d <= self._radius + other._radius+2:
                        # self.V[0] = -0.6*self.V[0]
                        # self.V[1] = -0.6*self.V[1]
                        Fx = Fy = 0
                    else:
                        F = (G * self._mass * other._mass)/d**2
                        Fx = F * dx/d
                        Fy = F * dy/d

            self.V[0] += -Fx/self._mass
            self.V[1] += -Fy/self._mass

    def draw(self):
        pygame.draw.circle(self.win, red, (self._x, self._y), self._radius)
        # pygame.draw.line(self.win, blue, (self._x, self._y), (self._x+ 10*self.V[0], self._y + 10*self.V[1]), 2)


class Sky():
    def __init__(self, win, stars, galaxies, planets, vectors):
        self.win = win
        self.planets = []
        self.stars_number = stars
        self.galaxy_number = galaxies
        self.galaxies = []
        self.stars = []
        self.fill()
        self.vectors = vectors
        # self.create_planets(planets)

    def change_vectors(self):
        if self.vectors == True:
            self.vectors = False
        elif self.vectors == False:
            self.vectors = True

    def clear(self):
        self.planets == []

    def add_planet(self, mass, x, y, V, stationary):
        self.planets.append(Planet(self.win, mass, x, y, V, stationary))

    def create_planets(self, number):
        for i in range(0, number):
            self.planets.append(Planet(self.win, randint(10, 1000), randint(5, WIDTH), randint(5, HEIGHT), [randint(1, 3), randint(1, 4)], False))

    def update(self):
        for planet1 in self.planets:
            for planet2 in self.planets:
                planet1.Fg(planet2)

            planet1._x += planet1.V[0]
            planet1._y += planet1.V[1]


            if planet1._x < planet1._radius:
                planet1._x = 1 + planet1._radius
                planet1.V[0] = -0.9*planet1.V[0]
            if planet1._x > WIDTH - planet1._radius:
                planet1._x = WIDTH - planet1._radius
                planet1.V[0] = -0.9*planet1.V[0]
            if planet1._y > HEIGHT - planet1._radius:
                planet1._y = HEIGHT - planet1._radius
                planet1.V[1] = -0.9*planet1.V[1]
            if planet1._y < planet1._radius:
                planet1._y = 1 + planet1._radius
                planet1.V[1] = -0.9*planet1.V[1]

    def fill(self):
        i = 0
        while i != self.stars_number:
            star = Star(self.win)
            self.stars.append(star)
            i += 1
        n = 0
        while n != self.galaxy_number:
            galaxy = Galaxy(self.win)
            self.galaxies.append(galaxy)
            n += 1

