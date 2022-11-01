import pygame
from pygame.draw import *
from random import randint

FPS = 60 #Частота обговления экрана
SC_X, SC_Y = 1200, 700 #Размер игрового поля

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN] #Палитра

Quant = 15 #Количество мячей
Vmax = 8 #Максимальная скорость мяча


class Ball:
    # Параметры шарика (положение, радиус, скорость, цвет)
    def __init__(self):
        self.x = randint(100, SC_X - 100)
        self.y = randint(100, SC_Y - 100)
        self.r = randint(20, 50)
        self.Vx = randint(-Vmax, Vmax)
        self.Vy = randint(-Vmax, Vmax)
        self.color = COLORS[randint(0, 5)]

    def draw(self):
        # Отрисовка шарика
        circle(screen, self.color, (self.x, self.y), self.r)

    def move(self):
        # Движение шарика
        self.x += self.Vx
        self.y += self.Vy

    def wall(self):
        # Отскок шарика от стены
        if self.x < self.r:
            self.x = 2 * self.r - self.x
            self.Vx = -self.Vx
        if self.y < self.r:
            self.y = 2 * self.r - self.y
            self.Vy = -self.Vy
        if self.x > SC_X - self.r:
            self.x = 2 * SC_X - 2 * self.r - self.x
            self.Vx = -self.Vx
        if self.y > SC_Y - self.r:
            self.y = 2 * SC_Y - 2 * self.r - self.y
            self.Vy = -self.Vy


def event(Balls):
    # Работа с событиями (конец игры, клики игрока)
    global finished, hits, clicks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicks += 1
            for ball in Balls:
                if (event.pos[0] - ball.x) ** 2 + (event.pos[1] - ball.y) ** 2 <= ball.r ** 2:
                    if ball.r in range(20, 30):
                        hits += 3
                    elif ball.r in range(30, 40):
                        hits += 2
                    elif ball.r in range(40, 51):
                        hits += 1
                    Balls.remove(ball)
                    Balls.append(Ball())


def Score(hits, clicks):
    # Подсчёт очков
    if clicks > 0:
        return round(hits / clicks, 3)
    else:
        return 0


def Display_score(score):
    # Вывод очков на экран
    score_font = pygame.font.SysFont('comicsans', 35)
    value = score_font.render('Ваш счёт: ' + str(score), True, YELLOW)
    screen.blit(value, [0, 0])


def ScoreTable(score):
    # Таблица лидеров
    Username = input('Enter name (less than 25 symbols):\n')[:26]
    f = open('ScoreTable', 'a', encoding='utf-8')
    f.writelines(Username + ' ' * (28 - len(Username)) + str(score) + '\n')
    f.close()


#Игра
pygame.init()
screen = pygame.display.set_mode((SC_X, SC_Y))
pygame.display.update()
clock = pygame.time.Clock()
finished = False
clicks = 0
hits = 0
Balls = [Ball() for i in range(Quant)]

while not finished:
    screen.fill(BLACK)
    for ball in Balls:
        ball.move()
        ball.wall()
        ball.draw()
    score = Score(hits, clicks)
    Display_score(score)
    pygame.display.update()
    clock.tick(FPS)
    event(Balls)

pygame.quit()

ScoreTable(score)
