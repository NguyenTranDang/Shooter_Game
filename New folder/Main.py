from pygame import *
from random import randint
from time import *


app_width = 700
app_height = 500

win = display.set_mode((app_width, app_height))
background = transform.scale(image.load("galaxy.jpg"), (app_width,app_height))

bullets = sprite.Group()

shooted = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (player_width, player_height))

        self.rect = self.image.get_rect()

        self.rect.x = player_x
        self.rect.y = player_y

        self.speed = player_speed
    
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < app_width - 80:
            self.rect.x += self.speed

    def fire(self):
        shooted = 0
        shooted += 1
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > app_width:
            self.rect.y = 0 
            self.rect.x = randint(80, app_width - 80)
            lost += 1 

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


player = Player("rocket.png", 5, app_height - 100, 80, 100, 10)

enemies = sprite.Group()
def create_enemy(level):
    enemies = sprite.Group()
    for i in range(level):
        enemy = Enemy("ufo.png", randint(80, app_width - 80), -40, 100, 80, randint(1,5))
        enemies.add(enemy)
    return enemies


level = 3
for i in range(level):
    enemy = Enemy("ufo.png", randint(80, app_width - 80), -40, 100, 80, randint(1,5))
    enemies.add(enemy)

asteroids = sprite.Group()
def create_asteroid():
    asteroids = sprite.Group()
    for i in range(level):
        asteroid = Enemy("asteroid.png",randint(80, app_width - 80), -40, 100, 80, randint(1,5))
        asteroids.add(asteroid)
    return asteroids


#clock = time.clock()

finish = False
run = True
FPS = 60
score = 0

font.init()
font2 = font.Font(None, 36)

while run:
    # the press the Close button event
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()


    if len(enemies) != level:
        enemy = create_enemy(level)
    elif len(asteroids) < 3:
        asteroid = create_asteroid()  
    else:
        pass

    if not finish:
        # refresh background
        win.blit(background,(0,0))

        # writing text on the screen
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        win.blit(text, (10, 20))

        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        win.blit(text_lose, (10, 50))

        text_level = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        win.blit(text_lose, (10, 80))

        lose = font2.render("YOU ARE POWERLESS!!",1,(255,255,255))

        collision1 = sprite.groupcollide(enemies, bullets, True, True)
        for c in collision1:
            score += 1
            enemy = Enemy("ufo.png", randint(80, app_width - 80), -40, 100, 80, randint(1,5))
            enemies.add(enemy)

        collision2 = sprite.spritecollide(player, enemies, False)
        for c in collision2:
            finish = True
            win.blit(lose, (app_width/2, app_height/2))

        collision3 = sprite.spritecollide(player, asteroids, False)
        for c in collision3:
            finish = True
            win.blit(lose, (app_width/2, app_height/2))

        if score > 10:
            level = 4 
            lost = 0
        if score > 20:
            level = 5
            lost = 0
        if lost > 10:
            level = 4
        if lost > 20:
            level = 5

        if score > 30:
            finish = True
            win.blit(lose, (app_width/2, app_height/2))
        if lost >= 5 and level == 3:
            finish = True
            win.blit(lose, (app_width/2, app_height/2))
        if lost >= 4 and level == 4:
            finish = True
            win.blit(lose, (app_width/2, app_height/2))
        if lost >= 2 and level == 5:
            finish = True
            win.blit(lose, (app_width/2, app_height/2))



        # producing sprite movements
        
        player.update()

        enemies.update()
        enemies.draw(win)

        bullets.update() 
        bullets.draw(win)
        
        asteroids.update()
        asteroids.draw(win)
        # updating them at a new location on each iteration of the loop
        player.reset()
        

        display.update()
    # the loop runs every 0.05 seconds
    #clock.tick(FPS)    
    
