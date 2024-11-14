import pygame
from sys import exit
import random
from pygame.examples.playmus import Window
from pygame.examples.sprite_texture import sprite
from pygame.sprite import spritecollide

pygame.init()
clock = pygame.time.Clock()

# Window/screen
Win_Height = 720
Win_Width = 551
window = pygame.display.set_mode((Win_Width, Win_Height))

# images
rocket_image = [pygame.image.load("assets/rocket1.png"),
                pygame.image.load("assets/rocket2.png"),
                pygame.image.load("assets/rocket3.png")]
background_image = pygame.image.load("assets/final_background.png")
moving_background = pygame.image.load("assets/backgroundmove.png")
top_portal_image = pygame.image.load("assets/portal_resized1.png")
bottom_portal_image = pygame.image.load("assets/portal_resized2.png")
game_over_image = pygame.image.load("assets/game_over.png")
start_image = pygame.image.load("assets/start.png")
coin_image = pygame.image.load("assets/coinwork.png")
asteroid_image = pygame.image.load("assets/asteroid.png")
bullet_image = pygame.image.load("assets/bullet.png")


# Games
changable_varible = 0
Scroll_speed = 2 + changable_varible
rocket_start_pos = (100,250)
score = 0
Coin_score = 0
font = pygame.font.SysFont("Arial", 26)
game_stop = True

#The rocket
class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = rocket_image[0]
        self.rect = self.image.get_rect()
        self.rect.center = rocket_start_pos
        self.image_index = 0
        self.vel = 0
        self.flying = False
        self.alive = True

    #animation
    def update(self, user_input):
        if self.alive:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = rocket_image[self.image_index // 10]

        #Movment
        self.vel += 0.5
        if self.vel > 7:
            self.vel = 7
        if self.rect.y < 550:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.flying = False

        #animation of the rocket
        self.image = pygame.transform.rotate(self.image, self.vel * -7)

        if user_input[pygame.K_SPACE] and not self.flying and self.rect.y > 0 and self.alive:
            self.flying = True
            self.vel = -7



class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipe_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.exit, self.passed = False, False, False
        self.pipe_type = pipe_type

    def update(self):
        #pipe go left
        self.rect.x -= Scroll_speed
        if self.rect.x <= -Win_Width:
            self.kill()

        #Score
        global score
        if self.pipe_type == "bottom":
            if rocket_start_pos[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if rocket_start_pos[0] > self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True
                score += 1



class Moving_ground(pygame.sprite.Sprite):
    def __init__(self, x, y,):
        pygame.sprite.Sprite.__init__(self)
        self.image = moving_background
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    #Update function for the ground
    def update(self):
        self.rect.x -= Scroll_speed
        if self.rect.x < -Win_Width:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.living = True


    def update(self):
        if self.alive:
            self.rect.x -= Scroll_speed
        if self.rect.x <= -Win_Width:
            self.kill()


def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def main():
    global score
    global Coin_score
    global changable_varible

    #rocket
    rocket = pygame.sprite.GroupSingle()
    rocket.add(Rocket())

    #portals
    portal_timer = 0
    portal = pygame.sprite.Group()

    #moving image
    x_pos_ground, y_pos_ground = 0, 520
    ground = pygame.sprite.Group()
    ground.add(Moving_ground(x_pos_ground, y_pos_ground))

    #coins
    coin_timer = 0
    coin = pygame.sprite.Group()


    run = True 
    while run:
        quit_game()


        window.fill((0,0,0))

        #users input
        user_input = pygame.key.get_pressed()

        #draw background
        window.blit(background_image,(0,0))

        if len(ground) <= 2:
            ground.add(Moving_ground(Win_Width, y_pos_ground))

        portal.draw(window)
        coin.draw(window)
        ground.draw(window)
        rocket.draw(window)


        #score
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        score_coin = font.render("Coins: " + str(Coin_score), True, (255, 255, 255))
        window.blit(score_text, (20, 20))
        window.blit(score_coin, (20, 40))




        if rocket.sprite.alive:
            portal.update()
            ground.update()
            rocket.update(user_input)
            coin.update()


        if coin_timer <= 0 and rocket.sprite.alive:
            coin_y = random.randint(200,400)
            coin_x = 620
            coin.add(Coin(coin_x, coin_y, coin_image))
            coin_timer = random.randint(180, 250)
        coin_timer -= 1


        coin_collision = pygame.sprite.spritecollide(rocket.sprites()[0], coin, False)
        if coin_collision:
            coin.remove(coin_collision[0])
            Coin_score += 1


        if Coin_score != score:
            for Coin_score in score:
                changable_varible += 1


        collision_portal = pygame.sprite.spritecollide(rocket.sprites()[0], portal, False)
        collision_ground = pygame.sprite.spritecollide(rocket.sprites()[0], ground, False)
        if collision_portal or collision_ground:
            rocket.sprite.alive = False
            if collision_portal or collision_ground:
                window.blit(game_over_image, (Win_Width //2 - game_over_image.get_width() // 2,
                                                   Win_Height //2 - game_over_image.get_height() // 2))
                if user_input[pygame.K_r]:
                    score = 0
                    Coin_score = 0
                    break


        #portals spawn
        if portal_timer <= 0 and rocket.sprite.alive:
            x_top, x_bottom = 550, 550
            y_top = random.randint(-600, -480)
            y_bottom = y_top + random.randint(100, 130) + bottom_portal_image.get_height()
            portal.add(Portal(x_top, y_top, top_portal_image, 'top'))
            portal.add(Portal(x_bottom, y_bottom, bottom_portal_image, 'bottom'))
            portal_timer = random.randint(180, 250)
        portal_timer -= 1


        clock.tick(60)
        pygame.display.update()


def menu ():
    global game_stop

    while game_stop:
        quit_game()

        window.fill((0,0,0))
        window.blit(background_image,(0,0))
        window.blit(moving_background, (0,520))
        window.blit(rocket_image[0], (100,250))
        window.blit(start_image, (Win_Width // 2 - start_image.get_width() // 2,
                                  Win_Height // 2 - start_image.get_height() // 2))

        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            main()

        pygame.display.update()

menu()