import math
from random import choice, randint, random
import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

G = 1
targets_number = 2

class Ball:
    def __init__(self, screen: pygame.Surface, x=0.5 * WIDTH, y=0.5 * HEIGHT, vx=0, vy=0, r=10, grav = 0):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.color = choice(GAME_COLORS)
        self.alive = FPS * 2
        self.grav = G

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy -= self.grav
        self.x += self.vx
        self.y -= self.vy
        self.alive -= 1
        if self.x < self.r:
            self.x = 2 * self.r - self.x
            self.vx = -0.85 * self.vx
        if self.y < self.r:
            self.y = 2 * self.r - self.y
            self.vy = -0.7 * self.vy
        if self.x > WIDTH - self.r:
            self.x = 2 * WIDTH - 2 * self.r - self.x
            self.vx = -0.85 * self.vx
        if self.y > HEIGHT - self.r:
            self.y = 2 * HEIGHT - 2 * self.r - self.y
            self.vy = -0.7 * self.vy

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 < (self.r + obj.r) ** 2:
            return True
        else:
            return False

    def remove(self):
        return self.alive <= 0


class Gun:
    def __init__(self, screen: pygame.Surface, x=0.5 * WIDTH, y=HEIGHT - 70):
        self.screen = screen
        self.f2_power = 25
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = x
        self.y = y
        self.vel = 3
        self.r = 30

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x, self.y)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - self.y), (event.pos[0] - self.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 25

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0] - self.x != 0:
                self.an = math.atan((event.pos[1] - self.y) / (event.pos[0] - self.x))
            else:
                self.an = math.atan((event.pos[1] - self.y) / 0.0001)
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        gun_w = 10
        gun_l = self.f2_power
        x0, y0 = pygame.mouse.get_pos()

        sin_an = math.sin(self.an)
        cos_an = math.cos(self.an)
        if self.x > x0:
            sin_an = -sin_an
            cos_an = -cos_an
        coords = [(self.x + gun_w * 0.5 * sin_an, self.y - gun_w * 0.5 * cos_an),
                  (self.x + gun_w * 0.5 * sin_an + gun_l * cos_an, self.y - gun_w * 0.5 * cos_an + gun_l * sin_an),
                  (self.x - gun_w * 0.5 * sin_an + gun_l * cos_an, self.y + gun_w * 0.5 * cos_an + gun_l * sin_an),
                  (self.x - gun_w * 0.5 * sin_an, self.y + gun_w * 0.5 * cos_an)]

        pygame.draw.polygon(screen, self.color, coords)
        pygame.draw.polygon(screen, BLACK, [(self.x - 30, self.y + 25), (self.x + 30, self.y + 25),
                                             (self.x + 50, self.y + 5), (self.x - 50, self.y + 5)])
        pygame.draw.circle(screen, BLACK, [self.x, self.y + 5], 15)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

    def gun_move(self, event):
        if (pygame.key.get_pressed()[pygame.K_d]) and (self.x <= WIDTH - 30):
            self.x += 10
        elif (pygame.key.get_pressed()[pygame.K_a]) and (self.x >= 30):
            self.x -= 10


class Target:
    def __init__(self, screen: pygame.Surface, x=700, vx=0, vy=0, y=450, r=20):
        self.points = 0
        self.alive = True
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.color = RED
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.alive = True
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.vx = randint(-7, 7)
        self.vy = randint(-7, 7)
        self.r = randint(10, 40)
        self.color = RED

    def move(self):
        '''Движение мишени'''
        self.x += self.vx
        self.y -= self.vy
        if self.x < self.r:
            self.x = 2 * self.r - self.x
            self.vx = -self.vx
        if self.y < self.r:
            self.y = 2 * self.r - self.y
            self.vy = -self.vy
        if self.x > WIDTH - self.r:
            self.x = 2 * WIDTH - 2 * self.r - self.x
            self.vx = -self.vx
        if self.y > (HEIGHT - 50) - self.r:
            self.y = 2 * (HEIGHT - 50) - 2 * self.r - self.y
            self.vy = -self.vy

    def draw(self):
        if self.alive:
            pygame.draw.circle(
                self.screen,
                self.color,
                (self.x, self.y),
                self.r
            )


