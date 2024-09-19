import pygame
from sys import exit

pygame.init()
clock = pygame.time.Clock()

# Window/screen
Win_Height = 720
Win_Width = 551
window = pygame.display.set_mode((Win_Width, Win_Height))

# images
rocket_image = [pygame.image.load("./assets/ spaceship straight final.png"),
                ("./assets/ spaceship down angle.png"),
                ("./assets/ spaceship staight final.png")]
background_image = pygame.image.load("./assets/final background.png")
top_portal_image = pygame.image.load("./assets/top_portal.png")
bottom_portal_image = pygame.image.load("./assets/bottom_portal.png")
game_over_image = pygame.image.load("./assets/Game over.png")
start_image = pygame.image.load("./assets/Start.png")

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def main():
    run = True
    while run:
        quit_game()


        window.fill((0,0,0))
#draw background
        window.blit(background_image,(0,0))


        clock.tick(60)
        pygame.display.update()

main()