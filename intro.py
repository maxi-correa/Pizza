import pygame
from boton import Boton
from constantes import *

class Intro():
    def __init__(self):
        pygame.display.set_caption("Adventure Time")
        self.screen = pygame.display.set_mode((PANTALLA_ANCHO, PANTALLA_ALTO))
        #Carga de imagenes de fondo
        self.intro_fondo = pygame.image.load('imagenes/introbackground.png')
        
        #Carga de imagenes para menú
        self.titulo_img = pygame.image.load('imagenes/adventure_time.png').convert_alpha()
        self.fondo_img = pygame.image.load('imagenes/fondo.png').convert_alpha()
        self.play_img = pygame.image.load('imagenes/play_btn.png').convert_alpha()
        self.quit_img = pygame.image.load('imagenes/quit_btn.png').convert_alpha()
        self.option_img = pygame.image.load('imagenes/option_btn.png').convert_alpha()
        self.sound_on_img = pygame.image.load('imagenes/sound_on_btn.png').convert_alpha()
        self.sound_off_img = pygame.image.load('imagenes/sound_off_btn.png').convert_alpha()
        
        #Carga de sonido de menú y de batalla
        self.menu_theme = pygame.mixer.Sound('sonidos/menu_theme.ogg')
        
    def menu(self):
        self.menu_theme.play(-1)
        #Instancia de botones
        boton_play = Boton(300, 250, self.play_img, 1)
        boton_quit = Boton(300, 450, self.quit_img, 1)
        boton_sound_on = Boton (520, 350, self.sound_on_img, 1.4)
        boton_sound_off = Boton(620, 350, self.sound_off_img, 1.4)
        boton_quit = Boton(300, 450, self.quit_img, 1)
        
        tema_menu = True
        movimiento_fondo = 0
        menu = True
        while menu:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
            
            #Fondo en movimiento
            movimiento_fondo_relativo = movimiento_fondo % self.fondo_img.get_rect().width
            self.screen.blit(self.fondo_img, (movimiento_fondo_relativo - self.fondo_img.get_rect().width,0))
            if movimiento_fondo_relativo < PANTALLA_ANCHO:
                self.screen.blit(self.fondo_img, (movimiento_fondo_relativo, 0))
            movimiento_fondo -= 1.5
            
            #Título del juego
            self.screen.blit(self.titulo_img, [50, -70])
            self.screen.blit(self.option_img, [300, 350])
            
            #Condiciones de los botones del menú
            if boton_play.dibujar(self.screen):
                menu = False
                self.menu_theme.stop()
            
            if boton_sound_on.dibujar(self.screen):
                if tema_menu == False:
                    tema_menu = True
                    self.menu_theme.play(-1)
            
            if boton_sound_off.dibujar(self.screen):
                tema_menu = False
                self.menu_theme.stop()
            
            if boton_quit.dibujar(self.screen):
                pygame.quit()
                
            pygame.display.update()