from pygame import *
from random import randint
from sys import exit


class Sprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Sprite):
    def __init__(self, speed_x, picture, w, h, x, y):
        super().__init__(picture, w, h, x, y)
        self.speed_x = speed_x
        self.count = 0

    def update(self):
        self.rect.x += self.speed_x
        self.speed_x = 0
        keys = key.get_pressed()
        if keys[K_a]:
            if not keys[K_d]:
                if self.rect.x >= 10:
                    self.speed_x = -5
        elif keys[K_d]:
            if self.rect.x <= 1210:
                self.speed_x = 5
        self.count += 1
        if self.count == 50:
            self.shoot()
            self.count = 0

    def shoot(self):
        bullet = Bullet(-5, 'bullet.png', 7, 27, self.rect.centerx - 3, self.rect.y - 25)
        bullets.add(bullet)


class Enemy(Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__(picture, w, h, x, y)
        self.count = 0
        self.fire_rate = randint(100, 700)

    def update(self):
        self.count += 1
        if self.count == self.fire_rate:
            self.shoot()
            self.count = 0

    def shoot(self):
        bullet = Bullet(5, 'bullet.png', 7, 27, self.rect.centerx - 3, self.rect.y + 15)
        bullets_enemy.add(bullet)

class Bullet(Sprite):
    def __init__(self, speed_y, picture, w, h, x, y):
        super().__init__(picture, w, h, x, y)
        self.speed_y = speed_y

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y <= -40 or self.rect.y >= 720:
            self.kill()


def spawn_enemys(wave):
    y = 50
    for i in range(wave):
        x = 50
        for i in range(7):
            enemy = Enemy("enemy.png", 50, 40, x, y)
            enemys.add(enemy)
            x += 200
        y += 100

def restart():
    global finish, wave
    finish = False
    wave = 0
    enemys.empty()
    bullets.empty()
    bullets_enemy.empty()
    button_restart.rect.x = 2000

background = transform.scale(image.load('background.png'), (1280, 720))
player = Player(0, 'spaceship.png', 60, 60, 600, 650)
button_restart = Sprite("restart.png", 100, 100, 600, 350)
bullets = sprite.Group()
bullets_enemy = sprite.Group()

window = display.set_mode((1280, 720))
clock = time.Clock()

wave = 1
enemys = sprite.Group()
spawn_enemys(wave)
finish = False
while True:
    window.blit(background, (0, 0))
    if not finish:
        player.update()
        player.draw()
        bullets.draw(window)
        bullets.update()
        bullets_enemy.draw(window)
        bullets_enemy.update()
        enemys.draw(window)
        enemys.update()

    sprite.groupcollide(enemys, bullets, True, True)
    if sprite.spritecollide(player, bullets_enemy, False):
        button_restart.draw()
        finish = True
        button_restart.rect.x = 600

    if len(enemys) == 0:
        wave += 1
        spawn_enemys(wave)

    if wave == 4:
        finish = True
        button_restart.draw()
        button_restart.rect.x = 600

    for e in event.get():
        if e.type == QUIT:
            exit()

        if e.type == MOUSEBUTTONDOWN:
            x, y = mouse.get_pos()
            if button_restart.rect.collidepoint(x, y):
                restart()

    clock.tick(60)
    display.update()
