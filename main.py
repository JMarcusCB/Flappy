import pygame, random

from flappy import Flappy
from pipes_ import Pipe

class Jogo():
    def __init__(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.resolution = (360, 640)

        self.rect = pygame.Rect(0,0, self.resolution[0], self.resolution[1])

        self.display_surface = pygame.display.set_mode((self.resolution))
        pygame.display.set_caption("Flappy Bird")

        icon = pygame.image.load("src\\assets\icons\\favicon.png")
        pygame.display.set_icon(icon)

        self.play_button_image = pygame.image.load("src\\assets\images\play.png")
        self.play_button_rect = self.play_button_image.get_rect()
        self.play_button_rect.x = self.resolution[0]//2 - self.play_button_image.get_width()//2
        self.play_button_rect.y = self.resolution[1]//2 - self.play_button_image.get_height()//2

        self.background_image = pygame.image.load("src\\assets\images\\background.png")
        self.background_image = pygame.transform.scale(self.background_image, (self.background_image.get_width(), self.resolution[1]))
        self.background_rect =  self.background_image.get_rect()

        self.flappy = Flappy()

        self.pipes_list = []

        self.last_pipe_time_generate = pygame.time.get_ticks()
        self.time_generate_list = [1000 ,2000, 3000, 4000, 5000]
        self.time_generate = random.choice(self.time_generate_list)
        

        self.points = 0
        self.record_points = 0

        self.playing = False
        self.restarting = False
        self.menu_open = True
        self.close_menu_time = None
        self.restart_cooldown = 3000

    def loop_principal(self):
        while True:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                
                if event.type == pygame.KEYDOWN: 
                    if self.menu_open == False:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP :
                            self.flappy.jump()

                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                            self.turn_menu(self.menu_open)
                            self.playing = False
                            self.restarting = True
                            self.close_menu_time = pygame.time.get_ticks()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  
                        mouse_posicao = pygame.mouse.get_pos()
                        if (mouse_posicao[0] >= self.play_button_rect.left and mouse_posicao[0] <= self.play_button_rect.right and
                            mouse_posicao[1]  >= self.play_button_rect.top and mouse_posicao[1] <= self.play_button_rect.bottom):
                            self.turn_menu(self.menu_open)
                            self.playing = False
                            self.restarting = True
                            self.close_menu_time = pygame.time.get_ticks()
                            

            self.display_surface.fill((0,0,0))
            self.draw_background()

            self.update()

            self.draw()

            pygame.display.flip()

    def update(self):
            if self.menu_open == True:
                pass

            if self.restarting:
                if self.menu_open == False:
                    self.game_starting()
            
            if self.playing:
                self.flappy.rect.clamp_ip(self.rect)
                self.generates_pipes()
                self.delete_pipes()
                self.punctuate()
                self.check_collision()
                self.flappy.update()

                if len(self.pipes_list) > 0:
                    for pipe in self.pipes_list:
                        pipe.update()
    
    def draw(self):
        self.flappy.draw()
        if len(self.pipes_list) > 0:
            for pipe in self.pipes_list:
                pipe.draw()

        self.draw_text(str(self.points), (self.resolution[0]//2, 30), (255,255,255), 60)

        if self.menu_open == True:
            self.draw_menu()

    def draw_background(self):
        background_2_pos = self.background_rect.right

        self.display_surface.blit(self.background_image, (self.background_rect.x, 0))
        self.display_surface.blit(self.background_image, (background_2_pos, 0))

        if self.background_rect.right < 0:
            self.background_rect.left = background_2_pos

        self.background_rect.x -= 5

    def generates_pipes(self):
        now = pygame.time.get_ticks()

       # print(now, self.last_pipe_time_generate)
        print(now-self.last_pipe_time_generate, self.time_generate)
        if now - self.last_pipe_time_generate >= self.time_generate:
            self.pipes_list.append(Pipe())
            print("GERADO")
            self.last_pipe_time_generate = now
            self.time_generate = random.choice(self.time_generate_list)

    def delete_pipes(self):
        for pipe in self.pipes_list:
            if pipe.bottom_pipe_rect.x < -50:
                self.pipes_list.remove(pipe)

    def draw_text(self, text, pos, color= (255,255,255), size = 50):
        text = str(text)
        font = pygame.font.Font(None, size)
        message = font.render(text, True, color)
        self.display_surface.blit(message, pos)

    def punctuate(self):
        for pipe in self.pipes_list:
            if pipe.accounted == False:
                if self.flappy.rect.x > pipe.bottom_pipe_rect.right:
                    self.points += 1
                    pipe.accounted = True

    def check_collision(self):
        for pipe in self.pipes_list:
            offset_pipe_bottom = pipe.bottom_pipe_rect.x - self.flappy.rect.x, pipe.bottom_pipe_rect.y - self.flappy.rect.y
            offset_pipe_top    = pipe.top_pipe_rect.x - self.flappy.rect.x, pipe.top_pipe_rect.y - self.flappy.rect.y
            if self.flappy.mask.overlap_area(pipe.bottom_pipe_mask, offset_pipe_bottom) or self.flappy.mask.overlap(pipe.top_pipe_mask, offset_pipe_top):
                self.death()  

        if self.flappy.rect.y > self.resolution[1]-100:
            self.death()
 
    def draw_menu(self):
        rect = pygame.Surface((self.resolution[0], self.resolution[1]), pygame.SRCALPHA)  # Cria uma superfície transparente
        rect.fill((0,0,0, 128))       # Define a cor com a opacidade
        self.display_surface.blit(rect, (0, 0))  
        
        self.draw_text(f"Record: {self.record_points}", (self.play_button_rect.left - 20, self.play_button_rect.top - 100))
        self.display_surface.blit(self.play_button_image, (self.play_button_rect.x, self.play_button_rect.y) )

    def turn_menu(self, menu_open):
        if menu_open == True:
            self.menu_open = False
        else:
            self.menu_open = True
            self.restarting = False
            self.playing = False

    def game_starting(self):
        time_now = pygame.time.get_ticks()

        difference_time = time_now - self.close_menu_time

        if difference_time >= self.restart_cooldown:
            self.playing = True
            self.last_pipe_time_generate = time_now - self.time_generate
            self.restarting = False

        if difference_time < 1000:
            self.draw_text(3, (self.resolution[0]//2 -15, self.resolution[1]//2), size=100)
        elif 1000 < difference_time < 2000:
            self.draw_text(2, (self.resolution[0]//2 -15, self.resolution[1]//2), size=100)
        elif 2000 < difference_time < 3000:
            self.draw_text(1, (self.resolution[0]//2 -15, self.resolution[1]//2), size=100)
        
    def death(self):
        self.playing = False
        self.restarting = False
        self.menu_open = True

        if self.points > self.record_points:
            self.record_points = self.points
        self.points = 0

        self.flappy.rect.y = self.resolution[1]//2
        self.pipes_list *= 0
        

if __name__ == "__main__":
    flappy = Jogo()
    flappy.loop_principal()