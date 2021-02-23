import pygame
from objects import Sky, Star, Galaxy, Planet
from constants import black, WIDTH, HEIGHT, white, green, blue
from random import randint

FPS = 120

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('t-tiny, y-small, u-big, a-particles, v-vectors')

clock = pygame.time.Clock()


def main():
    sky = Sky(WIN, 1000, 20, 10, False)
    sky.add_planet(10**5, 500, 500, [0, 0], True)
    # sky.add_planet(10**6, 200, 200, [0, 0], True)
    spawnx = spawny = 0
    MASS = 200
    hold = False
    run = True

    while run:
        WIN.fill(black)
        # for star in sky.stars:
        #     star.draw()
        # for galaxy in sky.galaxies:
        #     galaxy.draw()
        clock.tick(FPS)
        sky.update()
        if hold:
            x, y = pygame.mouse.get_pos()
            pygame.draw.line(WIN, green, (spawnx, spawny), (x, y), 1)
        for planet in sky.planets:
            planet.draw()
            if sky.vectors:
                pygame.draw.line(WIN, blue, (planet._x, planet._y), (planet._x+ 10*planet.V[0], planet._y + 10*planet.V[1]), 2)
        for event in pygame.event.get():
            if not hold:
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    hold = True
                    spawnx, spawny = pygame.mouse.get_pos()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        sky.planets.clear()
                    if event.key == pygame.K_t:
                        MASS = 10
                    if event.key == pygame.K_y:
                        MASS = 200
                    if event.key == pygame.K_u:
                        MASS = 10000
                    if event.key == pygame.K_v:
                        sky.change_vectors()
                    if event.key == pygame.K_a:
                        x, y = pygame.mouse.get_pos()
                        for i in range(0, 100):
                            sky.add_planet(1, x, y+i, [1, 1], False)
            elif hold:
                if event.type == pygame.MOUSEBUTTONUP:
                    hold = False
                    finalx, finaly = pygame.mouse.get_pos()
                    velx = (finalx - spawnx)/50
                    vely = (finaly - spawny)/50
                    sky.add_planet(MASS, spawnx, spawny, [velx, vely], False)

        pygame.display.update()

if __name__ == "__main__":
    main()