import pygame, random

class Pipe(pygame.sprite.Sprite):
    def __init__(self):
        self.surface = pygame.display.get_surface()

        # IMAGES
        self.bottom_pipe = pygame.image.load("src\\assets\images\pipe-green.png")
        self.top_pipe    = pygame.image.load("src\\assets\images\pipe-green-inverted.png")      

        # RECTS
        self.bottom_pipe_rect = self.bottom_pipe.get_rect()
        self.top_pipe_rect    = self.top_pipe.get_rect()

        self.top_pipe_rect.x    = 600
        self.bottom_pipe_rect.x = 600

        # SPACE BETWEEN PIPES
        self.space_between = 150

        # Y POSITION PIPES
        self.bottom_pipe_rect.y = random.randint(310, 480)
        self.top_pipe_rect.bottom = self.bottom_pipe_rect.top - self.space_between

        # MASKS
        self.bottom_pipe_mask = pygame.mask.from_surface(self.bottom_pipe)
        self.top_pipe_mask = pygame.mask.from_surface(self.top_pipe)
        
        # SPEED
        self.speed = 2

        self.accounted = False

    def update(self):
        self.bottom_pipe_rect.x -= self.speed
        self.top_pipe_rect.x    -= self.speed


    def draw(self):
        self.surface.blit(self.bottom_pipe, (self.bottom_pipe_rect.x , self.bottom_pipe_rect.y))
        self.surface.blit(self.top_pipe,    (self.top_pipe_rect.x    , self.top_pipe_rect.top))