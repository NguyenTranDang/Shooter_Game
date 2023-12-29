from pygame import *
from random import randint

WIN_WIDTH = 700
WIN_HEIGHT = 500

win = display.set_mode((WIN_WIDTH, WIN_HEIGHT))
background = transform.scale(image.load("galaxy.jpg"), (WIN_WIDTH, WIN_HEIGHT))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        sprite.Sprite.__init__(self)
        # Use the image to create the Sprite
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        # Create the hitbox for the Sprite
        self.rect = self.image.get_rect()
        # Place the Sprite in the screen
        self.rect.x = player_x
        self.rect.y = player_y
        # set the speed of the sprite
        self.speed = player_speed


    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):   
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < WIN_WIDTH - 80:
            self.rect.x += self.speed
        
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > WIN_WIDTH:
            self.rect.y = 0 
            self.rect.x = randint(80, WIN_WIDTH - 80)
            lost += 1 

class Bullet(GameSprite):
    # enemy movement
    def update(self):
        self.rect.y += self.speed
        # disappears upon reaching the screen edge
        if self.rect.y < 0:
            self.kill()
player = Player("rocket.png", 5, WIN_HEIGHT - 100, 80, 100, 10)




enemies = sprite.Group()
def create_enemy(level):
    enemies = sprite.Group()
    for i in range(level):
        enemy = Enemy("ufo.png", randint(80, WIN_WIDTH - 80), -40, 100, 80, randint(1,5))
        enemies.add(enemy)
    return enemies


clock = time.Clock()
finish = False
run = True
FPS = 60
score = 0

font.init() 
font2 = font.Font(None, 36)
level = 3
while run:

    # the press the Close button event
    for e in event.get():
        if e.type == QUIT:
            run = False

    if len(enemies) != level: 
        enemies = create_enemy(level)
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

        text_level = font2.render("Level: " + str(level), 1, (255, 255, 255))
        win.blit(text_level, (10, 80))

        if lost > 10:
            level = 4
        if lost > 20:
            level = 5
        # producing sprite movements
        player.update()
        
        enemies.update()
        enemies.draw(win)
        # updating them at a new location on each iteration of the loop

        player.reset()
        

        display.update()
    # the loop runs every 0.05 seconds
    clock.tick(FPS)