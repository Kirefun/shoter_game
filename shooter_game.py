#Создай собственный Шутер!
from pygame import *
from random import randint
from time import \
    time as timer
window = display.set_mode((700, 500))
display.set_caption('Шутер!')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

game = True
finish = False

mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

clock = time.Clock()
FRS = 60

win_height = 500
win_width = 700 

img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_asteroid = 'asteroid.png'

lost = 0
font.init()
font2 = font.SysFont('Arial', 36)
font1 = font.SysFont('Arial', 80)

score = 0

life = 3
max_lost = 7
rel_time = False
num_fire = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x 
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y)) 

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(60, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)
lose = font1.render('YOU LOSE', True, (255, 215, 0))
win = font1.render('YOU WIN', True, (255, 215, 0))


while game:
    for  e  in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0, 0))

        text = font2.render('Счёт: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload_time = font2.render('Идёт перезарядка...', 1, (150, 0, 0))
                window.blit(reload_time, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(bullets, monsters, True, True)

        for i in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life - 1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= 5:
            finish = True
            window.blit(win, (250, 200)) 

        if life == 3:
            life_color = (0, 150, 0)

        if life == 2:
            life_color = (150, 150, 0)

        if life == 1:
            life_color = (150, 0, 0)


        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        display.update()


    else:
        finish = False
        score = 0
        lost = 0
        life = 3

        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Enemy(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            asteroids.add(asteroid)

        clock.tick(FRS)
        






