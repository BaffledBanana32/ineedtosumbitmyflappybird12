import pygame
from sys import exit
import random
from pygame.examples.playmus import Window

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
moving_background = pygame.image.load("assets/moving_back final.png")
top_portal_image = pygame.image.load("assets/portal_resized1.png")
bottom_portal_image = pygame.image.load("assets/portal_resized2.png")
game_over_image = pygame.image.load("assets/Game over.png")
start_image = pygame.image.load("assets/Start.png")


# Games
Scroll_speed = 1
rocket_start_pos = (100,250)
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

    def update(self, user_input):
        self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = rocket_image[self.image_index // 10]

        #Movment
        self.vel += 0.5
        if self.vel > 7:
            self.vel = 7
        if self.rect.y < 500:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.flying = False

        #animation of the racket
        self.image = pygame.transform.rotate(self.image, self.vel * -7)

        if user_input[pygame.K_SPACE] and not self.flying and self.rect.y > 0:
            self.flying = True
            self.vel = -7

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        #pipe go left
        self.rect.x -= Scroll_speed
        if self.rect.x <= -Win_Width:
            self.kill()


class Moving_ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
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


def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def main():
    #rocket
    rocket = pygame.sprite.GroupSingle()
    rocket.add(Rocket())

    #portals
    portal_timer = 0
    portal = pygame.sprite.Group()


    #moving image
    x_pos_ground, y_pos_ground = 0, 411
    ground = pygame.sprite.Group()
    ground.add(Moving_ground(x_pos_ground, y_pos_ground))

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
        ground.draw(window)
        rocket.draw(window)

        portal.update()
        ground.update()
        rocket.update(user_input)

        #portals spawn
        if portal_timer <= 0:
            x_top, x_bottom = 550, 550
            y_top = random.randint(-600, -480)
            y_bottom = y_top + random.randint(90, 130) + bottom_portal_image.get_height()
            portal.add(Portal(x_top, y_top, top_portal_image))
            portal.add(Portal(x_bottom, y_bottom, bottom_portal_image))
            portal_timer = random.randint(180, 250)
        portal_timer -= 1

        clock.tick(60)
        pygame.display.update()

main()