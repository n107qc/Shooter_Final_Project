from pygame import *
from pygame.sprite import Sprite
from pygame.transform import scale, flip
from pygame.image import load
from random import randint
from time import time as timer

init()
font.init()
mixer.init()

# розміри вікна
WIDTH, HEIGHT = 900, 600

# картинка фону
bg= image.load("Img/фон4.jpg")
#картинки для спрайтів
player_img = image.load("Img/спрайт героя.png")
enemy1_img = image.load("Img/спарайт ворога1.png")
enemy2_img = image.load("Img/спрайт ворога2.png")
gun_img = image.load("Img/зброя1-removebg-preview.png")
gun2_img = image.load("Img/зброя2-removebg-preview.png")
gun3_img = image.load("Img/зброя3-removebg-preview.png")
ammo1_img = image.load("Img/куля3-removebg-preview.png")

# фонова музика
mixer.music.load('Sound/wildweststinger.wav')
mixer.music.set_volume(0.2)
mixer.music.play(loops=-1)

#окремі звуки
fire_sound = mixer.Sound("Sound/lmg_fire01.mp3")
fire_sound.set_volume(0.2)

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, width, height, x, y, speed = 3):
        super().__init__()
        self.image = transform.scale(sprite_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.mask = mask.from_surface(self.image)  

    def draw(self, surface): #відрисовуємо спрайт у вікні
        surface.blit(self.image, self.rect)

class Player(GameSprite):
    def __init__(self, sprite_img, width, height, x, y, speed=3):
        super().__init__(sprite_img, width, height, x, y, speed)
        self.arm = gun_img
        self.arm = transform.scale(gun_img, (90,50))

    def draw(self, surface):
        super().draw(surface)
        surface.blit(self.arm, (self.rect.centerx, self.rect.centery))

    def update(self): #рух спрайту
        old_pos = self.rect.x, self.rect.y
        keys_pressed = key.get_pressed() 
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < WIDTH - 70:
            self.rect.x += self.speed
        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < HEIGHT - 70:
            self.rect.y += self.speed 
        
        for w in walls:
            if sprite.collide_mask(self, w):
                self.rect.x, self.rect.y = old_pos      

    def fire(self):
        bullet = Bullet(ammo1_img, 15, 20, self.rect.right, self.rect.centery,  10)  
        bullets.add(bullet) 
    
     

class Enemy(GameSprite):
    def __init__(self, sprite_img, width, height, x, y, speed=3):
        super().__init__(sprite_img, width, height, x, y, speed)
        self.direction = 'down'  

    def update(self):
        if self.direction == 'down':
            self.rect.y += self.speed
            if self.rect.bottom >= HEIGHT:  
                self.rect.y = HEIGHT - self.rect.height  
                self.direction = 'up'  
        else:
            self.rect.y -= self.speed
            if self.rect.top <= 0:  
                self.rect.y = 0  
                self.direction = 'down'  

class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed  
        if self.rect.x > WIDTH:  
            self.kill()

class Wall(sprite.Sprite):
    def __init__(self, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.width = wall_width
        self.height = wall_height
        self.image = Surface([self.width, self.height]) 
        self.image.fill((152,100,84))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
 


class Text(GameSprite):
    def __init__(self, text, x, y, font_size=22, font_name="Impact", color=(255,255,255)):
        self.font = font.SysFont(font_name, font_size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        
    def draw(self): #відрисовуємо спрайт у вікні
        window.blit(self.image, self.rect)
    
    def set_text(self, new_text): #змінюємо текст напису
        self.image = self.font.render(new_text, True, self.color)

# створення вікна
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Шутер")

# написи для лічильників очок
score_text = Text("Рахунок:", 20, 50)
# напис з результатом гри
result_text = Text("Перемога!", 350, 250, font_size = 50)

#додавання фону
bg = transform.scale(bg, (WIDTH, HEIGHT))

# створення спрайтів
player = Player(player_img, width=300, height=200, x=0, y=415)
enemy1 = Enemy(enemy1_img, width=239, height=211, x=450, y=225)
enemy2 = Enemy(enemy2_img, width=200, height=189, x=670, y=15)

enemies = sprite.Group()
enemies.add(enemy1)
enemies.add(enemy2)


bullets = sprite.Group()

walls = sprite.Group()
wall1 = Wall(250, 300, 20, 550)
wall2 = Wall(430, 130, 20, 350)
wall3 = Wall(680, 450, 20, 180)

walls.add(wall1)
walls.add(wall2)
walls.add(wall3)

# основні змінні для гри
run = True
finish = False
clock = time.Clock()
FPS = 60

# ігровий цикл
while run:
    # перевірка подій
    for e in event.get():
        if e.type == QUIT:
            run = False
        if not finish and e.type == KEYDOWN and e.key == K_SPACE:
            player.fire()

    if not finish: # поки гра триває
        # рух спрайтів
        player.update() #рух гравця

        #зіткнення гравця і ворогів
        spritelist = sprite.spritecollide(player, enemies, False,sprite.collide_mask)
        for collide in spritelist:
            finish = True
            result_text.set_text("ПРОГРАШ!")

        #відрисовуємо фон
        window.blit(bg, (0, 0)) 
        #відрисовуємо спрайти
        player.draw(window) 
        enemies.draw(window)
        walls.draw(window)
        bullets.draw(window)
        enemies.update()
        walls.update()
        bullets.update()
    else:
        result_text.draw() 

    display.update()
    clock.tick(FPS)
