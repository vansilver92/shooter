#Создай собственный Шутер!

from random import randint

from pygame import *

init()
mixer.init()

mixer.music.load('space.ogg')
mixer.music.play()

window = display.set_mode((700, 500))
display.set_caption('шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
win = transform.scale(image.load('win2.jpg'), (700, 500))
defeat = transform.scale(image.load('defeat2.png'), (700, 500))

# ufo = transform.scale(image.load('ufo.png'), (65, 65))
rocket = transform.scale(image.load('rocket.png'), (65, 100))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, speed, x, y, size=65):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size, size))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 635:
            self.rect.x += self.speed

    def fire(self):
        flag = 1
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and flag == 1:
            bullets.add(Bullet_sprite('bullet.png', 10, self.rect.x+ 32.5, self.rect.y - 25, 20))
            flag = 0
        if not keys_pressed[K_w] and flag == 0:
            flag = 1

            


destroyed = 0
missed_ufos = 0
# global missed_ufos
class Enemy(GameSprite):
    def __init__(self, player_image, speed, x, y):
        super().__init__(player_image, speed, x, y)
        self.move_dir = 'up'

    def update(self):
        if self.rect.y >= 500:
            self.move_dir = 'down'
            self.rect.y = -100
            self.rect.x = randint(0, 650)
            self.speed = randint(2, 4)
            global missed_ufos
            missed_ufos += 1
        elif self.rect.y <= 0:
            self.move_dir = 'up'
        self.rect.y += self.speed if self.move_dir == 'up' else -self.speed
        # if self.rect.y > 500:
            # self.rect.y = 0

class Bullet_sprite(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -20:
            self.kill()

bullets = sprite.Group()
ufos = sprite.Group()

label_font = font.SysFont('Arial', 20)
event_font = font.SysFont('Arial', 100)
for i in range(6):
    ufos.add(Enemy('ufo.png', randint(1, 4), randint(0, 620), 0))
game = True
finish = False
rocket = Player('rocket.png', 12, 500, 420)
clock = time.Clock()
timer = 0
flag = 0
collision = 0
while game:
    timer += 1
    window.blit(background, (0, 0))
    window.blit(label_font.render(f'Уничтожено: {destroyed}', 1, (255, 255, 255)), (20, 20))
    window.blit(label_font.render(f'Пропущено: {missed_ufos}', 1, (255, 255, 255)), (20, 50))
    bullets.update()
    bullets.draw(window)
    ufos.draw(window)
    ufos.update()
        
    rocket.reset()
    rocket.move()

    dead = sprite.groupcollide(ufos, bullets, True, True)
    for i in range(len(dead)):
        destroyed += 1
        ufos.add(Enemy('ufo.png', randint(1, 4), randint(0, 620), 0))
    if timer >= 10:
        timer = 0
        rocket.fire()
    if destroyed  >= 150:
        window.blit(win, (0, 0))
        window.blit(event_font.render('ПОБЕДА', 1, (0, 255, 0)), (200, 220))
        flag = 1
    if missed_ufos >= 10 and flag == 0:
        window.blit(defeat, (0, 0))
        window.blit(event_font.render('ПОРЖЕИЕ', 1, (255, 0, 0)), (200, 220))
    # collision = sprite.spritecollide(rocket, ufos, False, True)
    # if len(collision) > 3:
    #     window.blit(defeat, (0, 0))
    #     window.blit(event_font.render('ПОРОЖЕИЕ', 1, (255, 0, 0)), (200, 220))
    for e in event.get():
        if e.type == QUIT:
            game = False    
    clock.tick(60)
    display.update()
