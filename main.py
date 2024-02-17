import random
import pygame as pg

class Bird(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("images/bird.png")
        self.image = pg.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.topleft = (25, 25)

        self.direction = 'right'
    
    def update(self):
        keys =  pg.key.get_pressed()

        if keys[pg.K_LEFT] and self.rect.left > 0:
            if self.direction == "right":
                self.image = pg.transform.flip(self.image, True, False)
                self.direction = "left"
            self.rect.x -= VELOCITY
        if keys[pg.K_RIGHT] and self.rect.right < window_width:
            if self.direction == "left":
                self.image = pg.transform.flip(self.image, True, False)
                self.direction = "right"
            self.rect.x += VELOCITY
        if keys[pg.K_UP] and self.rect.top > 0:
            self.rect.y -= VELOCITY
        if keys[pg.K_DOWN] and self.rect.bottom < window_hight:
            self.rect.y += VELOCITY
        
class Coin(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("images/coin.png")
        self.image = pg.transform.scale(self.image, (40, 40))
        
        self.rect = self.image.get_rect()
        self.rect.center = (window_width//2, window_hight//2)

class Butterfly(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        
        self.image = pg.image.load("images/бабочка.png")
        self.image = pg.transform.scale(self.image, (60, 60))

        self.rect = self.image.get_rect()
        
        self.rect.x = random.randint(0, window_width - 60)
        self.rect.y = random.randint(0, window_hight - 60)

    def update(self):
        v = 2
        
        if random.randint(0, 1) == 0:
            self.rect.x -= v
        else:
            self.rect.x += v

        if random.randint(0, 1) == 0:
            self.rect.y -= v
        else:
            self.rect.y += v

pg.init()


window_width = 600
window_hight = 300

#Создание объектов

bird = Bird()
coin = Coin()
butterflies = pg.sprite.Group()

for _ in range(5):
    butterflies.add(Butterfly())

display_surface = pg.display.set_mode((window_width, window_hight))
pg.display.set_caption('Hungry Bird!')

FPS = 60
clock = pg.time.Clock()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

#звуки

coin_sound = pg.mixer.Sound("sounds/coin_sound.wav")
coin_sound.set_volume(0.1)


VELOCITY = 5

score = 0

font = pg.font.Font("fonts\ProtestGuerrilla-Regular.ttf", 26)

heart = pg.image.load("images/heart.png")
heart = pg.transform.scale(heart, (30, 30)).convert_alpha()
heart_count = 3

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    butterflies.update()
    bird.update()

    if bird.rect.colliderect(coin.rect):
        score += 1
        coin_sound.play()
        coin.rect.left = random.randint(0,  window_width - coin.rect.w)
        coin.rect.top = random.randint(0, window_hight - coin.rect.h)


    display_surface.fill((WHITE))

    display_surface.blit(bird.image, bird.rect)
    display_surface.blit(coin.image, coin.rect)


    score_text = font.render(str(score), True, RED)
    display_surface.blit(score_text, (window_width - 60, 0))

    for i in range(heart_count):
            display_surface.blit(heart, (i * 30, 0))

    hits = pg.sprite.spritecollide(bird, butterflies, True)
    for hit in hits:
        heart_count -= 1
        if heart_count <=0:
            running = False

    butterflies.draw(display_surface)

    pg.display.update()

    clock.tick(FPS)


pg.quit()


