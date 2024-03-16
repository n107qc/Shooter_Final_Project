from pygame import *
from pygame.sprite import Sprite
from pygame.transform import scale, rotate
from pygame.image import load
from random import randint
from time import time as timer
from math import atan2, degrees, hypot

font.init()
mixer.init()

lost = 0
score = 0

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

font.init()
f = font.SysFont('Arial', 36)
f2 = font.SysFont('Arial', 80)

txt_lose_game = f2.render('Програв',True,(255,0,0))


ammo = 5
reload = False

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
        # Отримати розміри гравця
        player_width, player_height = self.rect.size
        # Розмістити зброю в центрі правої частини гравця
        arm_pos = (self.rect.right, self.rect.centery - self.arm.get_height() // 2)
        # Оновити позицію зображення зброї
        surface.blit(self.arm, arm_pos)


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

        for w in enemies:
            if sprite.collide_mask(self,w):
                self.rect.x, self.rect.y = old_pos

    def fire(self):
        # Отримати позицію зброї відносно гравця
        bullet_x = arm_rect.centerx
        bullet_y = arm_rect.centery
        bullet = Bullet(ammo1_img, 40, 45, bullet_x, bullet_y,  10, player.angle, player.dir)  
        bullets.add(bullet)   
    
     

class Enemy(GameSprite):
    def __init__(self, sprite_img, width, height, x, y, speed=3):
        super().__init__(sprite_img, width, height, x, y, speed)
        self.direction = 'down'
       

    def update(self, lost):  # Додали аргумент lost
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
                lost = lost + 1  

class Bullet(GameSprite):
    def __init__(self, sprite_img, width, height, x, y, speed=3, angle=0, dir = (1,0)):
        super().__init__(sprite_img, width, height, x, y, speed)

        self.angle = angle
        self.dir = dir

    def update(self):
        self.rect.x += self.dir[0] * self.speed  
        self.rect.y += self.dir[1] * self.speed  
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
        
    def draw(self, surface): #відрисовуємо спрайт у вікні
        surface.blit(self.image, self.rect)
    
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
enemy1 = Enemy(enemy1_img, width=200, height=189, x=450, y=225)
enemy2 = Enemy(enemy2_img, width=180, height=160, x=670, y=15)

enemies = sprite.Group()
enemies.add(enemy1)
enemies.add(enemy2)


bullets = sprite.Group()

walls = sprite.Group()
wall1 = Wall(250, 300, 20, 550)
wall2 = Wall(430, 100, 20, 350)
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
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if ammo > 0 and not reload:
                    player.fire()
                    ammo -= 1
                elif ammo <= 0 and not reload:
                    reload = True
                    start_reload = timer()

    if not finish:
        window.blit(bg, (0, 0))
        txt_lose = f.render(f'Пропущено:{lost}', True, (255,255,255))
        txt_score = f.render(f'Рахунок:{score}', True, (255,255,255))
        window.blit(txt_lose, (0,50))
        window.blit(txt_score, (0,0))

        mouse_pos = mouse.get_pos()

        dx = mouse_pos[0] - player.rect.centerx
        dy = mouse_pos[1] - player.rect.centery

        player.angle = atan2(dy, dx)
        player.dir = (dx,dy)
        length = hypot(*player.dir)
        player.dir = (dx/length, dy/length)

        rotated_arm = rotate(player.arm, degrees(-player.angle))
        arm_rect = rotated_arm.get_rect(center=player.rect.center)

        player.rect.topleft = (player.rect.topleft)
        window.blit(player.image, player.rect)
        window.blit(rotated_arm, arm_rect.topleft)

        player.update()

        if reload:
            now_time = timer()
            delta = now_time - start_reload
            if delta < 3:
                txt_reload = f.render('WAIT', True, [150,150,200])
                window.blit(txt_reload, [150, 0])
            else:
                ammo = 5
                reload = False

        for bullet in bullets:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1

        enemies.draw(window)
        walls.draw(window)
        bullets.draw(window)
        enemies.update(lost)
        walls.update()
        bullets.update()

    if score == 2:
        finish = True
    if finish:
        result_text.draw(window) 

    display.update()
    clock.tick(FPS)