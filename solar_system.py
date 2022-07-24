import math
import pygame

pygame.init()

WIDTH, HEIGHT = 1550, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System")
pygame.display.set_icon(pygame.image.load("solar-system.png"))

# colors
ORANGE = (222, 113, 11)
BLUE = (17, 20, 207)
RED = (117, 11, 11)
MERC_RED = (84, 9, 9)
WHITE = (255, 255, 255)
YELLOW = (153, 112, 23)

FONT = pygame.font.SysFont("comicsans", 16)

sizes = [25, 5, 7, 9, 10, 16, 15, 12, 11]


class Planet:
    AU = 149.6e6 * 1000  # astronomical unit (distance from the Earth to the sun)
    G = 6.67428e-11  # gravitational constant
    SCALE = 100 / AU  # 1AU = 100px
    TIME_STEP = 70000

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x  # postion on the x-axis
        self.y = y  # position on the y-axis
        self.radius = radius  # radius of the planet
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []
        self.sun = False
        self.sun_dist = 0

        self.x_vel = 0
        self.y_vel = 0

    def attract(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(
            distance_x ** 2 + distance_y ** 2)  # calculating the distance to each planet (Pythagoras theorem)

        if other.sun:
            self.sun_dist = distance

        force = self.G * self.mass * other.mass / distance ** 2  # the force by the formula of the gravitation
        theta = math.atan2(distance_y, distance_x)  # angle on which each planet should go
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attract(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIME_STEP
        self.y_vel += total_fy / self.mass * self.TIME_STEP

        self.x += self.x_vel * self.TIME_STEP
        self.y += self.y_vel * self.TIME_STEP
        self.orbit.append((self.x, self.y))

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) >= 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, (255, 255, 255), False, updated_points, 1)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_test = FONT.render(f"{self.name}: {round(self.sun_dist / 1000000)}e6 km", True, WHITE)
            win.blit(distance_test, (x - distance_test.get_width() / 2, y - distance_test.get_width() / 3))
        # WIN.blit(img, (x - 10, y - 10))


def main():
    run = True
    clock = pygame.time.Clock()

    # list of the planets
    sun = Planet(0, 0, sizes[0], (255, 255, 0), 1.989e30, "Sun")
    sun.sun = True

    mercury = Planet(0.387 * Planet.AU, 0, sizes[1], MERC_RED, 3.285e23, "Mercury")
    mercury.y_vel = -47.9 * 1000

    venus = Planet(0.72 * Planet.AU, 0, sizes[2], WHITE, 4.867e24, "Venus")
    venus.y_vel = -35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, sizes[3], BLUE, 5.972e24, "Earth")
    earth.y_vel = 29.8 * 1000

    mars = Planet(-1.52 * Planet.AU, 0, sizes[4], RED, 6.39e23, "Mars")
    mars.y_vel = 24.1 * 1000

    jupiter = Planet(5.4 * Planet.AU, 0, 21, YELLOW, 1.898e27, "Jupiter")
    jupiter.y_vel = 13.1 * 1000

    saturn = Planet(9.5 * Planet.AU, 0, 19, (224, 179, 13), 5.683e26, "Saturn")
    saturn.y_vel = 9.7 * 1000

    uranus = Planet(19.18 * Planet.AU, 0, 16, (0, 174, 255), 8.68e25, "Uranus")  # 12.18
    uranus.y_vel = -6.8 * 1000

    neptune = Planet(30.06 * Planet.AU, 0, 17, (0, 44, 242), 1.02e26, "Neptune")  # 19.06
    neptune.y_vel = 5.43 * 1000

    pluto = Planet(39.53 * Planet.AU, 0, 1, (204, 184, 151), 1.29e22, "Pluto")  # 22.53
    pluto.y_vel = 4.67 * 1000

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune, pluto]

        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            Planet.SCALE += 0.5 / Planet.AU
            for planet in planets:
                planet.radius += 0.05
        elif key[pygame.K_UP]:
            if Planet.SCALE > 1.3703208556150028e-100:
                Planet.SCALE -= 0.5 / Planet.AU
                for planet in planets:
                    planet.radius -= 0.05

        if key[pygame.K_LEFT]:
            Planet.TIME_STEP -= 2500
        elif key[pygame.K_RIGHT]:
            Planet.TIME_STEP += 2000

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()