class TargetR:
    def __init__(self, screen: pygame.Surface, X=400, Y=300, w=10,  r=20, R=50):
        self.alive = True
        self.screen = screen
        self.color = BLUE
        self.r = r
        self.R = R
        self.angle = math.pi
        self.X = X
        self.x = self.X + (self.R * math.cos(self.angle))
        self.Y = Y
        self.y = self.Y + (self.R * math.sin(self.angle))
        self.w = w
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.alive = True
        self.r = randint(10, 40)
        self.R = randint(50, 100)
        self.angle = random() * 2 * math.pi
        self.X = randint(100, 600)
        self.x = self.X + (self.R * math.cos(self.angle))
        self.Y = randint(100, 400)
        self.y = self.Y + (self.R * math.sin(self.angle))
        self.w = random() / 50

    def move(self):
        '''Движение мишени'''
        self.angle += self.w * 2 * math.pi
        self.x = self.X + (self.R * math.cos(self.angle))
        self.y = self.Y + (self.R * math.sin(self.angle))

    def draw(self):
        if self.alive:
            pygame.draw.circle(
                self.screen,
                self.color,
                (self.x, self.y),
                self.r
            )


class Bomb:
    def __init__(self, screen: pygame.Surface, x=50, y=50):
        self.screen = screen
        self.x = randint(50, WIDTH - 50)
        self.y = randint(50, 100)
        self.vx = randint(-5, 5)
        self.alive = True
        self.r = 7
        self.color = BLACK
        self.gun = 1000
        self.object = randint(0, 1)

    def move(self):
        global gunballs
        self.x += self.vx
        self.gun -= 5
        if self.x + self.vx >= WIDTH - 50:
            self.vx *= -1
        if self.x + self.vx <= 50:
            self.vx *= -1
        if self.gun % 400 == 0:
            gb = Ball(self.screen)
            gb.x = self.x
            gb.y = self.y
            gb.color = BLACK
            gb.vx = randint(-6, 6)
            gb.vy = 0
            gb.alive = FPS * 3
            gb.grav = round(G/5, 1)
            gunballs.append(gb)

    def draw(self):
        if self.alive:
            pygame.draw.circle(self.screen,
                               self.color,
                               (self.x, self.y),
                               self.r
                               )


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
finished = False
bullet = 0

gun = Gun(screen)
bombdropper = Bomb(screen)
gunballs = []
balls = []
targets = []
for i in range(targets_number):
    targets.append(Target(screen))
targetR = TargetR(screen)

while not finished:
    screen.fill(WHITE)
    gun.draw()
    bombdropper.draw()
    targetR.draw()
    for target in targets:
        target.draw()
    for b in balls:
        b.draw()
    for gb in gunballs:
        gb.draw()
    pygame.display.update()

    clock.tick(FPS)

    if (pygame.key.get_pressed()[pygame.K_d]) or (pygame.key.get_pressed()[pygame.K_a]):
        gun.gun_move(event)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    remove_balls = []
    remove_gunballs = []
    for i in range(len(balls)):
        if balls[i].remove():
            remove_balls.append(i)
    for i in remove_balls:
        del balls[i]
    for i in range(len(gunballs)):
        if gunballs[i].remove():
            remove_gunballs.append(i)
    for i in remove_gunballs:
        del gunballs[i]

    for b in balls:
        b.move()

    for gb in gunballs:
        gb.move()
        if gb.hittest(gun):
            finished = True
        for b in balls:
            for target in targets:
                if b.hittest(target) and target.alive:
                    target.alive = False
                    target.new_target()
            if b.hittest(targetR) and targetR.alive:
                targetR.alive = False
                targetR.new_target()
            if b.hittest(bombdropper):
                bombdropper.alive = False
                bombdropper = Bomb(screen)
            if b.hittest(gb):
                gb.alive = False

    bombdropper.move()
    for target in targets:
        target.move()
    targetR.move()

    gun.power_up()

pygame.quit()
