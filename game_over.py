import pygame
from boton import Boton
from constantes import *

class Game_Over():
    def __init__(self):
        pygame.display.set_caption("Adventure Time")
        self.screen = pygame.display.set_mode((PANTALLA_ANCHO, PANTALLA_ALTO))
        self.muerte_fondo = pygame.image.load('imagenes/gameover.png')
        #Carga de imagenes para game over
        self.fondo_game_over_img = pygame.image.load('imagenes/fondo_game_over.png').convert_alpha()
        self.game_over_img = pygame.image.load('imagenes/game_over.png').convert_alpha()
        self.restart_img = pygame.image.load('imagenes/restart_btn.png').convert_alpha()
        self.quit_2_img = pygame.image.load('imagenes/quit_2_btn.png').convert_alpha()
    
    def menu(self):
        #Instancia de botones
        boton_resume = Boton(100, 320, self.restart_img, 1.5)
        boton_quit_2 = Boton(350, 320, self.quit_2_img, 1.5)
        
        menu = True
        while menu:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    menu = False
            
            self.screen.blit(pygame.transform.scale(self.fondo_game_over_img, (960,600)), [-100,0])
            self.screen.blit(pygame.transform.scale(self.game_over_img, (600,80)), [0, 100])
            
            if boton_resume.dibujar(self.screen):
                menu = False
                self.continuar = True
            
            if boton_quit_2.dibujar(self.screen):
                pygame.quit()
            
            pygame.display.update()
    
    def verificar(self):
        if self.continuar:
            return True