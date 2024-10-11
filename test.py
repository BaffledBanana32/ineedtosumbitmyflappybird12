import pygame
from sys import exit

from pygame.examples.playmus import Window

pygame.init()
clock = pygame.time.Clock()

# Window/screen
Win_Height = 720
Win_Width = 551
window = pygame.display.set_mode((Win_Width, Win_Height))

# images
rocket_image = [pygame.image.load("assets/spaceship_downangle09.png"),
                pygame.image.load("assets/spaceship_upangle09.png"),
                pygame.image.load("assets/spaceship_straightfinal09.png")]
background_image = pygame.image.load("assets/final_background.png")
moving_background = pygame.image.load("assets/moving_back final.png")
top_portal_image = pygame.image.load("assets/top_portal.png")
bottom_portal_image = pygame.image.load("assets/bottom_portal.png")
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

    def update(self):
        self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = rocket_image[self.image_index // 10]

class Moving_ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = moving_background
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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

    rocket = pygame.sprite.GroupSingle()
    rocket.add(Rocket())

    x_pos_ground, y_pos_ground = 0, 411
    ground = pygame.sprite.Group()
    ground.add(Moving_ground(x_pos_ground, y_pos_ground))

    run = True 
    while run:
        quit_game()


        window.fill((0,0,0))
#draw background
        window.blit(background_image,(0,0))

        if len(ground) <= 2:
            ground.add(Moving_ground(Win_Width, y_pos_ground))

        ground.draw(window)
        rocket.draw(window)

        ground.update()
        rocket.update()

        clock.tick(60)
        pygame.display.update()

main()