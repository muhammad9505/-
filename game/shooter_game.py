from pygame import *
import random
init()
FPS = 60
win_width = 700
win_height = 500
speed = 10
fleem = 0
font.init()
font1 = font.Font(None, 36)
ship = 0
Bullets = []
finish = False
time_win = 0


window = display.set_mode((700,500))
display.set_caption('Шутер')

background = transform.scale(image.load('galaxy.jpg'),(700,500))
window.blit(background,(0,0))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (70, 110))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        global shot_time
        global Bullets
        global hero
        shot_time += 1
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
        if keys[K_SPACE]:
            if shot_time > 30:
                shot_time = 0
                bullet = Bullet('bullet.png',hero.rect.x + 35,hero.rect.y,1)
                Bullets.append(bullet)

            

    def fire(self):
        pass

hero = Player('rocket.png',300,400,speed)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image,player_x,player_y,player_speed)
        self.image = transform.scale(image.load(player_image), (70, 50))    

    def update(self):
        global fleem
        self.rect.y += 1
        if self.rect.y > win_height - 65:
            fleem += 1
            self.randMove()

    def randMove(self):
        self.rect.y = -65
        self.rect.x = random.randint(0,win_width)

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (30, 40))
    def update(self):
        self.rect.y -= 4
        self.killMonster()
    def isNotToMap(self):
        if self.rect.y < 0:
            return True
        else:
            return False
    
    def killMonster(self):
        global ship
        sprite_list = sprite_list = sprite.spritecollide(self, monsters, False)

        for monstr in sprite_list:
            monstr.randMove()
            ship += 1
            Bullets.remove(self)


monsters = sprite.Group()
for i in range(5):
    rn_x = random.randint(0,win_width-65)
    rn_y = random.randint(0,win_height//3)
    monstr = Enemy('ufo.png',rn_x,rn_y,1)
    monsters.add(monstr)
    monsters.update()
shot_time = 0
clock = time.Clock()
game = True
while game:
    window.blit(background,(0,0))
    hero.reset()
    hero.update()
    monsters.update()
    monsters.draw(window)
    text_lose = font1.render('Пропущено:' + str(fleem), 1, (255,255,255))
    window.blit(text_lose,(50,80))
    text_schet = font1.render('Счет: ' + str(ship), 1, (255, 255, 255))
    window.blit(text_schet, (50,50))
    if ship >= 50:
        font_win = font.Font(None, 80)
        text_lose = font_win.render('YOU WIN!', 1, (10, 255, 10))
        window.blit(text_lose,(1, 400))
        game = False
    sprite_list = sprite.spritecollide(hero, monsters, False)
    if fleem >= 3 or len (sprite_list) > 0:
        font_win = font.Font(None, 80)
        text_lose = font_win.render('YOU LOSE!', 1, (255, 10, 10))
        window.blit(text_lose,(200, 400))
        game = False

    for bullet in Bullets:
        bullet.update()
        bullet.reset()
        if bullet.isNotToMap():
            Bullets.remove(bullet)

    for ev in event.get():
        if ev.type == QUIT:
            quit()
        

    display.update()
    clock.tick(FPS)
clock.tick(0.5)