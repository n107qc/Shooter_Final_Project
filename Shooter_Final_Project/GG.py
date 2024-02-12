from pygame import *
from random import randint

import os

init()
font.init()
mixer.init()

# розміри вікна
WIDTH, HEIGHT = 900, 600

# картинка фону
bg_image = image.load("infinite_starts.jpg")
#картинки для спрайтів
player_image = image.load("spaceship.png")
ufo_image = image.load("alien.png")

# фонова музика
mixer.music.load('musictheme.ogg')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

#окремі звуки
fire_sound = mixer.Sound("laser1.wav")
fire_sound.set_volume(0.2)

# класи
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, width, height, x, y, speed = 3):
        super().__init__()
        self.image = transform.scale(sprite_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.mask = mask.from_surface(self.image)  

    def draw(self): #відрисовуємо спрайт у вікні
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def update(self): #рух спрайту
        keys_pressed = key.get_pressed() 
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < WIDTH - 70:
            self.rect.x += self.speed
        
class Text(sprite.Sprite):
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
score_text = Text("Рахунок: 0", 20, 50)
# напис з результатом гри
result_text = Text("Перемога!", 350, 250, font_size = 50)

#додавання фону
bg = transform.scale(bg_image, (WIDTH, HEIGHT))

# створення спрайтів
player = Player(player_image, width = 100, height = 100, x = 200, y = HEIGHT-150)
ufos = sprite.Group() #група спрайтів


# основні змінні для гри
run = True
finish = False
clock = time.Clock()
FPS = 60
score = 0
lost = 0

# ігровий цикл
while run:
    # перевірка подій
    for e in event.get():
        if e.type == QUIT:
            run = False
    if not finish: # поки гра триває
        # рух спрайтів
        player.update() #рух гравця
        ufos.update()

         #зіткнення гравця і ворогів
        spritelist = sprite.spritecollide(player, ufos, False)
        for collide in spritelist:
            finish = True
            result_text.set_text("ПРОГРАШ!")
        # перевірка зіткнення 2 груп спрайтів
        # spritelist = sprite.groupcollide(ufos, bullets, True, True)
        # for collide in spritelist:
        #     explosions.add(Explosion(collide.rect.x, collide.rect.y, images_list))
        #     score += 1
        #     score_text.set_text("Рахунок:" + str(score))
       
        if score >= 10:
            finish = True
         #відрисовуємо фон
        window.blit(bg, (0, 0)) 
        #відрисовуємо спрайти
        player.draw() 
        ufos.draw(window)
    else:
        result_text.draw() # текст вкінці гриfrom pygame import *
    # оновлення екрану і FPS
    display.update()
    clock.tick(FPS)