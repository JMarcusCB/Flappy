import pygame

class Flappy(pygame.sprite.Sprite):
    def __init__(self) -> None:
        self.surface = pygame.display.get_surface()
        self.image = pygame.image.load("src\\assets\images\\bird.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width()/3, self.image.get_height()/3))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = self.surface.get_height()//2

        self.speed = 0
        self.jump_force = 13
        self.is_jumping = False
        self.gravity = 1

        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        self.speed += self.gravity
        self.rect.y += self.speed        

    def jump(self):
        self.speed = -self.jump_force

    def check_vertical_status(self):
        if self.speed > 1 :
            return "rising"
        elif self.speed < 1:
            return "falling"
        else: 
            return "normal"
        

    def draw(self):
        flappy_vertical_state = self.check_vertical_status()

        if flappy_vertical_state == "falling":
            flappy_falling = pygame.transform.rotate(self.image, 45)
            self.surface.blit(flappy_falling, (self.rect.x, self.rect.y))
        elif flappy_vertical_state == "normal":
            flappy_normal = pygame.transform.rotate(self.image, 0)
            self.surface.blit(flappy_normal, (self.rect.x, self.rect.y))
        else:
            flappy_rising = pygame.transform.rotate(self.image, -45)
            self.surface.blit(flappy_rising, (self.rect.x, self.rect.y))