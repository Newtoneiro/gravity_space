"""Main file presenting the whole program in action."""

import pygame

from gravity.objects.canvas import Canvas
from gravity.constants import PYGAME_CONSTANTS, COLORS


def main():
    pygame.init()
    pygame.display.set_caption(PYGAME_CONSTANTS.WINDOW_TITLE)

    WIN = pygame.display.set_mode((PYGAME_CONSTANTS.WIDTH, PYGAME_CONSTANTS.HEIGHT))
    CLOCK = pygame.time.Clock()

    canvas = Canvas(WIN)
    canvas.add_planet(10**5, 500, 500, [0, 0], True)
    # sky.add_planet(10**6, 200, 200, [0, 0], True)
    spawnx = spawny = 0
    MASS = 200
    hold = False
    run = True

    while run:
        WIN.fill(COLORS.BLACK)
        CLOCK.tick(PYGAME_CONSTANTS.FPS)
        canvas.update()
        if hold:
            x, y = pygame.mouse.get_pos()
            pygame.draw.line(WIN, COLORS.GREEN, (spawnx, spawny), (x, y), 1)
        for planet in canvas._planets:
            planet.draw()
            if canvas._show_vectors:
                pygame.draw.line(
                    WIN,
                    COLORS.BLUE,
                    (planet._x, planet._y),
                    (
                        planet._x + 10 * planet._vector[0],
                        planet._y + 10 * planet._vector[1],
                    ),
                    2,
                )
        for event in pygame.event.get():
            if not hold:
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    hold = True
                    spawnx, spawny = pygame.mouse.get_pos()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        canvas.clear()
                    if event.key == pygame.K_t:
                        MASS = 10
                    if event.key == pygame.K_y:
                        MASS = 200
                    if event.key == pygame.K_u:
                        MASS = 10000
                    if event.key == pygame.K_v:
                        canvas.toggle_vectors_display()
                    if event.key == pygame.K_a:
                        x, y = pygame.mouse.get_pos()
                        for i in range(0, 100):
                            canvas.add_planet(1, x, y + i, [1, 1], False)
            elif hold:
                if event.type == pygame.MOUSEBUTTONUP:
                    hold = False
                    finalx, finaly = pygame.mouse.get_pos()
                    velx = (finalx - spawnx) / 50
                    vely = (finaly - spawny) / 50
                    canvas.add_planet(MASS, spawnx, spawny, [velx, vely], False)

        pygame.display.update()


if __name__ == "__main__":
    main()
